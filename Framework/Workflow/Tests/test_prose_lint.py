from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = WORKFLOW_ROOT / "Scripts"
SCRIPT = SCRIPTS / "prose-lint.py"


def load_script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


LINT = load_script("prose-lint.py")


def run_cli(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
    )


class CheckTests(unittest.TestCase):
    def count(self, check_id: str, text: str, **kwargs) -> int:
        return LINT.analyze(text, **kwargs)["checks"][check_id]["count"]

    def assert_flag(self, check_id: str, positive: str, negative: str, **kwargs) -> None:
        self.assertEqual(self.count(check_id, positive, **kwargs), 1, positive)
        self.assertEqual(self.count(check_id, negative, **kwargs), 0, negative)

    def test_long_sentence(self):
        self.assert_flag("long-sentence", "我们" * 40 + "。", "我们今天研究这个问题。")

    def test_de_chain(self):
        self.assert_flag("de-chain", "这是他的老师的学生的书。", "这是我们一起买来的书。")

    def test_light_verb(self):
        self.assert_flag("light-verb", "我们对这个问题进行了研究。", "我们今天讨论这个问题。")

    def test_zuowei_zhiyi(self):
        self.assert_flag("zuowei-zhiyi", "作为方法之一，它很重要。", "他是这个团队的成员之一。")

    def test_youyu_shide(self):
        self.assert_flag("youyu-shide", "由于时间紧迫，使得任务被推迟。", "由于天气原因，活动取消了。")

    def test_not_but(self):
        self.assert_flag("not-but", "这并不是终点，而是新的起点。", "这只是一个终点，同时也是起点。")

    def test_dash_insert(self):
        self.assert_flag("dash-insert", "他来了——或者说——他又走了。", "他很快就来了——然后又走了。")

    def test_long_paren(self):
        self.assert_flag(
            "long-paren",
            "这段话（这是一个非常长的括注内容用来测试长括注的检测效果）结束了。",
            "这段话（简短括注）结束了。",
        )

    def test_key_placeholder(self):
        self.assert_flag(
            "key-placeholder",
            "我们在本文中参见〔KEY1234567890〕一书的讨论。",
            "我们在本文中参见〔SHORT〕一书的讨论。",
        )

    def test_meta_phrase(self):
        self.assert_flag("meta-phrase", "值得注意的是，这个结论并不稳固。", "这个结论确实并不稳固。")

    def test_hedge_stack(self):
        self.assert_flag("hedge-stack", "这个结论或许是错的，也可能是对的。", "这个结论或许确实是错的。")

    def test_long_paragraph(self):
        self.assert_flag(
            "long-paragraph",
            "我们今天认真研究了这个问题。",
            "我们今天研究这个问题。",
            max_paragraph=12,
        )

    def test_bare_run(self):
        text = "天空很蓝很蓝的样子。草地很绿很绿的样子。湖水很静很静的样子。山峰很高很高的样子。"
        result = LINT.analyze(text)
        self.assertEqual(result["checks"]["bare-run"]["count"], 1)
        self.assertEqual(result["metrics"]["bare_run_pct"], 100.0)

    def test_bare_run_with_links(self):
        text = "天空很蓝很蓝的样子。因此草地很绿很绿的样子。湖水很静很静的样子。因此山峰很高很高的样子。"
        self.assertEqual(self.count("bare-run", text), 0)

    def test_signpost(self):
        text = "上一节说明了这一点。下一节将讨论另一个问题。"
        self.assertEqual(self.count("signpost", text), 2)

    def test_disclaimer(self):
        text = "这并不是说原则无用。它不等于全体同意。"
        result = LINT.analyze(text)
        self.assertEqual(result["checks"]["disclaimer"]["count"], 2)
        self.assertGreater(result["metrics"]["disclaimer_density"], 0)


