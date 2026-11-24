#!/usr/bin/env python3
"""Render a handout or slide deck from a content file and check it.

The content file is Pandoc Markdown with a small YAML header.  The script
replaces citation keys with author-year labels from the bibliography INDEX,
verifies quotations against their sources, appends a reference list to
handouts, reports slide and page problems, and renders PDF, PPTX, DOCX, or
HTML through Pandoc (and a headless browser for PDF).

Only the Python standard library is required; ``pdfminer`` is used only as an
optional fallback when counting pages.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
HAN = re.compile(r"[\u4e00-\u9fff]")
CITATION = re.compile(r"\[@([A-Z0-9][A-Z0-9-]*)(?:,\s*([^\]]+))?\]")
CITATION_WITH_SPACE = re.compile(r"[ \t]*" + CITATION.pattern)
LABEL_AFTER_STOP = re.compile(r"([。；！？])[ \t]*(（[^（）\n]+，[^（）\n]+）)")
QUOTE_MARKS = "“”\"「」『』"
ITEM_LINE = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+|\(@)")
HANDOUT_CSS = "Shared/Format/handout.css"
SLIDES_CSS = "Shared/Format/slides.css"

_BIBLIOGRAPHY_SCAN = None


# ---------------------------------------------------------------------------
# Text and header helpers
# ---------------------------------------------------------------------------

def han_count(text: str) -> int:
    return len(HAN.findall(text))


def latin_word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z]+", text))


def item_length(text: str) -> int:
    """Length as Han characters plus Latin words."""
    return han_count(text) + latin_word_count(text)


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def clean_value(raw: str) -> str:
    """Strip an inline ``# comment`` and matching surrounding quotes."""
    value = raw.strip()
    if value[:1] in ("'", '"'):
        end = value.find(value[0], 1)
        if end != -1:
            return value[1:end].strip()
    return re.sub(r"\s+#.*$", "", value).strip()


def split_header(text: str) -> tuple[dict[str, str], str, str]:
    """Split a content file into (metadata, raw header, body).

    The header is the block between the first two ``---`` lines.  Only simple
    ``key: value`` lines are parsed; no YAML dependency is added.  The raw
    header (including its fences) is returned so it can be re-emitted for
    Pandoc.
    """
    text = normalize_newlines(text)
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, "", text
    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        return {}, "", text
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        if key:
            meta[key] = clean_value(raw)
    header = "\n".join(lines[:end + 1])
    body = "\n".join(lines[end + 1:])
    return meta, header, body


def header_errors(meta: dict[str, str]) -> list[str]:
    """Return errors for a missing or invalid ``kind`` and a missing title."""
    errors: list[str] = []
    kind = meta.get("kind")
    if not kind:
        errors.append("missing-kind")
    elif kind not in ("handout", "slides"):
        errors.append(f"invalid-kind:{kind}")
    if not meta.get("title"):
        errors.append("missing-title")
    return errors


def parse_minutes(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"\d+", value)
    return int(match.group()) if match else None


# ---------------------------------------------------------------------------
# Bibliography and citations
# ---------------------------------------------------------------------------

