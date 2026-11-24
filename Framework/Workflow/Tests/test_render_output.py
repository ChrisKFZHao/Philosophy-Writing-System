from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = WORKFLOW_ROOT / "Scripts"
SCRIPT = SCRIPTS / "render-output.py"


def load_script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_cli(*args: object, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1", **(env or {})},
    )


RENDER = load_script("render-output.py")
PANDOC = RENDER.find_pandoc()
BROWSER = RENDER.find_browser()

INDEX_TEXT = """# Bibliography Index

## Reference Inventory

| KEY | Author | Title | PDF | Zotero | Analysis Level | Topics | Used By |
|-----|--------|-------|-----|--------|----------------|--------|---------|
| RAWLS-POLITICAL-LIBERALISM | Rawls, John | "Political Liberalism" | PDF/Rawls_2005_Political-Liberalism.pdf | — | Level 0.5 | x | — |
| SCHUSTER-MORAL-DISAGREEMENT | Schuster, Nick & Kilov, Daniel | "Moral disagreement and the limits" | PDF/Schuster_2025_Moral-Disagreement.pdf | — | Level 0.5 | x | — |
| BAI-CONSTITUTIONAL-AI | Bai, Yuntao et al. (Anthropic) | "Constitutional AI: Harmlessness" | PDF/Bai_2022_Constitutional-AI.pdf | — | Level 0.5 | x | — |
| NODATE-KEY | Noone, Nemo | "Undated Work" | — | — | Level 0.5 | x | — |
"""

REFS_TEXT = """# refs

| KEY | 角色 | 状态 | 备注 |
|-----|------|------|------|
| RAWLS-POLITICAL-LIBERALISM | core | cited | x |
| SCHUSTER-MORAL-DISAGREEMENT | core | cited | x |
| BAI-CONSTITUTIONAL-AI | core | cited | x |
| NODATE-KEY | core | cited | x |
"""


def row(key: str, author: str, title: str, pdf: str | None) -> dict:
    pdfs = [pdf] if pdf else []
    return {
        "key": key,
        "cells": [key, author, title, f"PDF/{pdf}" if pdf else "—", "", "Level 0.5", "", ""],
        "pdfs": pdfs,
    }


class HeaderTests(unittest.TestCase):
    def test_split_header_reads_simple_values(self):
        text = ("---\nkind: handout\ntitle: 测试 讲义   # note\nauthor: \"A B\"\n"
                "event: \"A # B\"\n---\n\nbody\n")
        meta, header, body = RENDER.split_header(text)
        self.assertEqual(meta["kind"], "handout")
        self.assertEqual(meta["title"], "测试 讲义")
        self.assertEqual(meta["author"], "A B")
        self.assertEqual(meta["event"], "A # B")
        self.assertTrue(header.startswith("---"))
        self.assertTrue(header.endswith("---"))
        self.assertEqual(body.strip(), "body")

    def test_missing_kind_is_an_error(self):
        self.assertIn("missing-kind", RENDER.header_errors({}))
        self.assertIn("missing-title", RENDER.header_errors({}))
        self.assertIn("invalid-kind:talk", RENDER.header_errors({"kind": "talk", "title": "T"}))
        self.assertEqual(RENDER.header_errors({"kind": "slides", "title": "T"}), [])


class CitationTests(unittest.TestCase):
    def replace(self, text: str, refs: set[str], rows: dict[str, dict]):
        return RENDER.replace_citations(text, refs, rows)

    def test_one_author(self):
        rows = {"K": row("K", "Rawls, John", '"Political Liberalism"', "Rawls_2005_Political-Liberalism.pdf")}
        body, errors, order = self.replace("见 [@K]", {"K"}, rows)
        self.assertEqual(body, "见（Rawls，2005）")
        moved, _, _ = self.replace("错误由谁纠正。[@K]\n下一条。 [@K, 12]", {"K"}, rows)
        self.assertEqual(moved, "错误由谁纠正（Rawls，2005）。\n下一条（Rawls，2005：12）。")
        self.assertEqual(errors, [])
        self.assertEqual(order, ["K"])

    def test_two_authors(self):
        rows = {"K": row("K", "Schuster, Nick & Kilov, Daniel", '"T"', "Schuster_2025_T.pdf")}
        body, _, _ = self.replace("[@K]", {"K"}, rows)
        self.assertEqual(body, "（Schuster & Kilov，2025）")

    def test_three_authors(self):
        rows = {"K": row("K", "Bai, Yuntao; Chen, Chen; Diaz, Dana", '"T"', "Bai_2022_T.pdf")}
        body, _, _ = self.replace("[@K]", {"K"}, rows)
        self.assertEqual(body, "（Bai 等，2022）")

    def test_et_al_is_rendered_with_deng(self):
        rows = {"K": row("K", "Bai, Yuntao et al. (Anthropic)", '"T"', "Bai_2022_T.pdf")}
        body, _, _ = self.replace("[@K]", {"K"}, rows)
        self.assertEqual(body, "（Bai 等，2022）")

    def test_locator(self):
        rows = {"K": row("K", "Rawls, John", '"T"', "Rawls_2005_T.pdf")}
        body, _, _ = self.replace("[@K, 137]", {"K"}, rows)
        self.assertEqual(body, "（Rawls，2005：137）")

    def test_undated_year(self):
        rows = {"K": row("K", "Noone, Nemo", '"T"', None)}
        body, _, _ = self.replace("[@K]", {"K"}, rows)
        self.assertEqual(body, "（Noone，n.d.）")

    def test_unknown_key(self):
        body, errors, order = self.replace("[@NOPE]", set(), {})
        self.assertEqual(body, "[citation needed]")
        self.assertIn("unknown-key:NOPE", errors)
        self.assertEqual(order, [])

    def test_key_missing_from_index(self):
        body, errors, _ = self.replace("[@ONLYREFS]", {"ONLYREFS"}, {})
        self.assertEqual(body, "[citation needed]")
        self.assertIn("key-not-in-index:ONLYREFS", errors)


