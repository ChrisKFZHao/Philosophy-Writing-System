from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = WORKFLOW_ROOT / "Scripts"
SCRIPT = SCRIPTS / "pdf-extract.py"
SCHEMA_PATH = WORKFLOW_ROOT / "Contracts" / "evidence-unit.schema.json"

try:
    import pdfminer  # noqa: F401

    HAVE_PDFMINER = True
except ImportError:
    HAVE_PDFMINER = False


def ocr_runtime_home() -> Path:
    override = os.environ.get("PHIL_OCR_HOME")
    if override:
        return Path(override)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "phil-ocr"
    return Path.home() / ".phil-ocr"


OCR_HOME = ocr_runtime_home()
HAVE_NODE = bool(shutil.which("node"))
HAVE_POWERSHELL = bool(
    shutil.which("powershell.exe") or shutil.which("powershell")
)
HAVE_TESSERACT = (
    (OCR_HOME / "node_modules" / "tesseract.js" / "package.json").is_file()
    and (OCR_HOME / "tessdata" / "eng.traineddata").is_file()
)


def load_script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


EXTRACT = load_script("pdf-extract.py")


def _escape_pdf_string(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _content_stream(boxes: list[dict]) -> bytes:
    operations: list[str] = []
    for box in boxes:
        size = box.get("size", 10)
        x = box.get("x", 72)
        y = box.get("y", 400)
        font = box.get("font", "F1")
        leading = box.get("leading", size * 1.2)
        lines = box.get("lines")
        if lines is None:
            lines = [box["text"]]
        for index, line in enumerate(lines):
            operations.append(
                f"BT /{font} {size} Tf {x} {y - index * leading} Td "
                f"({_escape_pdf_string(line)}) Tj ET"
            )
    payload = ("\n".join(operations) + "\n").encode("latin-1")
    return (
        b"<< /Length " + str(len(payload)).encode("ascii")
        + b" >>\nstream\n" + payload + b"endstream"
    )


class PdfBuilder:
    """Minimal PDF 1.4 writer using only standard Type1 fonts."""

    def __init__(self) -> None:
        self.objects: list[bytes | None] = []

    def reserve(self) -> int:
        self.objects.append(None)
        return len(self.objects)

    def add(self, body: str | bytes) -> int:
        if isinstance(body, str):
            body = body.encode("latin-1")
        self.objects.append(body)
        return len(self.objects)

    def set(self, number: int, body: str | bytes) -> None:
        if isinstance(body, str):
            body = body.encode("latin-1")
        self.objects[number - 1] = body

    def render(self, root: int, info: int | None = None) -> bytes:
        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets: list[int] = []
        for number, body in enumerate(self.objects, start=1):
            assert body is not None, f"object {number} was never written"
            offsets.append(len(out))
            out += f"{number} 0 obj\n".encode("latin-1")
            out += body + b"\nendobj\n"
        xref = len(out)
        out += f"xref\n0 {len(self.objects) + 1}\n".encode("latin-1")
        out += b"0000000000 65535 f \n"
        for offset in offsets:
            out += f"{offset:010d} 00000 n \n".encode("latin-1")
        trailer = (
            f"<< /Size {len(self.objects) + 1} /Root {root} 0 R"
        )
        if info is not None:
            trailer += f" /Info {info} 0 R"
        trailer += " >>"
        out += (
            f"trailer\n{trailer}\nstartxref\n{xref}\n%%EOF\n"
        ).encode("latin-1")
        return bytes(out)


def build_pdf(
    path: Path,
    pages: list[list[dict]],
    labels: list[tuple[int, str]] | None = None,
    outline: list[tuple[str, int]] | None = None,
    info: bool = True,
) -> None:
    """Write a small valid PDF with optional page labels and outline."""
    builder = PdfBuilder()
    catalog = builder.reserve()
    pages_object = builder.reserve()
    helvetica = builder.add(
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    )
    helvetica_bold = builder.add(
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
    )
    info_object = None
    if info:
        info_object = builder.add(
            "<< /Title (Test Paper) /Author (Tester) "
            "/CreationDate (D:20260101120000Z) >>"
        )
    labels_object = builder.reserve() if labels else None
    outline_object = builder.reserve() if outline else None

    page_numbers: list[int] = []
    for boxes in pages:
        content = builder.add(_content_stream(boxes))
        page_numbers.append(
            builder.add(
                f"<< /Type /Page /Parent {pages_object} 0 R "
                f"/MediaBox [0 0 612 792] /Contents {content} 0 R >>"
            )
        )

    kids = " ".join(f"{number} 0 R" for number in page_numbers)
    builder.set(
        pages_object,
        f"<< /Type /Pages /Count {len(pages)} /Kids [{kids}] "
        f"/Resources << /Font << /F1 {helvetica} 0 R "
        f"/F2 {helvetica_bold} 0 R >> >> >>",
    )

    if labels is not None:
        entries = " ".join(
            f"{start} << /S /{style} >>" for start, style in labels
        )
        builder.set(labels_object, f"<< /Nums [{entries}] >>")

    if outline:
        item_numbers = [builder.reserve() for _ in outline]
        builder.set(
            outline_object,
            f"<< /Type /Outlines /First {item_numbers[0]} 0 R "
            f"/Last {item_numbers[-1]} 0 R /Count {len(outline)} >>",
        )
        for index, (title, page_number) in enumerate(outline):
            parts = [
                f"/Parent {outline_object} 0 R",
                f"/Title ({_escape_pdf_string(title)})",
                f"/Dest [{page_numbers[page_number - 1]} 0 R /Fit]",
            ]
            if index:
                parts.append(f"/Prev {item_numbers[index - 1]} 0 R")
            if index + 1 < len(outline):
                parts.append(f"/Next {item_numbers[index + 1]} 0 R")
            builder.set(item_numbers[index], "<< " + " ".join(parts) + " >>")

    catalog_parts = ["/Type /Catalog", f"/Pages {pages_object} 0 R"]
    if labels is not None:
        catalog_parts.append(f"/PageLabels {labels_object} 0 R")
    if outline:
        catalog_parts.append(f"/Outlines {outline_object} 0 R")
    builder.set(catalog, "<< " + " ".join(catalog_parts) + " >>")
    path.write_bytes(builder.render(catalog, info_object))


def text_box(
    text: str,
    *,
    x: float = 72,
    y: float = 400,
    size: float = 10,
    font: str = "F1",
) -> dict:
    return {"text": text, "x": x, "y": y, "size": size, "font": font}


def line_box(
    lines: list[str],
    *,
    x: float = 72,
    y: float = 400,
    size: float = 10,
    font: str = "F1",
    leading: float | None = None,
) -> dict:
    box: dict = {"lines": lines, "x": x, "y": y, "size": size, "font": font}
    if leading is not None:
        box["leading"] = leading
    return box


@unittest.skipUnless(
    HAVE_PDFMINER, "pdfminer.six is required for pdf-extract tests"
)
class PdfExtractTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.temp = Path(self._temp.name)

    def fixture(self, name: str = "sample.pdf", **kwargs) -> Path:
        path = self.temp / name
        build_pdf(path, **kwargs)
        return path

    def run_main(self, *argv: object) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(
            stderr
        ):
            code = EXTRACT.main([str(argument) for argument in argv])
        return code, stdout.getvalue(), stderr.getvalue()

    def json_main(self, *argv: object) -> object:
        code, stdout, stderr = self.run_main(*argv)
        self.assertEqual(code, 0, stderr)
        return json.loads(stdout)

    def write_blocks(
        self, pdf: Path, key: str = "TEST", extra: tuple = ()
    ) -> list[dict]:
        out = self.temp / f"out-{key}"
        result = self.json_main(
            "blocks", pdf, "--key", key, "--out", out, *extra
        )
        self.assertEqual(result["status"], "written")
        lines = (out / "blocks.jsonl").read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines]

    def ocr_record(
        self,
        pdf: Path,
        page: int,
        lines: list[tuple[str, list[float]]],
        *,
        source_sha256: str | None = None,
        version: str | None = None,
    ) -> dict:
        """Build one ocr.jsonl record whose bboxes are already in points."""
        return {
            "pdf_page": page,
            "source_sha256": source_sha256
            or hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "ocr_version": version or EXTRACT.OCR_VERSION,
            "engine": "tesseract.js 7.0.0 eng fast",
            "width": 612,
            "height": 792,
            "confidence": 90,
            "text": " ".join(text for text, _bbox in lines),
            "lines": [
                {"text": text, "bbox": bbox, "confidence": 90}
                for text, bbox in lines
            ],
        }

    def write_ocr(self, out: Path, records: list[dict]) -> Path:
        out.mkdir(parents=True, exist_ok=True)
        path = out / "ocr.jsonl"
        path.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False) + "\n"
                for record in records
            ),
            encoding="utf-8",
        )
        return path

    def test_meta_reports_hash_info_and_first_page_text(self) -> None:
        pdf = self.fixture(
            pages=[[text_box("Hello metadata world.")]]
        )
        data = self.json_main("meta", pdf)
        self.assertEqual(data["path"], str(pdf))
        self.assertEqual(
            data["source_sha256"],
            hashlib.sha256(pdf.read_bytes()).hexdigest(),
        )
        self.assertEqual(data["page_count"], 1)
        self.assertEqual(data["info"]["Title"], "Test Paper")
        self.assertEqual(data["info"]["Author"], "Tester")
        self.assertEqual(
            data["info"]["CreationDate"], "D:20260101120000Z"
        )
        self.assertIn("Hello metadata world.", data["first_page_text"])

    def test_header_and_footer_removed_across_three_pages(self) -> None:
        pages = []
        for number in range(1, 4):
            pages.append(
                [
                    text_box(f"Running Header {number}", y=760, size=8),
                    text_box(
                        f"Body page {number} has its own unique sentences.",
                        y=400,
                    ),
                    text_box(f"{number}", x=300, y=20, size=8),
                ]
            )
        pdf = self.fixture(pages=pages)
        code, stdout, stderr = self.run_main("text", pdf)
        self.assertEqual(code, 0, stderr)
        self.assertNotIn("Running Header", stdout)
        for number in range(1, 4):
            self.assertIn(f"Body page {number}", stdout)
        units = self.write_blocks(pdf)
        texts = [unit["text_span"] for unit in units]
        self.assertFalse(
            any("Running Header" in text for text in texts), texts
        )
        self.assertNotIn("1", texts)
        self.assertEqual(len(units), 3)
        self.assertTrue(
            all(unit["layout"]["kind"] == "body" for unit in units)
        )

    def test_running_footer_near_band_edge_and_single_page_request(self) -> None:
        # The footer's bottom edge sits at about 9% of the page height, as in
        # Philosophers' Imprint; one requested page still sees its neighbours.
        pages = []
        for number in range(1, 6):
            pages.append(
                [
                    text_box("JOURNAL OF TESTS", y=760, size=11),
                    text_box(
                        f"Body page {number} has its own unique sentences.",
                        y=400,
                    ),
                    text_box(f"JOURNAL - {number} - VOL. 26", x=200, y=72, size=11),
                ]
            )
        pdf = self.fixture(pages=pages)
        code, stdout, stderr = self.run_main("text", pdf, "--pages", "3")
        self.assertEqual(code, 0, stderr)
        self.assertIn("Body page 3", stdout)
        self.assertNotIn("JOURNAL", stdout)
        self.assertNotIn("Body page 2", stdout)
        units = self.write_blocks(pdf)
        self.assertEqual([unit["layout"]["kind"] for unit in units], ["body"] * 5)

    def test_cjk_lines_join_without_spaces(self) -> None:
        self.assertEqual(EXTRACT.join_lines(["正义是社会制度的", "首要德性。"]), "正义是社会制度的首要德性。")
        self.assertEqual(EXTRACT.join_texts("罗尔斯认为", "Political Liberalism"), ("罗尔斯认为Political Liberalism", 5))
        self.assertEqual(EXTRACT.join_lines(["a reason-", "able view"]), "a reasonable view")
        self.assertTrue(EXTRACT.ends_terminal("首要德性。"))

    def test_cross_page_merge_rules(self) -> None:
        def block(text: str, page: int) -> object:
            return EXTRACT.Block("body", text, 72, 100, 500, 200, [page], [str(page)])

        merged = EXTRACT.merge_across_pages([[block("正义是社会制度的", 3)], [block("首要德性。", 4)]])
        self.assertEqual([b.text for b in merged[0]], ["正义是社会制度的首要德性。"])
        self.assertEqual(merged[0][0].page_breaks, [{"offset": 8, "page_label": "4"}])
        apart = EXTRACT.merge_across_pages([[block("the argument runs", 3)], [block("on and on.", 7)]])
        self.assertEqual([len(page) for page in apart], [1, 1])
        ended = EXTRACT.merge_across_pages([[block("首要德性。", 3)], [block("正义", 4)]])
        self.assertEqual([len(page) for page in ended], [1, 1])

    def test_alternating_heads_and_printed_page_numbers(self) -> None:
        # Even pages carry the author, odd pages the title, as in many journals;
        # the printed numbers 121-126 replace the PDF order 1-6 as labels.
        pages = []
        for number in range(1, 7):
            head = "AMIA SRINIVASAN" if number % 2 == 0 else "APTNESS OF ANGER"
            body = f"Page {number} argues its own distinct and unrepeated point here"
            if number == 3:
                body = "the third page continues mid sentence and ends without a stop"
            if number == 2:
                body = "The second page ends in the middle of a sentence that runs on to"
            pages.append([
                text_box(head, x=180, y=760, size=8),
                text_box(str(120 + number), x=72, y=760, size=8),
                text_box(body, y=400),
            ])
        pdf = self.fixture(pages=pages)
        units = self.write_blocks(pdf)
        texts = [unit["text_span"] for unit in units]
        self.assertFalse(any("SRINIVASAN" in t or "APTNESS" in t for t in texts), texts)
        self.assertEqual(units[0]["locator"], {"kind": "page", "value": "121"})
        merged = next(unit for unit in units if unit["locator"]["kind"] == "page-range")
        self.assertEqual(merged["locator"]["value"], "122-123")
        self.assertEqual(merged["layout"]["page_breaks"][0]["page_label"], "123")

    def test_small_type_with_body_below_is_a_quotation(self) -> None:
        pdf = self.fixture(pages=[[
            text_box("Body paragraph above the quotation, in the normal type size.", y=600),
            text_box("A quotation set in smaller type in the lower half.", y=330, size=8),
            text_box("Body text resumes below the quotation in normal type.", y=250),
            text_box("1 A real footnote at the foot of the page.", y=80, size=8),
        ]])
        kinds = {unit["text_span"][:5]: unit["layout"]["kind"] for unit in self.write_blocks(pdf)}
        self.assertEqual(kinds["A quo"], "blockquote")
        self.assertEqual(kinds["1 A r"], "footnote")

    def test_footnote_kind_uses_smaller_type(self) -> None:
        pdf = self.fixture(
            pages=[
                [
                    text_box(
                        "A body paragraph with enough characters to fix "
                        "the body size for the page.",
                        y=500,
                    ),
                    text_box("1. A footnote in smaller type.", y=100, size=8),
                ]
            ]
        )
        units = self.write_blocks(pdf)
        footnotes = [
            unit
            for unit in units
            if unit["layout"]["kind"] == "footnote"
        ]
        self.assertEqual(len(footnotes), 1)
        self.assertEqual(footnotes[0]["text_span"], "1. A footnote in smaller type.")
        self.assertTrue(
            any(unit["layout"]["kind"] == "body" for unit in units)
        )

    def test_heading_kind_uses_larger_type(self) -> None:
        pdf = self.fixture(
            pages=[
                [
                    text_box("Introduction", y=650, size=14),
                    text_box(
                        "This body paragraph is long enough to dominate "
                        "the character count on the page.",
                        y=400,
                    ),
                ]
            ]
        )
        units = self.write_blocks(pdf)
        headings = [
            unit for unit in units if unit["layout"]["kind"] == "heading"
        ]
        self.assertEqual(len(headings), 1)
        self.assertEqual(headings[0]["text_span"], "Introduction")

    def test_blockquote_kind_uses_indentation_and_two_lines(self) -> None:
        pdf = self.fixture(
            pages=[
                [
                    text_box(
                        "A body paragraph long enough to establish the "
                        "body column and dominate its character count.",
                        y=400,
                    ),
                    text_box(
                        "A second body paragraph keeps the median left "
                        "edge at the main body column.",
                        y=500,
                    ),
                    line_box(
                        [
                            "An indented quotation with two lines",
                            "continues here in the same block.",
                        ],
                        x=90,
                        y=250,
                    ),
                ]
            ]
        )
        units = self.write_blocks(pdf)
        quotes = [
            unit
            for unit in units
            if unit["layout"]["kind"] == "blockquote"
        ]
        self.assertEqual(len(quotes), 1)
        self.assertIn("indented quotation", quotes[0]["text_span"])

    def test_margin_reference_attaches_to_body_block(self) -> None:
        pdf = self.fixture(
            pages=[
                [
                    text_box(
                        "This body paragraph has a marginal reference.",
                        y=400,
                    ),
                    text_box("12a", x=20, y=400),
                ]
            ]
        )
        units = self.write_blocks(pdf)
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0]["layout"]["margin_refs"], ["12a"])
        self.assertEqual(units[0]["layout"]["kind"], "body")

    def test_cross_page_merge_records_offset_and_page_range(self) -> None:
        left = "the argument continues on"
        right = "the next page. It ends here."
        pdf = self.fixture(
            pages=[[text_box(left)], [text_box(right)]]
        )
        units = self.write_blocks(pdf)
        self.assertEqual(len(units), 1)
        unit = units[0]
        self.assertEqual(unit["text_span"], f"{left} {right}")
        self.assertEqual(unit["locator"], {"kind": "page-range", "value": "1-2"})
        self.assertEqual(unit["layout"]["pdf_pages"], [1, 2])
        self.assertEqual(
            unit["layout"]["page_breaks"],
            [{"offset": len(left) + 1, "page_label": "2"}],
        )
        self.assertEqual(unit["unit_id"], "TEST:p1:b0")

    def test_dehyphenation_joins_lines(self) -> None:
        self.assertEqual(
            EXTRACT.join_lines(["A hyphen-", "ation example works."]),
            "A hyphenation example works.",
        )
        pdf = self.fixture(
            pages=[[line_box(["A hyphen-", "ation example works."], y=500)]]
        )
        units = self.write_blocks(pdf)
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0]["text_span"], "A hyphenation example works.")

    def test_find_matches_phrase_broken_across_lines(self) -> None:
        pdf = self.fixture(
            pages=[[line_box(["The breeking", "can be seen here."], y=500)]]
        )
        results = self.json_main("find", pdf, "breeking can")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["pdf_page"], 1)
        self.assertEqual(results[0]["page_label"], "1")
        self.assertIn("breeking can", results[0]["context"])

    def test_ocr_needed_reports_page_without_text(self) -> None:
        pdf = self.fixture(
            pages=[
                [text_box("This page has plenty of extractable text.")],
                [],
            ]
        )
        data = self.json_main("ocr-needed", pdf)
        self.assertEqual(data["page_count"], 2)
        self.assertEqual(data["pages_without_text"], [2])
        self.assertFalse(data["needs_ocr"])

    def test_ocr_bbox_converts_pixels_to_points(self) -> None:
        # 1000x2000 px maps onto a 500x1000 pt page; y flips at the top edge.
        self.assertEqual(
            EXTRACT.ocr_bbox_to_points(
                [100, 100, 300, 200], 1000, 2000, 0, 0, 500, 1000
            ),
            (50.0, 900.0, 150.0, 950.0),
        )
        self.assertEqual(
            EXTRACT.ocr_bbox_to_points(
                [0, 0, 500, 1000], 500, 1000, 10, 20, 510, 1020
            ),
            (10.0, 20.0, 510.0, 1020.0),
        )
        with self.assertRaises(ValueError):
            EXTRACT.ocr_bbox_to_points([1, 2, 3], 10, 10, 0, 0, 10, 10)

    def test_ocr_lines_group_into_boxes(self) -> None:
        record = {
            "lines": [
                {"text": "First line", "bbox": [100, 700, 400, 710]},
                {"text": "Second line", "bbox": [100, 688, 390, 698]},
                {"text": "New paragraph", "bbox": [100, 650, 390, 660]},
                {"text": "A smaller note line", "bbox": [100, 100, 300, 108]},
                {"text": "Indented line", "bbox": [200, 84, 300, 94]},
            ]
        }
        boxes = EXTRACT.boxes_from_ocr_lines(record)
        self.assertEqual(len(boxes), 4)
        self.assertEqual(boxes[0].lines, ["First line", "Second line"])
        self.assertEqual(boxes[0].text, "First lineSecond line")
        self.assertEqual(
            (boxes[0].x0, boxes[0].y0, boxes[0].x1, boxes[0].y1),
            (100, 688, 400, 710),
        )
        self.assertEqual(boxes[0].dominant_size, 7.5)
        self.assertEqual(boxes[1].text, "New paragraph")
        self.assertEqual(boxes[2].text, "A smaller note line")
        self.assertEqual(boxes[2].dominant_size, 6.0)
        # The same height and a near line, but a far left edge, splits the box.
        self.assertEqual(boxes[3].text, "Indented line")
        self.assertEqual(boxes[3].x0, 200)

    def test_ocr_lines_split_paragraphs(self) -> None:
        record = {
            "lines": [
                {"text": "First paragraph line one runs to the right margin", "bbox": [100, 700, 500, 710]},
                {"text": "and this line also reaches the margin", "bbox": [100, 688, 500, 698]},
                {"text": "Second paragraph starts here", "bbox": [115, 676, 500, 686]},
                {"text": "second line reaches margin", "bbox": [100, 664, 500, 674]},
                {"text": "A short closing sentence.", "bbox": [100, 650, 300, 660]},
                {"text": "Next paragraph without an indent", "bbox": [100, 636, 500, 646]},
            ]
        }
        boxes = EXTRACT.boxes_from_ocr_lines(record)
        self.assertEqual(len(boxes), 3)
        self.assertEqual(
            boxes[0].lines,
            ["First paragraph line one runs to the right margin", "and this line also reaches the margin"],
        )
        self.assertEqual(
            boxes[1].lines,
            [
                "Second paragraph starts here",
                "second line reaches margin",
                "A short closing sentence.",
            ],
        )
        # The short terminal line ends the paragraph even without an indent.
        self.assertEqual(boxes[2].text, "Next paragraph without an indent")

    def test_blocks_read_ocr_from_default_dir_not_out(self) -> None:
        # --out redirects units and the manifest, never the OCR lookup.
        pdf = self.fixture(
            pages=[
                [text_box("The first page has ordinary extractable text.", y=400)],
                [],
            ]
        )
        extract_dir = self.temp / "default-extract"
        out = self.temp / "other-out"
        self.write_ocr(
            extract_dir,
            [
                self.ocr_record(
                    pdf,
                    2,
                    [
                        ("OCR recovered the second page text.", [72, 690, 400, 703.333]),
                        ("It continues on a second line.", [72, 672, 380, 685.333]),
                    ],
                )
            ],
        )
        with mock.patch.object(
            EXTRACT, "default_out_dir", return_value=extract_dir
        ):
            result = self.json_main(
                "blocks", pdf, "--key", "OCR", "--out", out
            )
        self.assertEqual(result["status"], "written")
        self.assertFalse((out / "ocr.jsonl").exists())
        units = [
            json.loads(line)
            for line in (out / "blocks.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        ocr_units = [unit for unit in units if unit["layout"].get("ocr")]
        self.assertEqual(len(ocr_units), 1)
        self.assertEqual(ocr_units[0]["layout"]["pdf_pages"], [2])
        self.assertIn(
            "OCR recovered the second page text.", ocr_units[0]["text_span"]
        )
        self.assertTrue(
            all(
                not unit["layout"].get("ocr")
                for unit in units
                if unit["layout"]["pdf_pages"] == [1]
            )
        )

    def test_ocr_skips_pages_already_done(self) -> None:
        pdf = self.fixture(
            pages=[[text_box("First page text.")], [text_box("Second page text.")]]
        )
        out = self.temp / "skip-out"
        self.write_ocr(
            out,
            [
                self.ocr_record(pdf, 1, [("one", [72, 700, 300, 712])]),
                self.ocr_record(pdf, 2, [("two", [72, 700, 300, 712])]),
            ],
        )
        data = self.json_main("ocr", pdf, "--pages", "1-2", "--out", out)
        self.assertEqual(data["pages_done"], 0)
        self.assertEqual(data["pages_skipped"], 2)
        self.assertIsNone(data["mean_confidence"])

    def test_ocr_record_with_wrong_hash_is_ignored(self) -> None:
        pdf = self.fixture(
            pages=[[text_box("First page text.")], []]
        )
        extract_dir = self.temp / "mismatch-extract"
        out = self.temp / "mismatch-out"
        self.write_ocr(
            extract_dir,
            [
                self.ocr_record(
                    pdf,
                    2,
                    [("Wrong hash OCR text.", [72, 700, 300, 714])],
                    source_sha256="0" * 64,
                )
            ],
        )
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        self.assertEqual(
            EXTRACT.load_ocr_records(extract_dir / "ocr.jsonl", digest), {}
        )
        with mock.patch.object(
            EXTRACT, "default_out_dir", return_value=extract_dir
        ):
            result = self.json_main(
                "blocks", pdf, "--key", "MISMATCH", "--out", out
            )
        self.assertEqual(result["status"], "written")
        units = [
            json.loads(line)
            for line in (out / "blocks.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertFalse(any(unit["layout"].get("ocr") for unit in units))
        self.assertFalse(
            any(unit["layout"]["pdf_pages"] == [2] for unit in units)
        )

    def test_blocks_cache_invalidated_when_ocr_is_added(self) -> None:
        pdf = self.fixture(
            pages=[[text_box("First page text.")], []]
        )
        extract_dir = self.temp / "cache-extract"
        out = self.temp / "cache-ocr"
        with mock.patch.object(
            EXTRACT, "default_out_dir", return_value=extract_dir
        ):
            first = self.json_main(
                "blocks", pdf, "--key", "CACHEOCR", "--out", out
            )
            self.assertEqual(first["status"], "written")
            self.assertEqual(first["unit_count"], 1)
            self.write_ocr(
                extract_dir,
                [
                    self.ocr_record(
                        pdf,
                        2,
                        [("Later OCR text.", [72, 690, 400, 703.333])],
                    )
                ],
            )
            second = self.json_main(
                "blocks", pdf, "--key", "CACHEOCR", "--out", out
            )
            self.assertEqual(second["status"], "written")
            units = [
                json.loads(line)
                for line in (out / "blocks.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
            ]
            self.assertTrue(
                any(unit["layout"].get("ocr") for unit in units)
            )
            third = self.json_main(
                "blocks", pdf, "--key", "CACHEOCR", "--out", out
            )
            self.assertEqual(third["status"], "cached")

    def test_folios_in_fifteen_percent_band_are_dropped(self) -> None:
        bodies = [
            "Alpha body sentence ends here.",
            "Beta body sentence ends here.",
            "Gamma body sentence ends here.",
        ]
        pages = [
            [
                text_box(body, y=400),
                text_box(str(number), x=300, y=100, size=8),
            ]
            for body, number in zip(bodies, (41, 42, 43))
        ]
        pages.append(
            [
                text_box("Roman folio page ends here.", y=400),
                text_box("xlv", x=300, y=100, size=8),
            ]
        )
        pdf = self.fixture(pages=pages)
        units = self.write_blocks(pdf, key="FOLIO")
        self.assertEqual(len(units), 4)
        self.assertEqual(
            [unit["text_span"] for unit in units],
            bodies + ["Roman folio page ends here."],
        )
        self.assertEqual(
            [unit["locator"]["value"] for unit in units],
            ["41", "42", "43", "44"],
        )

    def test_section_numeral_with_period_in_bottom_band_survives(self) -> None:
        pdf = self.fixture(
            pages=[
                [
                    text_box(
                        "A body paragraph with enough characters to dominate the page.",
                        y=400,
                    ),
                    text_box("V.", x=300, y=60, size=10),
                ]
            ]
        )
        units = self.write_blocks(pdf, key="SECTION")
        self.assertIn("V.", [unit["text_span"] for unit in units])
        self.assertFalse(EXTRACT.is_page_number("V."))
        self.assertTrue(EXTRACT.is_page_number("V"))

    def test_ocr_folio_and_noise_are_dropped(self) -> None:
        pdf = self.fixture(
            pages=[[text_box("First page text.", y=400)], []]
        )
        extract_dir = self.temp / "noise-extract"
        out = self.temp / "noise-out"
        self.write_ocr(
            extract_dir,
            [
                self.ocr_record(
                    pdf,
                    2,
                    [
                        ("Body line one on the OCR page.", [72, 690, 500, 703.333]),
                        ("Body line two on the OCR page.", [72, 676, 500, 689.333]),
                        ("liii", [300, 70, 330, 80]),
                        ("|", [300, 50, 305, 60]),
                    ],
                )
            ],
        )
        with mock.patch.object(
            EXTRACT, "default_out_dir", return_value=extract_dir
        ):
            self.json_main(
                "blocks", pdf, "--key", "NOISE", "--out", out
            )
        units = [
            json.loads(line)
            for line in (out / "blocks.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        ocr_units = [unit for unit in units if unit["layout"].get("ocr")]
        self.assertEqual(len(ocr_units), 1)
        self.assertEqual(ocr_units[0]["layout"]["kind"], "body")
        self.assertIn("Body line one", ocr_units[0]["text_span"])
        self.assertNotIn("liii", ocr_units[0]["text_span"])
        self.assertNotIn("|", ocr_units[0]["text_span"])
        self.assertTrue(
            EXTRACT.looks_like_page_label("litt", "liii")
        )
        self.assertTrue(
            EXTRACT.looks_like_page_label("xlix", "xlix")
        )
        self.assertFalse(EXTRACT.looks_like_page_label("litt", "2"))

    def test_ocr_footnote_kinds_by_page_size_and_note_number(self) -> None:
        def box(text: str, size: float, y0: float) -> object:
            return EXTRACT.BoxInfo(
                0.0,
                y0,
                500.0,
                y0 + 10.0,
                [text],
                text,
                {size: len(text)},
                size,
                False,
                1,
            )

        body_one = box("Main body text that fills the page.", 10.0, 600)
        body_two = box("Main body text continued down the page.", 10.0, 580)
        small = box("A smaller note without a number.", 8.0, 200)
        numbered = box("30. Same-size note below the text.", 10.0, 100)
        above = box("A small line above the main text.", 8.0, 700)
        EXTRACT.apply_ocr_footnote_kinds(
            [body_one, body_two, small, numbered, above]
        )
        self.assertEqual(small.kind, "footnote")
        self.assertEqual(numbered.kind, "footnote")
        self.assertEqual(body_one.kind, "body")
        self.assertEqual(body_two.kind, "body")
        self.assertEqual(above.kind, "body")

    def test_ocr_roman_digit_correction(self) -> None:
        cases = [
            ("(1V:5)", "(IV:5)", 1),
            ("V1:7.1—2", "VI:7.1—2", 1),
            ("see 1V and X1 here", "see IV and XI here", 2),
            ("11 and 1965 stay", "11 and 1965 stay", 0),
            ("IV:5", "IV:5", 0),
            ("A1V stays", "A1V stays", 0),
        ]
        for source, expected, fixes in cases:
            self.assertEqual(EXTRACT.fix_ocr_roman(source), (expected, fixes))

    @unittest.skipUnless(
        HAVE_NODE and HAVE_POWERSHELL and HAVE_TESSERACT,
        "node, tesseract.js, and PowerShell are required for real OCR",
    )
    def test_rendered_page_is_ocrd(self) -> None:
        pdf = self.fixture(
            pages=[[text_box("Hello OCR world", y=600, size=24)]]
        )
        batch = self.temp / "render-batch"
        rendered = EXTRACT.run_renderer(pdf, [1], batch, 1200)
        results = EXTRACT.run_ocr([1], rendered, "eng")
        self.assertEqual(rendered[1]["width"], 1200)
        self.assertIn("Hello", results[1]["text"])
        self.assertTrue(results[1]["lines"])

    @unittest.skipUnless(
        HAVE_NODE and HAVE_POWERSHELL and HAVE_TESSERACT,
        "node, tesseract.js, and PowerShell are required for real OCR",
    )
    def test_ocr_command_records_roman_fixes(self) -> None:
        pdf = self.fixture(
            pages=[[text_box("Hello OCR world", y=600, size=24)]]
        )
        out = self.temp / "ocr-command"
        data = self.json_main(
            "ocr", pdf, "--pages", "1", "--out", out
        )
        self.assertEqual(data["pages_done"], 1)
        record = json.loads(
            (out / "ocr.jsonl").read_text(encoding="utf-8").splitlines()[0]
        )
        self.assertIsInstance(record["roman_fixes"], int)
        self.assertIn("Hello", record["text"])

    def test_page_labels_drive_text_headers_and_locators(self) -> None:
        pages = [
            [text_box(f"Page body {number}")] for number in range(1, 4)
        ]
        pdf = self.fixture(
            pages=pages, labels=[(0, "r"), (2, "D")]
        )
        code, stdout, stderr = self.run_main("text", pdf)
        self.assertEqual(code, 0, stderr)
        self.assertIn("=== pi (pdf 1) ===", stdout)
        self.assertIn("=== pii (pdf 2) ===", stdout)
        self.assertIn("=== p1 (pdf 3) ===", stdout)
        units = self.write_blocks(pdf)
        self.assertEqual(
            [unit["locator"]["value"] for unit in units], ["i", "ii", "1"]
        )

    def test_toc_resolves_one_outline_entry(self) -> None:
        pdf = self.fixture(
            pages=[
                [text_box("First page")],
                [text_box("Second page")],
            ],
            outline=[("Second", 2)],
        )
        entries = self.json_main("toc", pdf)
        self.assertEqual(
            entries,
            [
                {
                    # pdfminer starts the outline root at level 0, so a
                    # top-level entry is reported at level 1.
                    "level": 1,
                    "title": "Second",
                    "pdf_page": 2,
                    "page_label": "2",
                }
            ],
        )

    def test_blocks_caching_and_force(self) -> None:
        pdf = self.fixture(pages=[[text_box("Cache me.")]])
        out = self.temp / "cache-out"
        first = self.json_main(
            "blocks", pdf, "--key", "CACHE", "--out", out
        )
        self.assertEqual(first["status"], "written")
        self.assertEqual(first["unit_count"], 1)
        manifest_path = out / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["unit_count"], 1)

        second = self.json_main(
            "blocks", pdf, "--key", "CACHE", "--out", out
        )
        self.assertEqual(second["status"], "cached")
        self.assertEqual(second["unit_count"], 1)

        manifest["unit_count"] = 999
        manifest_path.write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        forced = self.json_main(
            "blocks", pdf, "--key", "CACHE", "--out", out, "--force"
        )
        self.assertEqual(forced["status"], "written")
        self.assertEqual(forced["unit_count"], 1)
        rewritten = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(rewritten["unit_count"], 1)

    def resolve_schema(self, spec: dict, root: dict) -> dict:
        while "$ref" in spec:
            name = spec["$ref"].rsplit("/", 1)[-1]
            spec = root["$defs"][name]
        return spec

    def assert_schema_value(
        self, value: object, spec: dict, root: dict, path: str
    ) -> None:
        spec = self.resolve_schema(spec, root)
        if "enum" in spec:
            self.assertIn(value, spec["enum"], path)
            return
        kind = spec.get("type")
        if kind == "object":
            self.assertIsInstance(value, dict, path)
            allowed = set(spec.get("properties", {}))
            self.assertEqual(set(value) - allowed, set(), path)
            for required in spec.get("required", []):
                self.assertIn(required, value, f"{path}: missing {required}")
            for key, item in value.items():
                self.assert_schema_value(
                    item,
                    spec["properties"][key],
                    root,
                    f"{path}.{key}",
                )
        elif kind == "array":
            self.assertIsInstance(value, list, path)
            if "minItems" in spec:
                self.assertGreaterEqual(
                    len(value), spec["minItems"], path
                )
            for index, item in enumerate(value):
                self.assert_schema_value(
                    item, spec.get("items", {}), root, f"{path}[{index}]"
                )
        elif kind == "string":
            self.assertIsInstance(value, str, path)
            if "pattern" in spec:
                self.assertRegex(value, spec["pattern"], path)
            if "minLength" in spec:
                self.assertGreaterEqual(
                    len(value), spec["minLength"], path
                )
        elif kind == "integer":
            self.assertIsInstance(value, int, path)
            self.assertNotIsInstance(value, bool, path)
            if "minimum" in spec:
                self.assertGreaterEqual(value, spec["minimum"], path)

    def test_every_unit_validates_against_contract(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        pdf = self.fixture(
            pages=[
                [
                    text_box("A Heading", y=700, size=14),
                    text_box("this paragraph continues on", y=500),
                    text_box("1. A note in smaller type.", y=100, size=8),
                ],
                [text_box("the next page. Done.")],
            ]
        )
        units = self.write_blocks(pdf, key="SCHEMA")
        self.assertGreaterEqual(len(units), 3)
        for unit in units:
            self.assert_schema_value(unit, schema, schema, "unit")
            self.assertEqual(
                unit["unit_sha256"],
                hashlib.sha256(
                    unit["text_span"].encode("utf-8")
                ).hexdigest(),
            )
            self.assertRegex(unit["unit_id"], r"^SCHEMA:p\d+:b\d+$")
            self.assertEqual(
                unit["verification_status"], "provisional"
            )
            self.assertEqual(unit["coverage_label"], "full-reading")
            self.assertTrue(
                unit["extraction_version"].startswith(
                    EXTRACT.EXTRACTION_VERSION + "+pdfminer-"
                )
            )

        kinds = {unit["layout"]["kind"] for unit in units}
        self.assertEqual(kinds, {"heading", "body", "footnote"})
        merged = [
            unit
            for unit in units
            if len(unit["layout"]["pdf_pages"]) > 1
        ]
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["locator"]["kind"], "page-range")
        for page_break in merged[0]["layout"]["page_breaks"]:
            self.assertGreaterEqual(page_break["offset"], 0)
            self.assertLess(
                page_break["offset"], len(merged[0]["text_span"])
            )


if __name__ == "__main__":
    unittest.main()