def bibliography_scan_module():
    """Load ``bibliography-scan.py`` so its inventory parser is reused."""
    global _BIBLIOGRAPHY_SCAN
    if _BIBLIOGRAPHY_SCAN is None:
        path = SCRIPT_DIR / "bibliography-scan.py"
        spec = importlib.util.spec_from_file_location("bibliography_scan", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _BIBLIOGRAPHY_SCAN = module
    return _BIBLIOGRAPHY_SCAN


def load_refs_keys(path: Path | None) -> set[str]:
    """Collect the first cell of every table row in a refs.md file."""
    keys: set[str] = set()
    if path is None or not Path(path).is_file():
        return keys
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and cells[0]:
            keys.add(cells[0])
    return keys


def load_index_rows(path: Path | None) -> dict[str, dict]:
    """Return ``KEY -> inventory row`` from the INDEX Reference Inventory."""
    rows: dict[str, dict] = {}
    if path is None or not Path(path).is_file():
        return rows
    text = Path(path).read_text(encoding="utf-8")
    for row in bibliography_scan_module().inventory_rows(text):
        key = row.get("key") or ""
        if key and not row.get("malformed"):
            rows[key] = row
    return rows


def row_cell(row: dict, index: int) -> str:
    cells = row.get("cells") or []
    return cells[index] if index < len(cells) else ""


def author_label(cell: str) -> str:
    """Build the citation label from the INDEX Author cell.

    Authors are separated by ``&`` or ``;`` and written ``Surname, Given``.
    One author is named; two are joined by ``&``; three or more use ``等``.
    """
    parts = [part.strip() for part in re.split(r"[&;]", cell) if part.strip()]
    surnames: list[str] = []
    for part in parts:
        surname = part.split(",", 1)[0].strip()
        if surname:
            surnames.append(surname)
    if not surnames:
        return ""
    many = len(surnames) >= 3 or bool(re.search(r"\bet\s+al\b", cell, re.IGNORECASE))
    if many:
        return f"{surnames[0]} 等"
    if len(surnames) == 2:
        return f"{surnames[0]} & {surnames[1]}"
    return surnames[0]


def year_from_row(row: dict) -> str:
    """Take the second underscore segment of the first PDF stem."""
    pdfs = row.get("pdfs") or []
    if not pdfs:
        return "n.d."
    segments = Path(pdfs[0]).stem.split("_")
    if len(segments) >= 2 and segments[1]:
        return segments[1]
    return "n.d."


def citation_label(row: dict, locator: str | None) -> str:
    author = author_label(row_cell(row, 1))
    year = year_from_row(row)
    label = f"{author}，{year}" if author else year
    if locator:
        label += f"：{locator.strip()}"
    return f"（{label}）"


def replace_citations(
    body: str,
    refs_keys: set[str],
    index_rows: dict[str, dict],
) -> tuple[str, list[str], list[str]]:
    """Replace ``[@KEY]`` citations with author-year labels.

    Returns the rewritten body, errors, and cited keys in first-citation order.
    """
    errors: list[str] = []
    order: list[str] = []
    seen: set[str] = set()

    def substitute(match: re.Match[str]) -> str:
        key = match.group(1)
        locator = match.group(2)
        if key not in refs_keys:
            errors.append(f"unknown-key:{key}")
            return "[citation needed]"
        row = index_rows.get(key)
        if row is None:
            errors.append(f"key-not-in-index:{key}")
            return "[citation needed]"
        if key not in seen:
            seen.add(key)
            order.append(key)
        return citation_label(row, locator)

    # A full-width label needs no space before it: “偏见 [@KEY]” becomes “偏见（作者，年份）”.
    body = CITATION_WITH_SPACE.sub(substitute, body)
    # Chinese style puts the citation before the sentence's closing mark: “纠正。（作者，年份）” → “纠正（作者，年份）。”
    body = LABEL_AFTER_STOP.sub(r"\2\1", body)
    return body, errors, order


def extract_title(cell: str) -> str:
    """Return the first double-quoted span of a Title cell, else the cell."""
    match = re.search(r"[\"“](.+?)[\"”]", cell)
    return match.group(1).strip() if match else cell.strip()


def build_references(keys: list[str], index_rows: dict[str, dict]) -> str:
    lines = ["# 参考文献", ""]
    for key in keys:
        row = index_rows[key]
        author = row_cell(row, 1).rstrip(". ")
        title = extract_title(row_cell(row, 2)).rstrip(". ")
        lines.append(f"- {author}. {year_from_row(row)}. {title}.")
    return "\n".join(lines)


def append_references(body: str, keys: list[str], index_rows: dict[str, dict]) -> str:
    if not keys:
        return body
    section = build_references(keys, index_rows)
    return body.rstrip() + "\n\n" + section + "\n"


def preprocess_body(
    kind: str | None,
    body: str,
    refs_keys: set[str],
    index_rows: dict[str, dict],
) -> tuple[str, list[str], list[str]]:
    """Rewrite citations and, for handouts only, append the reference list."""
    body, errors, order = replace_citations(body, refs_keys, index_rows)
    if kind == "handout":
        body = append_references(body, order, index_rows)
    return body, errors, order


# ---------------------------------------------------------------------------
# Quotations
# ---------------------------------------------------------------------------

TRAILING_PAREN_CITATION = re.compile(r"（[^）]*，[^）]*）\s*$")
TRAILING_RAW_CITATION = re.compile(r"\[@[^\]]*\]\s*$")
TRAILING_RAW_KEY = re.compile(r"\[@([A-Z0-9][A-Z0-9-]*)(?:,[^\]]*)?\]\s*$")


def strip_quote_marks(text: str) -> str:
    return text.translate({ord(char): None for char in QUOTE_MARKS})


def remove_whitespace(text: str) -> str:
    return re.sub(r"\s+", "", text)


def drop_trailing_citation(text: str) -> str:
    """Remove a citation that ends a quotation, replaced or raw."""
    text = text.rstrip()
    text = TRAILING_RAW_CITATION.sub("", text)
    text = TRAILING_PAREN_CITATION.sub("", text)
    return text.rstrip()


def quotation_matches(query: str, source: str) -> bool:
    return bool(query) and (query in source or query in remove_whitespace(source))


def blocks_text_span(path: Path) -> list[str]:
    spans: list[str] = []
    if not path.is_file():
        return spans
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        span = record.get("text_span")
        if isinstance(span, str):
            spans.append(span)
    return spans


def collect_quotations(
    body: str,
    index_rows: dict[str, dict],
    quote_sources: list[Path],
    root: Path,
) -> tuple[list[dict], list[str]]:
    """Check every block quote and report it as ``{text, verified}``.

    A quotation is verified when its cleaned text occurs in a ``--quote-source``
    file or in the ``text_span`` of the cited KEY's ``blocks.jsonl``.  An
    unverified quotation is a warning, never an error.
    """
    sources: list[str] = []
    for path in quote_sources:
        path = Path(path)
        if path.is_file():
            sources.append(path.read_text(encoding="utf-8"))

    quotations: list[dict] = []
    warnings: list[str] = []
    lines = normalize_newlines(body).split("\n")
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith(">"):
            index += 1
            continue
        run: list[str] = []
        while index < len(lines) and lines[index].lstrip().startswith(">"):
            text = lines[index].lstrip()[1:]
            run.append(text[1:] if text.startswith(" ") else text)
            index += 1
        raw = "\n".join(run)
        key_match = TRAILING_RAW_KEY.search(raw)
        key = key_match.group(1) if key_match else None
        text = drop_trailing_citation(raw)
        core = strip_quote_marks(text)
        query = remove_whitespace(core)

        candidates = list(sources)
        if key is not None and key in index_rows:
            pdfs = index_rows[key].get("pdfs") or []
            if pdfs:
                stem = Path(pdfs[0]).stem
                extract = root / "Private/Bibliography/Extract" / stem / "blocks.jsonl"
                candidates.extend(blocks_text_span(extract))

        verified = any(quotation_matches(query, source) for source in candidates)
        cleaned = re.sub(r"\s+", " ", core).strip()
        quotations.append({"text": cleaned[:40], "verified": verified})
        if not verified:
            warnings.append(f"unverified-quotation:{len(quotations)}")
    return quotations, warnings


# ---------------------------------------------------------------------------
# Slide checks
# ---------------------------------------------------------------------------

def is_fence(stripped: str) -> bool:
    return stripped.startswith("```") or stripped.startswith("~~~")


def item_text(line: str) -> str:
    """Return a list item's text with its marker removed."""
    line = line.rstrip()
    example = re.match(r"^\(@[^)]*\)\s*", line)
    if example:
        return line[example.end():]
    marker = re.match(r"^(?:[-*+]|\d+[.)])\s+", line)
    return line[marker.end():] if marker else line


def split_slides(body: str) -> list[list[str]]:
    """Split a body into slides, each starting at a ``# `` heading line."""
    slides: list[list[str]] = []
    current: list[str] | None = None
    in_fence = False
    for line in normalize_newlines(body).split("\n"):
        stripped = line.strip()
        if in_fence:
            if current is not None:
                current.append(line)
            if is_fence(stripped):
                in_fence = False
            continue
        if is_fence(stripped):
            in_fence = True
            if current is not None:
                current.append(line)
            continue
        if line.startswith("# "):
            current = [line]
            slides.append(current)
            continue
        if current is not None:
            current.append(line)
    return slides


def analyze_slide(lines: list[str]) -> dict:
    """Collect items, notes, and quotes from one slide's lines."""
    items: list[str] = []
    quotes: list[str] = []
    has_notes = False
    in_notes = False
    in_fence = False
    quote_run: list[str] = []

    def flush_quote() -> None:
        if quote_run:
            quotes.append("".join(quote_run))
            quote_run.clear()

    for line in lines[1:]:
        stripped = line.strip()
        if in_fence:
            if is_fence(stripped):
                in_fence = False
            continue
        if is_fence(stripped):
            flush_quote()
            in_fence = True
            continue
        if in_notes:
            if stripped == ":::":
                in_notes = False
            continue
        if stripped.startswith("::: notes"):
            has_notes = True
            in_notes = True
            flush_quote()
            continue
        if stripped.startswith(":::"):
            continue
        if ITEM_LINE.match(line):
            flush_quote()
            items.append(item_text(line))
            continue
        if line.lstrip().startswith(">"):
            quote_run.append(line.lstrip()[1:].strip())
            continue
        flush_quote()
    flush_quote()
    return {"items": items, "quotes": quotes, "has_notes": has_notes}


def analyze_slides(body: str, minutes: int | None) -> tuple[list[str], dict]:
    """Return slide warnings and metrics."""
    warnings: list[str] = []
    slides = split_slides(body)
    for number, lines in enumerate(slides, start=1):
        data = analyze_slide(lines)
        if len(data["items"]) > 5:
            warnings.append(f"too-many-items:{number}")
        for text in data["items"]:
            if item_length(text) > 24:
                warnings.append(f"long-item:{number}:{text[:15]}")
        for quote in data["quotes"]:
            if han_count(quote) > 40:
                warnings.append(f"quote-on-slide:{number}")
        if 1 < number < len(slides) and not data["has_notes"]:
            warnings.append(f"no-notes:{number}")

    slide_count = len(slides) + 1  # content slides plus the title slide
    if minutes:
        if not (minutes / 1.5 <= slide_count <= minutes * 1.0 + 2):
            warnings.append(f"slide-count:{slide_count} for {minutes} min")
    return warnings, {"slide_count": slide_count, "minutes": minutes}


# ---------------------------------------------------------------------------
# Page counting and tool discovery
# ---------------------------------------------------------------------------

def count_pages(pdf_path: Path) -> int | None:
    """Count PDF pages, falling back to pdfminer when objects are compressed."""
    try:
        data = Path(pdf_path).read_bytes()
    except OSError:
        return None
    count = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", data))
    if count:
        return count
    try:
        from pdfminer.high_level import extract_pages

        return sum(1 for _ in extract_pages(str(pdf_path)))
    except Exception:
        return None


def find_root(start: Path | None = None) -> Path | None:
    """Walk up to the directory that contains Framework/Workflow/manifest.json."""
    directory = Path(start or SCRIPT_DIR).resolve()
    for parent in [directory, *directory.parents]:
        if (parent / "Framework/Workflow/manifest.json").is_file():
            return parent
    return None


def find_refs(content_path: Path, root: Path | None) -> Path | None:
    """Find the nearest refs.md above the content file, stopping at root."""
    directory = Path(content_path).resolve().parent
    stop = root.resolve() if root is not None else None
    while True:
        candidate = directory / "refs.md"
        if candidate.is_file():
            return candidate
        if stop is not None and directory == stop:
            return None
        if directory == directory.parent:
            return None
        directory = directory.parent


def find_pandoc() -> Path | None:
    env = os.environ.get("PANDOC")
    if env and Path(env).is_file():
        return Path(env)
    found = shutil.which("pandoc")
    if found:
        return Path(found)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidate = Path(local) / "Programs/pandoc/pandoc.exe"
        if candidate.is_file():
            return candidate
    return None


def find_browser() -> Path | None:
    env = os.environ.get("PHIL_BROWSER")
    if env:
        return Path(env)
    candidates: list[Path] = []
    program_files_x86 = os.environ.get("ProgramFiles(x86)")
    program_files = os.environ.get("ProgramFiles")
    local = os.environ.get("LOCALAPPDATA")
    if program_files_x86:
        candidates.append(Path(program_files_x86) / "Microsoft/Edge/Application/msedge.exe")
    if program_files:
        candidates.append(Path(program_files) / "Microsoft/Edge/Application/msedge.exe")
        candidates.append(Path(program_files) / "Google/Chrome/Application/chrome.exe")
    if local:
        candidates.append(Path(local) / "Google/Chrome/Application/chrome.exe")
    candidates.extend([
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
    ])
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    for name in ("chromium", "chromium-browser", "google-chrome", "microsoft-edge"):
        found = shutil.which(name)
        if found:
            return Path(found)
    return None


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def run_pandoc(pandoc: Path, arguments: list, errors: list[str]) -> bool:
    """Run Pandoc; a non-zero exit becomes an error containing its stderr."""
    command = [str(pandoc)] + [str(argument) for argument in arguments]
    completed = subprocess.run(command, check=False, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        errors.append(f"pandoc-failed: {detail}")
        return False
    return True


def assemble_markdown(header: str, body: str) -> str:
    return header + "\n" + body if header else body


def render_html(pandoc: Path, kind: str, markdown_path: Path, html_path: Path,
                root: Path, errors: list[str]) -> bool:
    css = root / (SLIDES_CSS if kind == "slides" else HANDOUT_CSS)
    arguments = ["-f", "markdown", "--quiet", "-t", "html5", "-s",
                 "--embed-resources", "--css", css, "-M", "lang=zh-CN"]
    if kind == "slides":
        arguments.append("--section-divs")
    arguments += ["-o", html_path, markdown_path]
    return run_pandoc(pandoc, arguments, errors)


def print_pdf(browser: Path, html_path: Path, pdf_path: Path,
              profile_dir: Path, errors: list[str]) -> bool:
    target = Path(pdf_path).resolve()
    # A stale PDF from an earlier run must not pass as this run's output.
    target.unlink(missing_ok=True)
    command = [str(browser), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
               f"--user-data-dir={profile_dir}", f"--print-to-pdf={target}",
               html_path.as_uri()]
    try:
        completed = subprocess.run(command, check=False, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        errors.append("pdf-failed: browser timed out")
        return False
    if not target.is_file() or target.stat().st_size == 0:
        detail = (completed.stderr or b"").decode("utf-8", "replace").strip()
        errors.append(f"pdf-failed: {detail or 'browser produced no output'}")
        return False
    return True


def render_document(fmt: str, kind: str, header: str, body: str, output_path: Path,
                    root: Path, pandoc: Path, browser: Path | None,
                    errors: list[str], warnings: list[str]) -> bool:
    """Render the content to ``fmt``; returns True when the output exists."""
    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        markdown_path = directory / "content.md"
        markdown_path.write_text(assemble_markdown(header, body), encoding="utf-8")

        if fmt in ("html", "pdf"):
            html_path = output_path if fmt == "html" else directory / "content.html"
            if not render_html(pandoc, kind, markdown_path, html_path, root, errors):
                return False
            if fmt == "html":
                return True
            return print_pdf(browser, html_path, output_path, directory / "profile", errors)

        reference = root / f"Shared/Format/reference.{fmt}"
        arguments = ["-f", "markdown", "--quiet", "-t", fmt]
        if fmt == "pptx":
            arguments.append("--slide-level=1")
        if reference.is_file():
            arguments += ["--reference-doc", reference]
        else:
            warnings.append(f"reference-{fmt}-missing")
        arguments += ["-o", output_path, markdown_path]
        return run_pandoc(pandoc, arguments, errors)


# ---------------------------------------------------------------------------
# make-reference
# ---------------------------------------------------------------------------

PTX_THEME = "ppt/theme/theme1.xml"
DOCX_STYLES = "word/styles.xml"
DOCX_RFONTS = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
               'w:cs="Times New Roman" w:eastAsia="SimSun" />')


def patch_pptx_theme(data: bytes) -> bytes:
    text = data.decode("utf-8")

    def set_fonts(block: str) -> str:
        for tag in ("latin", "ea"):
            block = re.sub(rf'(<a:{tag}\b[^>]*?typeface=")[^"]*(")',
                           rf"\g<1>Microsoft YaHei\g<2>", block, count=1)
        return block

    def set_color(block: str) -> str:
        return re.sub(r'(<a:srgbClr\b[^>]*?val=")[^"]*(")',
                      r"\g<1>1F3A5F\g<2>", block, count=1)

    text = re.sub(r"<a:majorFont>.*?</a:majorFont>", lambda m: set_fonts(m.group(0)),
                  text, flags=re.S)
    text = re.sub(r"<a:minorFont>.*?</a:minorFont>", lambda m: set_fonts(m.group(0)),
                  text, flags=re.S)
    text = re.sub(r"<a:accent1>.*?</a:accent1>", lambda m: set_color(m.group(0)),
                  text, flags=re.S)
    text = re.sub(r"<a:dk2>.*?</a:dk2>", lambda m: set_color(m.group(0)), text, flags=re.S)
    return text.encode("utf-8")


def patch_docx_styles(data: bytes) -> bytes:
    text = data.decode("utf-8")
    defaults = re.search(r"<w:docDefaults>.*?</w:docDefaults>", text, re.S)
    if defaults:
        block = re.sub(r"<w:rFonts\b[^>]*/>|<w:rFonts\b[^>]*>.*?</w:rFonts>",
                       DOCX_RFONTS, defaults.group(0), count=1, flags=re.S)
        text = text[:defaults.start()] + block + text[defaults.end():]
    return text.encode("utf-8")


def rewrite_zip(source: Path, target: Path, member: str, patcher) -> None:
    """Copy a zip entry by entry, patching one member and keeping order."""
    with zipfile.ZipFile(source) as source_zip, zipfile.ZipFile(target, "w") as target_zip:
        for info in source_zip.infolist():
            data = source_zip.read(info.filename)
            if info.filename == member:
                data = patcher(data)
            target_zip.writestr(info, data)


def make_reference(out_dir: Path, pandoc: Path) -> list[Path] | None:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        for name in ("pptx", "docx"):
            raw = directory / f"raw.{name}"
            completed = subprocess.run(
                [str(pandoc), "-o", str(raw), "--print-default-data-file", f"reference.{name}"],
                check=False, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if completed.returncode != 0 or not raw.is_file():
                print((completed.stderr or "pandoc could not print reference data").strip(),
                      file=sys.stderr)
                return None
            target = out_dir / f"reference.{name}"
            member = PTX_THEME if name == "pptx" else DOCX_STYLES
            patcher = patch_pptx_theme if name == "pptx" else patch_docx_styles
            rewrite_zip(raw, target, member, patcher)
            paths.append(target)
    return paths


# ---------------------------------------------------------------------------
# Reporting and commands
# ---------------------------------------------------------------------------

def write_report(report: dict, path: Path) -> None:
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_report(content: Path, kind: str | None, to: str | None, output: str | None,
                 errors: list[str], warnings: list[str], metrics: dict,
                 quotations: list[dict]) -> dict:
    return {
        "content": str(content),
        "kind": kind,
        "to": to,
        "output": output,
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
        "quotations": quotations,
    }


def check_report_path(content: Path) -> Path:
    return content.with_suffix(".check.json")


def render_report_path(content: Path, to: str) -> Path:
    return content.with_suffix(f".{to}.check.json")


def citation_metrics(body: str) -> dict:
    matches = list(CITATION.finditer(body))
    return {
        "citations": len(matches),
        "unique_keys": len({match.group(1) for match in matches}),
    }


def command_check(args, root: Path) -> int:
    content = args.content
    meta, _header, body = split_header(content.read_text(encoding="utf-8"))
    kind = meta.get("kind")
    errors = header_errors(meta)

    refs_keys = load_refs_keys(args.refs or find_refs(content, root))
    index_rows = load_index_rows(args.index or root / "Private/Bibliography/INDEX.md")
    quotations, quote_warnings = collect_quotations(body, index_rows, args.quote_source, root)
    warnings = list(quote_warnings)

    metrics = citation_metrics(body)
    body, citation_errors, _ = preprocess_body(kind, body, refs_keys, index_rows)
    errors += citation_errors

    if kind == "slides":
        slide_warnings, slide_metrics = analyze_slides(body, parse_minutes(meta.get("minutes")))
        warnings += slide_warnings
        metrics.update(slide_metrics)

    report = build_report(content, kind, None, None, errors, warnings, metrics, quotations)
    write_report(report, check_report_path(content))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def command_render(args, root: Path) -> int:
    content = args.content
    fmt = args.to
    meta, header, body = split_header(content.read_text(encoding="utf-8"))
    kind = meta.get("kind")

    pandoc = find_pandoc()
    if pandoc is None:
        print("pandoc not found: install it or set PANDOC", file=sys.stderr)
        return 2
    browser = None
    if fmt == "pdf":
        browser = find_browser()
        if browser is None:
            print("browser not found: install Edge or Chrome or set PHIL_BROWSER", file=sys.stderr)
            return 2

    errors = header_errors(meta)
    refs_keys = load_refs_keys(args.refs or find_refs(content, root))
    index_rows = load_index_rows(args.index or root / "Private/Bibliography/INDEX.md")
    quotations, quote_warnings = collect_quotations(body, index_rows, args.quote_source, root)
    warnings = list(quote_warnings)

    metrics = citation_metrics(body)
    body, citation_errors, _ = preprocess_body(kind, body, refs_keys, index_rows)
    errors += citation_errors

    if kind == "slides":
        slide_warnings, slide_metrics = analyze_slides(body, parse_minutes(meta.get("minutes")))
        warnings += slide_warnings
        metrics.update(slide_metrics)

    output = args.out or content.with_suffix(f".{fmt}")
    rendered = False
    if kind in ("handout", "slides"):
        rendered = render_document(fmt, kind, header, body, output, root, pandoc, browser,
                                   errors, warnings)

    if fmt == "pdf" and kind == "handout":
        pages = count_pages(output) if rendered else None
        metrics["pages"] = pages
        if pages and pages > 2:
            warnings.append(f"handout-pages:{pages}")

    report = build_report(content, kind, fmt, str(output) if rendered else None,
                          errors, warnings, metrics, quotations)
    write_report(report, render_report_path(content, fmt))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(
        description="Render and check a handout or slide deck content file."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_content_arguments(subparser) -> None:
        subparser.add_argument("content", type=Path)
        subparser.add_argument("--refs", type=Path)
        subparser.add_argument("--index", type=Path)
        subparser.add_argument("--quote-source", action="extend", nargs="+", type=Path,
                               default=[], metavar="FILE")

    render = subparsers.add_parser("render", help="render a content file")
    add_content_arguments(render)
    render.add_argument("--to", choices=["pdf", "pptx", "docx", "html"], required=True)
    render.add_argument("--out", type=Path)

    check = subparsers.add_parser("check", help="check without rendering")
    add_content_arguments(check)

    reference = subparsers.add_parser("make-reference", help="create patched Pandoc reference files")
    reference.add_argument("--out-dir", type=Path)

    args = parser.parse_args(argv)
    root = find_root() or Path.cwd()

    if args.command == "render":
        return command_render(args, root)
    if args.command == "check":
        return command_check(args, root)

    pandoc = find_pandoc()
    if pandoc is None:
        print("pandoc not found: install it or set PANDOC", file=sys.stderr)
        return 2
    paths = make_reference(args.out_dir or root / "Shared/Format", pandoc)
    if paths is None:
        return 2
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