class MetricsTests(unittest.TestCase):
    def test_known_text_metrics(self):
        metrics = LINT.analyze("我们因此研究了这个问题的重要方面。这个问题显然很重要。")["metrics"]
        self.assertEqual(metrics["chars"], 25)
        self.assertEqual(metrics["paragraphs"], 1)
        self.assertEqual(metrics["sentences"], 2)
        self.assertEqual(metrics["sentence_mean"], 12.5)
        self.assertEqual(metrics["over_limit_pct"], 0.0)
        self.assertEqual(metrics["longest_sentence"], 16)
        self.assertEqual(metrics["connective_density"], 80.0)
        self.assertEqual(metrics["de_density"], 40.0)

    def test_empty_text_is_all_zero(self):
        metrics = LINT.analyze("")["metrics"]
        self.assertEqual(metrics["chars"], 0)
        self.assertEqual(metrics["paragraphs"], 0)
        self.assertEqual(metrics["sentences"], 0)
        self.assertEqual(metrics["sentence_mean"], 0.0)
        self.assertEqual(metrics["over_limit_pct"], 0.0)
        self.assertEqual(metrics["longest_sentence"], 0)
        self.assertEqual(metrics["connective_density"], 0.0)
        self.assertEqual(metrics["de_density"], 0.0)

    def test_short_paragraphs_are_ignored(self):
        result = LINT.analyze("标题\n\n我们今天研究这个问题。")
        self.assertEqual(result["metrics"]["paragraphs"], 1)
        self.assertEqual(result["metrics"]["chars"], 10)


