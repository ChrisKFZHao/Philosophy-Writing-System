from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent.parent / "Scripts"


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
        self.assertEqual(level_one["run"], ["phil-argument-reconstruct"])
        self.assertGreater(len(level_two["run"]), len(level_one["run"]))
        self.assertIn("phil-contextualize", level_three["run"])
        self.assertNotIn("phil-conceptual-analysis", level_two["run"])
        conceptual = next(
            item for item in level_two["decisions"]
            if item["module"] == "phil-conceptual-analysis"
        )
        self.assertEqual(conceptual["action"], "skip")
        self.assertEqual(conceptual["reason"], "feature-or-intent-absent")

    def test_current_coverage_is_reused_but_changed_source_invalidates(self):
        covered = self.artifact(["argument reconstruction", "charity audit"])
        current = self.policy.reconstruction_plan(2, covered, self.source_hash, self.analysis_hash)
        self.assertEqual(current["reuse"], ["phil-argument-reconstruct", "phil-charity-check"])
        stale = self.policy.reconstruction_plan(2, covered, "c" * 64, self.analysis_hash)
        self.assertTrue(stale["source_changed"])
        self.assertIn("source-hash-changed", stale["invalidation"])
        self.assertIn("phil-argument-reconstruct", stale["run"])

    def test_full_and_deep_override_expand_reconstruction(self):
        full = self.policy.reconstruction_plan(1, source_sha256=self.source_hash, analysis_sha256=self.analysis_hash, full=True)
        deep = self.policy.reconstruction_plan(1, source_sha256=self.source_hash, analysis_sha256=self.analysis_hash, deep=True)
        self.assertEqual(full["level"], 3)
        self.assertNotIn("phil-modal-arg", full["run"])
        self.assertEqual(deep["override"], "deep")

    def test_evaluation_keeps_lightweight_scans_and_selects_dimensions(self):
        artifact = self.artifact(["counterexample", "analogy-check"])
        plan = self.policy.evaluation_plan("comparison", artifact, self.source_hash, self.analysis_hash)
        self.assertEqual(plan["run"][:2], ["inference-scan", "fallacy-scan"])
        self.assertEqual(plan["reuse"], ["phil-analogy-check"])
        self.assertIn("phil-parity-check", plan["run"])
        analogy = next(item for item in plan["decisions"] if item["module"] == "phil-analogy-check")
        self.assertEqual(analogy["action"], "reuse")
        self.assertEqual(analogy["selector"], "intent:comparison")
        full = self.policy.evaluation_plan(source_sha256=self.source_hash, analysis_sha256=self.analysis_hash, full=True)
        self.assertIn("phil-counterexample", full["run"])
        self.assertNotIn("phil-methodology", full["run"])

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
        self.assertIn("phil-argument-reconstruct", plan["run"])

    def test_current_artifact_reuses_despite_separate_stale_artifact(self):
        artifacts = [
            self.artifact(["argument-reconstruct"], status="stale"),
            self.artifact(["argument-reconstruct"]),
        ]
        plan = self.policy.reconstruction_plan(1, artifacts, self.source_hash, self.analysis_hash)
        self.assertEqual(plan["reuse"], ["phil-argument-reconstruct"])
        self.assertIn("analysis-stale", plan["invalidation"])


if __name__ == "__main__":
    unittest.main()
