"""Tests for reader-build.py."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "Scripts" / "reader-build.py"
REPO_ROOT = Path(__file__).resolve().parents[3]
STEM = "Author_2019_Title"
REAL_STEM = "Srinivasan_2018_The-Aptness-of-Anger"
REAL_READER = REPO_ROOT / "Private/Bibliography/Reader" / REAL_STEM
REAL_BLOCKS = REPO_ROOT / "Private/Bibliography/Extract" / REAL_STEM / "blocks.jsonl"


def load_build_module():
    spec = importlib.util.spec_from_file_location("reader_build", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILD = load_build_module()


def make_unit(unit_id, text, sha="hash", kind="body", page="10", breaks=None):
    layout = {"kind": kind}
    if breaks:
        layout["page_breaks"] = breaks
    return {"unit_id": unit_id, "text_span": text, "unit_sha256": sha,
            "locator": {"kind": "page", "value": page}, "layout": layout}


def make_translation(unit_id, zh, sha="hash"):
    return {"unit_id": unit_id, "unit_sha256": sha, "zh": zh,
            "model": "test-model", "glossary": "test-glossary"}


class ReaderBuildTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name)
        template = self.root / "Framework/Workflow/Templates/Reader/reader.html"
        template.parent.mkdir(parents=True)
        template.write_text("__READER_DATA__", encoding="utf-8")
        self.bibliography = self.root / "Private/Bibliography"
        self.extract = self.bibliography / "Extract" / STEM
        self.reader = self.bibliography / "Reader" / STEM
        self.extract.mkdir(parents=True)
        self.reader.mkdir(parents=True)
        self.out = self.root / "out/reader.html"

    def write_blocks(self, *records):
        lines = [json.dumps(record, ensure_ascii=False) for record in records]
        (self.extract / "blocks.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_translations(self, *records, name="translation-part1.jsonl"):
        lines = [json.dumps(record, ensure_ascii=False) for record in records]
        (self.reader / name).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_json(self, name, value):
        (self.reader / name).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def run_build(self, stem=STEM):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = BUILD.main([stem, "--root", str(self.root), "--out", str(self.out)])
        text = stdout.getvalue()
        return code, (json.loads(text) if text.strip() else None)

    def data(self):
        return json.loads(self.out.read_text(encoding="utf-8"))

    def test_unit_selection_and_order(self):
        self.write_blocks(make_unit("u1", "one"), make_unit("u2", "two"),
                          make_unit("u3", "three"))
        self.write_translations(make_translation("u3", "三"), make_translation("u1", "一"))
        code, report = self.run_build()
        self.assertEqual(code, 0)
        self.assertEqual([unit["id"] for unit in self.data()["units"]], ["u1", "u3"])
        self.assertEqual(report["units"], 2)
        self.assertTrue((self.out.parent / "reader.check.json").is_file())

    def test_footnotes_split_out(self):
        self.write_blocks(make_unit("u1", "body"), make_unit("u2", "note", kind="footnote"))
        self.write_translations(make_translation("u1", "正文"), make_translation("u2", "脚注"))
        code, report = self.run_build()
        self.assertEqual(code, 0)
        data = self.data()
        self.assertEqual([unit["id"] for unit in data["units"]], ["u1"])
        self.assertEqual([note["id"] for note in data["footnotes"]], ["u2"])
        self.assertEqual(report["footnotes"], 1)

    def test_page_markers_inserted_at_offsets(self):
        breaks = [{"offset": 2, "page_label": "12"}, {"offset": 4, "page_label": "13"}]
        self.write_blocks(make_unit("u1", "abcdef", breaks=breaks))
        self.write_translations(make_translation("u1", "ab⟦p12⟧cd⟦p13⟧ef"))
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        self.assertEqual(self.data()["units"][0]["en"], "ab⟦p12⟧cd⟦p13⟧ef")

    def test_stale_translation_is_an_error_and_excluded(self):
        self.write_blocks(make_unit("u1", "one", sha="current"),
                          make_unit("u2", "two", sha="hash"))
        self.write_translations(make_translation("u1", "一", sha="old"),
                                make_translation("u2", "二"))
        code, report = self.run_build()
        self.assertEqual(code, 1)
        self.assertIn("stale:u1", report["errors"])
        self.assertEqual([unit["id"] for unit in self.data()["units"]], ["u2"])

    def test_later_translation_line_wins(self):
        self.write_blocks(make_unit("u1", "one"))
        self.write_translations(make_translation("u1", "旧"))
        self.write_translations(make_translation("u1", "新"), name="translation-part2.jsonl")
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        self.assertEqual(self.data()["units"][0]["zh"], "新")

    def test_page_marker_mismatch_is_an_error(self):
        self.write_blocks(make_unit("u1", "abcd",
                                    breaks=[{"offset": 2, "page_label": "9"}]))
        self.write_translations(make_translation("u1", "译文"))
        code, report = self.run_build()
        self.assertEqual(code, 1)
        self.assertIn("page-markers:u1", report["errors"])

    def test_anchor_warnings(self):
        self.write_blocks(make_unit("u1", "source text"), make_unit("u2", "two"))
        self.write_translations(make_translation("u1", "翻译文字"))
        self.write_json("agent-notes.json", {"notes": [
            {"id": "n1", "unit_id": "u1", "kind": "term",
             "anchor_en": "missing", "anchor_zh": "翻译", "title": "t", "body": "b"},
            {"id": "n2", "unit_id": "u1", "kind": "term",
             "anchor_en": "source", "anchor_zh": "不存在", "title": "t", "body": "b"},
            {"id": "n3", "unit_id": "u2", "kind": "context",
             "anchor_en": "two", "title": "t", "body": "b"},
        ]})
        code, report = self.run_build()
        self.assertEqual(code, 0)
        self.assertIn("anchor-en:n1", report["warnings"])
        self.assertNotIn("anchor-zh:n1", report["warnings"])
        self.assertIn("anchor-zh:n2", report["warnings"])
        self.assertNotIn("anchor-en:n2", report["warnings"])
        self.assertIn("note-unit:n3", report["warnings"])

    def test_reader_json_overrides_and_epigraph(self):
        self.write_blocks(make_unit("u1", "one"), make_unit("u2", "two"))
        self.write_translations(make_translation("u1", "一"), make_translation("u2", "二"))
        self.write_json("reader.json", {
            "key": "KEY-1", "title_zh": "中文题", "author_zh": "作者",
            "venue": "期刊", "section_label": "第一节",
            "epigraph": ["u2"], "footer": "页脚",
        })
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        data = self.data()
        self.assertEqual(data["meta"]["key"], "KEY-1")
        self.assertEqual(data["meta"]["title_zh"], "中文题")
        self.assertEqual(data["meta"]["author_zh"], "作者")
        self.assertEqual(data["meta"]["venue"], "期刊")
        self.assertEqual(data["meta"]["section_label"], "第一节")
        self.assertEqual(data["meta"]["footer"], "页脚")
        self.assertFalse(data["units"][0]["epigraph"])
        self.assertTrue(data["units"][1]["epigraph"])

    def test_index_author_title_and_year(self):
        index = "\n".join([
            "# Index",
            "## Reference Inventory",
            "| KEY | Author | Title | PDF | Zotero | Analysis Level | Topics | Used By |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            '| TEST-KEY | Srinivasan, Amia & Smith, John | "The Aptness of Anger" (2018) '
            "| PDF/Author_2019_Title.pdf | Z | Level 3 | anger | x |",
        ])
        (self.bibliography / "INDEX.md").write_text(index, encoding="utf-8")
        self.write_blocks(make_unit("u1", "one"))
        self.write_translations(make_translation("u1", "一"))
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        meta = self.data()["meta"]
        self.assertEqual(meta["key"], "TEST-KEY")
        self.assertEqual(meta["author"], "Amia Srinivasan & John Smith")
        self.assertEqual(meta["title"], "The Aptness of Anger")
        self.assertEqual(meta["year"], "2019")

    def test_script_close_is_escaped(self):
        self.write_blocks(make_unit("u1", "one"))
        self.write_translations(make_translation("u1", "危险 </script> 文字"))
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        html = self.out.read_text(encoding="utf-8")
        self.assertIn("<\\/script>", html)
        self.assertNotIn("</script>", html)

    def test_missing_inputs_exit_2(self):
        self.write_translations(make_translation("u1", "一"))
        code, report = self.run_build()
        self.assertEqual(code, 2)
        self.assertIsNone(report)

        self.write_blocks(make_unit("u1", "one"))
        (self.reader / "translation-part1.jsonl").unlink()
        code, report = self.run_build()
        self.assertEqual(code, 2)
        self.assertIsNone(report)

    @unittest.skipUnless(REAL_BLOCKS.is_file() and REAL_READER.is_dir(),
                         "real Srinivasan files are absent")
    def test_real_srinivasan_build(self):
        out = self.root / "real/reader.html"
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = BUILD.main([REAL_STEM, "--root", str(REPO_ROOT), "--out", str(out)])
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["errors"], [])
        self.assertGreater(report["units"], 10)
        self.assertEqual(code, 0)
        self.assertTrue(out.is_file())


if __name__ == "__main__":
    unittest.main()
