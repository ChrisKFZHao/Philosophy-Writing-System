#!/usr/bin/env python3
"""Extract deterministic text, outline, and evidence-unit data from PDF files.

The script is the local extraction backend for the evidence-retrieval service.
It never rewrites a source: every subcommand only reads a PDF and either prints
JSON to stdout or writes an extraction cache under ``--out``.

Layout heuristics are recorded as facts about the extraction, not as claims
about the document.  Every unit written by ``blocks`` is marked
``provisional`` until a human or a later workflow step verifies it.

pdfminer.six is imported lazily so that ``--help`` and test collection work on
hosts where it is not installed.  The active interpreter note for this
repository is ``py -3`` on Windows.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import logging
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

EXTRACTION_VERSION = "pdf-extract/3"
# Justified text with wide word gaps splits lines at pdfminer's default of 2.0
# character widths; 3.0 keeps such lines whole without joining column gutters
# or marginal Stephanus/Bekker numbers to the text.
CHAR_MARGIN = 3.0
MISSING_PDFMINER = "pdfminer.six is required: py -3 -m pip install --user pdfminer.six"

OCR_VERSION = "ocr/1"
OCR_ENGINE_VERSION = "tesseract.js 7.0.0"
OCR_TESSDATA_URL = (
    "https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/"
    "{lang}.traineddata"
)
OCR_PROXY = "http://ss.deepseek.com:3129"
OCR_BATCH_SIZE = 10
OCR_DEFAULT_WIDTH = 1800
OCR_DEFAULT_LANG = "eng"
# Two OCR lines join when the vertical gap is below this share of the page's
# median line height and their left edges differ by less than the tolerance.
OCR_GAP_RATIO = 0.8
OCR_HEIGHT_TOLERANCE = 0.35
OCR_LEFT_TOLERANCE_FACTOR = 2.0
OCR_MIN_LEFT_TOLERANCE = 4.0
# A box's uniform type size is its median line height times this factor, which
# puts body lines near their nominal point size for rule K.
OCR_SIZE_FACTOR = 0.75
# A line indented this far beyond the column's left edge starts a paragraph.
OCR_PARAGRAPH_INDENT = 0.8
# A short terminal line (under this share of the column width) ends a paragraph.
OCR_SHORT_LINE_RATIO = 0.75
# On OCR pages, smaller type below the main text is a footnote.
OCR_SMALL_LINE_RATIO = 0.85
# Page numbers beyond the 10% head band still count as folios.
PAGE_NUMBER_BAND = 0.15
OCR_NOISE_BAND = 0.15
NOTE_NUMBER_RE = re.compile(r"^\d{1,3}\.\s")
# OCR often reads I as 1 inside roman numerals: (1V:5) for (IV:5).
ROMAN_OCR_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9])([IVXLC1]+)(?:([:.][0-9]+))?(?![A-Za-z0-9])"
)
ROMAN_PREFIX_RE = re.compile(r"[VXLC]")
OCR_LABEL_TRANS = str.maketrans({"1": "i", "t": "i"})

PAGE_NUMBER_RE = re.compile(r"^\W*\d+\W*$")
ROMAN_PAGE_RE = re.compile(
    r"^\W*(?=[ivxlcdm])m{0,4}(?:cm|cd|d?c{0,3})"
    r"(?:xc|xl|l?x{0,3})(?:ix|iv|v?i{0,3})\W*$",
    re.IGNORECASE,
)
MARGIN_REF_RE = re.compile(r"^(?:\d+[a-e]|\d+[ab]\d+)$")
DIGITS_RE = re.compile(r"\d+")

TERMINAL_CHARS = set(".?!:;”\"')]")
TERMINAL_CHARS |= set("。！？：；」』）】")
# Han, kana, CJK punctuation, and full-width forms: no space at a line break.
CJK_RE = re.compile("[\u3000-\u303f\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uff00-\uffef]")
HEADER_BAND = 0.10
CONTEXT_PAGES = 8  # pages read to detect running heads when fewer are requested
REPEAT_SHARE = 0.6
MIN_REPEAT_PAGES = 3
MIN_TEXT_CHARACTERS = 20
CONTEXT_RADIUS = 120


class PdfminerMissing(RuntimeError):
    """pdfminer.six is not importable in the active interpreter."""


def load_pdfminer() -> dict[str, Any]:
    """Import pdfminer lazily and return the pieces the extractor uses."""
    try:
        import pdfminer
        from pdfminer.high_level import extract_pages, extract_text
        from pdfminer.layout import LAParams, LTChar, LTTextBox, LTTextLine
        from pdfminer.pdfdocument import (
            PDFDocument,
            PDFNoOutlines,
            PDFNoPageLabels,
        )
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser, PDFSyntaxError
        from pdfminer.pdftypes import resolve1
    except ImportError as error:
        raise PdfminerMissing(str(error)) from error
    # pdfminer logs recoverable font and syntax warnings; they say nothing the
    # caller can act on and would mix into captured output.
    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    return {
        "pdfminer": pdfminer,
        "extract_pages": extract_pages,
        "extract_text": extract_text,
        "LAParams": LAParams,
        "LTChar": LTChar,
        "LTTextBox": LTTextBox,
        "LTTextLine": LTTextLine,
        "PDFDocument": PDFDocument,
        "PDFNoOutlines": PDFNoOutlines,
        "PDFNoPageLabels": PDFNoPageLabels,
        "PDFPage": PDFPage,
        "PDFParser": PDFParser,
        "PDFSyntaxError": PDFSyntaxError,
        "resolve1": resolve1,
    }


def json_output(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def decode_pdf_text(value: Any) -> Any:
    """Decode a PDF string value; dates remain their original text."""
    if isinstance(value, bytes):
        if value.startswith(b"\xfe\xff"):
            try:
                return value.decode("utf-16")
            except UnicodeDecodeError:
                pass
        return value.decode("latin-1")
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def page_fingerprint(text: str) -> str:
    """Normalize running text so repeated headers compare equal across pages."""
    return DIGITS_RE.sub("#", collapse_ws(text))


def is_page_number(text: str) -> bool:
    stripped = collapse_ws(text)
    # A trailing period marks a section numeral ("V."), not a folio.
    if stripped.endswith("."):
        return False
    return bool(PAGE_NUMBER_RE.match(stripped) or ROMAN_PAGE_RE.match(stripped))


def looks_like_page_label(text: str, label: str) -> bool:
    """Whether OCR text is this page's folio, allowing i/1/t confusions.

    Used only for OCR pages, where a folio such as ``liii`` is sometimes read
    as ``litt``. The expected label must itself be a page number.
    """
    if not is_page_number(label):
        return False
    token = "".join(char for char in text if char.isalnum()).lower()
    expected = "".join(char for char in label if char.isalnum()).lower()
    if not token or not expected:
        return False
    if expected.isdigit():
        return token == expected
    return token.translate(OCR_LABEL_TRANS) == expected


def _should_dehyphenate(left: str, right: str) -> bool:
    return (
        len(left) >= 2
        and left.endswith("-")
        and left[-2].isalpha()
        and bool(right)
        and right[0].islower()
    )


def is_cjk(char: str) -> bool:
    return bool(CJK_RE.match(char))


def join_texts(left: str, right: str) -> tuple[str, int]:
    """Join adjacent text per rule D; return the join and the right offset.

    Lines meet with one space, except after a dehyphenated break or where
    either side of the break is a CJK character, which takes no space.
    """
    if not left:
        return right, 0
    if not right:
        return left, len(left)
    if _should_dehyphenate(left, right):
        return left[:-1] + right, len(left) - 1
    if is_cjk(left[-1]) or is_cjk(right[0]):
        return left + right, len(left)
    return left + " " + right, len(left) + 1


def join_lines(lines: Iterable[str]) -> str:
    """Join text lines per rule D (spaces, dehyphenation, CJK without spaces)."""
    text = ""
    for raw in lines:
        line = collapse_ws(raw)
        if line:
            text, _ = join_texts(text, line)
    return text


def ends_terminal(text: str) -> bool:
    """Whether text ends a paragraph, ignoring trailing footnote digits."""
    stripped = re.sub(r"[\d\s]+$", "", text)
    return bool(stripped) and stripped[-1] in TERMINAL_CHARS


def parse_page_spec(spec: str | None, page_count: int) -> list[int]:
    """Parse ``5``, ``3-7``, ``1,4-6`` into sorted 1-based page numbers."""
    if not spec:
        return list(range(1, page_count + 1))
    pages: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            raise ValueError(f"invalid page specification: {spec!r}")
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start < 1 or end < start:
                raise ValueError(f"invalid page range: {token!r}")
            pages.update(range(start, end + 1))
        else:
            number = int(token)
            if number < 1:
                raise ValueError(f"invalid page number: {token!r}")
            pages.add(number)
    if not pages:
        raise ValueError(f"invalid page specification: {spec!r}")
    if max(pages) > page_count:
        raise ValueError(
            f"page {max(pages)} is beyond the document ({page_count} pages)"
        )
    return sorted(pages)


def repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "Framework/Workflow/manifest.json").is_file():
            return parent
    raise ValueError("repository root not found from script location")


def default_out_dir(pdf_path: Path) -> Path:
    return repository_root() / "Private/Bibliography/Extract" / pdf_path.stem


@contextmanager
def open_document(pdf_path: Path, pm: dict[str, Any]):
    """Open a pdfminer document and close the underlying file afterwards."""
    with open(pdf_path, "rb") as handle:
        parser = pm["PDFParser"](handle)
        document = pm["PDFDocument"](parser)
        yield document


def page_count_and_labels(
    pdf_path: Path, pm: dict[str, Any]
) -> tuple[int, list[str]]:
    """Return the PDF page count and one label per page (1-based order)."""
    with open_document(pdf_path, pm) as document:
        count = sum(1 for _ in pm["PDFPage"].create_pages(document))
        labels: list[str] = []
        try:
            iterator = document.get_page_labels()
            for number in range(1, count + 1):
                try:
                    label = next(iterator)
                except StopIteration:
                    label = None
                labels.append(label or str(number))
        except Exception:
            # PDFNoPageLabels, malformed trees, and unknown styles all degrade
            # to the 1-based PDF page number.
            labels = [str(number) for number in range(1, count + 1)]
    return count, labels


@dataclass
class BoxInfo:
    """One LTTextBox with the facts the layout rules need."""

    x0: float
    y0: float
    x1: float
    y1: float
    lines: list[str]
    text: str
    size_counts: dict[float, int]
    dominant_size: float
    all_bold: bool
    line_count: int
    kind: str = "body"
    column: str = "full"
    dropped: bool = False

    @property
    def width(self) -> float:
        return self.x1 - self.x0


@dataclass
class Block:
    """A reading-order block ready to become an evidence unit."""

    kind: str
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    pdf_pages: list[int]
    labels: list[str]
    page_breaks: list[dict[str, Any]] = field(default_factory=list)
    margin_refs: list[str] = field(default_factory=list)
    ocr: bool = False


@dataclass
class PageInfo:
    """One extracted page: geometry, label, and text boxes."""

    number: int
    label: str
    x0: float
    y0: float
    x1: float
    y1: float
    boxes: list[BoxInfo]
    printed: int | None = None
    ocr: bool = False


def make_box(lt_box: Any, pm: dict[str, Any]) -> BoxInfo:
    """Convert an LTTextBox into a BoxInfo, collecting size and font facts."""
    lines: list[str] = []
    size_counts: dict[float, int] = {}
    fonts: list[str] = []
    for line in lt_box:
        if not isinstance(line, pm["LTTextLine"]):
            continue
        lines.append(line.get_text())
        for char in line:
            if not isinstance(char, pm["LTChar"]):
                continue
            size = round(float(char.size) * 2) / 2
            size_counts[size] = size_counts.get(size, 0) + 1
            fonts.append(char.fontname or "")
    dominant = (
        max(size_counts, key=lambda size: (size_counts[size], size))
        if size_counts
        else 0.0
    )
    x0, y0, x1, y1 = lt_box.bbox
    return BoxInfo(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        lines=lines,
        text="".join(lines),
        size_counts=size_counts,
        dominant_size=dominant,
        all_bold=bool(fonts) and all("Bold" in font for font in fonts),
        line_count=len(lines),
    )


def default_ocr_path(pdf_path: Path, out_dir: Path | None = None) -> Path:
    return (out_dir or default_out_dir(pdf_path)) / "ocr.jsonl"


def non_space_characters(boxes: list[BoxInfo]) -> int:
    raw = "".join(box.text for box in boxes)
    return sum(1 for char in raw if not char.isspace())


def count_alphanumeric(text: str) -> int:
    return sum(1 for char in text if char.isalnum())


def fix_ocr_roman(text: str) -> tuple[str, int]:
    """Correct OCR's 1-for-I reading inside roman numerals.

    Only a whole token of ``IVXLC1`` (optionally followed by ``:``/``.`` and
    digits) is touched, and only when it contains both ``1`` and one of
    ``V X L C``. All-digit tokens such as ``11`` or ``1965`` are left alone.
    Returns the corrected text and the number of tokens changed.
    """
    fixes = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal fixes
        token = match.group(1)
        if "1" not in token or not ROMAN_PREFIX_RE.search(token):
            return match.group(0)
        fixes += 1
        suffix = match.group(2) or ""
        return token.replace("1", "I") + suffix

    return ROMAN_OCR_TOKEN_RE.sub(replace, text), fixes


def load_ocr_records(
    path: Path, source_sha256: str, version: str = OCR_VERSION
) -> dict[int, dict[str, Any]]:
    """Read the last usable OCR record per page for one source and version.

    Records written for another PDF hash or another ``ocr_version`` are
    ignored, so a changed source silently falls back to pdfminer text.
    """
    records: dict[int, dict[str, Any]] = {}
    if not path.is_file():
        return records
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return records
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        if record.get("source_sha256") != source_sha256:
            continue
        if record.get("ocr_version") != version:
            continue
        try:
            page = int(record.get("pdf_page"))
        except (TypeError, ValueError):
            continue
        if page < 1 or not isinstance(record.get("lines"), list):
            continue
        records[page] = record
    return records


def ocr_bbox_to_points(
    bbox: Iterable[float],
    image_width: float,
    image_height: float,
    page_x0: float,
    page_y0: float,
    page_x1: float,
    page_y1: float,
) -> tuple[float, float, float, float]:
    """Convert a pixel bbox (origin top-left) to points (origin bottom-left)."""
    values = [float(value) for value in bbox]
    if len(values) != 4:
        raise ValueError(f"OCR bbox needs four numbers, got {bbox!r}")
    if image_width <= 0 or image_height <= 0:
        raise ValueError("OCR image dimensions must be positive")
    scale_x = (page_x1 - page_x0) / image_width
    scale_y = (page_y1 - page_y0) / image_height
    x0 = page_x0 + values[0] * scale_x
    x1 = page_x0 + values[2] * scale_x
    y1 = page_y1 - values[1] * scale_y
    y0 = page_y1 - values[3] * scale_y
    return x0, y0, x1, y1


def boxes_from_ocr_lines(record: dict[str, Any]) -> list[BoxInfo]:
    """Group OCR lines into paragraph-like boxes with one size per box.

    Consecutive lines join when the vertical gap is below OCR_GAP_RATIO of the
    page's median line height, the two lines are set at about the same height,
    and their left edges are close. A line indented beyond the column's left
    edge starts a new paragraph, as does a line following a short terminal
    line. Each box gets a uniform type size so rule K can still separate body
    text from smaller footnotes.
    """
    lines: list[dict[str, Any]] = []
    for item in record.get("lines") or []:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        bbox = item.get("bbox")
        if not isinstance(text, str) or not text.strip():
            continue
        if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
            continue
        try:
            x0, y0, x1, y1 = (float(value) for value in bbox)
        except (TypeError, ValueError):
            continue
        if x1 <= x0 or y1 <= y0:
            continue
        lines.append(
            {
                "text": text.strip(),
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
            }
        )
    if not lines:
        return []
    lines.sort(key=lambda line: (-line["y1"], line["x0"]))
    median_height = statistics.median(
        line["y1"] - line["y0"] for line in lines
    )
    if median_height <= 0:
        return []
    gap_limit = OCR_GAP_RATIO * median_height
    height_limit = OCR_HEIGHT_TOLERANCE * median_height
    left_tolerance = max(
        OCR_MIN_LEFT_TOLERANCE, OCR_LEFT_TOLERANCE_FACTOR * median_height
    )
    column_left = statistics.median(line["x0"] for line in lines)
    column_right = statistics.median(line["x1"] for line in lines)
    column_width = max(column_right - column_left, median_height)
    indent_limit = column_left + OCR_PARAGRAPH_INDENT * median_height
    short_limit = column_left + OCR_SHORT_LINE_RATIO * column_width
    groups: list[list[dict[str, Any]]] = [[lines[0]]]
    for line in lines[1:]:
        group = groups[-1]
        previous = group[-1]
        gap = previous["y0"] - line["y1"]
        line_height = line["y1"] - line["y0"]
        previous_height = previous["y1"] - previous["y0"]
        indented = line["x0"] > indent_limit
        previous_short_terminal = (
            previous["x1"] < short_limit and ends_terminal(previous["text"])
        )
        if (
            not indented
            and not previous_short_terminal
            and gap < gap_limit
            and abs(line_height - previous_height) <= height_limit
            and abs(line["x0"] - group[0]["x0"]) <= left_tolerance
        ):
            group.append(line)
        else:
            groups.append([line])

    boxes: list[BoxInfo] = []
    for group in groups:
        size = round(
            statistics.median(
                line["y1"] - line["y0"] for line in group
            )
            * OCR_SIZE_FACTOR
            * 2
        ) / 2
        texts = [line["text"] for line in group]
        text = "".join(texts)
        characters = sum(1 for char in text if not char.isspace()) or 1
        boxes.append(
            BoxInfo(
                x0=min(line["x0"] for line in group),
                y0=min(line["y0"] for line in group),
                x1=max(line["x1"] for line in group),
                y1=max(line["y1"] for line in group),
                lines=texts,
                text=text,
                size_counts={size: characters},
                dominant_size=size,
                all_bold=False,
                line_count=len(group),
            )
        )
    return boxes


def apply_ocr_footnote_kinds(boxes: list[BoxInfo]) -> None:
    """Mark notes on one OCR page relative to that page's main text size.

    The main text is the character-weighted dominant size. A smaller box below
    the main text is a footnote, as is any box below it that starts with a note
    number, even when its type matches the body.
    """
    if not boxes:
        return
    weight: dict[float, int] = {}
    for box in boxes:
        size = box.dominant_size
        weight[size] = weight.get(size, 0) + (
            count_alphanumeric(box.text) or 1
        )
    if not weight:
        return
    main_size = max(weight, key=lambda size: (weight[size], size))
    small_limit = OCR_SMALL_LINE_RATIO * main_size
    main_boxes = [
        box
        for box in boxes
        if box.dominant_size >= main_size - 0.5
        and not NOTE_NUMBER_RE.match(box.text)
    ]
    if not main_boxes:
        return
    main_bottom = min(box.y0 for box in main_boxes)
    for box in boxes:
        if box.y1 > main_bottom:
            continue
        if box.dominant_size <= small_limit or NOTE_NUMBER_RE.match(box.text):
            box.kind = "footnote"


def extract_page_layouts(
    pdf_path: Path,
    numbers: list[int],
    labels: list[str],
    pm: dict[str, Any],
    ocr_records: dict[int, dict[str, Any]] | None = None,
) -> list[PageInfo]:
    """Extract the requested 1-based pages in ascending document order.

    A page whose pdfminer text is too sparse uses its OCR lines as boxes when
    ``ocr_records`` holds a usable record for it.
    """
    ordered = sorted(numbers)
    layouts = pm["extract_pages"](
        str(pdf_path),
        page_numbers={number - 1 for number in ordered},
        laparams=pm["LAParams"](char_margin=CHAR_MARGIN),
    )
    pages: list[PageInfo] = []
    for number, layout in zip(ordered, layouts):
        boxes = [
            make_box(item, pm)
            for item in layout
            if isinstance(item, pm["LTTextBox"]) and item.get_text().strip()
        ]
        used_ocr = False
        record = ocr_records.get(number) if ocr_records else None
        if record is not None and non_space_characters(boxes) < MIN_TEXT_CHARACTERS:
            ocr_boxes = boxes_from_ocr_lines(record)
            if ocr_boxes:
                boxes = ocr_boxes
                used_ocr = True
        label = labels[number - 1] if number - 1 < len(labels) else str(number)
        x0, y0, x1, y1 = layout.bbox
        pages.append(
            PageInfo(
                number,
                label,
                x0,
                y0,
                x1,
                y1,
                boxes,
                ocr=used_ocr,
            )
        )
    return pages


def body_font_size(pages: list[PageInfo]) -> float:
    """The most frequent half-point character size across extracted pages."""
    counts: dict[float, int] = {}
    for page in pages:
        for box in page.boxes:
            for size, count in box.size_counts.items():
                counts[size] = counts.get(size, 0) + count
    if not counts:
        return 0.0
    return max(counts, key=lambda size: (counts[size], size))


def _in_header_band(
    box: BoxInfo, page: PageInfo, band: float = HEADER_BAND
) -> bool:
    height = page.y1 - page.y0
    if height <= 0:
        return False
    top = (box.y1 - page.y0) / height
    bottom = (box.y0 - page.y0) / height
    return top >= 1.0 - band or bottom <= band


def mark_running_headers(pages: list[PageInfo]) -> None:
    """Apply rule H: drop repeated running heads and page-number boxes.

    Journals and books often alternate heads (author on even pages, title on
    odd ones), so a head counts as repeated when it appears on REPEAT_SHARE of
    all pages or of the pages of one parity. A dropped arabic page number is
    kept as the page's printed number.
    """
    hits: dict[str, int] = {}
    parity_hits: dict[int, dict[str, int]] = {0: {}, 1: {}}
    parity_pages = {0: 0, 1: 0}
    for page in pages:
        parity = page.number % 2
        parity_pages[parity] += 1
        seen: set[str] = set()
        for box in page.boxes:
            if not _in_header_band(box, page):
                continue
            fingerprint = page_fingerprint(box.text)
            if fingerprint:
                seen.add(fingerprint)
        for fingerprint in seen:
            hits[fingerprint] = hits.get(fingerprint, 0) + 1
            parity_hits[parity][fingerprint] = parity_hits[parity].get(fingerprint, 0) + 1

    def threshold(count: int) -> int:
        # ceil(0.6 * count), computed with integers to stay deterministic.
        return max(MIN_REPEAT_PAGES, (3 * count + 4) // 5)

    repeated = {key for key, count in hits.items() if count >= threshold(len(pages))}
    for parity in (0, 1):
        if parity_pages[parity] >= MIN_REPEAT_PAGES:
            limit = threshold(parity_pages[parity])
            repeated |= {key for key, count in parity_hits[parity].items() if count >= limit}

    for page in pages:
        for box in page.boxes:
            numbered = is_page_number(box.text)
            folio_like = page.ocr and looks_like_page_label(
                box.text, page.label
            )
            band = PAGE_NUMBER_BAND if (numbered or folio_like) else HEADER_BAND
            # OCR sometimes turns a folio into one or two stray marks, or into
            # a near misspelling such as "litt" for "liii".
            if (
                page.ocr
                and _in_header_band(box, page, OCR_NOISE_BAND)
                and (folio_like or count_alphanumeric(box.text) < 3)
            ):
                box.dropped = True
            if not _in_header_band(box, page, band):
                continue
            fingerprint = page_fingerprint(box.text)
            repeats = len(pages) >= MIN_REPEAT_PAGES and fingerprint in repeated
            if numbered or repeats:
                box.dropped = True
            digits = collapse_ws(box.text).strip("-–— ")
            if numbered and digits.isdigit():
                page.printed = int(digits)


def infer_printed_labels(pages: list[PageInfo], labels: list[str]) -> None:
    """Label pages with their printed numbers when the PDF defines no labels.

    Printed numbers must agree on one offset from the PDF page order on at
    least half of the pages (and two pages); otherwise PDF order stays.
    """
    if any(label != str(index + 1) for index, label in enumerate(labels)):
        return
    offsets: dict[int, int] = {}
    for page in pages:
        if page.printed is not None:
            offset = page.printed - page.number
            offsets[offset] = offsets.get(offset, 0) + 1
    if not offsets:
        return
    offset, votes = max(offsets.items(), key=lambda item: (item[1], -abs(item[0])))
    if offset == 0 or votes < max(2, len(pages) // 2):
        return
    for page in pages:
        if page.number + offset >= 1:
            page.label = str(page.number + offset)


def classify_box(box: BoxInfo, body_size: float, page_mid: float) -> str:
    """Apply rule K to a single box."""
    if box.dominant_size <= body_size - 1.0 and box.y1 < page_mid:
        return "footnote"
    if box.dominant_size >= body_size + 1.0:
        return "heading"
    if len(collapse_ws(box.text)) <= 120 and box.all_bold:
        return "heading"
    return "body"


def assign_columns(boxes: list[BoxInfo], page: PageInfo) -> bool:
    """Mark each box left/right/full and report whether rule C applies."""
    middle = (page.x0 + page.x1) / 2
    body = [box for box in boxes if box.kind == "body"]
    left_body = [box for box in body if box.x1 <= middle]
    right_body = [box for box in body if box.x0 >= middle]
    two_columns = len(left_body) >= 2 and len(right_body) >= 2
    if not two_columns:
        # Rule C only distinguishes columns on two-column pages; a
        # single-column page has one column even when a short box is narrow.
        for box in boxes:
            box.column = "full"
        return False
    for box in boxes:
        if box.x1 <= middle:
            box.column = "left"
        elif box.x0 >= middle:
            box.column = "right"
        else:
            box.column = "full"
    return True


def column_edges(
    boxes: list[BoxInfo],
) -> dict[str, tuple[float, float]]:
    """Median left/right body edges per column, with a full-page fallback."""
    body = [box for box in boxes if box.kind == "body"]
    edges: dict[str, tuple[float, float]] = {}
    if not body:
        return edges
    fallback = (
        statistics.median([box.x0 for box in body]),
        statistics.median([box.x1 for box in body]),
    )
    for column in ("left", "right", "full"):
        members = [box for box in body if box.column == column]
        if members:
            edges[column] = (
                statistics.median([box.x0 for box in members]),
                statistics.median([box.x1 for box in members]),
            )
    edges.setdefault("full", fallback)
    return edges


def _order_key(box: BoxInfo) -> tuple[float, float]:
    return (-box.y1, box.x0)


def order_boxes(boxes: list[BoxInfo], two_columns: bool) -> list[BoxInfo]:
    """Apply rule C: column order on two-column pages, else top-to-bottom."""
    if not two_columns:
        return sorted(boxes, key=_order_key)
    full = [box for box in boxes if box.column == "full"]
    left = [box for box in boxes if box.column == "left"]
    right = [box for box in boxes if box.column == "right"]
    if not left and not right:
        return sorted(boxes, key=_order_key)
    column_top = max(box.y1 for box in left + right)
    before = sorted([box for box in full if box.y1 >= column_top], key=_order_key)
    after = sorted([box for box in full if box.y1 < column_top], key=_order_key)
    return (
        before
        + sorted(left, key=_order_key)
        + sorted(right, key=_order_key)
        + after
    )


def build_page_blocks(page: PageInfo, body_size: float) -> list[Block]:
    """Classify, order, and convert one page's boxes into reading blocks."""
    boxes = [box for box in page.boxes if not box.dropped]
    page_mid = (page.y0 + page.y1) / 2
    for box in boxes:
        box.kind = classify_box(box, body_size, page_mid)
    if page.ocr:
        apply_ocr_footnote_kinds(boxes)
    # Footnotes sit below all body text. Small type with body text below it is
    # a quotation set in smaller type, not a note.
    body_bottoms = [box.y0 for box in boxes if box.kind == "body"]
    if body_bottoms:
        lowest_body = min(body_bottoms)
        for box in boxes:
            if box.kind == "footnote" and box.y0 > lowest_body:
                box.kind = "blockquote"
    two_columns = assign_columns(boxes, page)
    edges = column_edges(boxes)

    for box in boxes:
        if box.kind != "body":
            continue
        edge = edges.get(box.column) or edges.get("full")
        if edge is not None and box.line_count >= 2 and box.x0 >= edge[0] + 15:
            box.kind = "blockquote"

    unit_boxes: list[BoxInfo] = []
    margin_boxes: list[BoxInfo] = []
    for box in boxes:
        edge = edges.get(box.column) or edges.get("full")
        outside = (
            edge is not None
            and (box.x1 < edge[0] - 5 or box.x0 > edge[1] + 5)
        )
        if (
            box.width <= 40
            and outside
            and MARGIN_REF_RE.match(collapse_ws(box.text))
        ):
            margin_boxes.append(box)
        else:
            unit_boxes.append(box)

    blocks: list[Block] = []
    for box in order_boxes(unit_boxes, two_columns):
        blocks.append(
            Block(
                kind=box.kind,
                text=nfc(join_lines(box.lines)).strip(),
                x0=box.x0,
                y0=box.y0,
                x1=box.x1,
                y1=box.y1,
                pdf_pages=[page.number],
                labels=[page.label],
                ocr=page.ocr,
            )
        )

    for margin in margin_boxes:
        best: Block | None = None
        best_overlap = 0.0
        for block in blocks:
            if block.kind != "body":
                continue
            overlap = min(margin.y1, block.y1) - max(margin.y0, block.y0)
            if overlap > best_overlap:
                best, best_overlap = block, overlap
        if best is not None:
            best.margin_refs.append(collapse_ws(margin.text))
    return blocks


