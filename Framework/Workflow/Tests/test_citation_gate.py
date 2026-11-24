from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
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

    def _run_gate(self, *arguments):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "workflow-policy.py"),
                "citation-gate",
                "--required-level",
                "2",
                *arguments,
            ],
            capture_output=True,
            text=True,
        )

    def test_sha256_file_normalizes_line_endings_for_text_but_not_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            lf_text = root / "lf.txt"
            crlf_text = root / "crlf.txt"
            lf_text.write_bytes(b"first\nsecond\n")
            crlf_text.write_bytes(b"first\r\nsecond\r\n")
            self.assertEqual(self.policy.sha256_file(lf_text), self.policy.sha256_file(crlf_text))
            self.assertEqual(
                self.policy.sha256_file(crlf_text),
                hashlib.sha256(b"first\nsecond\n").hexdigest(),
            )
            lf_pdf = root / "lf.pdf"
            crlf_pdf = root / "crlf.pdf"
            lf_pdf.write_bytes(b"first\nsecond\n")
            crlf_pdf.write_bytes(b"first\r\nsecond\r\n")
            self.assertNotEqual(self.policy.sha256_file(lf_pdf), self.policy.sha256_file(crlf_pdf))

    def test_cli_exit_code_follows_decision(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.pdf"
            analysis = root / "analysis.txt"
            source.write_bytes(b"%PDF-1.4\n")
            analysis.write_bytes(b"analysis\n")
            metadata = root / "analysis.meta.json"
            metadata.write_text(json.dumps({
                "bib_key": "SMITH-A",
                "analysis_level": 2,
                "verification_status": "verified",
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "analysis_sha256": hashlib.sha256(analysis.read_bytes()).hexdigest(),
            }), encoding="utf-8")
            common = [
                "--metadata", str(metadata),
                "--source-path", str(source),
                "--analysis-path", str(analysis),
            ]
            passed = self._run_gate("--registered", *common)
            self.assertEqual(passed.returncode, 0)
            self.assertEqual(json.loads(passed.stdout)["decision"], "pass")
            blocked = self._run_gate(*common)
            self.assertEqual(blocked.returncode, 1)
            self.assertEqual(json.loads(blocked.stdout)["reason"], "key-not-in-refs")

    def test_refs_status_fails_closed_on_any_rejected_row(self):
        with tempfile.TemporaryDirectory() as temp:
            refs = Path(temp) / "refs.md"
            refs.write_text(
                "| KEY | role | status | notes |\n"
                "|---|---|---|---|\n"
                "| DOUBLE | support | cited | first row |\n"
                "| DOUBLE | support | rejected | later row |\n"
                "| NOTED | support | rejected (out of scope) | annotated |\n",
                encoding="utf-8",
            )
            self.assertEqual(self.policy.refs_status(refs, "DOUBLE"), "rejected")
            self.assertEqual(self.policy.refs_status(refs, "NOTED"), "rejected")

    def test_refs_status_reads_first_cell_exactly(self):
        with tempfile.TemporaryDirectory() as temp:
            refs = Path(temp) / "refs.md"
            refs.write_text(
                "| KEY | role | status | notes |\n"
                "|---|---|---|---|\n"
                "| SMITH-AB | support | cited | longer key |\n"
                "| GONE | support | Rejected | removed |\n"
                "| NOTEONLY | support | candidate | see KANT-1781 |\n"
                "PLAIN | support | cited | no leading pipe |\n",
                encoding="utf-8",
            )
            self.assertEqual(self.policy.refs_status(refs, "SMITH-AB"), "registered")
            self.assertEqual(self.policy.refs_status(refs, "NOTEONLY"), "registered")
            self.assertEqual(self.policy.refs_status(refs, "PLAIN"), "registered")
            self.assertEqual(self.policy.refs_status(refs, "GONE"), "rejected")
            self.assertEqual(self.policy.refs_status(refs, "SMITH"), "absent")
            self.assertEqual(self.policy.refs_status(refs, "KANT-1781"), "absent")
            self.assertEqual(self.policy.refs_status(Path(temp) / "missing.md", "SMITH-AB"), "absent")

    def test_cli_refs_blocks_rejected_and_absent_keys(self):
        with tempfile.TemporaryDirectory() as temp:
            refs = Path(temp) / "refs.md"
            refs.write_text(
                "| KEY | role | status | notes |\n"
                "|---|---|---|---|\n"
                "| GONE | support | rejected | removed |\n"
                "| KEPT | support | cited | active |\n",
                encoding="utf-8",
            )
            rejected = self._run_gate("--key", "GONE", "--refs", str(refs))
            self.assertEqual(rejected.returncode, 1)
            self.assertEqual(
                json.loads(rejected.stdout),
                {"decision": "block", "hop": 1, "reason": "key-rejected"},
            )
            absent = self._run_gate("--key", "MISSING", "--refs", str(refs))
            self.assertEqual(
                json.loads(absent.stdout),
                {"decision": "block", "hop": 1, "reason": "key-not-in-refs"},
            )
            kept = self._run_gate("--key", "KEPT", "--refs", str(refs))
            self.assertEqual(json.loads(kept.stdout)["reason"], "analysis-metadata-missing")
            self.assertEqual(self._run_gate("--refs", str(refs)).returncode, 2)

    def test_blocks_metadata_key_mismatch(self):
        mismatch = self.policy.citation_gate(
            True, 2, None,
            self.metadata | {"bib_key": "SMITH-B"},
            self.source_hash, self.analysis_hash,
            cited_key="SMITH-A",
        )
        self.assertEqual(mismatch, {"decision": "block", "hop": 2, "reason": "analysis-key-mismatch"})
        matched = self.policy.citation_gate(
            True, 2, None,
            self.metadata | {"bib_key": "SMITH-A"},
            self.source_hash, self.analysis_hash,
            cited_key="SMITH-A",
        )
        self.assertEqual(matched["decision"], "pass")
        no_field = self.policy.citation_gate(
            True, 2, None,
            self.metadata,
            self.source_hash, self.analysis_hash,
            cited_key="SMITH-A",
        )
        self.assertEqual(no_field["decision"], "pass")

    def test_philosopher_claim_requires_strict_boolean_hashes(self):
        arguments = ("source-backed", [{"bib_key": "SOURCE-ONE", "analysis_level": 2}], {"SOURCE-ONE"}, 2)
        for source_flag, analysis_flag in (("false", True), (True, "false"), ("true", True)):
            result = self.policy.philosopher_claim_gate(
                *arguments,
                {"SOURCE-ONE": {
                    "analysis_level": 2,
                    "verification_status": "verified",
                    "source_hash_matches": source_flag,
                    "analysis_hash_matches": analysis_flag,
                }},
            )
            self.assertEqual(result["reason"], "analysis-stale")

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