class CliTests(unittest.TestCase):
    def test_json_output_has_documented_shape(self):
        text = "我们" * 40 + "。这并不是终点，而是新的起点。"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.txt"
            path.write_bytes(text.encode("utf-8"))
            completed = run_cli(path, "--json")
            self.assertEqual(completed.returncode, 0)
            data = json.loads(completed.stdout)
            self.assertEqual(data["file"], str(path))
            self.assertEqual(
                set(data["metrics"]),
                {
                    "chars",
                    "paragraphs",
                    "sentences",
                    "sentence_mean",
                    "over_limit_pct",
                    "longest_sentence",
                    "connective_density",
                    "de_density",
                    "bare_run_pct",
                    "disclaimer_density",
                },
            )
            self.assertEqual(list(data["checks"]), [check_id for check_id, _ in LINT.CHECKS])
            for item in data["checks"].values():
                self.assertEqual(set(item), {"label", "count", "matches"})
                self.assertEqual(item["count"], len(item["matches"]))
                for match in item["matches"]:
                    self.assertEqual(set(match), {"paragraph", "excerpt"})
                    self.assertGreaterEqual(match["paragraph"], 1)
                    self.assertLessEqual(len(match["excerpt"]), 40)
            self.assertEqual(data["checks"]["long-sentence"]["count"], 1)
            self.assertEqual(data["checks"]["not-but"]["count"], 1)
            self.assertIn("长句", completed.stdout)

    def test_compare_reports_net_change(self):
        old_text = "我们今天研究这个问题。"
        new_text = "我们今天认真研究这个问题。"
        with tempfile.TemporaryDirectory() as temp:
            old = Path(temp) / "old.txt"
            new = Path(temp) / "new.txt"
            old.write_bytes(old_text.encode("utf-8"))
            new.write_bytes(new_text.encode("utf-8"))
            completed = run_cli(new, "--compare", old, "--json")
            self.assertEqual(completed.returncode, 0)
            compare = json.loads(completed.stdout)["compare"]
            self.assertEqual(
                list(compare),
                [
                    "old_chars",
                    "new_chars",
                    "net_change",
                    "old_sentence_mean",
                    "new_sentence_mean",
                    "old_over_limit_pct",
                    "new_over_limit_pct",
                ],
            )
            self.assertEqual(compare["old_chars"], 10)
            self.assertEqual(compare["new_chars"], 12)
            self.assertEqual(compare["net_change"], 2)
            self.assertEqual(compare["old_sentence_mean"], 10.0)
            self.assertEqual(compare["new_sentence_mean"], 12.0)

            text_completed = run_cli(new, "--compare", old)
            self.assertEqual(text_completed.returncode, 0)
            self.assertEqual(text_completed.stdout.count("对比:"), 1)

    def test_crlf_matches_lf(self):
        lf = "我们今天研究这个问题。\n\n这个结论确实并不稳固。"
        with tempfile.TemporaryDirectory() as temp:
            lf_path = Path(temp) / "lf.txt"
            crlf_path = Path(temp) / "crlf.txt"
            lf_path.write_bytes(lf.encode("utf-8"))
            crlf_path.write_bytes(lf.replace("\n", "\r\n").encode("utf-8"))
            lf_data = json.loads(run_cli(lf_path, "--json").stdout)
            crlf_data = json.loads(run_cli(crlf_path, "--json").stdout)
            lf_data.pop("file")
            crlf_data.pop("file")
            self.assertEqual(lf_data, crlf_data)

    def test_exit_codes_and_judgment_line(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.txt"
            path.write_bytes("这并不是终点，而是新的起点。".encode("utf-8"))
            completed = run_cli(path)
            self.assertEqual(completed.returncode, 0)
            self.assertIn("not-but", completed.stdout)
            self.assertTrue(completed.stdout.rstrip().endswith(LINT.JUDGMENT))

            missing = run_cli(Path(temp) / "missing.txt")
            self.assertEqual(missing.returncode, 2)
            self.assertTrue(missing.stderr.startswith("ERROR "))


class GlossaryTests(unittest.TestCase):
    GLOSSARY = (
        "| English | 中文 | 备注 |\n"
        "| --- | --- | --- |\n"
        "| aptness / fitting | 合适性 | 避免：恰当、贴切 |\n"
        "| anger | 愤怒 | 避免：怒气 |\n"
    )

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.glossary_path = Path(self._temp.name) / "glossary.md"
        self.glossary_path.write_text(self.GLOSSARY, encoding="utf-8")
        self.entries = LINT.load_glossary_entries([self.glossary_path])

    def count(self, check_id: str, text: str) -> int:
        return LINT.analyze(text, glossary=self.entries)["checks"][check_id]["count"]

    def test_correct_rendering_passes(self):
        self.assertEqual(self.count("glossary-gloss", "合适性（aptness）"), 0)
        self.assertEqual(self.count("glossary-gloss", "合适性(aptness)"), 0)

    def test_wrong_rendering_is_flagged_with_expected_term(self):
        result = LINT.analyze("恰当（aptness）", glossary=self.entries)
        item = result["checks"]["glossary-gloss"]
        self.assertEqual(item["count"], 1)
        excerpt = item["matches"][0]["excerpt"]
        self.assertIn("合适性", excerpt)
        self.assertIn("恰当", excerpt)

    def test_quoted_rendering_before_gloss_passes(self):
        self.assertEqual(self.count("glossary-gloss", "“合适性”（aptness）"), 0)
        self.assertEqual(self.count("glossary-gloss", "\"合适性\"（aptness）"), 0)

    def test_gloss_match_ignores_case_and_ligatures(self):
        self.assertEqual(self.count("glossary-gloss", "合适性（APTNESS）"), 0)
        self.assertEqual(self.count("glossary-gloss", "合适性（ﬁtting）"), 0)

    def test_avoid_variant_is_reported(self):
        result = LINT.analyze("他满怀怒气。", glossary=self.entries)
        item = result["checks"]["glossary-avoid"]
        self.assertEqual(item["count"], 1)
        self.assertIn("怒气", item["matches"][0]["excerpt"])

    def test_avoid_skips_quoted_text(self):
        self.assertEqual(self.count("glossary-avoid", "他说「怒气」。"), 0)

    def test_repeated_gloss_is_flagged_once(self):
        self.assertEqual(
            self.count("glossary-gloss-repeat", "愤怒（anger）与愤怒（anger）"), 1)

    def test_checks_appear_only_with_a_glossary(self):
        text = "恰当（aptness）"
        without = LINT.analyze(text)["checks"]
        self.assertEqual(list(without), [check_id for check_id, _ in LINT.CHECKS])
        with_glossary = LINT.analyze(text, glossary=self.entries)["checks"]
        self.assertEqual(
            list(with_glossary),
            [check_id for check_id, _ in LINT.CHECKS]
            + [check_id for check_id, _ in LINT.GLOSSARY_CHECKS])

    def test_cli_glossary_flag(self):
        path = Path(self._temp.name) / "sample.txt"
        path.write_text("恰当（aptness）与愤怒（anger）。", encoding="utf-8")
        completed = run_cli(path, "--glossary", self.glossary_path, "--json")
        self.assertEqual(completed.returncode, 0)
        data = json.loads(completed.stdout)
        self.assertIn("glossary-gloss", data["checks"])
        self.assertEqual(data["checks"]["glossary-gloss"]["count"], 1)

        plain = json.loads(run_cli(path, "--json").stdout)
        self.assertNotIn("glossary-gloss", plain["checks"])


if __name__ == "__main__":
    unittest.main()