def _last_body(blocks: list[Block]) -> Block | None:
    for block in reversed(blocks):
        if block.kind == "body":
            return block
    return None


def _first_body(blocks: list[Block]) -> Block | None:
    for block in blocks:
        if block.kind == "body":
            return block
    return None


def _can_merge(left: Block | None, right: Block | None) -> bool:
    return (
        left is not None
        and right is not None
        and left.kind == "body"
        and right.kind == "body"
        and bool(left.text)
        and bool(right.text)
        and right.pdf_pages[0] == left.pdf_pages[-1] + 1
        and not ends_terminal(left.text)
        and (right.text[0].islower() or (is_cjk(left.text[-1]) and is_cjk(right.text[0])))
    )


def merge_blocks(left: Block, right: Block) -> Block:
    """Rule M: join two body blocks across a page boundary."""
    text, offset = join_texts(left.text, right.text)
    breaks = [{"offset": offset, "page_label": right.labels[0]}]
    breaks.extend(
        {
            "offset": offset + item["offset"],
            "page_label": item["page_label"],
        }
        for item in right.page_breaks
    )
    return Block(
        kind="body",
        text=text,
        x0=left.x0,
        y0=left.y0,
        x1=left.x1,
        y1=left.y1,
        pdf_pages=left.pdf_pages + right.pdf_pages,
        labels=left.labels + right.labels,
        page_breaks=left.page_breaks + breaks,
        margin_refs=left.margin_refs + right.margin_refs,
        ocr=left.ocr or right.ocr,
    )


