from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent.parent / "Scripts"


def load_policy():
    path = SCRIPTS / "workflow-policy.py"
    spec = importlib.util.spec_from_file_location("workflow_policy", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CitationGateVerificationTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy()
        self.source_hash = "a" * 64
        self.analysis_hash = "b" * 64
        self.metadata = {
            "analysis_level": 3,
            "verification_status": "verified",
            "source_sha256": self.source_hash,
            "analysis_sha256": self.analysis_hash,
        }

    def gate(self, **changes):
        metadata = self.metadata | changes.pop("metadata", {})
        return self.policy.citation_gate(
            changes.pop("registered", True),
            changes.pop("required_level", 2),
            changes.pop("available_level", None),
            metadata if not changes.pop("without_metadata", False) else None,
            changes.pop("source_hash", self.source_hash),
            changes.pop("analysis_hash", self.analysis_hash),
        )

    def test_blocks_unregistered_key(self):
        self.assertEqual(self.gate(registered=False)["reason"], "key-not-in-refs")

    def test_blocks_when_metadata_is_absent(self):
        self.assertEqual(self.gate(without_metadata=True)["reason"], "analysis-metadata-missing")

    def test_blocks_insufficient_analysis_level(self):
        self.assertEqual(self.gate(metadata={"analysis_level": 1})["reason"], "analysis-level-insufficient")

    def test_blocks_malformed_levels_without_raising(self):
        for malformed in (True, "2", float("nan"), float("inf"), -1, 0, 2.5):
            self.assertEqual(
                self.gate(required_level=malformed)["reason"],
                "analysis-level-insufficient",
            )
            self.assertEqual(
                self.gate(metadata={"analysis_level": malformed})["reason"],
                "analysis-level-insufficient",
            )

    def test_blocks_unverified_analysis(self):
        self.assertEqual(self.gate(metadata={"verification_status": "provisional"})["reason"], "analysis-unverified")

    def test_blocks_stale_source_or_analysis(self):
        self.assertEqual(self.gate(source_hash="c" * 64)["reason"], "analysis-stale")
        self.assertEqual(self.gate(analysis_hash="c" * 64)["reason"], "analysis-stale")
        self.assertEqual(self.gate(metadata={"verification_status": "stale"})["reason"], "analysis-stale")

    def test_passes_only_with_verified_matching_evidence(self):
        self.assertEqual(self.gate(), {"decision": "pass", "hop": 2, "reason": "verified"})

    def test_legacy_sufficient_call_blocks(self):
        result = self.policy.citation_gate(True, 2, 2)
        self.assertEqual(result["reason"], "analysis-metadata-missing")

    def test_philosopher_claim_requires_verified_analysis_metadata(self):
        evidence = [{"bib_key": "SOURCE-ONE", "analysis_level": 2}]
        arguments = ("source-backed", evidence, {"SOURCE-ONE"}, 2)
        self.assertEqual(
            self.policy.philosopher_claim_gate(*arguments)["reason"],
            "analysis-metadata-missing",
        )
        self.assertEqual(
            self.policy.philosopher_claim_gate(
                *arguments,
                {"SOURCE-ONE": {"analysis_level": 2, "verification_status": "provisional"}},
            )["reason"],
            "analysis-unverified",
        )
        self.assertEqual(
            self.policy.philosopher_claim_gate(
                *arguments,
                {"SOURCE-ONE": {
                    "analysis_level": 2,
                    "verification_status": "verified",
                    "source_hash_matches": True,
                    "analysis_hash_matches": False,
                }},
            )["reason"],
            "analysis-stale",
        )
        passed = self.policy.philosopher_claim_gate(
            *arguments,
            {"SOURCE-ONE": {
                "analysis_level": 2,
                "verification_status": "verified",
                "source_hash_matches": True,
                "analysis_hash_matches": True,
            }},
        )
        self.assertEqual(passed["eligible_keys"], ["SOURCE-ONE"])

    def test_philosopher_claim_blocks_malformed_levels_without_raising(self):
        arguments = ("source-backed", [{"bib_key": "SOURCE-ONE", "analysis_level": "two"}], {"SOURCE-ONE"}, 2)
        self.assertEqual(
            self.policy.philosopher_claim_gate(*arguments)["reason"],
            "analysis-level-insufficient",
        )
        self.assertEqual(
            self.policy.philosopher_claim_gate(
                "source-backed",
                [{"bib_key": "SOURCE-ONE", "analysis_level": 2}],
                {"SOURCE-ONE"},
                True,
            )["reason"],
            "analysis-level-insufficient",
        )
