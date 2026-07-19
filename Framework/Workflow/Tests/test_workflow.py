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
        self.assertEqual(
            policy.citation_gate(True, 2, 2)["reason"],
            "analysis-metadata-missing",
        )

    def test_philosopher_claims_route_through_source_gate(self):
        policy = load_script("workflow-policy.py")
        evidence = [{"bib_key": "LEWIS-WORLDS", "analysis_level": 2}]
        prompt = policy.philosopher_claim_gate("prompt-only", [], set(), 1)
        self.assertEqual(prompt["reason"], "philosopher-claim-prompt-only")
        missing = policy.philosopher_claim_gate("source-backed", evidence, set(), 1)
        self.assertEqual((missing["decision"], missing["hop"]), ("block", 1))
        shallow = policy.philosopher_claim_gate("source-backed", evidence, {"LEWIS-WORLDS"}, 3)
        self.assertEqual((shallow["decision"], shallow["hop"]), ("block", 2))
        passed = policy.philosopher_claim_gate(
            "source-backed",
            evidence,
            {"LEWIS-WORLDS"},
            2,
            {"LEWIS-WORLDS": {
                "analysis_level": 2,
                "verification_status": "verified",
                "source_hash_matches": True,
                "analysis_hash_matches": True,
            }},
        )
        self.assertEqual(passed["eligible_keys"], ["LEWIS-WORLDS"])


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


class PhilosopherDatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = load_script("philosopher-db.py")

    def make_repo(self, root: Path, with_profile: bool = False):
        paths = self.database.paths_for(root)
        paths["profiles"].mkdir(parents=True)
        paths["domains"].mkdir(parents=True)
        self.database.write_json(paths["domain_registry"], self.database.DOMAIN_REGISTRY)
        if with_profile:
            profile = {
                "profile_version": "1.0",
                "person_id": "test-philosopher",
                "identity": {
                    "display_name": "Test Philosopher",
                    "canonical_name": "Test Philosopher",
                    "aliases": ["Test Philosopher"],
                    "legacy_paths": [],
                },
                "claims": [],
                "domains": [],
                "relations": [],
                "created_at": "2026-07-19T00:00:00Z",
                "updated_at": "2026-07-19T00:00:00Z",
            }
            self.database.write_json(paths["profiles"] / "test-philosopher.json", profile)
        return paths

    def observation(self, artifact, bib_key, role, substantive, statement="", topics=None, person="New Thinker"):
        claims = []
        if statement:
            claims.append({"statement": statement, "category": "position", "locator": "summary:core_thesis"})
        return {
            "record_type": "observation-batch",
            "observation_id": f"PHO-{artifact}",
            "bib_key": bib_key,
            "artifact_id": artifact,
            "artifact_hash": artifact,
            "artifact_type": "summary",
            "analysis_level": 0.5,
            "source_metadata": {"author": person, "year": "2026", "title": artifact},
            "topics": topics or [],
            "people": [{
                "display_name": person,
                "canonical_name": person,
                "aliases": [],
                "role": role,
                "substantive": substantive,
                "claims": claims,
            }],
            "generated_at": "2026-07-19T00:00:00Z",
        }

    def test_live_migration_preserves_all_legacy_content_as_prompts(self):
        paths = self.database.paths_for(REPO_ROOT)
        profiles = self.database.load_profiles(paths["profiles"])
        self.assertEqual(len(profiles), 49)
        claims = [claim for profile in profiles.values() for claim in profile["claims"]]
        self.assertEqual(len(claims), 640)
        self.assertTrue(all(claim["support_status"] == "prompt-only" and not claim["evidence"] for claim in claims))
        for profile in profiles.values():
            for legacy in profile["identity"]["legacy_paths"]:
                resolved, ambiguous = self.database.resolve_person(Path(legacy).stem, profiles)
                self.assertFalse(ambiguous)
                self.assertEqual(resolved, profile["person_id"])

    def test_new_person_threshold_is_five_sources_three_substantive(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.make_repo(Path(temp))
            paths["observations"].mkdir(parents=True)
            roles = [("author", True), ("supporting", True), ("opposition", True), ("background", False), ("passing-mention", False)]
            for index, (role, substantive) in enumerate(roles):
                observation = self.observation(f"A{index}", f"KEY-{index}", role, substantive)
                self.database.write_json(paths["observations"] / f"{index}.json", observation)
            duplicate = self.observation("A5", "KEY-4", "background", False)
            self.database.write_json(paths["observations"] / "duplicate.json", duplicate)
            state, _ = self.database.rebuild_queue(paths, self.database.empty_state())
            pending = [item for item in state["candidates"].values() if item["candidate_type"] == "new-person"]
            self.assertEqual(len(pending), 1)
            person = next(iter(state["people"].values()))
            self.assertEqual(len(person["source_keys"]), 5)
            self.assertEqual(len(person["substantive_source_keys"]), 3)

    def test_existing_profile_gets_immediate_candidate_and_domain_promotion(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.make_repo(Path(temp), with_profile=True)
            paths["observations"].mkdir(parents=True)
            first = self.observation("A1", "KEY-1", "author", True, "Claim one", ["metaphysics"], "Test Philosopher")
            second = self.observation("A2", "KEY-2", "background", False, topics=["grounding"], person="Test Philosopher")
            self.database.write_json(paths["observations"] / "1.json", first)
            self.database.write_json(paths["observations"] / "2.json", second)
            state, profiles = self.database.rebuild_queue(paths, self.database.empty_state())
            pending = [item for item in state["candidates"].values() if item["status"] == "pending"]
            self.assertEqual(len(pending), 1)
            self.assertEqual(pending[0]["candidate_type"], "new-claim")
            self.assertEqual(self.database.synchronize_domains(paths, state, profiles), 1)
            profile = self.database.load_profiles(paths["profiles"])["test-philosopher"]
            self.assertEqual(profile["domains"][0]["support_status"], "source-backed")
            self.assertEqual({item["bib_key"] for item in profile["domains"][0]["evidence"]}, {"KEY-1", "KEY-2"})

    def test_observe_is_idempotent_and_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root, with_profile=True)
            summary = root / "summary.txt"
            payload = {
                "summary_id": "SUM-ONE",
                "bib_key": "KEY-ONE",
                "source_metadata": {"title": "One", "author": "Test Philosopher", "year": "2026"},
                "core_thesis": "One claim",
                "topics": ["metaphysics"],
                "philosopher_observations": [],
                "generated_at": "2026-07-19T00:00:00Z",
            }
            summary.write_text("```json\n" + json.dumps(payload) + "\n```\n", encoding="utf-8")
            dry = self.database.observe(paths, [summary], True, None)
            self.assertEqual(dry["changed"], 1)
            self.assertFalse(paths["state"].exists())
            first = self.database.observe(paths, [summary], False, None)
            second = self.database.observe(paths, [summary], False, None)
            self.assertEqual((first["changed"], second["unchanged"]), (1, 1))
            state = self.database.load_state(paths["state"])
            self.assertEqual(len(state["processed_artifacts"]), 1)
            self.assertEqual(len(state["candidates"]), 1)

    def test_candidate_approve_reject_and_reopen(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root, with_profile=True)
            paths["observations"].mkdir(parents=True)
            observation = self.observation("A1", "KEY-1", "author", True, "Approved claim", person="Test Philosopher")
            self.database.write_json(paths["observations"] / "1.json", observation)
            state, _ = self.database.rebuild_queue(paths, self.database.empty_state())
            self.database.write_json(paths["state"], state)
            cid = next(iter(state["candidates"]))
            self.database.approve_candidate(paths, cid)
            profile = self.database.load_profiles(paths["profiles"])["test-philosopher"]
            self.assertEqual(profile["claims"][0]["support_status"], "source-backed")
            self.assertIn("approved_at", profile["claims"][0]["evidence"][0])
            second = self.observation("A2", "KEY-2", "author", True, "Rejected claim", person="Test Philosopher")
            self.database.write_json(paths["observations"] / "2.json", second)
            state, _ = self.database.rebuild_queue(paths, self.database.load_state(paths["state"]))
            self.database.write_json(paths["state"], state)
            cid2 = next(item["candidate_id"] for item in state["candidates"].values() if item["status"] == "pending")
            self.assertEqual(self.database.change_candidate_status(paths, cid2, "reject")["status"], "rejected")
            self.assertEqual(self.database.change_candidate_status(paths, cid2, "reopen")["status"], "pending")

    def test_changed_artifact_supersedes_only_removed_candidate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root, with_profile=True)
            summary = root / "summary.txt"
            payload = {
                "summary_id": "SUM-CHANGE",
                "bib_key": "KEY-CHANGE",
                "source_metadata": {"title": "Change", "author": "Test Philosopher", "year": "2026"},
                "core_thesis": "Stable claim",
                "topics": [],
                "generated_at": "2026-07-19T00:00:00Z",
            }
            summary.write_text("```json\n" + json.dumps(payload) + "\n```\n", encoding="utf-8")
            self.database.observe(paths, [summary], False, None)
            original = next(iter(self.database.load_state(paths["state"])["candidates"]))
            payload["topics"] = ["metaphysics"]
            summary.write_text("```json\n" + json.dumps(payload) + "\n```\n", encoding="utf-8")
            self.database.observe(paths, [summary], False, None)
            self.assertEqual(self.database.load_state(paths["state"])["candidates"][original]["status"], "pending")
            payload["core_thesis"] = "Replacement claim"
            summary.write_text("```json\n" + json.dumps(payload) + "\n```\n", encoding="utf-8")
            self.database.observe(paths, [summary], False, None)
            candidates = self.database.load_state(paths["state"])["candidates"]
            self.assertEqual(candidates[original]["status"], "superseded")
            self.assertEqual(sum(item["status"] == "pending" for item in candidates.values()), 1)

    def test_conflict_adds_evidence_and_marks_existing_claim(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root, with_profile=True)
            profile_path = paths["profiles"] / "test-philosopher.json"
            profile = self.database.read_json(profile_path)
            profile["claims"].append({
                "claim_id": "P-test-philosopher-C0001",
                "category": "position",
                "statement": "Original wording",
                "support_status": "prompt-only",
                "dispute_status": "unmarked",
                "status": "active",
                "evidence": [],
            })
            self.database.write_json(profile_path, profile)
            paths["observations"].mkdir(parents=True)
            observation = self.observation("A1", "KEY-1", "opposition", True, person="Test Philosopher")
            observation["people"][0]["claims"] = [{
                "statement": "Contrary attribution",
                "category": "position",
                "locator": "analysis:conflict",
                "candidate_type": "conflict",
                "claim_id": "P-test-philosopher-C0001",
            }]
            self.database.write_json(paths["observations"] / "1.json", observation)
            state, _ = self.database.rebuild_queue(paths, self.database.empty_state())
            self.database.write_json(paths["state"], state)
            cid = next(iter(state["candidates"]))
            self.database.approve_candidate(paths, cid, merge_claim_id="P-test-philosopher-C0001")
            claim = self.database.read_json(profile_path)["claims"][0]
            self.assertEqual(claim["statement"], "Original wording")
            self.assertEqual(claim["dispute_status"], "contested")
            self.assertEqual(claim["support_status"], "source-backed")
            self.assertEqual(claim["evidence"][0]["bib_key"], "KEY-1")


class AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((WORKFLOW_ROOT / "manifest.json").read_text(encoding="utf-8"))

    def test_manifest_inventory(self):
        counts = {kind: 0 for kind in ("skill", "workflow", "role")}
        for item in self.manifest["items"]:
            counts[item["kind"]] += 1
        self.assertEqual(counts, {"skill": 30, "workflow": 9, "role": 7})

    def test_philosopher_workflow_is_registered(self):
        item = self.workflow_item("philosophers")
        self.assertEqual(item["dependencies"], [])
        self.assertEqual(item["capabilities"], ["read", "search", "write"])

    def workflow_item(self, workflow_id: str) -> dict:
        return next(item for item in self.manifest["items"] if item["id"] == workflow_id)

    def test_key_workflow_sections(self):
        required = {
            "reconstruct": [
                "Preplan and coverage ledger", "Executive summary and argument reconstruction",
                "Only the Level 2 and Level 3 sections", "Domain-specific findings",
                "Open questions and remaining coverage gaps",
            ],
            "evaluate": [
                "Preplan", "Inference and fallacy baseline", "One labeled section",
                "highest-priority revisions", "coverage gaps and not-applicable dimensions",
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
        self.assertIn("phil-dialectical-map", reconstruct)
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