def merge_across_pages(page_blocks: list[list[Block]]) -> list[list[Block]]:
    """Apply rule M across adjacent extracted pages, including chains."""
    pages = [list(blocks) for blocks in page_blocks]
    carry: Block | None = None
    carry_location: tuple[list[Block], int] | None = None
    for index in range(len(pages) - 1):
        left = carry if carry is not None else _last_body(pages[index])
        right = _first_body(pages[index + 1])
        if not _can_merge(left, right):
            carry, carry_location = None, None
            continue
        assert left is not None and right is not None
        merged = merge_blocks(left, right)
        if carry is not None:
            assert carry_location is not None
            holder, position = carry_location
        else:
            holder = pages[index]
            position = holder.index(left)
        holder[position] = merged
        pages[index + 1].pop(pages[index + 1].index(right))
        # Carry the merged unit forward only when it is also the last body
        # block of the next page (otherwise that page's own last body merges).
        if not any(block.kind == "body" for block in pages[index + 1]):
            carry, carry_location = merged, (holder, position)
        else:
            carry, carry_location = None, None
    return pages


def analyze_pages(
    pdf_path: Path,
    numbers: list[int],
    labels: list[str],
    pm: dict[str, Any],
    ocr_dir: Path | None = None,
    source_sha256: str | None = None,
) -> tuple[list[PageInfo], list[list[Block]]]:
    """Extract pages, apply running-head removal, and build page blocks.

    Running heads and the body font size are judged on at least CONTEXT_PAGES
    neighbouring pages, so a one-page request still drops repeated heads.
    Sparse pages reuse OCR records from the same directory as ``blocks``.
    """
    wanted = set(numbers)
    context = detection_pages(wanted, len(labels))
    if source_sha256 is None:
        source_sha256 = sha256_file(pdf_path)
    ocr_records = load_ocr_records(
        default_ocr_path(pdf_path, ocr_dir), source_sha256
    )
    pages = extract_page_layouts(
        pdf_path, sorted(context), labels, pm, ocr_records
    )
    mark_running_headers(pages)
    infer_printed_labels(pages, labels)
    body_size = body_font_size(pages)
    pages = [page for page in pages if page.number in wanted]
    page_blocks = [build_page_blocks(page, body_size) for page in pages]
    return pages, page_blocks