class ReferenceListTests(unittest.TestCase):
    def rows(self) -> dict[str, dict]:
        return {
            "RAWLS-POLITICAL-LIBERALISM": row(
                "RAWLS-POLITICAL-LIBERALISM", "Rawls, John", '"Political Liberalism"',
                "Rawls_2005_Political-Liberalism.pdf"),
            "BAI-CONSTITUTIONAL-AI": row(
                "BAI-CONSTITUTIONAL-AI", "Bai, Yuntao et al. (Anthropic)",
                '"Constitutional AI: Harmlessness from AI Feedback"', "Bai_2022_Constitutional-AI.pdf"),
        }

    def test_handout_gets_references_in_first_citation_order(self):
        body = "先 [@BAI-CONSTITUTIONAL-AI]，再 [@RAWLS-POLITICAL-LIBERALISM]，又 [@BAI-CONSTITUTIONAL-AI]"
        result, errors, order = RENDER.preprocess_body(
            "handout", body, set(self.rows()), self.rows())
        self.assertEqual(errors, [])
        self.assertEqual(order, ["BAI-CONSTITUTIONAL-AI", "RAWLS-POLITICAL-LIBERALISM"])
        self.assertIn("# 参考文献", result)
        self.assertEqual(result.count("Constitutional AI: Harmlessness from AI Feedback"), 1)
        first = result.index("Constitutional AI")
        second = result.index("Political Liberalism")
        self.assertLess(first, second)

    def test_slides_do_not_get_references(self):
        body = "[@RAWLS-POLITICAL-LIBERALISM]"
        result, _, _ = RENDER.preprocess_body("slides", body, set(self.rows()), self.rows())
        self.assertNotIn("参考文献", result)


