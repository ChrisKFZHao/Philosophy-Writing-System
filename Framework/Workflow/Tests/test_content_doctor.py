from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = WORKFLOW_ROOT / "Scripts"


def load_script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index(rows: list[str], extra: str = "") -> str:
    return "\n".join([
        "# Index", "", "## Reference Inventory", "",
        "| KEY | Author | Title | PDF | Zotero | Analysis Level | Topics | Used By |",
        "|-----|--------|-------|-----|--------|----------------|--------|---------|",
        *rows, "", extra,
    ])


class BibliographyScanTests(unittest.TestCase):
    def test_ignores_documentation_example_and_supports_shared_pdf(self):
        scan = load_script("bibliography-scan.py")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / "Private/Bibliography/PDF/Volume_2020_Collected-Papers.pdf"
            pdf.parent.mkdir(parents=True)
            pdf.write_bytes(b"pdf")
            (root / "Private/Bibliography/Summaries").mkdir()
            (root / "Private/Bibliography/Summaries/Volume_2020_Collected-Papers.summary.txt").write_text("x")
            (root / "Private/Bibliography/INDEX.md").write_text(index([
                "| VOLUME | A | V | PDF/Volume_2020_Collected-Papers.pdf | - | Level 0.5 | x | - |",
                "| MEMBER | B | M | PDF/Volume_2020_Collected-Papers.pdf, pp. 1-20, in VOLUME | - | Level 0.5 | x | - |",
            ], "Example: PDF/Chalmers_2009_Metametaphysics.pdf"), encoding="utf-8")
            result = scan.scan(root)
            self.assertEqual(result["registered_pdf_count"], 1)
            self.assertEqual(result["dangling_index_pdfs"], [])
            self.assertEqual(result["unprocessed_count"], 0)

    def test_strict_fails_for_dangling_index_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bibliography = root / "Private/Bibliography"
            bibliography.mkdir(parents=True)
            (bibliography / "INDEX.md").write_text(index([
                "| LOST | A | T | PDF/Lost_2020_Title.pdf | - | Level 0.5 | x | - |",
            ]), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPTS / "bibliography-scan.py"), "--root", str(root), "--strict"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("dangling INDEX PDF", result.stdout)


class ContentDoctorTests(unittest.TestCase):
    def test_no_private_is_cleanly_skipped(self):
        doctor = load_script("content-doctor.py")
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(doctor.check(Path(temp))["status"], "skipped")

    def test_reports_missing_summary_dangling_refs_and_validates_member_by_key(self):
        doctor = load_script("content-doctor.py")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bibliography = root / "Private/Bibliography"
            pdf_dir = bibliography / "PDF"
            summaries = bibliography / "Summaries"
            pdf_dir.mkdir(parents=True)
            summaries.mkdir()
            volume = pdf_dir / "Bennett_2020_Collected-Papers.pdf"
            volume.write_bytes(b"volume")
            (bibliography / "INDEX.md").write_text(index([
                "| VOLUME | A | V | PDF/Bennett_2020_Collected-Papers.pdf | - | Level 0.5 | x | - |",
                "| MEMBER | B | M | PDF/Bennett_2020_Collected-Papers.pdf, pp. 1-20, in VOLUME | - | Level 0.5 | x | - |",
                "| MISSING | C | X | PDF/Missing_2020_X.pdf | - | Level 0.5 | x | - |",
            ]), encoding="utf-8")
            (summaries / "member.summary.txt").write_text("```json\n" + json.dumps({"bib_key": "MEMBER"}) + "\n```", encoding="utf-8")
            project = root / "Private/Projects/demo"
            project.mkdir(parents=True)
            (project / "refs.md").write_text("UNKNOWN | support | candidate | test\n", encoding="utf-8")
            result = doctor.check(root)
            self.assertIn("summary-missing-or-key-mismatch:VOLUME", result["failures"])
            self.assertNotIn("summary-missing-or-key-mismatch:MEMBER", result["failures"])
            self.assertIn("index-dangling-pdf:Missing_2020_X.pdf", result["failures"])
            self.assertIn("project-ref-key-missing:demo:UNKNOWN", result["failures"])
            self.assertTrue(any(item.startswith("project-guidance-missing:demo") for item in result["warnings"]))

    def test_checks_analysis_metadata_and_hashes(self):
        doctor = load_script("content-doctor.py")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bibliography = root / "Private/Bibliography"
            pdf_dir = bibliography / "PDF"
            summaries = bibliography / "Summaries"
            analysis_dir = bibliography / "Analysis"
            pdf_dir.mkdir(parents=True)
            summaries.mkdir()
            analysis_dir.mkdir()
            pdf = pdf_dir / "Author_2020_Title.pdf"
            analysis = analysis_dir / "Author_2020_Title.analysis.txt"
            pdf.write_bytes(b"pdf")
            analysis.write_text("analysis", encoding="utf-8")
            (bibliography / "INDEX.md").write_text(index([
                "| KEY | A | T | PDF/Author_2020_Title.pdf | - | Level 1 | x | - |",
            ]), encoding="utf-8")
            (summaries / "key.summary.txt").write_text("```json\n" + json.dumps({"bib_key": "KEY"}) + "\n```", encoding="utf-8")
            metadata = {"bib_key": "KEY", "analysis_level": 1, "verification_status": "verified", "pdf_sha256": digest(pdf), "analysis_sha256": digest(analysis), "analysis_file": analysis.name}
            (analysis_dir / "Author_2020_Title.analysis.meta.json").write_text(json.dumps(metadata), encoding="utf-8")
            self.assertEqual(doctor.check(root)["status"], "ok")
            metadata["verification_status"] = "provisional"
            (analysis_dir / "Author_2020_Title.analysis.meta.json").write_text(json.dumps(metadata), encoding="utf-8")
            self.assertIn("analysis-unverified:KEY", doctor.check(root)["failures"])

    def test_reports_duplicate_summary_key_and_uses_state_validators(self):
        doctor = load_script("content-doctor.py")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bibliography = root / "Private/Bibliography"
            (bibliography / "PDF").mkdir(parents=True)
            (bibliography / "Summaries").mkdir()
            (bibliography / "INDEX.md").write_text(index([]), encoding="utf-8")
            for name in ("one.summary.txt", "two.summary.txt"):
                (bibliography / "Summaries" / name).write_text("```json\n" + json.dumps({"bib_key": "DUP"}) + "\n```", encoding="utf-8")
            project = root / "Private/Projects/demo"
            project.mkdir(parents=True)
            (project / "demo-idea-ledger.json").write_text(json.dumps({"schema_version": 1}), encoding="utf-8")
            (project / "demo-workflow-state.json").write_text(json.dumps({"schema_version": 1}), encoding="utf-8")
            failures = doctor.check(root)["failures"]
            self.assertTrue(any(item.startswith("summary-bib-key-duplicate:DUP:") for item in failures))
            self.assertTrue(any(item.startswith("invalid-demo-idea-ledger.json:demo:") for item in failures))
            self.assertTrue(any(item.startswith("invalid-demo-workflow-state.json:demo:") for item in failures))


if __name__ == "__main__":
    unittest.main()