def detection_pages(wanted: set[int], total: int) -> set[int]:
    """The requested pages widened with neighbours to CONTEXT_PAGES pages."""
    target = min(CONTEXT_PAGES, total)
    context = set(wanted)
    if not wanted:
        return context
    low, high = min(wanted), max(wanted)
    while len(context) < target and (low > 1 or high < total):
        if low > 1:
            low -= 1
            context.add(low)
        if len(context) < target and high < total:
            high += 1
            context.add(high)
    return context


def block_to_unit(
    block: Block,
    key: str,
    source_stem: str,
    source_sha256: str,
    extraction_version: str,
    order: int,
    coverage_label: str,
) -> dict[str, Any]:
    """Build one evidence unit that validates against the contract schema."""
    text = block.text
    if len(block.pdf_pages) == 1:
        locator = {"kind": "page", "value": block.labels[0]}
    else:
        locator = {
            "kind": "page-range",
            "value": f"{block.labels[0]}-{block.labels[-1]}",
        }
    layout: dict[str, Any] = {
        "kind": block.kind,
        "order": order,
        "pdf_pages": block.pdf_pages,
    }
    if block.ocr:
        layout["ocr"] = True
    if block.page_breaks:
        layout["page_breaks"] = block.page_breaks
    if block.margin_refs:
        layout["margin_refs"] = block.margin_refs
    return {
        "unit_id": f"{key}:p{block.pdf_pages[0]}:b{order}",
        "bib_key": key,
        "source_stem": source_stem,
        "source_sha256": source_sha256,
        "locator": locator,
        "text_span": text,
        "extraction_version": extraction_version,
        "unit_sha256": sha256_bytes(text.encode("utf-8")),
        "coverage_label": coverage_label,
        "verification_status": "provisional",
        "layout": layout,
    }


