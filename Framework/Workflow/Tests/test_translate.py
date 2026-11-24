"""Tests for translate.py: selection, cache, QA, repair, and secret safety."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "Scripts" / "translate.py"
STEM = "Author_2020_Title"


def load_module():
    spec = importlib.util.spec_from_file_location("translate_tested", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TRANSLATE = load_module()


def block(unit_id, text, page="10", kind="body", breaks=None):
    return {
        "unit_id": unit_id,
        "text_span": text,
        "unit_sha256": TRANSLATE.sha256_text(text),
        "locator": {"kind": "page", "value": page},
        "layout": {"kind": kind, "page_breaks": breaks or []},
    }


class FakeAPI:
    """Stand-in for translate.call_model; returns scripted responses."""

    def __init__(self, responses=()):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, system, messages, model, max_tokens):
        self.calls.append({"system": system, "messages": messages,
                           "model": model, "max_tokens": max_tokens})
        text = self.responses.pop(0) if self.responses else "译文。"
        return {"text": text, "stop_reason": "end_turn",
                "usage": {"input_tokens": 10, "output_tokens": 5,
                          "cache_read_input_tokens": 2}}


class TranslateTestCase(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name)
        template = self.root / TRANSLATE.TEMPLATE_REL
        template.parent.mkdir(parents=True)
        template.write_text("Translate faithfully.\n", encoding="utf-8")
        (self.root / "Framework/Workflow/manifest.json").write_text("{}", encoding="utf-8")
        self.blocks_dir = self.root / TRANSLATE.EXTRACT_REL / STEM
        self.blocks_dir.mkdir(parents=True)
        self.reader_dir = self.root / TRANSLATE.READER_REL / STEM
        self.reader_dir.mkdir(parents=True)
        self._original_call = TRANSLATE.call_model
        self.addCleanup(self._restore_call)

    def _restore_call(self):
        TRANSLATE.call_model = self._original_call

    def fake(self, responses=()):
        api = FakeAPI(responses)
        TRANSLATE.call_model = api
        return api

    def write_blocks(self, blocks):
        path = self.blocks_dir / "blocks.jsonl"
        path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n"
                                for item in blocks), encoding="utf-8")

    def write_cache(self, records, directory=None, name="translation.jsonl"):
        directory = directory or self.reader_dir
        directory.mkdir(parents=True, exist_ok=True)
        (directory / name).write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records),
            encoding="utf-8")

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = TRANSLATE.main(argv)
        return code, out.getvalue(), err.getvalue()


class SelectionTests(TranslateTestCase):
    def test_pages_use_locator_and_page_breaks(self):
        blocks = [
            block("u1", "one", page="10"),
            block("u2", "two", page="11", breaks=[{"offset": 0, "page_label": "12"}]),
            block("u3", "three", page="13-14"),
            block("u4", "four", page="15"),
        ]
        selected = TRANSLATE.select_units(blocks, pages=("11", "13"))
        self.assertEqual([item["unit_id"] for item in selected], ["u2", "u3"])

    def test_non_numeric_labels_compare_by_document_order(self):
        blocks = [
            block("u1", "a", page="front"),
            block("u2", "b", page="middle"),
            block("u3", "c", page="back"),
        ]
        selected = TRANSLATE.select_units(blocks, pages=("middle", "back"))
        self.assertEqual([item["unit_id"] for item in selected], ["u2", "u3"])

    def test_skip_other_and_references(self):
        blocks = [
            block("u1", "body", page="10"),
            block("u2", "table", page="10", kind="other"),
            block("u3", "REFERENCES", page="11"),
            block("u4", "after", page="11"),
        ]
        selected = TRANSLATE.select_units(blocks, pages=("10", "11"))
        self.assertEqual([item["unit_id"] for item in selected], ["u1"])
        selected = TRANSLATE.select_units(blocks, pages=("10", "11"),
                                          include_references=True)
        self.assertEqual([item["unit_id"] for item in selected], ["u1", "u3", "u4"])

    def test_from_to_is_inclusive(self):
        blocks = [block(f"u{index}", "x", page=str(index)) for index in range(4)]
        selected = TRANSLATE.select_units(blocks, from_id="u1", to_id="u2")
        self.assertEqual([item["unit_id"] for item in selected], ["u1", "u2"])

    def test_missing_selection_errors(self):
        with self.assertRaises(TRANSLATE.SelectionError):
            TRANSLATE.select_units([block("u1", "x")])


class CacheAndVerbatimTests(TranslateTestCase):
    def test_cached_unit_makes_no_api_call(self):
        item = block("u1", "Be angry, but sin not.", page="10")
        self.write_blocks([item])
        self.write_cache([{"unit_id": "u1", "unit_sha256": item["unit_sha256"],
                           "zh": "可以生气，但不要犯罪。"}])
        api = self.fake()
        code, out, _ = self.run_main(["run", STEM, "--root", str(self.root), "--all"])
        self.assertEqual(code, 0)
        self.assertEqual(api.calls, [])
        self.assertIn("cached: 1", out)

    def test_changed_hash_is_not_cached(self):
        item = block("u1", "Be angry.", page="10")
        self.write_blocks([item])
        self.write_cache([{"unit_id": "u1", "unit_sha256": "stale", "zh": "旧"}])
        api = self.fake(["可以生气。"])
        code, out, _ = self.run_main(["run", STEM, "--root", str(self.root), "--all",
                                      "--no-terms"])
        self.assertEqual(code, 0)
        self.assertEqual(len(api.calls), 1)
        self.assertIn("translated: 1", out)

    def test_verbatim_numeral_copies_without_api_call(self):
        item = block("u1", "II.", page="10")
        self.write_blocks([item])
        api = self.fake()
        code, out, _ = self.run_main(["run", STEM, "--root", str(self.root), "--all"])
        self.assertEqual(code, 0)
        self.assertEqual(api.calls, [])
        records = TRANSLATE.read_jsonl(self.reader_dir / "translation.jsonl")
        self.assertEqual(records[0]["zh"], "II.")
        self.assertEqual(records[0]["model"], TRANSLATE.DEFAULT_MODEL)

    def test_refuses_more_than_sixty_units_without_yes(self):
        blocks = [block(f"u{index}", f"unit {index} text", page="10")
                  for index in range(61)]
        self.write_blocks(blocks)
        api = self.fake()
        code, _, err = self.run_main(["run", STEM, "--root", str(self.root), "--all"])
        self.assertEqual(code, 2)
        self.assertIn("refusing", err)
        self.assertEqual(api.calls, [])

    def test_run_proposes_terms_when_glossary_is_missing(self):
        item = block("u1", "This sentence needs a translation.", page="10")
        self.write_blocks([item])
        proposal = json.dumps([{"en": "gadget", "zh": "小装置", "note": ""}])
        api = self.fake([proposal, "这句话需要翻译。"])
        code, out, _ = self.run_main(["run", STEM, "--root", str(self.root), "--all"])
        self.assertEqual(code, 0)
        self.assertEqual(len(api.calls), 2)
        self.assertIn("JSON 数组", api.calls[0]["messages"][0]["content"])
        glossary = (self.reader_dir / "glossary.md").read_text(encoding="utf-8")
        self.assertIn("| gadget | 小装置 | 自动提议，待确认 |", glossary)
        self.assertIn("translated: 1", out)


class GlossaryTests(TranslateTestCase):
    def write_glossary(self, path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        body = "| English | 中文 | 备注 |\n| --- | --- | --- |\n"
        body += "".join(f"| {en} | {zh} | |\n" for en, zh in rows)
        path.write_text(body, encoding="utf-8")

    def test_reader_beats_project_and_variants_merge(self):
        self.write_glossary(self.reader_dir / "glossary.md",
                            [("apt / fitting", "合适的")])
        self.write_glossary(self.root / TRANSLATE.PROJECTS_REL / "topic" / "glossary.md",
                            [("apt", "贴切的"), ("anger", "愤怒")])
        entries, conflicts = TRANSLATE.load_glossary(
            self.root, STEM, "topic", self.reader_dir)
        by_term = {entry["en"]: entry["zh"] for entry in entries}
        self.assertEqual(by_term["apt"], "合适的")
        self.assertEqual(by_term["fitting"], "合适的")
        self.assertEqual(by_term["anger"], "愤怒")
        self.assertTrue(any(conflict["en"] == "apt" for conflict in conflicts))

    def test_shared_glossary_is_supported(self):
        self.write_glossary(self.root / TRANSLATE.SHARED_GLOSSARY_REL / "general.md",
                            [("reason", "理由")])
        entries, _ = TRANSLATE.load_glossary(self.root, STEM, None, self.reader_dir)
        self.assertEqual(entries[0]["zh"], "理由")

    def test_first_occurrence_is_document_order(self):
        entries = [{"en": "aptness", "zh": "合适性"},
                   {"en": "apt", "zh": "合适的"}]
        blocks = [block("u1", "Aptness first.", page="10"),
                  block("u2", "Aptness again; apt now.", page="11")]
        first = TRANSLATE.first_occurrence_map(blocks, entries)
        self.assertEqual(first["aptness"], 0)
        self.assertEqual(first["apt"], 1)

    def test_matching_is_case_insensitive_and_word_bounded(self):
        entries = [{"en": "anger", "zh": "愤怒"}]
        self.assertEqual(len(TRANSLATE.term_occurrences("Anger here.", entries)), 1)
        self.assertEqual(len(TRANSLATE.term_occurrences("angry men.", entries)), 0)

    def test_avoid_variants_are_parsed_from_note(self):
        path = self.root / "glossary.md"
        path.write_text(
            "| English | 中文 | 备注 |\n| --- | --- | --- |\n"
            "| anger | 愤怒 | noun only; 避免：怒气、火气 |\n"
            "| apt | 合适的 | 避免: 恰当,贴切 |\n"
            "| fitting | 合适的 | avoid nothing here |\n",
            encoding="utf-8")
        entries = {entry["en"]: entry for entry in TRANSLATE.parse_glossary_file(path)}
        self.assertEqual(entries["anger"]["avoid"], ["怒气", "火气"])
        self.assertEqual(entries["apt"]["avoid"], ["恰当", "贴切"])
        self.assertEqual(entries["fitting"]["avoid"], [])

    def test_avoid_survives_load_glossary(self):
        self.write_glossary_note(self.root / TRANSLATE.PROJECTS_REL / "topic" / "glossary.md",
                                 [("anger", "愤怒", "避免：怒气")])
        entries, _ = TRANSLATE.load_glossary(self.root, STEM, "topic", self.reader_dir)
        self.assertEqual(entries[0]["avoid"], ["怒气"])

    def test_glossary_digest_ignores_the_avoid_field(self):
        plain = [{"en": "anger", "zh": "愤怒", "note": ""}]
        with_avoid = [{"en": "anger", "zh": "愤怒", "note": "", "avoid": ["怒气"]}]
        self.assertEqual(TRANSLATE.glossary_digest(with_avoid),
                         TRANSLATE.glossary_digest(plain))

    def write_glossary_note(self, path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        body = "| English | 中文 | 备注 |\n| --- | --- | --- |\n"
        body += "".join(f"| {en} | {zh} | {note} |\n" for en, zh, note in rows)
        path.write_text(body, encoding="utf-8")


class QATests(TranslateTestCase):
    def flags(self, source, zh, entries=None, kind="body", breaks=None):
        item = block("u1", source, kind=kind, breaks=breaks)
        return [flag["code"] for flag in TRANSLATE.qa_unit(item, zh, entries or [])]

    def test_page_markers(self):
        codes = self.flags("one two three four",
                           "一二三",
                           breaks=[{"offset": 3, "page_label": "10"}])
        self.assertIn("page-markers", codes)

    def test_glossary(self):
        codes = self.flags("anger is wrong", "怒气是错的",
                           [{"en": "anger", "zh": "愤怒"}])
        self.assertIn("glossary", codes)

    def test_glossary_avoid_warns_only_when_source_has_term(self):
        entries = [{"en": "anger", "zh": "愤怒", "avoid": ["怒气"]}]
        item = block("u1", "anger is wrong", page="10")
        flags = TRANSLATE.qa_unit(item, "怒气是错的", entries)
        avoid = [flag for flag in flags if flag["code"] == "glossary-avoid"]
        self.assertEqual(len(avoid), 1)
        self.assertEqual(avoid[0]["level"], "warning")
        self.assertIn("怒气", avoid[0]["detail"])
        # The source must contain the term for the avoid warning to fire.
        codes = self.flags("sadness is wrong", "怒气是错的", entries)
        self.assertNotIn("glossary-avoid", codes)
        # The fixed rendering is not an avoided variant.
        codes = self.flags("anger is wrong", "愤怒是错的", entries)
        self.assertNotIn("glossary-avoid", codes)

    def test_note_markers(self):
        codes = self.flags("as the crow flies’2 and anger.4", "像乌鸦直线飞行。")
        self.assertIn("note-markers", codes)

    def test_numbers(self):
        codes = self.flags("In 1965 the debate happened.", "辩论发生了。")
        self.assertIn("numbers", codes)

    def test_latin_residue(self):
        codes = self.flags("something here", "这是 the residual English phrase here")
        self.assertIn("latin-residue", codes)

    def test_negation(self):
        codes = self.flags("It is not never nothing.", "它是。")
        self.assertIn("negation", codes)

    def test_added_hedge(self):
        codes = self.flags("Anger is wrong.", "愤怒可能是错的。")
        self.assertIn("added-hedge", codes)

    def test_only(self):
        codes = self.flags("She is only angry.", "她愤怒。")
        self.assertIn("only", codes)

    def test_length(self):
        codes = self.flags("This sentence is deliberately long enough to matter.",
                           "短。")
        self.assertIn("length", codes)

    def test_clean_translation_has_no_flags(self):
        codes = self.flags("Be angry, but sin not.", "可以生气，但不要犯罪。")
        self.assertEqual(codes, [])

    def test_ligature_matches_glossary_term(self):
        entries = [{"en": "justification", "zh": "正当化"}]
        self.assertEqual(len(TRANSLATE.term_occurrences("justiﬁcation", entries)), 1)
        blocks = [block("u1", "A justiﬁcation here.", page="10")]
        first = TRANSLATE.first_occurrence_map(blocks, entries)
        self.assertEqual(first["justification"], 0)
        item = block("u2", "This justiﬁcation is fine.", page="10")
        flags = TRANSLATE.qa_unit(item, "这一正当化没问题。", entries)
        self.assertNotIn("glossary", [flag["code"] for flag in flags])

    def test_footnote_number_normalisation(self):
        item = block("u1", "18Tessman says this.", kind="footnote", page="10")
        self.assertEqual(
            TRANSLATE.normalize_footnote_numbers("[18]泰斯曼这样说。", item,
                                                 item["text_span"]),
            "18 泰斯曼这样说。")
        item = block("u1", "18First note. 19Second note.", kind="footnote", page="10")
        self.assertEqual(
            TRANSLATE.normalize_footnote_numbers("18 第一条。 [19]第二条。", item,
                                                 item["text_span"]),
            "18 第一条。19 第二条。")
        self.assertEqual(
            TRANSLATE.normalize_footnote_numbers("18 第一条。[20]保留。", item,
                                                 item["text_span"]),
            "18 第一条。[20]保留。")

    def test_footnote_plain_numbers_pass_note_markers_qa(self):
        item = block("u1", "2A phrase. 3While the Greeks disagreed.",
                     kind="footnote", page="10")
        codes = [flag["code"] for flag in
                 TRANSLATE.qa_unit(item, "2 这是巴克利的说法。3 古希腊人意见不一。", [])]
        self.assertNotIn("note-markers", codes)

    def test_body_notes_keep_brackets(self):
        item = block("u1", "virtue,3 the Stoics argued.", page="10")
        self.assertEqual(
            TRANSLATE.normalize_footnote_numbers("美德[3]，斯多亚派主张。", item,
                                                 item["text_span"]),
            "美德[3]，斯多亚派主张。")


class PromptTests(TranslateTestCase):
    def test_translation_label_is_not_marked_do_not_translate(self):
        item = block("u1", "Be angry.", page="10")
        messages = TRANSLATE.build_messages(
            item, 0, [item], {}, [], {}, "")
        content = messages[0]["content"]
        self.assertIn("待译原文：", content)
        self.assertNotIn("[不要翻译] 待译原文", content)

    def test_glossary_header_only_parenthesises_marked_terms(self):
        entries = [{"en": "aptness", "zh": "合适性", "note": ""}]
        rendered = TRANSLATE.render_glossary_block(entries)
        self.assertIn("只有本单元标记（首次出现）的条目", rendered)
        self.assertIn("其余条目一律不加英文括注", rendered)

    def test_system_prompt_requires_marked_first_occurrences(self):
        template = Path(__file__).resolve().parents[1] / "Templates/Translate/system.md"
        text = template.read_text(encoding="utf-8")
        self.assertIn("only", text)
        self.assertIn("（首次出现）", text)


class RepairTests(TranslateTestCase):
    def test_error_flags_trigger_one_repair_call(self):
        item = block("u1", "one two three four", page="10",
                     breaks=[{"offset": 3, "page_label": "10"}])
        self.write_blocks([item])
        api = self.fake(["一二三", "一⟦p10⟧二三"])
        code, out, _ = self.run_main(["run", STEM, "--root", str(self.root), "--all",
                                      "--no-terms"])
        self.assertEqual(code, 0)
        self.assertEqual(len(api.calls), 2)
        repair_messages = api.calls[1]["messages"]
        self.assertEqual(repair_messages[-2]["role"], "assistant")
        self.assertIn("译文有以下问题", repair_messages[-1]["content"])
        self.assertIn("只输出修正后的译文", repair_messages[-1]["content"])
        records = TRANSLATE.read_jsonl(self.reader_dir / "translation.jsonl")
        self.assertEqual(records[0]["zh"], "一⟦p10⟧二三")
        self.assertFalse([flag for flag in records[0]["qa"]
                          if flag["level"] == "error"])


class CompactionTests(TranslateTestCase):
    def test_compaction_keeps_last_and_document_order(self):
        first = block("u1", "one", page="10")
        second = block("u2", "two", page="11")
        path = self.reader_dir / "translation.jsonl"
        records = [
            {"unit_id": "u2", "unit_sha256": second["unit_sha256"], "zh": "旧二"},
            {"unit_id": "u1", "unit_sha256": first["unit_sha256"], "zh": "旧一"},
            {"unit_id": "u1", "unit_sha256": first["unit_sha256"], "zh": "新一"},
        ]
        path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n"
                                for item in records), encoding="utf-8")
        count = TRANSLATE.compact_translation(path, [first, second])
        self.assertEqual(count, 2)
        result = TRANSLATE.read_jsonl(path)
        self.assertEqual([item["unit_id"] for item in result], ["u1", "u2"])
        self.assertEqual(result[0]["zh"], "新一")


class SecretSafetyTests(TranslateTestCase):
    TOKEN = "sk-test-secret-1234567890"

    def setUp(self):
        super().setUp()
        self._saved = {key: os.environ.get(key) for key in
                       ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN")}
        self.addCleanup(self._restore_env)
        os.environ["ANTHROPIC_BASE_URL"] = "https://example.invalid/v1"
        os.environ["ANTHROPIC_AUTH_TOKEN"] = self.TOKEN

    def _restore_env(self):
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_gateway_error_redacts_token(self):
        original = TRANSLATE.urllib.request.urlopen

        def boom(request, timeout=None):
            raise urllib.error.HTTPError(
                "https://example.invalid", 400, "bad", {},
                io.BytesIO(f"bad token {self.TOKEN}".encode("utf-8")))

        TRANSLATE.urllib.request.urlopen = boom
        self.addCleanup(setattr, TRANSLATE.urllib.request, "urlopen", original)
        with self.assertRaises(TRANSLATE.GatewayError) as caught:
            TRANSLATE.call_model([], [{"role": "user", "content": "x"}], "m", 100)
        self.assertNotIn(self.TOKEN, str(caught.exception))

    def test_token_never_reaches_output_or_files(self):
        item = block("u1", "Be angry.", page="10")
        self.write_blocks([item])
        self.fake(["可以生气。"])
        out_dir = self.root / "out"
        code, out, err = self.run_main(
            ["run", STEM, "--root", str(self.root), "--all", "--no-terms",
             "--out", str(out_dir)])
        self.assertEqual(code, 0)
        self.assertNotIn(self.TOKEN, out)
        self.assertNotIn(self.TOKEN, err)
        for path in self.root.rglob("*"):
            if path.is_file():
                self.assertNotIn(self.TOKEN,
                                 path.read_text(encoding="utf-8", errors="replace"))


if __name__ == "__main__":
    unittest.main()