class QuotationTests(unittest.TestCase):
    def collect(self, body: str, sources: list[Path], root: Path, rows=None):
        return RENDER.collect_quotations(body, rows or {}, sources, root)

    def test_verified_against_quote_source(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("自由是重要的。", encoding="utf-8")
            quotations, warnings = self.collect("> 自由是重要的。", [source], Path(temp))
        self.assertEqual(len(quotations), 1)
        self.assertTrue(quotations[0]["verified"])
        self.assertEqual(warnings, [])

    def test_unverified_is_a_warning(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("完全不同的一段话。", encoding="utf-8")
            quotations, warnings = self.collect("> 自由是重要的。", [source], Path(temp))
        self.assertFalse(quotations[0]["verified"])
        self.assertEqual(len(warnings), 1)

    def test_whitespace_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("自 由\n是 重 要 的 。", encoding="utf-8")
            quotations, _ = self.collect("> 自由是重要的。", [source], Path(temp))
        self.assertTrue(quotations[0]["verified"])

    def test_curly_quotes_are_stripped(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("自由是重要的。", encoding="utf-8")
            quotations, _ = self.collect("> “自由是重要的。”", [source], Path(temp))
        self.assertTrue(quotations[0]["verified"])

    def test_trailing_citation_is_dropped(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("自由是重要的。", encoding="utf-8")
            body = "> 自由是重要的。[@RAWLS-POLITICAL-LIBERALISM, 12]"
            quotations, _ = self.collect(body, [source], Path(temp))
        self.assertTrue(quotations[0]["verified"])
        self.assertNotIn("RAWLS", quotations[0]["text"])


class SlideTests(unittest.TestCase):
    def test_too_many_items(self):
        body = "# Slide\n" + "\n".join(f"- item {number}" for number in range(6)) + "\n"
        warnings, metrics = RENDER.analyze_slides(body, None)
        self.assertIn("too-many-items:1", warnings)
        self.assertEqual(metrics["slide_count"], 2)

    def test_long_item(self):
        body = "# Slide\n- " + "汉" * 30 + "\n"
        warnings, _ = RENDER.analyze_slides(body, None)
        self.assertTrue(any(warning.startswith("long-item:1:") for warning in warnings))

    def test_missing_notes_on_middle_slide(self):
        body = "\n".join([
            "# One", "- a", "::: notes", "note one", ":::",
            "# Two", "- b",
            "# Three", "- c", "::: notes", "note three", ":::",
        ]) + "\n"
        warnings, _ = RENDER.analyze_slides(body, None)
        self.assertIn("no-notes:2", warnings)
        self.assertNotIn("no-notes:1", warnings)
        self.assertNotIn("no-notes:3", warnings)

    def test_slide_count_warning(self):
        body = "# One\n- a\n# Two\n- b\n"
        warnings, metrics = RENDER.analyze_slides(body, 20)
        self.assertEqual(metrics["slide_count"], 3)
        self.assertIn("slide-count:3 for 20 min", warnings)

    def test_notes_and_fences_are_not_counted_as_items(self):
        body = "# One\n```\n- not an item\n```\n::: notes\n- note text\n:::\n"
        _, metrics = RENDER.analyze_slides(body, None)
        self.assertEqual(metrics["slide_count"], 2)


class ToolDiscoveryTests(unittest.TestCase):
    def test_pandoc_honours_environment(self):
        with tempfile.TemporaryDirectory() as temp:
            fake = Path(temp) / "pandoc.exe"
            fake.write_text("", encoding="utf-8")
            with mock.patch.dict(os.environ, {"PANDOC": str(fake)}):
                self.assertEqual(RENDER.find_pandoc(), fake)


@unittest.skipUnless(PANDOC, "pandoc not found")
class IntegrationTests(unittest.TestCase):
    def fixture(self, temp: Path, kind: str) -> tuple[Path, Path, Path]:
        index = temp / "INDEX.md"
        refs = temp / "refs.md"
        index.write_text(INDEX_TEXT, encoding="utf-8")
        refs.write_text(REFS_TEXT, encoding="utf-8")
        content = temp / f"content-{kind}.md"
        return content, refs, index

    def handout(self) -> str:
        return "\n".join([
            "---", "kind: handout", "title: 测试讲义", "---", "",
            "::: thesis", "这是唯一的论点。", ":::", "",
            "- 前提一 [@RAWLS-POLITICAL-LIBERALISM]", "",
        ])

    def slides(self) -> str:
        return "\n".join([
            "---", "kind: slides", "title: 测试幻灯片", "minutes: 20", "---", "",
            "# 第一页", "- 要点", "", "::: notes", "讲第一页。", ":::", "",
            "# 第二页", "- 要点二", "", "::: notes", "讲第二页。", ":::", "",
        ])

    def test_handout_to_html(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            content, refs, index = self.fixture(directory, "handout")
            content.write_text(self.handout(), encoding="utf-8")
            completed = run_cli("render", content, "--to", "html", "--refs", refs, "--index", index)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            html = content.with_suffix(".html")
            self.assertTrue(html.is_file())
            text = html.read_text(encoding="utf-8")
            self.assertIn('class="thesis"', text)
            self.assertIn("参考文献", text)
            self.assertTrue(content.with_suffix(".html.check.json").is_file())

    def test_slides_to_pptx(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            content, refs, index = self.fixture(directory, "slides")
            content.write_text(self.slides(), encoding="utf-8")
            completed = run_cli("render", content, "--to", "pptx", "--refs", refs, "--index", index)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            deck = content.with_suffix(".pptx")
            self.assertTrue(deck.is_file())
            with zipfile.ZipFile(deck) as archive:
                names = archive.namelist()
            slides = [name for name in names if name.startswith("ppt/slides/slide")
                      and name.endswith(".xml")]
            notes = [name for name in names if name.startswith("ppt/notesSlides/notesSlide")
                     and name.endswith(".xml")]
            self.assertGreaterEqual(len(slides), 1)
            self.assertGreaterEqual(len(notes), 1)

    @unittest.skipUnless(
        os.environ.get("PHIL_TEST_BROWSER") == "1" and BROWSER,
        "set PHIL_TEST_BROWSER=1 to exercise the browser",
    )
    def test_handout_to_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            content, refs, index = self.fixture(directory, "handout")
            content.write_text(self.handout(), encoding="utf-8")
            completed = run_cli("render", content, "--to", "pdf", "--refs", refs, "--index", index)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            pdf = content.with_suffix(".pdf")
            self.assertTrue(pdf.is_file())
            self.assertGreater(pdf.stat().st_size, 0)
            report = json.loads(content.with_suffix(".pdf.check.json").read_text(encoding="utf-8"))
            self.assertEqual(report["to"], "pdf")


if __name__ == "__main__":
    unittest.main()