def command_meta(args: argparse.Namespace, pm: dict[str, Any]) -> int:
    path = Path(args.pdf)
    data = path.read_bytes()
    count, _labels = page_count_and_labels(path, pm)
    info: dict[str, Any] = {}
    with open_document(path, pm) as document:
        if document.info:
            for raw_key, raw_value in document.info[0].items():
                info[str(raw_key)] = decode_pdf_text(pm["resolve1"](raw_value))
    first_page_text = pm["extract_text"](
        str(path), page_numbers=[0], maxpages=1
    )[:1500]
    json_output(
        {
            "path": str(path),
            "source_sha256": sha256_bytes(data),
            "page_count": count,
            "info": info,
            "first_page_text": first_page_text,
        }
    )
    return 0


def _named_destination(document: Any, name: Any) -> Any:
    candidates = [name]
    if isinstance(name, str):
        candidates.append(name.encode("latin-1"))
    for candidate in candidates:
        try:
            return document.get_dest(candidate)
        except Exception:
            continue
    return None


def _outline_page(
    document: Any,
    dest: Any,
    action: Any,
    page_map: dict[Any, int],
    page_count: int,
    pm: dict[str, Any],
) -> int | None:
    """Resolve an outline destination to a 1-based PDF page number."""
    resolve1 = pm["resolve1"]
    if action is not None:
        resolved_action = resolve1(action)
        if isinstance(resolved_action, dict):
            kind = resolved_action.get("S")
            kind_name = getattr(kind, "name", kind)
            if kind_name not in ("GoTo", "GoToR"):
                return None
            dest = resolved_action.get("D")
    if dest is None:
        return None
    if hasattr(dest, "objid"):
        dest = resolve1(dest)
    if isinstance(dest, (bytes, str)):
        dest = _named_destination(document, dest)
        if hasattr(dest, "objid"):
            dest = resolve1(dest)
    if not isinstance(dest, (list, tuple)) or not dest:
        return None
    first = dest[0]
    if hasattr(first, "objid"):
        return page_map.get(first.objid)
    first = resolve1(first)
    if isinstance(first, int):
        if 1 <= first <= page_count:
            return first
        if 0 <= first < page_count:
            return first + 1
    return None


