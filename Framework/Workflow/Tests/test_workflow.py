from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = WORKFLOW_ROOT / "Scripts"
REPO_ROOT = WORKFLOW_ROOT.parent.parent


def load_script(name: str, directory: Path | None = None):
    path = (directory or SCRIPTS) / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PolicyTests(unittest.TestCase):
    def test_nested_projects_have_outer_workflow_bridges(self):
        projects = REPO_ROOT / "Private/Projects"
        for project in sorted(path for path in projects.iterdir() if path.is_dir()):
            self.assertTrue((project / "PROJECT.md").is_file(), project)
        workflow_bridge = REPO_ROOT / "Private/.agents/skills/phil-tutor/SKILL.md"
        self.assertTrue(workflow_bridge.is_file())
        bridge_text = workflow_bridge.read_text(encoding="utf-8")
        self.assertIn("External Workflow Bridge", bridge_text)
        self.assertIn("<outer-root>/.agents/skills/phil-tutor/SKILL.md", bridge_text)
        self.assertNotIn("## Usage", bridge_text)
        for project in sorted(path for path in projects.iterdir() if path.is_dir()):
            local_bridge = project / ".agents/skills/phil-tutor/SKILL.md"
            self.assertTrue(local_bridge.is_file(), project)
            self.assertIn("name: phil-tutor", local_bridge.read_text(encoding="utf-8"))

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
        cls.migration = json.loads(
            (WORKFLOW_ROOT / "Migration/migration-v0.7.json").read_text(encoding="utf-8")
        )

    def kinds(self):
        kinds: dict[str, list[dict]] = {}
        for item in self.manifest["items"]:
            kinds.setdefault(item["kind"], []).append(item)
        return kinds

    def test_manifest_inventory_matches_plan(self):
        kinds = self.kinds()
        self.assertEqual(len(kinds.get("skill", [])), 4)
        self.assertEqual(len(kinds.get("method_package", [])), 5)
        self.assertEqual(len(kinds.get("method", [])), 30)
        self.assertEqual(len(kinds.get("service", [])), 5)
        self.assertEqual(len(kinds.get("command", [])), 1)
        self.assertEqual(
            sorted(item["id"] for item in kinds["skill"]),
            ["phil-research", "phil-review", "phil-tutor", "phil-write"],
        )

    def test_exposure_lists_exactly_the_skills(self):
        self.assertEqual(
            sorted(self.manifest["exposure"]["skills"]),
            sorted(item["id"] for item in self.kinds()["skill"]),
        )

    def test_each_runtime_exposes_exactly_four_skills(self):
        for root in (REPO_ROOT / ".claude/skills", REPO_ROOT / ".agents/skills"):
            names = sorted(path.parent.name for path in root.glob("*/SKILL.md"))
            self.assertEqual(names, ["phil-research", "phil-review", "phil-tutor", "phil-write"], root)
        self.assertFalse((REPO_ROOT / ".claude/agents").exists())
        leftovers = sorted((REPO_ROOT / ".agents/skills").glob("source-command-*"))
        self.assertEqual(leftovers, [])

    def test_claude_wrappers_delegate_and_are_not_canonical(self):
        wrappers = sorted(path.stem for path in (REPO_ROOT / ".claude/commands").glob("*.md"))
        self.assertEqual(wrappers, sorted(self.manifest["exposure"]["claude_command_wrappers"]))
        for wrapper in (REPO_ROOT / ".claude/commands").glob("*.md"):
            text = wrapper.read_text(encoding="utf-8")
            self.assertIn("Delegation only", text)
            self.assertIn("not a canonical definition", text)

    def test_research_mode_contracts_exist_and_are_isolated(self):
        modes_dir = WORKFLOW_ROOT / "Skills/phil-research/references/modes"
        self.assertEqual(
            sorted(path.stem for path in modes_dir.glob("*.md")),
            ["comment", "evaluate", "ingest", "philosophers", "reconstruct"],
        )
        generated = REPO_ROOT / ".claude/skills/phil-research/references/modes/reconstruct.md"
        self.assertTrue(generated.is_file())
        self.assertIn("Generated from Framework/Workflow", generated.read_text(encoding="utf-8"))

    def test_methods_tree_matches_manifest_and_headers_carry_metadata(self):
        methods = {item["id"]: item for item in self.kinds()["method"]}
        files = {p.relative_to(WORKFLOW_ROOT).as_posix() for p in (WORKFLOW_ROOT / "Methods").rglob("*.md")
                 if "references" not in p.parts}
        self.assertEqual(files, {item["source"] for item in methods.values()})
        for item in methods.values():
            text = (WORKFLOW_ROOT / item["source"]).read_text(encoding="utf-8")
            self.assertIn(f"id: {item['id']}", text)
            self.assertIn("side_effects: read-only", text)
            self.assertTrue(item["legacy_ids"])
            self.assertTrue(item["label"])

    def test_conditional_references_are_preserved_and_linked(self):
        """v0.6 examples/checklists must survive as conditional references named by their method."""
        references = sorted((WORKFLOW_ROOT / "Methods").glob("*/references/*.md"))
        self.assertGreaterEqual(len(references), 50)
        for reference in references:
            slug = reference.stem.rsplit("-", 1)[0]
            package = reference.parent.parent.name
            method = WORKFLOW_ROOT / "Methods" / package / f"{slug}.md"
            self.assertTrue(method.is_file(), reference)
            text = method.read_text(encoding="utf-8")
            self.assertIn(f"references/{reference.name}", text, f"{method.name} must name {reference.name}")
            header = reference.read_text(encoding="utf-8")
            self.assertIn("conditional reference", header.lower(), reference)

    def test_migration_map_covers_all_30_legacy_ids_with_labels(self):
        method_map = self.migration["method_map"]
        self.assertEqual(len(method_map), 30)
        manifest_legacy = {
            legacy
            for item in self.kinds()["method"]
            for legacy in item["legacy_ids"]
        }
        self.assertEqual(manifest_legacy, set(method_map))
        for old, entry in method_map.items():
            self.assertIn("label", entry, old)
            self.assertRegex(entry["method_id"], r"^method\.[a-z-]+\.[a-z-]+$")

    def test_removed_entrypoints_resolve_with_replacement_and_mode(self):
        policy = load_script("workflow-policy.py")
        replaced = {
            "phil:reconstruct": "phil:research reconstruct",
            "phil:evaluate": "phil:research evaluate",
            "phil:comment": "phil:research comment",
            "phil:ingest": "phil:research ingest",
            "phil:philosophers": "phil:research philosophers",
            "phil:pipeline": "phil:full start",
        }
        for old, new in replaced.items():
            result = policy.removed_entrypoint(old)
            self.assertEqual(result["replacement"], new, old)
            self.assertIn(old, result["message"])
            self.assertIn(new, result["message"])
            self.assertNotIn("silently", result["message"].replace("No alias or deprecation shim is retained.", ""))

    def test_doctor_inventory_passes(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "workflow-doctor.py")],
            cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_stale_phrase_scan_detects_obsolete_counts(self):
        doctor = load_script("workflow-doctor.py")
        failures: list[str] = []
        doctor.check_stale_phrases(failures)
        self.assertEqual(failures, [])
        with tempfile.TemporaryDirectory() as temp:
            probe_root = Path(temp) / ".claude"
            probe_root.mkdir()
            (probe_root / "probe.md").write_text("we had 39 skills back then", encoding="utf-8")
            original_phrases = list(doctor.STALE_PHRASES)
            original_repo = doctor.REPO_ROOT
            doctor.STALE_PHRASES = ("39 skills",)
            doctor.REPO_ROOT = Path(temp)
            try:
                failures2: list[str] = []
                doctor.check_stale_phrases(failures2)
            finally:
                doctor.STALE_PHRASES = original_phrases
                doctor.REPO_ROOT = original_repo
        self.assertTrue(any("39 skills" in failure for failure in failures2))

    def test_core_model_selection_is_neutral(self):
        provider_model = re.compile(r"\b(?:opus|sonnet|haiku|gpt-[A-Za-z0-9.-]+)\b", re.IGNORECASE)
        for directory in ("Skills", "Methods", "Services", "Commands", "Rules"):
            for path in (WORKFLOW_ROOT / directory).rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(provider_model.search(text), path)
                self.assertNotRegex(text, r"^model:\s*", path)
                self.assertNotIn("quality_tier:", text, path)

    def test_cost_aware_delegation_is_session_scoped_and_reversible(self):
        text = (WORKFLOW_ROOT / "Rules/runtime-compatibility.md").read_text(encoding="utf-8")
        self.assertIn("economic_delegation = unknown | enabled | disabled", text)
        self.assertIn("ask the user once", text)
        self.assertRegex(text, r"Never persist\s+this authorization")
        self.assertIn("the user may revoke it", text)
        self.assertIn("do not ask or delegate again in that session", text)
        self.assertIn("parent task must validate", text)

    def test_delegation_guidance_is_generated_into_each_runtime(self):
        for root in (REPO_ROOT / ".claude/skills/phil-research", REPO_ROOT / ".agents/skills/phil-research"):
            text = (root / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("session-scoped policy", text)
            self.assertIn("lower-cost host candidate", text)

    def test_skill_entrypoints_stay_under_the_line_ceiling(self):
        for skill in self.kinds()["skill"]:
            text = (WORKFLOW_ROOT / skill["source"]).read_text(encoding="utf-8")
            self.assertLess(len(text.splitlines()), 500, skill["id"])

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

    def test_manifest_rejects_exposure_mismatch(self):
        skills = [item for item in self.manifest["items"] if item["kind"] == "skill"]

        def mutate(data):
            next(item for item in data["items"] if item["id"] == skills[0]["id"]).__setitem__("id", "phil-extra")

        self.assert_manifest_rejected(mutate)

    def test_manifest_rejects_unknown_package_member(self):
        package = next(item for item in self.manifest["items"] if item["kind"] == "method_package")

        def mutate(data):
            next(item for item in data["items"] if item["id"] == package["id"])["members"].append("method.nope.nope")

        self.assert_manifest_rejected(mutate)

    def test_manifest_rejects_unknown_consumer(self):
        method = next(item for item in self.manifest["items"] if item["kind"] == "method")

        def mutate(data):
            target = next(item for item in data["items"] if item["id"] == method["id"])
            target["consumers"].append("phil-nonsense/mode")

        self.assert_manifest_rejected(mutate)

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

    def test_second_generation_leaves_no_diff(self):
        before = subprocess.run(
            ["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
        ).stdout
        subprocess.run(
            [sys.executable, str(SCRIPTS / "build-adapters.py")], cwd=REPO_ROOT,
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        after = subprocess.run(
            ["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
        ).stdout
        self.assertEqual(before, after, "regeneration produced a diff — adapters are not idempotent")


class ContractTextTests(unittest.TestCase):
    """Enforce the load-bearing clauses of the 0.7 plan inside the canonical files."""

    def read(self, relative: str) -> str:
        return (WORKFLOW_ROOT / relative).read_text(encoding="utf-8")

    def test_every_command_and_mode_is_documented(self):
        expected = {
            "Skills/phil-research/SKILL.md": ["`ingest`", "`reconstruct`", "`evaluate`", "`comment`", "`philosophers`"],
            "Skills/phil-tutor/SKILL.md": ["reading", "incubating"],
            "Skills/phil-write/SKILL.md": ["outline", "draft", "revision"],
            "Skills/phil-review/SKILL.md": ["full", "targeted", "re-review"],
            "Commands/phil-full.md": ["`start`", "`status`", "`resume`"],
        }
        for relative, modes in expected.items():
            text = self.read(relative)
            for mode in modes:
                self.assertIn(mode, text, f"{relative} must document mode {mode}")
        guide = (WORKFLOW_ROOT / "Templates/Root/root-guidance.md").read_text(encoding="utf-8")
        for command in ("phil:research", "phil:tutor", "phil:write", "phil:review", "phil:full"):
            self.assertIn(command, guide)

    def test_routing_rules_are_present_in_each_skill(self):
        import re as re_module
        for relative in ("Skills/phil-research/SKILL.md", "Skills/phil-tutor/SKILL.md",
                         "Skills/phil-write/SKILL.md", "Skills/phil-review/SKILL.md"):
            text = self.read(relative)
            self.assertIsNotNone(
                re_module.search(r"explicit mode( argument)? always wins|explicit mode wins", text, re_module.IGNORECASE),
                relative,
            )
            self.assertIn("one focused question", text.replace("**", ""), relative)

    def test_collaboration_modes_share_gates_and_split_authority(self):
        text = self.read("Skills/phil-write/SKILL.md")
        self.assertIn("identical quality gates", text)
        self.assertIn("passage-level authorization", text)
        self.assertIn("within the approved outline", text)
        self.assertIn("[AI 补全]", text)
        self.assertIn("user-led", text)
        self.assertIn("assistant-led", text)

    def test_writing_protocol_sequence_and_artifacts(self):
        text = self.read("Skills/phil-write/SKILL.md")
        plain = text.replace("**", "")
        self.assertIn("intake -> outline -> outline approval -> section brief -> draft -> section audit -> revision -> citation closure", plain)
        self.assertIn("{topic}-outline.txt", text)
        self.assertIn("{topic}-conception.txt", text)
        self.assertIn("never silently delete, collapse, or mark a finding resolved", plain.lower().replace("never silently", "never silently"))
        self.assertIn("Never silently delete, collapse, or mark a finding resolved", plain)
        self.assertIn("cannot be waived", plain)

    def test_review_is_read_only_and_findings_drive_revision(self):
        text = self.read("Skills/phil-review/SKILL.md")
        self.assertIn("never edits the draft", text)
        self.assertIn("Finding ledger", text)
        self.assertIn("project-state.py finding", text)
        self.assertIn("without evidence", text.replace("**", ""))

    def test_research_kernel_invariants_and_write_isolation(self):
        text = self.read("Skills/phil-research/SKILL.md")
        self.assertIn("only `ingest`", text)
        self.assertIn("Citation Gate boundary", text)
        self.assertIn("two hops", text)
        self.assertIn("never silently load an entire package", text)
        for mode in ("ingest", "reconstruct", "evaluate", "comment", "philosophers"):
            self.assertTrue(
                (WORKFLOW_ROOT / "Skills/phil-research/references/modes" / f"{mode}.md").is_file(), mode
            )

    def test_full_pipeline_state_rules(self):
        text = self.read("Commands/phil-full.md")
        self.assertIn("intake -> research -> [incubation] -> outline -> section_brief -> draft -> section_audit -> review -> revision -> citation_closure -> complete", text)
        self.assertIn("must not overwrite an unfinished run", text)
        self.assertIn("earliest affected stage", text)
        self.assertIn("**cannot be waived**", text)
        self.assertIn("never duplicates the dialogue protocol", text)

    def test_evidence_unit_contract_has_required_fields(self):
        import json as json_module
        contract = json_module.loads((WORKFLOW_ROOT / "Contracts/evidence-unit.schema.json").read_text(encoding="utf-8"))
        required = set(contract["required"])
        for field in ("locator", "text_span", "source_sha256", "extraction_version", "unit_sha256", "verification_status"):
            self.assertIn(field, required)
        self.assertIn("coverage_label", contract["properties"])
        self.assertIn("neighborhood", contract["properties"])
        self.assertIn("selection_reason", contract["properties"])

    def test_services_declare_authority_boundaries(self):
        for service in (WORKFLOW_ROOT / "Services").glob("*.md"):
            header = service.read_text(encoding="utf-8").split("---")[1]
            self.assertIn("authority:", header, service.name)
            self.assertIn("consumers:", header, service.name)


class MigrationScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.migration = json.loads(
            (WORKFLOW_ROOT / "Migration/migration-v0.7.json").read_text(encoding="utf-8")
        )

    def test_canonical_coverage_fails_on_unknown_ids(self):
        script = load_script("migrate-v07.py", WORKFLOW_ROOT / "Migration")
        with self.assertRaises(script.MigrationError):
            script.canonical_coverage("not-a-known-coverage", self.migration)
        self.assertEqual(
            script.canonical_coverage("charity audit", self.migration),
            "method.argument.charity-check",
        )
        self.assertEqual(
            script.canonical_coverage("phil-charity-check", self.migration),
            "method.argument.charity-check",
        )
        self.assertEqual(
            script.canonical_coverage("method.argument.charity-check", self.migration),
            "method.argument.charity-check",
        )

    def test_v1_state_migration_maps_stages_and_gates(self):
        script = load_script("migrate-v07.py", WORKFLOW_ROOT / "Migration")
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            project.mkdir()
            state_path = project / "topic-workflow-state.json"
            state_path.write_text(json.dumps({
                "schema_version": 1,
                "project": "topic",
                "current_stage": 4,
                "status": "paused",
                "artifacts": [{
                    "path": "topic-draft.txt", "hash": "a" * 64,
                    "workflow": "write", "version": "1", "level": None, "stale": False,
                }],
                "gates": [{"stage": 4, "decision": "pass", "reason": "ok", "recorded_at": "2026-01-01T00:00:00Z"}],
                "next_action": None,
            }), encoding="utf-8")
            changes = script.migrate_workflow_state(state_path, self.migration)
            self.assertTrue(changes)
            migrated = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(migrated["schema_version"], 2)
            self.assertEqual(migrated["stage"], "outline")
            self.assertEqual(migrated["status"], "awaiting_user")
            self.assertEqual(migrated["approvals"]["outline"]["decision"], "approved")
            self.assertEqual(migrated["artifacts"][0]["path"], "topic-draft.txt")

    def test_writable_whitelist_and_protection(self):
        script = load_script("migrate-v07.py", WORKFLOW_ROOT / "Migration")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            meta = root / "Private/Bibliography/Analysis/X_2000_T.analysis.meta.json"
            meta.parent.mkdir(parents=True)
            meta.write_text("{}", encoding="utf-8")
            script.check_writable(meta, root)
            notes = root / "Private/Projects/p/working-notes.md"
            with self.assertRaises(script.MigrationError):
                script.check_writable(notes, root)
            stray = root / "Private/Projects/p/evil.txt"
            with self.assertRaises(script.MigrationError):
                script.check_writable(stray, root)


if __name__ == "__main__":
    unittest.main()
