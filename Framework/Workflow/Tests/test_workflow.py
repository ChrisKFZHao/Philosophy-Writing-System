from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = WORKFLOW_ROOT / "Scripts"
REPO_ROOT = WORKFLOW_ROOT.parent.parent


def load_script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PolicyTests(unittest.TestCase):
    def test_collaboration_aliases(self):
        policy = load_script("workflow-policy.py")
        self.assertEqual(policy.normalize_collaboration("assistant-led")["canonical"], "assistant-led")
        self.assertFalse(policy.normalize_collaboration("assistant-led")["deprecated_alias"])
        for alias in ("claude-led", "codex-led"):
            result = policy.normalize_collaboration(alias)
            self.assertEqual(result["canonical"], "assistant-led")
            self.assertTrue(result["deprecated_alias"])

    def test_zotero_statuses(self):
        policy = load_script("workflow-policy.py")
        self.assertEqual(policy.zotero_status(True, False), "full")
        self.assertEqual(policy.zotero_status(False, True), "partial")
        self.assertEqual(policy.zotero_status(False, False), "skipped")

    def test_zotero_dry_run_never_writes(self):
        policy = load_script("workflow-policy.py")
        for mcp, local, expected in (
            (True, False, "full"),
            (False, True, "partial"),
            (False, False, "skipped"),
        ):
            plan = policy.zotero_plan(mcp, local, dry_run=True)
            self.assertEqual(plan["status"], expected)
            self.assertFalse(plan["write_allowed"])

    def test_citation_gate_two_hops(self):
        policy = load_script("workflow-policy.py")
        self.assertEqual(policy.citation_gate(False, 1, 3)["hop"], 1)
        insufficient = policy.citation_gate(True, 2, 1)
        self.assertEqual(insufficient, {
            "decision": "block",
            "hop": 2,
            "reason": "analysis-level-insufficient",
        })
        self.assertEqual(policy.citation_gate(True, 2, 2)["decision"], "pass")


class BibliographyScanTests(unittest.TestCase):
    def test_reports_each_unprocessed_reason(self):
        scanner = load_script("bibliography-scan.py")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf_dir = root / "Private/Bibliography/PDF"
            summary_dir = root / "Private/Bibliography/Summaries"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            (pdf_dir / "Raw.pdf").write_bytes(b"pdf")
            (pdf_dir / "Austin_1956_A-Plea-for-Excuses.pdf").write_bytes(b"pdf")
            (root / "Private/Bibliography/INDEX.md").write_text(
                "| AUSTIN-PLEA | PDF/Austin_1956_A-Plea-for-Excuses.pdf |\n", encoding="utf-8"
            )
            result = scanner.scan(root)
            self.assertEqual(result["unprocessed_count"], 2)
            reasons = {item["file"]: item["reasons"] for item in result["unprocessed"]}
            self.assertEqual(reasons["Raw.pdf"], ["noncanonical-name", "missing-index-row", "missing-summary"])
            self.assertEqual(reasons["Austin_1956_A-Plea-for-Excuses.pdf"], ["missing-summary"])


class AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((WORKFLOW_ROOT / "manifest.json").read_text(encoding="utf-8"))

    def test_manifest_inventory(self):
        counts = {kind: 0 for kind in ("skill", "workflow", "role")}
        for item in self.manifest["items"]:
            counts[item["kind"]] += 1
        self.assertEqual(counts, {"skill": 30, "workflow": 8, "role": 7})

    def workflow_item(self, workflow_id: str) -> dict:
        return next(item for item in self.manifest["items"] if item["id"] == workflow_id)

    def test_key_workflow_sections(self):
        required = {
            "reconstruct": [
                "Executive summary", "Argument reconstruction", "Charity audit", "Concept map",
                "Distinction index", "Thought experiments and intuition pumps", "Modal assessment",
                "Contextual positioning", "Domain-specific analysis", "Open questions",
            ],
            "evaluate": [
                "Executive summary", "Counterexample inventory", "Dialectical structure",
                "Analogy assessment", "Parity check", "Intuition pump analysis",
                "Methodological audit", "Fallacy inventory", "Improvement recommendations",
            ],
            "review": [
                "Overall assessment", "Dimension-by-dimension scores and comments",
                "Major issues", "Minor issues", "Revision recommendations",
            ],
        }
        for workflow_id, headings in required.items():
            text = (WORKFLOW_ROOT / "Workflows" / f"{workflow_id}.md").read_text(encoding="utf-8")
            output_format = text.split("## Output Format", 1)[1]
            positions = [output_format.index(heading) for heading in headings]
            self.assertEqual(positions, sorted(positions), workflow_id)

    def test_dependency_order_and_role_contracts(self):
        reconstruct = self.workflow_item("reconstruct")["dependencies"]
        expected_prefix = [
            "phil-argument-reconstruct", "phil-charity-check", "phil-premise-detect", "phil-modal-arg",
            "phil-conceptual-analysis", "phil-distinction-track", "phil-thought-experiment",
            "phil-intuition-pump", "phil-contextualize",
        ]
        self.assertEqual(reconstruct[: len(expected_prefix)], expected_prefix)
        evaluate = self.workflow_item("evaluate")
        self.assertEqual(evaluate["dependencies"], [
            "phil-counterexample", "phil-dialectical-map", "phil-analogy-check",
            "phil-parity-check", "phil-intuition-pump", "phil-methodology",
        ])
        review = self.workflow_item("review")
        self.assertEqual((review["role"], review["dependencies"]), ("phil-reviewer", ["phil-reviewer"]))

    def test_codex_delegation_fallback_is_generated(self):
        for workflow_id in ("reconstruct", "evaluate"):
            path = REPO_ROOT / ".agents/skills" / f"source-command-{workflow_id}" / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("When delegation is available", text)
            self.assertIn("dependency order serially", text)

    def test_rendering_is_deterministic(self):
        builder = load_script("build-adapters.py")
        first = builder.render_outputs(builder.load_manifest())
        second = builder.render_outputs(builder.load_manifest())
        def digest(outputs):
            hasher = hashlib.sha256()
            for path, content in sorted(outputs.items(), key=lambda pair: pair[0].as_posix()):
                hasher.update(path.as_posix().encode())
                hasher.update(content if isinstance(content, bytes) else content.encode())
            return hasher.hexdigest()
        self.assertEqual(digest(first), digest(second))

    def assert_manifest_rejected(self, mutate):
        builder = load_script("build-adapters.py")
        data = copy.deepcopy(self.manifest)
        mutate(data)
        with tempfile.TemporaryDirectory() as temp:
            manifest_path = Path(temp) / "manifest.json"
            manifest_path.write_text(json.dumps(data), encoding="utf-8")
            original = builder.MANIFEST_PATH
            builder.MANIFEST_PATH = manifest_path
            try:
                with self.assertRaises(builder.ManifestError):
                    builder.load_manifest()
            finally:
                builder.MANIFEST_PATH = original

    def test_manifest_rejects_unknown_fields(self):
        self.assert_manifest_rejected(lambda data: data["items"][0].__setitem__("unknown", True))

    def test_manifest_rejects_duplicate_ids(self):
        self.assert_manifest_rejected(lambda data: data["items"][1].__setitem__("id", data["items"][0]["id"]))

    def test_manifest_rejects_missing_dependencies(self):
        workflow = next(item for item in self.manifest["items"] if item["kind"] == "workflow")
        workflow_id = workflow["id"]
        self.assert_manifest_rejected(
            lambda data: next(item for item in data["items"] if item["id"] == workflow_id)["dependencies"].append("missing-item")
        )

    def test_output_collisions_are_rejected(self):
        builder = load_script("build-adapters.py")
        outputs = {}
        builder.add_output(outputs, Path("same.md"), "first")
        with self.assertRaises(builder.ManifestError):
            builder.add_output(outputs, Path("same.md"), "second")

    def test_generated_adapters_are_current(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "build-adapters.py"), "--check"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