def command_toc(args: argparse.Namespace, pm: dict[str, Any]) -> int:
    path = Path(args.pdf)
    count, labels = page_count_and_labels(path, pm)
    entries: list[dict[str, Any]] = []
    with open_document(path, pm) as document:
        page_map = {
            page.pageid: number
            for number, page in enumerate(
                pm["PDFPage"].create_pages(document), start=1
            )
        }
        try:
            outlines = list(document.get_outlines())
        except pm["PDFNoOutlines"]:
            outlines = []
        for level, title, dest, action, _se in outlines:
            page = _outline_page(document, dest, action, page_map, count, pm)
            label = labels[page - 1] if page is not None else None
            entries.append(
                {
                    "level": level,
                    "title": decode_pdf_text(title),
                    "pdf_page": page,
                    "page_label": label,
                }
            )
    json_output(entries)
    return 0


def command_text(args: argparse.Namespace, pm: dict[str, Any]) -> int:
    path = Path(args.pdf)
    count, labels = page_count_and_labels(path, pm)
    numbers = parse_page_spec(args.pages, count)
    pages, page_blocks = analyze_pages(path, numbers, labels, pm)
    lines: list[str] = []
    for page, blocks in zip(pages, page_blocks):
        body = [block.text for block in blocks if block.kind != "footnote"]
        notes = [block.text for block in blocks if block.kind == "footnote"]
        lines.append(f"=== p{page.label} (pdf {page.number}) ===")
        if body:
            lines.append("\n\n".join(body))
        if notes:
            lines.append("--- notes ---")
            lines.append("\n\n".join(notes))
        lines.append("")
    print("\n".join(lines).rstrip("\n"))
    return 0


def _page_search_text(blocks: list[Block]) -> str:
    text = ""
    for block in blocks:
        text, _offset = join_texts(text, block.text)
    return text


def command_find(args: argparse.Namespace, pm: dict[str, Any]) -> int:
    path = Path(args.pdf)
    count, labels = page_count_and_labels(path, pm)
    numbers = parse_page_spec(args.pages, count)
    pages, page_blocks = analyze_pages(path, numbers, labels, pm)
    needle = join_lines(args.phrase.splitlines())
    if not needle:
        raise ValueError("phrase must contain at least one non-space character")
    lowered = needle.lower()
    limit = args.limit if args.limit > 0 else None
    results: list[dict[str, Any]] = []
    for page, blocks in zip(pages, page_blocks):
        text = _page_search_text(blocks)
        haystack = text.lower()
        start = 0
        while True:
            position = haystack.find(lowered, start)
            if position < 0:
                break
            left = max(0, position - CONTEXT_RADIUS)
            right = min(
                len(text), position + len(needle) + CONTEXT_RADIUS
            )
            results.append(
                {
                    "pdf_page": page.number,
                    "page_label": page.label,
                    "context": collapse_ws(text[left:right]),
                }
            )
            if limit is not None and len(results) >= limit:
                break
            start = position + len(lowered)
        if limit is not None and len(results) >= limit:
            break
    json_output(results)
    return 0


def pages_without_text(
    path: Path, numbers: list[int], labels: list[str], pm: dict[str, Any]
) -> list[int]:
    pages = extract_page_layouts(path, numbers, labels, pm)
    return [
        page.number
        for page in pages
        if non_space_characters(page.boxes) < MIN_TEXT_CHARACTERS
    ]


def command_ocr_needed(args: argparse.Namespace, pm: dict[str, Any]) -> int:
    path = Path(args.pdf)
    count, labels = page_count_and_labels(path, pm)
    without_text = pages_without_text(
        path, list(range(1, count + 1)), labels, pm
    )
    json_output(
        {
            "page_count": count,
            "pages_without_text": without_text,
            "needs_ocr": bool(count) and len(without_text) * 2 > count,
        }
    )
    return 0


def ocr_home() -> Path:
    """The per-user OCR runtime, overridable with PHIL_OCR_HOME."""
    override = os.environ.get("PHIL_OCR_HOME")
    if override:
        return Path(override)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "phil-ocr"
    return Path.home() / ".phil-ocr"


def ocr_languages(value: str) -> list[str]:
    languages = [part.strip() for part in re.split(r"[,+]", value) if part.strip()]
    if not languages:
        raise ValueError("--lang must name at least one language")
    for language in languages:
        if not re.match(r"^[A-Za-z0-9_]+$", language):
            raise ValueError(f"invalid language code: {language!r}")
    return languages


def download_ocr_language(language: str, tessdata: Path) -> Path:
    """Download one tessdata_fast file, retrying through the proxy."""
    destination = tessdata / f"{language}.traineddata"
    if destination.is_file() and destination.stat().st_size > 1000:
        return destination
    url = OCR_TESSDATA_URL.format(lang=language)
    errors: list[str] = []
    for proxies in ({}, {"http": OCR_PROXY, "https": OCR_PROXY}):
        try:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler(proxies)
            )
            with opener.open(url, timeout=60) as response:
                data = response.read()
            if len(data) < 1000:
                raise ValueError(f"short download ({len(data)} bytes)")
            temporary = destination.with_suffix(".tmp")
            temporary.write_bytes(data)
            temporary.replace(destination)
            return destination
        except Exception as error:  # noqa: BLE001 - retry via the proxy
            errors.append(f"{type(error).__name__}: {error}")
    raise ValueError(
        f"could not download {url} directly or through {OCR_PROXY}: "
        f"{errors[-1]}"
    )


def npm_command() -> list[str]:
    """Return an invocable npm command, preferring node + npm-cli.js."""
    node = shutil.which("node")
    npm = shutil.which("npm")
    if npm:
        cli = Path(npm).parent / "node_modules/npm/bin/npm-cli.js"
        if node and cli.is_file():
            return [node, str(cli)]
        return [npm]
    raise ValueError("npm was not found on PATH")


