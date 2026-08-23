from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent.parent / "Scripts"
WORKFLOW_ROOT = SCRIPTS.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_policy():
    path = SCRIPTS / "workflow-policy.py"
    spec = importlib.util.spec_from_file_location("workflow_policy_planning", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy()
        self.source_hash = "a" * 64
        self.analysis_hash = "b" * 64

    def artifact(self, coverage, source_hash=None, analysis_hash=None, status="verified"):
        return {
            "source_sha256": source_hash or self.source_hash,
            "analysis_sha256": analysis_hash or self.analysis_hash,
            "verification_status": status,
            "coverage": coverage,
        }

    def test_reconstruction_levels_are_progressive(self):
        level_one = self.policy.reconstruction_plan(1, source_sha256=self.source_hash, analysis_sha256=self.analysis_hash)
        level_two = self.policy.reconstruction_plan(2, source_sha256=self.source_hash, analysis_sha256=self.analysis_hash)
        level_three = self.policy.reconstruction_plan(3, source_sha256=self.source_hash, analysis_sha256=self.analysis_hash)
        self.assertEqual(level_one["run"], ["method.argument.argument-reconstruct"])
        self.assertGreater(len(level_two["run"]), len(level_one["run"]))
        self.assertIn("method.dialectic.contextualize", level_three["run"])
        self.assertNotIn("method.concept.conceptual-analysis", level_two["run"])
        conceptual = next(
            item for item in level_two["decisions"]
            if item["module"] == "method.concept.conceptual-analysis"
        )
        self.assertEqual(conceptual["action"], "skip")
        self.assertEqual(conceptual["reason"], "feature-or-intent-absent")

    def test_current_coverage_is_reused_but_changed_source_invalidates(self):
        covered = self.artifact(["argument reconstruction", "charity audit"])
        current = self.policy.reconstruction_plan(2, covered, self.source_hash, self.analysis_hash)
        self.assertEqual(current["reuse"], ["method.argument.argument-reconstruct", "method.argument.charity-check"])
        stale = self.policy.reconstruction_plan(2, covered, "c" * 64, self.analysis_hash)
        self.assertTrue(stale["source_changed"])
        self.assertIn("source-hash-changed", stale["invalidation"])
        self.assertIn("method.argument.argument-reconstruct", stale["run"])

    def test_legacy_coverage_ids_normalize_on_read(self):
        legacy = self.artifact(["phil-argument-reconstruct", "phil-charity-check", "implicit premises"])
        plan = self.policy.reconstruction_plan(2, legacy, self.source_hash, self.analysis_hash)
        self.assertEqual(
            plan["reuse"],
            ["method.argument.argument-reconstruct", "method.argument.charity-check", "method.argument.premise-detect"],
        )

    def test_full_and_deep_override_expand_reconstruction(self):
        full = self.policy.reconstruction_plan(1, source_sha256=self.source_hash, analysis_sha256=self.analysis_hash, full=True)
        deep = self.policy.reconstruction_plan(1, source_sha256=self.source_hash, analysis_sha256=self.analysis_hash, deep=True)
        self.assertEqual(full["level"], 3)
        self.assertNotIn("method.metaphysics.modal-arg", full["run"])
        self.assertEqual(deep["override"], "deep")

    def test_evaluation_keeps_lightweight_scans_and_selects_dimensions(self):
        artifact = self.artifact(["counterexample", "analogy-check"])
        plan = self.policy.evaluation_plan("comparison", artifact, self.source_hash, self.analysis_hash)
        self.assertEqual(plan["run"][:2], ["inference-scan", "fallacy-scan"])
        self.assertEqual(plan["reuse"], ["method.argument.analogy-check"])
        self.assertIn("method.argument.parity-check", plan["run"])
        analogy = next(item for item in plan["decisions"] if item["module"] == "method.argument.analogy-check")
        self.assertEqual(analogy["action"], "reuse")
        self.assertEqual(analogy["selector"], "intent:comparison")
        full = self.policy.evaluation_plan(source_sha256=self.source_hash, analysis_sha256=self.analysis_hash, full=True)
        self.assertIn("method.argument.counterexample", full["run"])
        self.assertNotIn("method.dialectic.methodology", full["run"])

    def test_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.policy.reconstruction_plan(4)
        with self.assertRaises(ValueError):
            self.policy.reconstruction_plan(features=["unknown"])
        with self.assertRaises(ValueError):
            self.policy.evaluation_plan(intent="unknown")
        with self.assertRaises(ValueError):
            self.policy.evaluation_plan(intent="full")
        with self.assertRaises(ValueError):
            self.policy.evaluation_plan(source_sha256="not-a-hash")

    def test_unverified_or_mismatched_analysis_cannot_reuse(self):
        provisional = self.artifact(["argument-reconstruct"], status="provisional")
        plan = self.policy.reconstruction_plan(1, provisional, self.source_hash, self.analysis_hash)
        self.assertEqual(plan["reuse"], [])
        self.assertIn("analysis-unverified", plan["invalidation"])
        mismatch = self.artifact(["argument-reconstruct"], analysis_hash="c" * 64)
        plan = self.policy.reconstruction_plan(1, mismatch, self.source_hash, self.analysis_hash)
        self.assertIn("analysis-hash-changed", plan["invalidation"])
        self.assertIn("method.argument.argument-reconstruct", plan["run"])

    def test_current_artifact_reuses_despite_separate_stale_artifact(self):
        artifacts = [
            self.artifact(["argument-reconstruct"], status="stale"),
            self.artifact(["argument-reconstruct"]),
        ]
        plan = self.policy.reconstruction_plan(1, artifacts, self.source_hash, self.analysis_hash)
        self.assertEqual(plan["reuse"], ["method.argument.argument-reconstruct"])
        self.assertIn("analysis-stale", plan["invalidation"])

    def test_removed_entrypoint_resolver(self):
        replaced = self.policy.removed_entrypoint("phil:reconstruct")
        self.assertEqual((replaced["status"], replaced["replacement"]), ("removed", "phil:research reconstruct"))
        self.assertIn("phil:research reconstruct", replaced["message"])
        self.assertIn("No alias", replaced["message"])
        pipeline = self.policy.removed_entrypoint("phil:pipeline")
        self.assertEqual(pipeline["replacement"], "phil:full start")
        retained = self.policy.removed_entrypoint("phil:tutor")
        self.assertEqual(retained["status"], "retained")
        with self.assertRaises(ValueError):
            self.policy.removed_entrypoint("phil:nonsense")


class RegressionBaselineTests(unittest.TestCase):
    """Replay the v0.6 planner baseline captured before the 0.7 restructure.

    Module IDs are mapped old -> new through the committed migration map; every
    decision, selector, and reason must be identical. Any intentional behavior
    change must update the fixture with a recorded rationale.
    """

    @classmethod
    def setUpClass(cls):
        cls.policy = load_policy()
        cls.migration = json.loads(
            (WORKFLOW_ROOT / "Migration/migration-v0.7.json").read_text(encoding="utf-8")
        )
        cls.old_to_new = {
            old: entry["method_id"] for old, entry in cls.migration["method_map"].items()
        }
        cls.baseline = json.loads(
            (FIXTURES / "v06-planner-baseline.json").read_text(encoding="utf-8")
        )

    def map_ids(self, value):
        if isinstance(value, list):
            return [self.map_ids(item) for item in value]
        if isinstance(value, str):
            return self.old_to_new.get(value, value)
        return value

    def test_baseline_replays_identically(self):
        self.assertGreaterEqual(len(self.baseline["cases"]), 30)
        for case in self.baseline["cases"]:
            with self.subTest(case=case["tag"]):
                call = dict(case["call"])
                for key in ("artifacts", "source_sha256", "analysis_sha256"):
                    if call.get(key) is None:
                        call.pop(key, None)
                plan = (
                    self.policy.reconstruction_plan(**call)
                    if case["kind"] == "reconstruction"
                    else self.policy.evaluation_plan(**call)
                )
                expected = case["expected"]
                for field in ("run", "reuse", "required_coverage"):
                    self.assertEqual(
                        self.map_ids(expected[field]), plan[field],
                        f"{case['tag']}: {field} drifted",
                    )
                self.assertEqual(expected["invalidation"], plan["invalidation"], case["tag"])
                self.assertEqual(expected["override"], plan["override"], case["tag"])
                self.assertEqual(expected.get("level"), plan.get("level"), case["tag"])
                self.assertEqual(expected.get("intent"), plan.get("intent"), case["tag"])
                self.assertEqual(expected.get("features"), plan.get("features"), case["tag"])
                expected_decisions = {d["module"]: d for d in self.map_ids(
                    [dict(item) for item in expected["decisions"]]
                )}
                # map_ids above maps module strings inside dicts only at top level lists;
                # rebuild explicitly:
                expected_decisions = {}
                for decision in expected["decisions"]:
                    module = self.old_to_new.get(decision["module"], decision["module"])
                    expected_decisions[module] = {
                        "module": module,
                        "action": decision["action"],
                        "reason": decision["reason"],
                        "selector": decision["selector"],
                    }
                actual_decisions = {d["module"]: d for d in plan["decisions"]}
                self.assertEqual(
                    sorted(expected_decisions), sorted(actual_decisions), case["tag"]
                )
                for module, decision in expected_decisions.items():
                    actual = actual_decisions[module]
                    self.assertEqual(decision["action"], actual["action"], f"{case['tag']}/{module}")
                    self.assertEqual(decision["reason"], actual["reason"], f"{case['tag']}/{module}")
                    self.assertEqual(decision["selector"], actual["selector"], f"{case['tag']}/{module}")


if __name__ == "__main__":
    unittest.main()
