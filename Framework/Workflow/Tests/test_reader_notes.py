"""Tests for reader-notes.py."""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "Scripts" / "reader-notes.py"
IDEA_LEDGER = Path(__file__).resolve().parents[1] / "Scripts" / "idea-ledger.py"
POLICY = Path(__file__).resolve().parents[1] / "Scripts" / "workflow-policy.py"
RENDER = Path(__file__).resolve().parents[1] / "Scripts" / "render-output.py"
STEM = "Author_2019_Title"
KEY = "AUTHOR-TITLE"
TOPIC = "demo-project"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NOTES = load_module(SCRIPT, "reader_notes")
POLICY_MODULE = load_module(POLICY, "workflow_policy")
RENDER_MODULE = load_module(RENDER, "render_output")


def annotation(identifier, target, bodies, created="2026-11-24T10:00:00Z"):
    return {"@context": "http://www.w3.org/ns/anno.jsonld", "type": "Annotation",
            "id": identifier, "created": created, "motivation": "highlighting",
            "body": bodies, "target": target}


def quote_target(unit, exact, prefix="", suffix="", start=0):
    return {"source": unit, "layer": "zh", "selector": [
        {"type": "TextQuoteSelector", "exact": exact, "prefix": prefix, "suffix": suffix},
        {"type": "TextPositionSelector", "start": start, "end": start + len(exact)}]}


def comment(value):
    return {"type": "TextualBody", "purpose": "commenting", "value": value}


def tag(value):
    return {"type": "TextualBody", "purpose": "tagging", "value": value}


class ReaderNotesTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name)
        self.bibliography = self.root / "Private/Bibliography"
        self.extract = self.bibliography / "Extract" / STEM
        self.reader = self.bibliography / "Reader" / STEM
        self.project = self.root / "Private/Projects" / TOPIC
        for path in (self.extract, self.reader, self.project):
            path.mkdir(parents=True)
        (self.bibliography / "INDEX.md").write_text(
            "# Bibliography Index\n\n## Reference Inventory\n\n"
            "| KEY | Author | Title | PDF | Hash | Level | Keywords | Projects |\n"
            "|-----|--------|-------|-----|------|-------|----------|----------|\n"
            f"| {KEY} | Author, Ann | \"Title\" (2019) | PDF/{STEM}.pdf | ABC | Level 1 | anger | {TOPIC} |\n",
            encoding="utf-8")
        self.write_blocks()
        self.write_translations()
        self.write_notes(self.default_notes())
        self.write_refs(
            "# 文献清单 — demo-project\n\n"
            "| KEY | 角色 | 状态 | 备注 |\n"
            "|-----|------|------|------|\n"
            "| OTHER-KEY | background | candidate | 既有一行 |\n"
            f"| {KEY} | background | candidate | 书目已有 |\n\n"
            "## 待验证引用（手稿中已出现、尚未入库）\n\n（暂无）\n")

    def write_blocks(self):
        records = [
            {"unit_id": "U1", "locator": {"kind": "page", "value": "100"},
             "text_span": "First unit about anger.", "unit_sha256": "u1",
             "layout": {"kind": "body"}},
            {"unit_id": "U2", "locator": {"kind": "page", "value": "101"},
             "text_span": "Second unit about value.", "unit_sha256": "u2",
             "layout": {"kind": "body"}},
        ]
        lines = [json.dumps(record, ensure_ascii=False) for record in records]
        (self.extract / "blocks.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_translations(self):
        records = [
            {"unit_id": "U1", "unit_sha256": "u1",
             "zh": "⟦p100⟧第一段：愤怒是否适切？这是问题。"},
            {"unit_id": "U2", "unit_sha256": "u2",
             "zh": "⟦p101⟧第二段：愤怒有其价值。⟦p102⟧换页之后的内容。"},
        ]
        lines = [json.dumps(record, ensure_ascii=False) for record in records]
        (self.reader / "translation-part1.jsonl").write_text(
            "\n".join(lines) + "\n", encoding="utf-8")

    def default_notes(self):
        return {"@context": "http://www.w3.org/ns/anno.jsonld",
                "type": "AnnotationCollection", "source": KEY, "items": [
                    annotation("urn:uuid:n1", quote_target("U2", "愤怒有其价值", "："),
                               [tag("idea"), comment("愤怒的适切性是否取决于政治语境？")]),
                    annotation("urn:uuid:n2", quote_target("U2", "换页之后的内容", "。"),
                               [tag("cite"), comment("这句要引")]),
                    annotation("urn:uuid:n3", quote_target("U1", "愤怒是否适切"),
                               [comment("这里的问号和反问有什么区别？")]),
                    annotation("urn:uuid:n4", quote_target("U1", "第一段"), []),
                    annotation("urn:uuid:n5", {"source": "U2", "layer": "zh"},
                               [comment("整段的结构是什么？")]),
                ]}

    def write_notes(self, value):
        (self.reader / "user-notes.json").write_text(
            json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def write_refs(self, text):
        (self.project / "refs.md").write_text(text, encoding="utf-8")

    def refs(self):
        return (self.project / "refs.md").read_text(encoding="utf-8")

    def run_main(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = NOTES.main([*arguments, "--root", str(self.root)])
        return code, stdout.getvalue(), stderr.getvalue()

    def run_json(self, *arguments):
        code, output, error = self.run_main(*arguments, "--json")
        return code, json.loads(output), error

    def test_summary_kinds_pages_and_questions_first(self):
        code, data, error = self.run_json("summary", STEM)
        self.assertEqual(code, 0, error)
        notes = data["sources"][0]["notes"]
        self.assertEqual([note["id"] for note in notes],
                         ["urn:uuid:n3", "urn:uuid:n5", "urn:uuid:n1",
                          "urn:uuid:n4", "urn:uuid:n2"])
        by_id = {note["id"]: note for note in notes}
        self.assertEqual(by_id["urn:uuid:n1"]["kind"], "idea")
        self.assertEqual(by_id["urn:uuid:n1"]["page"], "101")
        self.assertEqual(by_id["urn:uuid:n2"]["page"], "102")
        self.assertEqual(by_id["urn:uuid:n2"]["quote"], "换页之后的内容")
        self.assertEqual(by_id["urn:uuid:n3"]["kind"], "comment")
        self.assertTrue(by_id["urn:uuid:n3"]["question"])
        self.assertEqual(by_id["urn:uuid:n4"]["kind"], "highlight")
        self.assertEqual(by_id["urn:uuid:n5"]["kind"], "paragraph-comment")
        self.assertEqual(by_id["urn:uuid:n5"]["page"], "101")

    def test_start_page_of_a_range(self):
        self.assertEqual(NOTES.start_page("126-127"), "126")
        self.assertEqual(NOTES.start_page("126–127"), "126")
        self.assertEqual(NOTES.start_page("xlix"), "xlix")
        self.assertEqual(NOTES.start_page(""), "")

    def test_summary_text_and_project_listing(self):
        code, output, error = self.run_main("summary", "--project", TOPIC)
        self.assertEqual(code, 0, error)
        self.assertIn(KEY, output)
        self.assertIn("问  p. 100", output)
        self.assertIn("想法", output)
        self.assertNotIn("OTHER-KEY", output)
        code, output, error = self.run_main("summary", "Missing_2020_Stem")
        self.assertEqual(code, 2)
        self.assertIn("没有阅读页批注", error)

    def test_dry_run_writes_nothing(self):
        before = self.refs()
        code, output, error = self.run_main(
            "route", STEM, "--project", TOPIC, "--dry-run")
        self.assertEqual(code, 0, error)
        self.assertIn("statement: 愤怒的适切性是否取决于政治语境？", output)
        self.assertIn("换页之后的内容", output)
        self.assertIn("--dry-run", output)
        self.assertEqual(self.refs(), before)
        self.assertFalse((self.reader / "notes-routed.json").exists())
        self.assertFalse((self.project / f"{TOPIC}-idea-ledger.json").exists())

    def test_route_idea_and_cite_then_idempotent(self):
        code, output, error = self.run_main("route", STEM, "--project", TOPIC)
        self.assertEqual(code, 0, error)
        ledger = json.loads((self.project / f"{TOPIC}-idea-ledger.json")
                            .read_text(encoding="utf-8"))
        self.assertEqual(len(ledger["ideas"]), 1)
        idea = ledger["ideas"][0]
        self.assertEqual(idea["statement"], "愤怒的适切性是否取决于政治语境？")
        self.assertEqual(idea["provenance"], "user")
        self.assertEqual(idea["status"], "parked")
        self.assertEqual(idea["related_bib_keys"], [KEY])

        validation = subprocess.run(
            [sys.executable, str(IDEA_LEDGER), "--project-dir", str(self.project), "validate"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

        refs = self.refs()
        self.assertEqual(refs.count(f"| {KEY} | background | candidate | 来自阅读页批注 |"), 0)
        self.assertIn(f"| {KEY} | background | candidate | 书目已有 |", refs)
        self.assertEqual(refs.count("## 阅读页引用候选"), 1)
        self.assertIn("p. 102", refs)
        self.assertIn("unit `U2`", refs)
        self.assertIn("<!-- note:urn:uuid:n2 -->", refs)
        self.assertIn("这句要引", refs)
        self.assertIn("| OTHER-KEY | background | candidate | 既有一行 |", refs)
        self.assertEqual(POLICY_MODULE.refs_status(self.project / "refs.md", KEY),
                         "registered")

        routed = json.loads((self.reader / "notes-routed.json").read_text(encoding="utf-8"))
        self.assertEqual(routed["urn:uuid:n1"]["to"], "idea-ledger")
        self.assertEqual(routed["urn:uuid:n1"]["project"], TOPIC)
        self.assertEqual(routed["urn:uuid:n2"]["to"], "refs")
        self.assertIn("ledger_id", routed["urn:uuid:n1"])

        snapshot = {"refs": refs,
                    "ledger": (self.project / f"{TOPIC}-idea-ledger.json").read_text(encoding="utf-8"),
                    "routed": (self.reader / "notes-routed.json").read_text(encoding="utf-8")}
        code, output, error = self.run_main("route", STEM, "--project", TOPIC)
        self.assertEqual(code, 0, error)
        self.assertIn("没有待归档", output)
        self.assertEqual(self.refs(), snapshot["refs"])
        self.assertEqual((self.project / f"{TOPIC}-idea-ledger.json").read_text(encoding="utf-8"),
                         snapshot["ledger"])
        self.assertEqual((self.reader / "notes-routed.json").read_text(encoding="utf-8"),
                         snapshot["routed"])

        code, data, error = self.run_json("summary", STEM, "--new")
        self.assertEqual(code, 0, error)
        remaining = {note["id"] for note in data["sources"][0]["notes"]}
        self.assertNotIn("urn:uuid:n1", remaining)
        self.assertNotIn("urn:uuid:n2", remaining)
        self.assertIn("urn:uuid:n3", remaining)

    def test_route_only_and_ids(self):
        code, output, error = self.run_main(
            "route", STEM, "--project", TOPIC, "--only", "cite")
        self.assertEqual(code, 0, error)
        self.assertEqual(self.refs().count("## 阅读页引用候选"), 1)
        self.assertFalse((self.project / f"{TOPIC}-idea-ledger.json").exists())
        routed = json.loads((self.reader / "notes-routed.json").read_text(encoding="utf-8"))
        self.assertEqual(set(routed), {"urn:uuid:n2"})
        code, output, error = self.run_main(
            "route", STEM, "--project", TOPIC, "--ids", "urn:uuid:nope")
        self.assertEqual(code, 2)
        self.assertIn("找不到批注", error)

    def test_existing_row_is_not_duplicated_and_refs_status_works(self):
        self.write_refs(
            "# 文献清单 — demo-project\n\n"
            "| KEY | 角色 | 状态 | 备注 |\n"
            "|-----|------|------|------|\n"
            f"| {KEY} | core-target | cited | 已引用 |\n")
        code, output, error = self.run_main("route", STEM, "--project", TOPIC)
        self.assertEqual(code, 0, error)
        self.assertEqual(self.refs().count(f"| {KEY} | core-target | cited | 已引用 |"), 1)
        self.assertEqual(self.refs().count(f"| {KEY} | background | candidate | 来自阅读页批注 |"), 0)
        self.assertEqual(
            POLICY_MODULE.refs_status(self.project / "refs.md", KEY), "registered")

    def test_cite_adds_row_only_when_missing(self):
        self.write_refs(
            "# 文献清单 — demo-project\n\n"
            "| KEY | 角色 | 状态 | 备注 |\n"
            "|-----|------|------|------|\n"
            "| OTHER-KEY | background | candidate | 既有一行 |\n\n"
            "## 待验证引用（手稿中已出现、尚未入库）\n\n（暂无）\n")
        code, output, error = self.run_main(
            "route", STEM, "--project", TOPIC, "--only", "cite")
        self.assertEqual(code, 0, error)
        refs = self.refs()
        self.assertEqual(refs.count(f"| {KEY} | background | candidate | 来自阅读页批注 |"), 1)
        self.assertEqual(refs.count("## 阅读页引用候选"), 1)
        self.assertLess(refs.index(f"| {KEY} | background | candidate |"),
                        refs.index("## 待验证引用"))
        self.assertEqual(POLICY_MODULE.refs_status(self.project / "refs.md", KEY),
                         "registered")
        self.assertIn(KEY, RENDER_MODULE.load_refs_keys(self.project / "refs.md"))

    def test_missing_project_fails_cleanly(self):
        code, output, error = self.run_main("summary", "--project", "no-such-project")
        self.assertEqual(code, 2)
        self.assertIn("项目目录不存在", error)
        code, output, error = self.run_main(
            "route", STEM, "--project", "no-such-project")
        self.assertEqual(code, 2)
        self.assertIn("项目目录不存在", error)


if __name__ == "__main__":
    unittest.main()