def npm_install(home: Path, package: str) -> None:
    base = npm_command() + ["install", package, "--no-fund", "--no-audit"]
    attempts = [
        base,
        base + ["--proxy", OCR_PROXY, "--https-proxy", OCR_PROXY],
    ]
    detail = ""
    for command in attempts:
        process = subprocess.run(command, cwd=str(home), capture_output=True)
        if process.returncode == 0:
            return
        detail = (process.stderr or process.stdout).decode("utf-8", "replace")
    raise ValueError(f"npm install failed: {detail.strip()[-400:]}")


def installed_tesseract_version(home: Path) -> str | None:
    marker = home / "node_modules/tesseract.js/package.json"
    if not marker.is_file():
        return None
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    version = data.get("version") if isinstance(data, dict) else None
    return version if isinstance(version, str) else None


def command_ocr_setup(args: argparse.Namespace, _pm: Any = None) -> int:
    """Install tesseract.js and the requested language files, idempotently."""
    home = ocr_home()
    home.mkdir(parents=True, exist_ok=True)
    package_json = home / "package.json"
    if not package_json.is_file():
        package_json.write_text(
            json.dumps(
                {"name": "phil-ocr", "private": True, "version": "1.0.0"},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
    version = installed_tesseract_version(home)
    if version != "7.0.0":
        npm_install(home, "tesseract.js@7.0.0")
        version = installed_tesseract_version(home)
    if version != "7.0.0":
        raise ValueError("tesseract.js 7.0.0 is not installed after npm install")
    tessdata = home / "tessdata"
    tessdata.mkdir(parents=True, exist_ok=True)
    languages: dict[str, Any] = {}
    for language in ocr_languages(args.lang):
        path = download_ocr_language(language, tessdata)
        languages[language] = {
            "path": str(path),
            "bytes": path.stat().st_size,
        }
    json_output(
        {
            "runtime": str(home),
            "node": shutil.which("node"),
            "node_modules": str(home / "node_modules"),
            "tesseract_js": version,
            "installed": True,
            "tessdata": str(tessdata),
            "languages": languages,
        }
    )
    return 0


def chunked(items: list[int], size: int) -> list[list[int]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def run_renderer(
    pdf_path: Path, pages: list[int], out_dir: Path, width: int
) -> dict[int, dict[str, Any]]:
    """Render pages through pdf-render.ps1 and return one entry per page."""
    script = Path(__file__).resolve().parent / "pdf-render.ps1"
    if not script.is_file():
        raise ValueError(f"renderer script not found: {script}")
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not powershell:
        raise ValueError("Windows PowerShell 5.1 was not found")
    command = [
        powershell,
        "-NoProfile",
        "-NonInteractive",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        "-Pdf",
        str(pdf_path),
        "-Pages",
        ",".join(str(number) for number in pages),
        "-OutDir",
        str(out_dir),
        "-Width",
        str(width),
    ]
    process = subprocess.run(command, capture_output=True)
    if process.returncode != 0:
        detail = (process.stderr or process.stdout).decode(
            "utf-8", "replace"
        )
        raise ValueError(f"pdf-render.ps1 failed: {detail.strip()[-500:]}")
    rendered: dict[int, dict[str, Any]] = {}
    for line in process.stdout.decode("utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            number = int(item["page"])
            rendered[number] = {
                "png": str(item["png"]),
                "width": int(item["width"]),
                "height": int(item["height"]),
            }
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"unreadable renderer output: {line!r}"
            ) from error
    missing = [number for number in pages if number not in rendered]
    if missing:
        raise ValueError(f"renderer did not report pages {missing}")
    return rendered


def run_ocr(
    pages: list[int],
    rendered: dict[int, dict[str, Any]],
    language: str,
) -> dict[int, dict[str, Any]]:
    """OCR rendered pages through ocr-pages.js, keyed by page number."""
    script = Path(__file__).resolve().parent / "ocr-pages.js"
    if not script.is_file():
        raise ValueError(f"OCR script not found: {script}")
    node = shutil.which("node")
    if not node:
        raise ValueError("node was not found on PATH")
    home = ocr_home()
    tessdata = home / "tessdata"
    for part in ocr_languages(language):
        if not (tessdata / f"{part}.traineddata").is_file():
            raise ValueError(
                f"OCR language data for {part!r} is missing; "
                f"run ocr-setup --lang {part}"
            )
    pngs = [rendered[number]["png"] for number in pages]
    environment = os.environ.copy()
    environment["PHIL_OCR_HOME"] = str(home)
    command = [
        node,
        str(script),
        "--lang",
        language,
        "--tessdata",
        str(tessdata),
        *pngs,
    ]
    process = subprocess.run(command, capture_output=True, env=environment)
    if process.returncode != 0:
        detail = (process.stderr or process.stdout).decode(
            "utf-8", "replace"
        )
        raise ValueError(f"ocr-pages.js failed: {detail.strip()[-500:]}")
    by_png: dict[str, dict[str, Any]] = {}
    for line in process.stdout.decode("utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            key = os.path.normcase(os.path.abspath(str(item["png"])))
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise ValueError(f"unreadable OCR output: {line!r}") from error
        by_png[key] = item
    results: dict[int, dict[str, Any]] = {}
    for number in pages:
        key = os.path.normcase(os.path.abspath(rendered[number]["png"]))
        if key not in by_png:
            raise ValueError(f"OCR produced no result for page {number}")
        results[number] = by_png[key]
    return results


def append_ocr_record(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def compact_ocr_records(path: Path) -> None:
    """Rewrite ocr.jsonl keeping the last record per source/version/page."""
    if not path.is_file():
        return
    records: dict[tuple[str, str, int], dict[str, Any]] = {}
    order: list[tuple[str, str, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        try:
            page = int(record.get("pdf_page"))
        except (TypeError, ValueError):
            continue
        key = (
            str(record.get("source_sha256")),
            str(record.get("ocr_version")),
            page,
        )
        if key not in records:
            order.append(key)
        records[key] = record
    payload = "".join(
        json.dumps(records[key], ensure_ascii=False) + "\n" for key in order
    )
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8", newline="\n")
    temporary.replace(path)


def command_ocr(args: argparse.Namespace, pm: dict[str, Any]) -> int:
    """OCR pages and append one record per page to ``ocr.jsonl``."""
    path = Path(args.pdf)
    count, labels = page_count_and_labels(path, pm)
    if args.pages:
        numbers = parse_page_spec(args.pages, count)
    else:
        numbers = pages_without_text(
            path, list(range(1, count + 1)), labels, pm
        )
    source_sha256 = sha256_file(path)
    out_dir = Path(args.out) if args.out else default_out_dir(path)
    out_dir.mkdir(parents=True, exist_ok=True)
    ocr_path = out_dir / "ocr.jsonl"
    existing = load_ocr_records(ocr_path, source_sha256)
    todo = [
        number
        for number in numbers
        if args.force or number not in existing
    ]
    skipped = len(numbers) - len(todo)
    started = time.monotonic()
    done = 0
    confidences: list[float] = []
    for batch in chunked(todo, OCR_BATCH_SIZE):
        # One temporary directory per batch keeps at most ten PNGs on disk.
        with tempfile.TemporaryDirectory(
            prefix=f"phil-ocr-{batch[0]:05d}-"
        ) as temporary:
            batch_dir = Path(temporary)
            rendered = run_renderer(path, batch, batch_dir, args.width)
            page_info = {
                page.number: page
                for page in extract_page_layouts(path, batch, labels, pm)
            }
            results = run_ocr(batch, rendered, args.lang)
            for number in batch:
                page = page_info[number]
                image = rendered[number]
                lines: list[dict[str, Any]] = []
                roman_fixes = 0
                for line in results[number].get("lines") or []:
                    if not isinstance(line, dict):
                        continue
                    text = line.get("text")
                    bbox = line.get("bbox")
                    if not isinstance(text, str) or not text.strip():
                        continue
                    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
                        continue
                    text, fixes = fix_ocr_roman(text.strip())
                    roman_fixes += fixes
                    x0, y0, x1, y1 = ocr_bbox_to_points(
                        bbox,
                        image["width"],
                        image["height"],
                        page.x0,
                        page.y0,
                        page.x1,
                        page.y1,
                    )
                    lines.append(
                        {
                            "text": text,
                            "bbox": [x0, y0, x1, y1],
                            "confidence": line.get("confidence"),
                        }
                    )
                confidence = results[number].get("confidence")
                record_text, _ = fix_ocr_roman(
                    results[number].get("text") or ""
                )
                record = {
                    "pdf_page": number,
                    "source_sha256": source_sha256,
                    "ocr_version": OCR_VERSION,
                    "engine": f"{OCR_ENGINE_VERSION} {args.lang} fast",
                    "width": image["width"],
                    "height": image["height"],
                    "confidence": confidence,
                    "text": record_text,
                    "roman_fixes": roman_fixes,
                    "lines": lines,
                }
                append_ocr_record(ocr_path, record)
                done += 1
                if isinstance(confidence, (int, float)):
                    confidences.append(float(confidence))
    if args.force:
        compact_ocr_records(ocr_path)
    json_output(
        {
            "pdf": str(path),
            "source_sha256": source_sha256,
            "pages_requested": len(numbers),
            "pages_done": done,
            "pages_skipped": skipped,
            "mean_confidence": (
                round(statistics.mean(confidences), 1)
                if confidences
                else None
            ),
            "seconds": round(time.monotonic() - started, 2),
            "out": str(ocr_path),
            "runtime": str(ocr_home()),
        }
    )
    return 0


def command_blocks(args: argparse.Namespace, pm: dict[str, Any]) -> int:
    path = Path(args.pdf)
    key = args.key.strip()
    if not key:
        raise ValueError("--key must not be empty")
    count, labels = page_count_and_labels(path, pm)
    numbers = parse_page_spec(args.pages, count)
    source_sha256 = sha256_file(path)
    version = f"{EXTRACTION_VERSION}+pdfminer-{pm['pdfminer'].__version__}"

    # Check the cache before extracting: a hit must cost only a hash. The OCR
    # file is part of the key, so running `ocr` later invalidates stale units.
    # OCR always comes from the source's default Extract directory: --out only
    # redirects units and the manifest.
    out_dir = Path(args.out) if args.out else default_out_dir(path)
    manifest_path = out_dir / "manifest.json"
    ocr_path = default_ocr_path(path)
    ocr_fingerprint = sha256_file(ocr_path) if ocr_path.is_file() else ""
    if manifest_path.exists() and not args.force:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            manifest = None
        if (
            isinstance(manifest, dict)
            and manifest.get("source_sha256") == source_sha256
            and manifest.get("extraction_version") == version
            and manifest.get("pages") == numbers
            and manifest.get("ocr_fingerprint", "") == ocr_fingerprint
        ):
            json_output(
                {
                    "status": "cached",
                    "unit_count": manifest.get("unit_count"),
                    "out": str(out_dir),
                }
            )
            return 0

    pages, page_blocks = analyze_pages(
        path, numbers, labels, pm, source_sha256=source_sha256
    )
    merged = merge_across_pages(page_blocks)
    flat = [block for blocks in merged for block in blocks]
    complete = set(numbers) == set(range(1, count + 1))
    coverage = "full-reading" if complete else "partial-retrieval"
    units = [
        block_to_unit(block, key, path.stem, source_sha256, version, order, coverage)
        for order, block in enumerate(flat)
    ]

    out_dir.mkdir(parents=True, exist_ok=True)
    payload = "".join(
        json.dumps(unit, ensure_ascii=False) + "\n" for unit in units
    )
    (out_dir / "blocks.jsonl").write_text(
        payload, encoding="utf-8", newline="\n"
    )
    manifest = {
        "source_path": str(path.resolve()),
        "source_sha256": source_sha256,
        "extraction_version": version,
        "pages": numbers,
        "ocr_fingerprint": ocr_fingerprint,
        "unit_count": len(units),
        "created": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    json_output(
        {"status": "written", "unit_count": len(units), "out": str(out_dir)}
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-extract.py",
        description="Deterministic PDF text and evidence-unit extraction.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    meta = subparsers.add_parser("meta", help="document info and SHA-256")
    meta.add_argument("pdf")
    meta.set_defaults(handler=command_meta)

    toc = subparsers.add_parser("toc", help="outline entries")
    toc.add_argument("pdf")
    toc.set_defaults(handler=command_toc)

    text = subparsers.add_parser("text", help="page text with running heads removed")
    text.add_argument("pdf")
    text.add_argument("--pages")
    text.set_defaults(handler=command_text)

    blocks = subparsers.add_parser("blocks", help="write evidence units")
    blocks.add_argument("pdf")
    blocks.add_argument("--key", required=True)
    blocks.add_argument("--pages")
    blocks.add_argument("--out")
    blocks.add_argument("--force", action="store_true")
    blocks.set_defaults(handler=command_blocks)

    find = subparsers.add_parser("find", help="case-insensitive phrase search")
    find.add_argument("pdf")
    find.add_argument("phrase")
    find.add_argument("--pages")
    find.add_argument("--limit", type=int, default=20)
    find.set_defaults(handler=command_find)

    ocr_needed = subparsers.add_parser(
        "ocr-needed", help="pages without extractable text"
    )
    ocr_needed.add_argument("pdf")
    ocr_needed.set_defaults(handler=command_ocr_needed)

    ocr_setup = subparsers.add_parser(
        "ocr-setup", help="install tesseract.js and language data"
    )
    ocr_setup.add_argument("--lang", default=OCR_DEFAULT_LANG)
    ocr_setup.set_defaults(handler=command_ocr_setup)

    ocr = subparsers.add_parser("ocr", help="OCR pages without extractable text")
    ocr.add_argument("pdf")
    ocr.add_argument("--pages")
    ocr.add_argument("--lang", default=OCR_DEFAULT_LANG)
    ocr.add_argument("--width", type=int, default=OCR_DEFAULT_WIDTH)
    ocr.add_argument("--force", action="store_true")
    ocr.add_argument("--out")
    ocr.set_defaults(handler=command_ocr)

    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        pm = load_pdfminer()
    except PdfminerMissing:
        print(MISSING_PDFMINER, file=sys.stderr)
        return 2
    try:
        return args.handler(args, pm)
    except (OSError, ValueError, UnicodeError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    except pm["PDFSyntaxError"] as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

