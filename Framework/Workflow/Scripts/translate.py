#!/usr/bin/env python3
"""Translate evidence units into Chinese through the user's model gateway.

Reads the evidence units written by ``pdf-extract.py blocks``, selects a page
or unit range, and translates each unit with ``deepseek-flash`` (or another
model) through the Anthropic-format gateway configured in the user's
environment or ``~/.claude/settings.json``.

Subcommands:

* ``plan``   — selection, cache, character and call estimates; no API calls.
* ``terms``  — propose glossary terms for the selection; one API call per chunk.
* ``run``    — translate uncached units and append each result immediately.
* ``check``  — deterministic QA over existing ``translation*.jsonl``; no API.

Only the Python standard library is required. Credentials are read from
``ANTHROPIC_BASE_URL`` and ``ANTHROPIC_AUTH_TOKEN`` and are never printed,
logged, or written.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_REL = "Framework/Workflow/Templates/Translate/system.md"
READER_REL = "Private/Bibliography/Reader"
EXTRACT_REL = "Private/Bibliography/Extract"
PROJECTS_REL = "Private/Projects"
SHARED_GLOSSARY_REL = "Shared/Glossary"
TRANSLATION_GLOB = "translation*.jsonl"
PAGE_MARKER = re.compile(r"⟦p([^⟧]+)⟧")
SECTION_NUMERAL = re.compile(r"^(?:[IVXLCDM]+|\d+)[.)]?$", re.IGNORECASE)
REFERENCES_HEADING = re.compile(r"^(?:references|bibliography|works cited)\.?$",
                                re.IGNORECASE)
# A note number glued to a word: ``flies’2`` or ``anger.4``. The digit run must
# follow a letter or closing punctuation and end at a word boundary.
GLUED_NOTE = re.compile(
    r"(?<!\d)(?<!\d\.)(?<=[A-Za-z’\"'”\)\].,])(\d{1,3})(?=[\s“\"(]|,(?=\d)|$)")
DEFAULT_MODEL = "deepseek-flash"
THINKING_BUDGET = 2000
MAX_UNITS_WITHOUT_YES = 60
DEFAULT_JOBS = 4
REQUEST_TIMEOUT = 180
TERMS_CHUNK = 40000


class TranslateError(Exception):
    """A user-facing error; the message is safe to print."""


class SelectionError(TranslateError):
    """The requested selection is missing or empty."""


class GatewayError(TranslateError):
    """The model gateway failed; credentials are already redacted."""


# ---------------------------------------------------------------------------
# Reuse reader-build.py for page markers, INDEX rows, and stem names
# ---------------------------------------------------------------------------

_READER_BUILD = None


def reader_build():
    global _READER_BUILD
    if _READER_BUILD is None:
        path = SCRIPT_DIR / "reader-build.py"
        spec = importlib.util.spec_from_file_location("reader_build_translate", path)
        if spec is None or spec.loader is None:
            raise TranslateError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _READER_BUILD = module
    return _READER_BUILD


def insert_page_markers(text: str, page_breaks: list[dict]) -> str:
    return reader_build().insert_page_markers(text, page_breaks or [])


def index_row(root: Path, stem: str) -> dict:
    return reader_build().index_row(root, stem)


def find_root(start: Path | None = None) -> Path | None:
    directory = Path(start or SCRIPT_DIR).resolve()
    for parent in [directory, *directory.parents]:
        if (parent / "Framework/Workflow/manifest.json").is_file():
            return parent
    return None


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def read_jsonl(path: Path) -> list[dict]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# Explicit Latin ligature map. NFKC is deliberately avoided: it would also turn
# superscript digits into note numbers.
LIGATURES = str.maketrans({
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi",
    "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st",
})


def normalize_ligatures(text: str) -> str:
    return (text or "").translate(LIGATURES)


def block_text(block: dict) -> str:
    return block.get("text_span") or ""


def block_hash(block: dict) -> str:
    return block.get("unit_sha256") or sha256_text(block_text(block))


def block_kind(block: dict) -> str:
    return (block.get("layout") or {}).get("kind") or "body"


def page_labels_of(block: dict) -> list[str]:
    labels: list[str] = []
    value = (block.get("locator") or {}).get("value") or ""
    labels.extend(split_label(value))
    for page_break in (block.get("layout") or {}).get("page_breaks") or []:
        labels.extend(split_label(str(page_break.get("page_label") or "")))
    return [label for label in labels if label]


def split_label(value: str) -> list[str]:
    value = (value or "").strip()
    if not value:
        return []
    if re.fullmatch(r"\d+\s*[–-]\s*\d+", value):
        return [part.strip() for part in re.split(r"[–-]", value)]
    return [value]


def page_order(blocks: list[dict]) -> list[str]:
    order: list[str] = []
    seen: set[str] = set()
    for block in blocks:
        for label in page_labels_of(block):
            if label not in seen:
                seen.add(label)
                order.append(label)
    return order


def label_in_range(label: str, low: str, high: str, order: list[str]) -> bool:
    numeric = (re.fullmatch(r"\d+", low) and re.fullmatch(r"\d+", high)
               and re.fullmatch(r"\d+", label))
    if numeric:
        return int(low) <= int(label) <= int(high)
    positions = {value: index for index, value in enumerate(order)}
    if label in positions and low in positions and high in positions:
        return positions[low] <= positions[label] <= positions[high]
    return low <= label <= high


def is_verbatim(text: str) -> bool:
    stripped = (text or "").strip()
    if not re.search(r"[A-Za-z]", stripped):
        return True
    return bool(SECTION_NUMERAL.match(stripped))


def references_cutoff(blocks: list[dict]) -> int:
    for index, block in enumerate(blocks):
        if REFERENCES_HEADING.match(block_text(block).strip()):
            return index
    return len(blocks)


def select_units(blocks: list[dict], *, pages: tuple[str, str] | None = None,
                 from_id: str | None = None, to_id: str | None = None,
                 all_units: bool = False, include_references: bool = False) -> list[dict]:
    """Return the selected units after kind and reference-list filtering."""
    count = len(blocks)
    if all_units:
        indexes = set(range(count))
    elif pages:
        low, high = pages
        order = page_order(blocks)
        indexes = {index for index, block in enumerate(blocks)
                   if any(label_in_range(label, low, high, order)
                          for label in page_labels_of(block))}
    elif from_id or to_id:
        ids = [block["unit_id"] for block in blocks]
        for unit_id in (from_id, to_id):
            if unit_id and unit_id not in ids:
                raise SelectionError(f"unknown unit: {unit_id}")
        start = ids.index(from_id) if from_id else 0
        end = ids.index(to_id) if to_id else count - 1
        if start > end:
            raise SelectionError("--from unit comes after --to unit")
        indexes = set(range(start, end + 1))
    else:
        raise SelectionError("no selection: pass --pages, --from/--to, or --all")

    cutoff = references_cutoff(blocks)
    selected = []
    for index in sorted(indexes):
        block = blocks[index]
        if block_kind(block) == "other":
            continue
        if index >= cutoff and not include_references:
            continue
        selected.append(block)
    return selected


# ---------------------------------------------------------------------------
# Glossary
# ---------------------------------------------------------------------------

# The 备注 cell may carry ``避免：A、B``. Accept both colons and the common
# Chinese and ASCII separators.
AVOID_MARKER = re.compile(r"避免\s*[：:]\s*(.+)$")
AVOID_SPLIT = re.compile(r"[、，,]")


def parse_avoid(note: str) -> list[str]:
    """Return the ``避免：`` variants named in a glossary note cell."""
    match = AVOID_MARKER.search(note or "")
    if not match:
        return []
    variants = [part.strip() for part in AVOID_SPLIT.split(match.group(1))]
    return [variant for variant in variants if variant]


def parse_glossary_file(path: Path) -> list[dict]:
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip().replace("**", "") for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        english, chinese = cells[0], cells[1]
        note = cells[2] if len(cells) > 2 else ""
        if not english or not chinese:
            continue
        if english.lower() in {"english", "term", "source term"}:
            continue
        if set(english) <= set("-: "):
            continue
        avoid = parse_avoid(note)
        for variant in re.split(r"\s+/\s+", english):
            variant = normalize_ligatures(variant.strip())
            if variant:
                entries.append({"en": variant, "zh": chinese, "note": note,
                                "avoid": avoid, "source": path.name})
    return entries


def glossary_paths(root: Path, stem: str, project: str | None,
                   out: Path | None) -> list[Path]:
    """Return glossary files, highest precedence first."""
    paths: list[Path] = []
    if out is not None:
        out_glossary = out / "glossary.md"
        if out_glossary.is_file():
            paths.append(out_glossary)
    reader_glossary = root / READER_REL / stem / "glossary.md"
    if reader_glossary.is_file():
        paths.append(reader_glossary)
    if project:
        project_glossary = root / PROJECTS_REL / project / "glossary.md"
        if project_glossary.is_file():
            paths.append(project_glossary)
    shared = root / SHARED_GLOSSARY_REL
    if shared.is_dir():
        paths.extend(sorted(shared.glob("*.md")))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def load_glossary(root: Path, stem: str, project: str | None,
                  out: Path | None) -> tuple[list[dict], list[dict]]:
    """Merge glossary sources; return ``(entries, conflicts)``.

    Entries are sorted by lowercase English term. On a conflict the
    higher-precedence source wins and the conflict is reported.
    """
    merged: dict[str, dict] = {}
    conflicts: list[dict] = []
    for path in glossary_paths(root, stem, project, out):
        for entry in parse_glossary_file(path):
            key = entry["en"].lower()
            if key not in merged:
                merged[key] = dict(entry)
            elif merged[key]["zh"] != entry["zh"]:
                conflicts.append({"en": entry["en"], "kept": merged[key]["zh"],
                                  "rejected": entry["zh"],
                                  "source": entry["source"]})
    entries = [merged[key] for key in sorted(merged)]
    return entries, conflicts


def glossary_digest(entries: list[dict]) -> str:
    payload = [{"en": entry["en"], "zh": entry["zh"],
                "note": entry.get("note", "")} for entry in entries]
    return sha256_text(json.dumps(payload, ensure_ascii=False, sort_keys=True))


_TERM_PATTERNS: dict[str, re.Pattern] = {}


def term_pattern(term: str) -> re.Pattern:
    term = normalize_ligatures(term)
    if term not in _TERM_PATTERNS:
        _TERM_PATTERNS[term] = re.compile(
            r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", re.IGNORECASE)
    return _TERM_PATTERNS[term]


def term_occurrences(text: str, entries: list[dict]) -> list[dict]:
    text = normalize_ligatures(text)
    return [entry for entry in entries if term_pattern(entry["en"]).search(text)]


def first_occurrence_map(blocks: list[dict], entries: list[dict]) -> dict[str, int]:
    """Map lowercase English term to the first block index it occurs in."""
    first: dict[str, int] = {}
    for index, block in enumerate(blocks):
        text = normalize_ligatures(block_text(block))
        for entry in entries:
            key = entry["en"].lower()
            if key in first:
                continue
            if term_pattern(entry["en"]).search(text):
                first[key] = index
    return first


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

def document_line(root: Path, stem: str, row: dict) -> str:
    """Return ``Author. Title (Year).`` from the INDEX row when available."""
    build = reader_build()
    author = build.display_author(build.cell(row, 1))
    title = build.extract_title(build.cell(row, 2))
    year = build.year_of(stem)
    parts = [part for part in (author, title) if part]
    line = ". ".join(parts)
    if year:
        line = f"{line} ({year})" if line else f"({year})"
    return f"{line}." if line and not line.endswith(".") else line


def context_excerpt(text: str, limit: int, *, leading: bool) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit] if leading else text[-limit:]


def render_glossary_block(entries: list[dict]) -> str:
    lines = ["固定术语表（English → 中文）。这些译名不可更改；"
             "只有本单元标记（首次出现）的条目，才在中文后括注英文；"
             "其余条目一律不加英文括注。", ""]
    if entries:
        lines.append("| English | 中文 |")
        lines.append("| --- | --- |")
        for entry in entries:
            lines.append(f"| {entry['en']} | {entry['zh']} |")
    else:
        lines.append("（术语表为空。）")
    return "\n".join(lines)


def system_blocks(root: Path, entries: list[dict]) -> list[dict]:
    template = root / TEMPLATE_REL
    if not template.is_file():
        raise TranslateError(f"missing translation prompt: {template}")
    rules = template.read_text(encoding="utf-8").strip()
    return [
        {"type": "text", "text": rules},
        {"type": "text", "text": render_glossary_block(entries),
         "cache_control": {"type": "ephemeral"}},
    ]


def build_messages(block: dict, index: int, blocks: list[dict], cache: dict[str, dict],
                   entries: list[dict], first_map: dict[str, int], doc_line: str) -> list[dict]:
    """Build the single user message for one unit."""
    text = normalize_ligatures(insert_page_markers(
        block_text(block), (block.get("layout") or {}).get("page_breaks") or []))
    lines: list[str] = []
    if doc_line:
        lines.append(f"文献：{doc_line}")
        lines.append("")

    if index > 0:
        previous = blocks[index - 1]
        source = normalize_ligatures(
            context_excerpt(block_text(previous), 1200, leading=False))
        if source:
            lines.append("[不要翻译] 上一段原文（节选）：")
            lines.append(source)
            lines.append("")
        cached = cache.get(previous.get("unit_id"))
        if cached and cached.get("unit_sha256") == block_hash(previous):
            zh = (cached.get("zh") or "").strip()
            if zh:
                lines.append("[不要翻译] 上一段译文：")
                lines.append(zh)
                lines.append("")

    if index + 1 < len(blocks):
        source = normalize_ligatures(
            context_excerpt(block_text(blocks[index + 1]), 600, leading=True))
        if source:
            lines.append("[不要翻译] 下一段原文（节选）：")
            lines.append(source)
            lines.append("")

    lines.append(f"本单元类型：{block_kind(block)}")
    occurring = term_occurrences(block_text(block), entries)
    lines.append("本单元出现的术语（只有标注（首次出现）的条目才加英文括注，其余一律不加）：")
    if occurring:
        for entry in occurring:
            is_first = first_map.get(entry["en"].lower()) == index
            marker = ("（首次出现，须在中文后括注英文）" if is_first
                      else "（非首次出现，不加英文括注）")
            lines.append(f"- {entry['en']} → {entry['zh']}{marker}")
    else:
        lines.append("- （无）")
    lines.append("")
    lines.append("待译原文：")
    lines.append(text)
    return [{"role": "user", "content": "\n".join(lines).strip()}]


# ---------------------------------------------------------------------------
# Gateway
# ---------------------------------------------------------------------------

def gateway_credentials() -> tuple[str, str]:
    base = os.environ.get("ANTHROPIC_BASE_URL")
    token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not (base and token):
        settings = Path.home() / ".claude/settings.json"
        if settings.is_file():
            try:
                data = json.loads(settings.read_text(encoding="utf-8"))
                env = data.get("env") if isinstance(data, dict) else None
            except (OSError, ValueError):
                env = None
            env = env if isinstance(env, dict) else {}
            base = base or env.get("ANTHROPIC_BASE_URL")
            token = token or env.get("ANTHROPIC_AUTH_TOKEN")
    if not (base and token):
        raise GatewayError(
            "no model credentials: set ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN")
    return base.rstrip("/"), token


def redact(text: str, token: str) -> str:
    if token:
        text = text.replace(token, "<redacted>")
    return text


def endpoint_candidates(base: str) -> list[str]:
    base = base.rstrip("/")
    candidates = [f"{base}/messages"]
    if base.endswith("/v1"):
        candidates.append(f"{base[:-3]}/v1/messages")
    else:
        candidates.append(f"{base}/v1/messages")
    unique: list[str] = []
    for url in candidates:
        if url not in unique:
            unique.append(url)
    return unique


def call_model(system: list[dict], messages: list[dict], model: str,
               max_tokens: int, timeout: int = REQUEST_TIMEOUT,
               retries: int = 3) -> dict:
    """POST to the gateway with thinking on; return text, stop reason, usage."""
    base, token = gateway_credentials()
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "thinking": {"type": "enabled", "budget_tokens": THINKING_BUDGET},
        "system": system,
        "messages": messages,
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "content-type": "application/json",
        "anthropic-version": "2023-06-01",
        "x-api-key": token,
        "authorization": f"Bearer {token}",
    }

    last_error: GatewayError | None = None
    for attempt in range(retries):
        saw_not_found = False
        for url in endpoint_candidates(base):
            request = urllib.request.Request(url, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    raw = response.read().decode("utf-8")
            except urllib.error.HTTPError as exc:
                detail = ""
                try:
                    detail = exc.read().decode("utf-8", "replace")
                except OSError:
                    pass
                message = redact(f"gateway HTTP {exc.code}: {detail[:400]}", token)
                if exc.code in (404, 405):
                    saw_not_found = True
                    last_error = GatewayError(message)
                    continue
                if exc.code == 429 or exc.code >= 500:
                    last_error = GatewayError(message)
                    break
                raise GatewayError(message) from None
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = GatewayError(
                    redact(f"gateway unreachable: {exc}", token))
                break

            try:
                data = json.loads(raw)
            except ValueError:
                last_error = GatewayError("gateway returned invalid JSON")
                break
            text = "".join(part.get("text", "") for part in data.get("content") or []
                           if part.get("type") == "text")
            return {"text": text,
                    "stop_reason": data.get("stop_reason"),
                    "usage": data.get("usage") or {}}

        if attempt < retries - 1:
            time.sleep(2 ** attempt)
        elif saw_not_found and last_error is None:
            last_error = GatewayError("gateway endpoint not found")
    raise last_error or GatewayError("gateway request failed")


def complete(system: list[dict], messages: list[dict], model: str,
             max_tokens: int, usage_log: list[dict] | None = None) -> str:
    """One logical completion, retrying once if the answer is truncated."""
    result = call_model(system, messages, model, max_tokens)
    if usage_log is not None:
        usage_log.append(result.get("usage") or {})
    if result.get("stop_reason") == "max_tokens":
        result = call_model(system, messages, model, max_tokens * 2)
        if usage_log is not None:
            usage_log.append(result.get("usage") or {})
    return (result.get("text") or "").strip()


# ---------------------------------------------------------------------------
# Deterministic QA
# ---------------------------------------------------------------------------

NEGATION_SOURCE = re.compile(
    r"\b(?:not|no|never|nothing|none|neither|nor|cannot|without)\b|n't",
    re.IGNORECASE)
NEGATION_ZH = "不没无非未否莫勿别"
HEDGE_SOURCE = re.compile(
    r"\b(?:may|might|perhaps|possibly|likely|probably|seems?|appears?|could|"
    r"presumably|potentially?|possibilit(?:y|ies))\b",
    re.IGNORECASE)
HEDGE_ZH = re.compile(r"(?:可能|也许|或许|大概|似乎)(?!性)")
ONLY_SOURCE = re.compile(r"\b(?:only|alone|solely|exclusively)\b", re.IGNORECASE)
ONLY_ZH = "只唯仅才单独"
CITATION = re.compile(
    r"\b[A-Z][A-Za-z’'\-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-z’'\-]+)?"
    r"\s+\d{4}[a-z]?(?:\s*,\s*(?:pp?\.\s*)?\d+(?:\s*[–-]\s*\d+)?)?")
LATIN_RUN = re.compile(r"[A-Za-z][A-Za-z’'\-]*(?:\s+[A-Za-z][A-Za-z’'\-]*){3,}")

# Calibrated on the hand-reviewed Srinivasan demo translations; the observed
# range was 0.36–1.00, so the band sits just outside it.
LENGTH_BAND = (0.30, 1.10)


def marker_labels(text: str) -> list[str]:
    return PAGE_MARKER.findall(text)


def latin_residue(zh: str) -> str | None:
    """Return a residual Latin run, ignoring parentheticals and citations."""
    text = re.sub(r"（[^）]*）|\([^)]*\)", " ", zh)
    text = CITATION.sub(" ", text)
    for match in LATIN_RUN.finditer(text):
        run = match.group(0)
        # Proper-noun runs (titles, names) are expected in bibliographic prose;
        # a leftover English phrase normally contains a lowercase word.
        if any(word[:1].islower() for word in run.split()):
            return run
    return None


def qa_unit(block: dict, zh: str, entries: list[dict]) -> list[dict]:
    """Run the deterministic checks and return flags ``{code, level, detail}``."""
    flags: list[dict] = []
    raw = block_text(block)
    # Insert markers against the original offsets first, then normalise.
    marked = normalize_ligatures(insert_page_markers(
        raw, (block.get("layout") or {}).get("page_breaks") or []))
    source = normalize_ligatures(raw)
    zh_plain = PAGE_MARKER.sub("", zh)
    source_plain = PAGE_MARKER.sub("", marked)

    if marker_labels(marked) != marker_labels(zh):
        flags.append({"code": "page-markers", "level": "error",
                      "detail": f"source {marker_labels(marked)} vs zh {marker_labels(zh)}"})

    missing = sorted({entry["en"] for entry in term_occurrences(source, entries)
                      if entry["zh"] not in zh})
    if missing:
        flags.append({"code": "glossary", "level": "error",
                      "detail": "missing: " + ", ".join(missing)})

    avoided = []
    for entry in term_occurrences(source, entries):
        for variant in entry.get("avoid") or []:
            if variant in zh:
                avoided.append(f"{entry['en']} → {variant}")
    if avoided:
        flags.append({"code": "glossary-avoid", "level": "warning",
                      "detail": "avoided: " + ", ".join(sorted(set(avoided)))})

    source_notes = len(GLUED_NOTE.findall(source))
    zh_notes = len(re.findall(r"\[\d{1,3}\]", zh))
    if block_kind(block) == "footnote" and zh_notes and \
            re.match(r"\s*\d{1,3}(?=\D)", source) and \
            re.match(r"\s*\[\d{1,3}\]", zh):
        # A footnote unit's own leading number may be rendered ``[n]``; that is
        # not a running-text marker and must not count as one.
        zh_notes -= 1
    if source_notes != zh_notes:
        flags.append({"code": "note-markers", "level": "warning",
                      "detail": f"source {source_notes} vs zh {zh_notes}"})

    numbering_source = re.sub(r"\(cid:\d+\)", "", source_plain)
    missing_numbers = [run for run in sorted(set(re.findall(r"\d+", numbering_source)))
                       if run not in zh_plain]
    if missing_numbers:
        flags.append({"code": "numbers", "level": "warning",
                      "detail": "missing: " + ", ".join(missing_numbers)})

    residue = latin_residue(zh)
    if residue:
        flags.append({"code": "latin-residue", "level": "warning",
                      "detail": residue})

    source_negations = len(NEGATION_SOURCE.findall(source))
    zh_negations = sum(zh.count(char) for char in NEGATION_ZH)
    if zh_negations < source_negations:
        flags.append({"code": "negation", "level": "warning",
                      "detail": f"source {source_negations} vs zh {zh_negations}"})

    hedges = HEDGE_ZH.findall(zh)
    if not HEDGE_SOURCE.search(source) and hedges:
        flags.append({"code": "added-hedge", "level": "warning",
                      "detail": "added: " + ", ".join(sorted(set(hedges)))})

    if ONLY_SOURCE.search(source) and not any(char in zh for char in ONLY_ZH):
        flags.append({"code": "only", "level": "warning",
                      "detail": "source has only/alone but zh has no limiting word"})

    en_length = len(re.sub(r"\s", "", source_plain))
    zh_length = len(re.sub(r"\s", "", zh_plain))
    if en_length and zh_length:
        ratio = zh_length / en_length
        if not LENGTH_BAND[0] <= ratio <= LENGTH_BAND[1]:
            flags.append({"code": "length", "level": "warning",
                          "detail": f"ratio {ratio:.2f} outside "
                                    f"{LENGTH_BAND[0]}-{LENGTH_BAND[1]}"})
    return flags


def normalize_footnote_numbers(zh: str, block: dict, source: str) -> str:
    """Use the demo convention for note numbers inside footnote units."""
    if block_kind(block) != "footnote":
        return zh
    source = normalize_ligatures(source)
    match = re.match(r"\s*(\d{1,3})(?=\D)", source)
    if not match:
        return zh
    current = int(match.group(1))
    zh = re.sub(r"^\s*\[(\d{1,3})\]", lambda item: f"{item.group(1)} ", zh, count=1)
    zh = re.sub(r"^(\d{1,3})(?![\d\s])", lambda item: f"{item.group(1)} ", zh, count=1)

    def next_note(item: re.Match) -> str:
        nonlocal current
        number = int(item.group(1))
        if number == current + 1:
            current = number
            return f"{number} "
        return item.group(0)

    return re.sub(r"(?<=[。．.；;！!？?])\s*\[(\d{1,3})\]", next_note, zh)


def translate_unit(block: dict, messages: list[dict], system: list[dict],
                   model: str, entries: list[dict],
                   usage_log: list[dict] | None = None) -> tuple[str, list[dict]]:
    """Translate one unit; repair once when an error-level flag survives."""
    text = normalize_ligatures(insert_page_markers(
        block_text(block), (block.get("layout") or {}).get("page_breaks") or []))
    max_tokens = THINKING_BUDGET + max(1024, len(text))
    zh = normalize_footnote_numbers(
        complete(system, messages, model, max_tokens, usage_log),
        block, block_text(block))
    flags = qa_unit(block, zh, entries)
    errors = [flag for flag in flags if flag["level"] == "error"]
    if errors:
        detail = "；".join(f"{flag['code']}: {flag['detail']}" for flag in errors)
        repair = messages + [
            {"role": "assistant", "content": zh},
            {"role": "user",
             "content": f"译文有以下问题：{detail}。只输出修正后的译文。"},
        ]
        repaired = complete(system, repair, model, max_tokens, usage_log)
        if repaired:
            zh = normalize_footnote_numbers(repaired, block, block_text(block))
            flags = qa_unit(block, zh, entries)
    return zh, flags


# ---------------------------------------------------------------------------
# Cache and output
# ---------------------------------------------------------------------------

def cache_dirs(root: Path, stem: str, out: Path) -> list[Path]:
    default = root / READER_REL / stem
    directories = [default]
    if out.resolve() != default.resolve():
        directories.append(out)
    return directories


def load_cache(directories: list[Path]) -> dict[str, dict]:
    cached: dict[str, dict] = {}
    for directory in directories:
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob(TRANSLATION_GLOB), key=lambda item: item.name):
            for record in read_jsonl(path):
                if record.get("unit_id"):
                    cached[record["unit_id"]] = record
    return cached


def is_cached(block: dict, cache: dict[str, dict], force: bool) -> bool:
    if force:
        return False
    record = cache.get(block.get("unit_id"))
    return bool(record and record.get("unit_sha256") == block_hash(block))


def make_record(block: dict, zh: str, model: str, glossary_name: str,
                glossary_sha: str, flags: list[dict]) -> dict:
    return {
        "unit_id": block["unit_id"],
        "unit_sha256": block_hash(block),
        "zh": zh,
        "model": model,
        "glossary": glossary_name,
        "glossary_sha256": glossary_sha,
        "translated": datetime.date.today().isoformat(),
        "qa": flags,
    }


def append_record(path: Path, record: dict, lock: threading.Lock) -> None:
    line = json.dumps(record, ensure_ascii=False) + "\n"
    with lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())


def compact_translation(path: Path, blocks: list[dict]) -> int:
    """Dedupe by unit_id keeping the last line, in document order."""
    if not path.is_file():
        return 0
    order = {block["unit_id"]: index for index, block in enumerate(blocks)}
    records: dict[str, dict] = {}
    for record in read_jsonl(path):
        records[record["unit_id"]] = record
    rows = [records[unit_id] for unit_id in
            sorted(records, key=lambda unit_id: order.get(unit_id, len(order)))]
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8", newline="\n")
    os.replace(temporary, path)
    return len(rows)


def usage_totals(usage_log: list[dict]) -> dict[str, int]:
    total = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0}
    for usage in usage_log:
        for key in total:
            total[key] += int(usage.get(key) or 0)
    return total


# ---------------------------------------------------------------------------
# Term proposals
# ---------------------------------------------------------------------------

def chunk_source(text: str, size: int = TERMS_CHUNK) -> list[str]:
    chunks: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        piece = paragraph.strip()
        if not piece:
            continue
        if current and len(current) + len(piece) + 2 > size:
            chunks.append(current)
            current = piece
        else:
            current = f"{current}\n\n{piece}" if current else piece
    if current:
        chunks.append(current)
    return chunks


def parse_term_json(text: str) -> list[dict]:
    start, end = text.find("["), text.rfind("]")
    if start < 0 or end <= start:
        return []
    try:
        data = json.loads(text[start:end + 1])
    except ValueError:
        return []
    proposals = []
    for item in data if isinstance(data, list) else []:
        if not isinstance(item, dict):
            continue
        english = normalize_ligatures(str(item.get("en") or "").strip())
        chinese = str(item.get("zh") or "").strip()
        if english and chinese:
            proposals.append({"en": english, "zh": chinese,
                              "note": str(item.get("note") or "").strip()})
    return proposals


def propose_terms(root: Path, selected: list[dict], entries: list[dict],
                  model: str, usage_log: list[dict]) -> list[dict]:
    """Ask the model for recurring or central terms not already in the glossary."""
    system = system_blocks(root, entries)
    known = {entry["en"].lower() for entry in entries}
    seen: dict[str, dict] = {}
    source = "\n\n".join(normalize_ligatures(block_text(block)) for block in selected)
    for chunk in chunk_source(source):
        prompt = (
            "下面是文献原文节选。请列出其中反复出现或对论证关键的哲学术语，"
            "排除已经在术语表中的词。只输出 JSON 数组，每项为 "
            '{"en": "英文术语", "zh": "建议中译", "note": "简短说明"}，不要输出其他内容。\n\n'
            + chunk)
        raw = complete(system, [{"role": "user", "content": prompt}], model,
                       THINKING_BUDGET + 2048, usage_log)
        for proposal in parse_term_json(raw):
            key = proposal["en"].lower()
            if key in known or key in seen:
                continue
            seen[key] = proposal
    return [seen[key] for key in sorted(seen)]


def write_terms(path: Path, stem: str, proposals: list[dict]) -> int:
    """Append ``自动提议，待确认`` rows, skipping terms already present."""
    if not proposals:
        return 0
    existing = {entry["en"].lower() for entry in parse_glossary_file(path)} \
        if path.is_file() else set()
    rows = [proposal for proposal in proposals
            if proposal["en"].lower() not in existing]
    if not rows:
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        prefix = "\n" if not path.read_text(encoding="utf-8").endswith("\n") else ""
    else:
        prefix = (f"# Glossary — {stem}\n\n"
                  "| English | 中文 | 备注 |\n| --- | --- | --- |\n")
    lines = [f"| {row['en']} | {row['zh']} | 自动提议，待确认 |" for row in rows]
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(prefix + "\n".join(lines) + "\n")
    return len(rows)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def load_inputs(args) -> dict:
    root = (args.root or find_root() or Path.cwd()).resolve()
    stem = args.stem
    blocks_path = root / EXTRACT_REL / stem / "blocks.jsonl"
    if not blocks_path.is_file():
        raise TranslateError(
            f"missing evidence units: {blocks_path}\n"
            f"run: py -3 Framework/Workflow/Scripts/pdf-extract.py blocks "
            f"\"{root / 'Private/Bibliography/PDF' / (stem + '.pdf')}\" --key <KEY>")
    blocks = read_jsonl(blocks_path)
    out = Path(args.out).resolve() if args.out else (root / READER_REL / stem)
    entries, conflicts = load_glossary(root, stem, args.project, out)
    return {"root": root, "stem": stem, "blocks": blocks, "out": out,
            "entries": entries, "conflicts": conflicts,
            "glossary_name": args.project or "default",
            "glossary_sha": glossary_digest(entries),
            "cache": load_cache(cache_dirs(root, stem, out))}


def selection_of(args, blocks: list[dict]) -> list[dict]:
    return select_units(blocks, pages=args.pages, from_id=args.from_id,
                        to_id=args.to_id, all_units=args.all,
                        include_references=args.include_references)


def classify(selected: list[dict], cache: dict[str, dict], force: bool) -> dict:
    state = {"cached": [], "verbatim": [], "todo": []}
    for block in selected:
        if is_verbatim(block_text(block)):
            state["verbatim"].append(block)
        elif is_cached(block, cache, force):
            state["cached"].append(block)
        else:
            state["todo"].append(block)
    return state


# Per-call overheads measured on the Srinivasan trial (2026-11-24, deepseek-flash, thinking
# budget 2,000): about 1,500 uncached input tokens of rules and context besides the source,
# and about 4,000 output tokens of thinking besides the translation itself (five units:
# 7,661 input + 7,936 cached input, 21,598 output).
INPUT_OVERHEAD_TOKENS = 1500
OUTPUT_OVERHEAD_TOKENS = 4000


def estimate_text(state: dict) -> str:
    characters = sum(len(block_text(block)) for block in state["todo"])
    calls = len(state["todo"])
    source_tokens = characters // 4
    input_tokens = source_tokens * 3 + calls * INPUT_OVERHEAD_TOKENS
    output_tokens = source_tokens * 2 + calls * OUTPUT_OVERHEAD_TOKENS
    return (f"to translate: {calls} units, {characters} source characters "
            f"(~{source_tokens} source tokens; estimated ~{input_tokens} input and "
            f"~{output_tokens} output tokens including thinking, {calls} calls)")


def cmd_plan(args) -> int:
    data = load_inputs(args)
    selected = selection_of(args, data["blocks"])
    if not selected:
        raise SelectionError("selection is empty")
    state = classify(selected, data["cache"], args.force)
    print(f"stem: {data['stem']}")
    print(f"selected: {len(selected)} units")
    print(f"cached: {len(state['cached'])}")
    print(f"verbatim (no API call): {len(state['verbatim'])}")
    print(estimate_text(state))
    print(f"glossary: {data['glossary_name']} ({len(data['entries'])} terms, "
          f"sha256 {data['glossary_sha'][:12]})")
    for conflict in data["conflicts"]:
        print(f"glossary conflict: {conflict['en']} kept {conflict['kept']!r} "
              f"from {conflict['source']}, dropped {conflict['rejected']!r}")
    return 0


def cmd_terms(args) -> int:
    data = load_inputs(args)
    selected = selection_of(args, data["blocks"])
    if not selected:
        raise SelectionError("selection is empty")
    usage_log: list[dict] = []
    proposals = propose_terms(data["root"], selected, data["entries"],
                              args.model, usage_log)
    path = data["out"] / "glossary.md"
    written = write_terms(path, data["stem"], proposals)
    print(f"proposed terms: {len(proposals)}, written: {written}")
    for proposal in proposals:
        print(f"- {proposal['en']} → {proposal['zh']}")
    print(f"glossary file: {path}")
    totals = usage_totals(usage_log)
    print(f"usage: input={totals['input_tokens']} output={totals['output_tokens']} "
          f"cache_read={totals['cache_read_input_tokens']}")
    return 0


def cmd_run(args) -> int:
    data = load_inputs(args)
    selected = selection_of(args, data["blocks"])
    if not selected:
        raise SelectionError("selection is empty")
    state = classify(selected, data["cache"], args.force)
    if len(state["todo"]) > MAX_UNITS_WITHOUT_YES and not args.yes:
        raise TranslateError(
            f"refusing to translate {len(state['todo'])} units without --yes; "
            f"{estimate_text(state)}")

    root, stem, out = data["root"], data["stem"], data["out"]
    entries, conflicts = data["entries"], data["conflicts"]
    usage_log: list[dict] = []
    terms_written = 0
    if state["todo"] and not args.no_terms:
        reader_glossary = root / READER_REL / stem / "glossary.md"
        out_glossary = out / "glossary.md"
        if not reader_glossary.is_file() and not out_glossary.is_file():
            proposals = propose_terms(root, selected, entries, args.model, usage_log)
            terms_written = write_terms(out_glossary, stem, proposals)
            if terms_written:
                entries, conflicts = load_glossary(root, stem, args.project, out)

    system = system_blocks(root, entries)
    first_map = first_occurrence_map(data["blocks"], entries)
    doc_line = document_line(root, stem, index_row(root, stem))
    positions = {block["unit_id"]: index for index, block in enumerate(data["blocks"])}
    lock = threading.Lock()
    output_path = out / "translation.jsonl"
    glossary_sha = glossary_digest(entries)
    failures: list[str] = []
    flagged: list[str] = []

    def finish(block: dict, zh: str, flags: list[dict]) -> None:
        append_record(output_path, make_record(
            block, zh, args.model, data["glossary_name"], glossary_sha, flags), lock)
        if flags:
            flagged.append(f"{block['unit_id']} ({', '.join(f['code'] for f in flags)})")

    for block in state["verbatim"]:
        text = insert_page_markers(
            block_text(block), (block.get("layout") or {}).get("page_breaks") or [])
        finish(block, text, [])

    def work(block: dict) -> tuple[dict, str, list[dict]]:
        messages = build_messages(block, positions[block["unit_id"]], data["blocks"],
                                  data["cache"], entries, first_map, doc_line)
        zh, flags = translate_unit(block, messages, system, args.model, entries,
                                   usage_log)
        return block, zh, flags

    if state["todo"]:
        with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
            futures = {pool.submit(work, block): block for block in state["todo"]}
            for future in as_completed(futures):
                block = futures[future]
                try:
                    finished_block, zh, flags = future.result()
                except Exception as exc:  # noqa: BLE001 - per-unit isolation
                    failures.append(f"{block['unit_id']}: {exc}")
                    continue
                finish(finished_block, zh, flags)

    compacted = compact_translation(output_path, data["blocks"])
    totals = usage_totals(usage_log)
    print(f"run: {stem}")
    print(f"selected: {len(selected)}  cached: {len(state['cached'])}  "
          f"verbatim: {len(state['verbatim'])}  "
          f"translated: {len(state['todo']) - len(failures)}  failed: {len(failures)}")
    if terms_written:
        print(f"glossary terms proposed: {terms_written}")
    for conflict in conflicts:
        print(f"glossary conflict: {conflict['en']} kept {conflict['kept']!r} "
              f"from {conflict['source']}, dropped {conflict['rejected']!r}")
    print(f"output: {output_path} ({compacted} records after compaction)")
    for item in flagged:
        print(f"flag: {item}")
    for item in failures:
        print(f"failed: {item}")
    print(f"usage: input={totals['input_tokens']} output={totals['output_tokens']} "
          f"cache_read={totals['cache_read_input_tokens']}")
    return 1 if failures else 0


def cmd_check(args) -> int:
    data = load_inputs(args)
    blocks = data["blocks"]
    by_id = {block["unit_id"]: block for block in blocks}
    # ``check --out DIR`` inspects that directory only; without ``--out`` it
    # inspects the default Reader directory.
    if args.out:
        cache = load_cache([data["out"]])
    else:
        cache = load_cache([data["root"] / READER_REL / data["stem"]])
    order = {block["unit_id"]: index for index, block in enumerate(blocks)}
    errors = 0
    warnings = 0
    stale: list[str] = []
    print(f"check: {data['stem']} ({len(cache)} translation records)")
    for unit_id in sorted(cache, key=lambda unit: order.get(unit, len(order))):
        record = cache[unit_id]
        block = by_id.get(unit_id)
        if block is None:
            stale.append(f"{unit_id} (unit missing from blocks.jsonl)")
            continue
        if record.get("unit_sha256") != block_hash(block):
            stale.append(f"{unit_id} (source hash changed)")
            continue
        flags = qa_unit(block, record.get("zh") or "", data["entries"])
        if not flags:
            continue
        parts = []
        for flag in flags:
            if flag["level"] == "error":
                errors += 1
            else:
                warnings += 1
            parts.append(f"{flag['code']}({flag['level']}): {flag['detail']}")
        print(f"- {unit_id}: " + " | ".join(parts))
    for item in stale:
        print(f"stale: {item}")
    print(f"summary: flags={errors + warnings} (errors={errors}, warnings={warnings}) "
          f"stale={len(stale)}")
    return 1 if errors else 0


def page_range(value: str) -> tuple[str, str]:
    match = re.fullmatch(r"\s*(\S+?)\s*[–-]\s*(\S+)\s*", value)
    if not match:
        match = re.fullmatch(r"\s*(\S+)\s*", value)
        if not match:
            raise argparse.ArgumentTypeError("use A-B for a page range")
        return (match.group(1), match.group(1))
    return (match.group(1), match.group(2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Translate evidence units into Chinese through the model gateway.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def common(sub: argparse.ArgumentParser) -> None:
        sub.add_argument("stem", help="bibliography stem, e.g. Author_2018_Title")
        sub.add_argument("--root", type=Path, help="repository root")
        sub.add_argument("--out", type=Path, help="output directory")
        sub.add_argument("--project", help="project topic for its glossary")
        sub.add_argument("--model", default=DEFAULT_MODEL, help="model name")
        sub.add_argument("--include-references", action="store_true",
                         help="also translate units after a references heading")
        selection = sub.add_mutually_exclusive_group()
        selection.add_argument("--pages", type=page_range, metavar="A-B",
                               help="printed page label range")
        selection.add_argument("--all", action="store_true", help="every unit")
        sub.add_argument("--from", dest="from_id", metavar="UNIT_ID")
        sub.add_argument("--to", dest="to_id", metavar="UNIT_ID")

    plan = subparsers.add_parser("plan", help="estimate without API calls")
    common(plan)
    plan.add_argument("--force", action="store_true", help="ignore the cache")

    terms = subparsers.add_parser("terms", help="propose glossary terms")
    common(terms)

    run = subparsers.add_parser("run", help="translate uncached units")
    common(run)
    run.add_argument("--force", action="store_true", help="ignore the cache")
    run.add_argument("--yes", action="store_true", help="allow more than 60 units")
    run.add_argument("--jobs", type=int, default=DEFAULT_JOBS,
                     help="parallel API calls (default 4)")
    run.add_argument("--no-terms", action="store_true",
                     help="skip automatic term proposals")

    check = subparsers.add_parser("check", help="deterministic QA, no API calls")
    common(check)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {"plan": cmd_plan, "terms": cmd_terms,
                "run": cmd_run, "check": cmd_check}
    try:
        return handlers[args.command](args)
    except TranslateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

