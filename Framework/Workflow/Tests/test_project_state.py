from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load(name):
    path = ROOT / "Scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class IdeaLedgerTests(unittest.TestCase):
    def setUp(self): self.ledger = load("idea-ledger.py")

    def test_record_is_idempotent_and_active_needs_confirmation(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            data = self.ledger.empty_ledger(project)
            idea, changed = self.ledger.record(data, "A thesis", "user", "parked", "too broad", ["scope"], [], [{"event": "scope-change", "description": "narrower project"}])
            duplicate, duplicate_changed = self.ledger.record(data, "  a   THESIS ", "joint", "parked", "", [], [], [])
            self.assertTrue(changed); self.assertFalse(duplicate_changed); self.assertEqual(idea["id"], duplicate["id"])
            with self.assertRaises(ValueError):
                self.ledger.record(data, "An active thesis", "user", "active", "", [], [], [])
            with self.assertRaises(ValueError): self.ledger.transition(data, idea["id"], "active", "revived", False, None)
            self.ledger.transition(data, idea["id"], "active", "revived", True, None)

    def test_surfacing_does_not_change_status(self):
        with tempfile.TemporaryDirectory() as temp:
            data = self.ledger.empty_ledger(Path(temp) / "topic")
            idea, _ = self.ledger.record(data, "A thesis", "user", "parked", "", [], [], [])
            surfaced = self.ledger.mark_surfaced(data, idea["id"], "new evidence")
            self.assertEqual(surfaced["status"], "parked")
            self.assertEqual(surfaced["last_surfaced_reason"], "new evidence")
            self.assertIsNotNone(surfaced["last_surfaced_at"])

    def test_candidate_filtering_has_event_and_overlap_constraints(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"; data = self.ledger.empty_ledger(project)
            for number in range(3):
                self.ledger.record(data, f"idea {number}", "user", "parked", "", ["anger"], ["KEY"], [{"event": "new-evidence", "description": "evidence"}])
            self.assertEqual(len(self.ledger.candidates(data, "new-evidence", ["anger"], [])), 2)
            self.assertEqual(self.ledger.candidates(data, "new-evidence", ["other"], []), [])
            data["ideas"][0]["status"] = "rejected"
            self.assertEqual(self.ledger.candidates(data, "new-evidence", ["anger"], []), [data["ideas"][1], data["ideas"][2]])
            requested = self.ledger.candidates(data, "user-request", ["anger"], [])
            self.assertEqual(requested[0], data["ideas"][0])

    def test_validation_requires_complete_idea_shape(self):
        with tempfile.TemporaryDirectory() as temp:
            data = self.ledger.empty_ledger(Path(temp) / "topic")
            data["ideas"].append({"id": "IDEA-001"})
            self.assertIn("invalid idea fields", self.ledger.validate(data))

    def test_validate_command_reports_corrupt_ledger_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            project.mkdir()
            path = self.ledger.ledger_path(project)
            path.write_text(json.dumps({"ideas": "invalid"}), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "Scripts/idea-ledger.py"), "--project-dir", str(project), "validate"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn('"valid": false', result.stdout)

    def test_superseded_idea_requires_another_existing_id(self):
        with tempfile.TemporaryDirectory() as temp:
            data = self.ledger.empty_ledger(Path(temp) / "topic")
            old, _ = self.ledger.record(data, "Old", "user", "parked", "", [], [], [])
            new, _ = self.ledger.record(data, "New", "user", "parked", "", [], [], [])
            self.ledger.transition(data, old["id"], "superseded", "replaced", False, new["id"])
            self.assertEqual(self.ledger.validate(data), [])
            old["superseded_by"] = old["id"]
            self.assertIn(f"{old['id']}: invalid superseded_by", self.ledger.validate(data))

    def test_record_rejects_malformed_write_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            data = self.ledger.empty_ledger(Path(temp) / "topic")
            invalid_inputs = [
                ("   ", "user", "parked", [], [], []),
                ("Idea", "user", "superseded", [], [], []),
                ("Idea", "user", "parked", [""], [], []),
                ("Idea", "user", "parked", [], [""], []),
                ("Idea", "user", "parked", [], [], [{"event": "wrong", "description": "x"}]),
            ]
            for statement, provenance, status, keywords, bib_keys, triggers in invalid_inputs:
                with self.assertRaises(ValueError):
                    self.ledger.record(data, statement, provenance, status, "", keywords, bib_keys, triggers)

    def test_transition_enforces_supersession_target(self):
        with tempfile.TemporaryDirectory() as temp:
            data = self.ledger.empty_ledger(Path(temp) / "topic")
            old, _ = self.ledger.record(data, "Old", "user", "parked", "", [], [], [])
            with self.assertRaises(ValueError):
                self.ledger.transition(data, old["id"], "superseded", "", False, old["id"])
            with self.assertRaises(ValueError):
                self.ledger.transition(data, old["id"], "parked", "", False, "IDEA-999")

    def test_save_refuses_invalid_ledger(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            data = self.ledger.empty_ledger(project)
            data["ideas"].append({"id": "IDEA-001"})
            with self.assertRaises(ValueError):
                self.ledger.save(project, data)


class WorkflowStateTests(unittest.TestCase):
    def setUp(self): self.state = load("project-state.py")

    def test_changed_artifact_becomes_stale(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"; project.mkdir(); artifact = project / "draft.txt"; artifact.write_text("one", encoding="utf-8")
            state = self.state.empty_state(project)
            state["artifacts"].append({"path": "draft.txt", "hash": self.state.sha256(artifact), "workflow": "write", "version": "1", "level": 1, "stale": False})
            self.assertFalse(self.state.refresh_artifacts(project, state))
            artifact.write_text("two", encoding="utf-8")
            self.assertTrue(self.state.refresh_artifacts(project, state)); self.assertTrue(state["artifacts"][0]["stale"])

    def test_validation_rejects_stage_outside_range(self):
        with tempfile.TemporaryDirectory() as temp:
            state = self.state.empty_state(Path(temp) / "topic"); state["current_stage"] = 7
            self.assertIn("current_stage must be 0 through 6", self.state.validate(state))

    def test_validate_command_reports_corrupt_state_without_refreshing(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            project.mkdir()
            path = self.state.state_path(project)
            path.write_text(json.dumps({"artifacts": "invalid"}), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "Scripts/project-state.py"), "--project-dir", str(project), "validate"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn('"valid": false', result.stdout)

    def test_state_rejects_unsafe_artifact_path_and_invalid_save(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            state = self.state.empty_state(project)
            state["artifacts"].append({
                "path": "../outside.txt",
                "hash": "0" * 64,
                "workflow": "write",
                "version": "1",
                "level": None,
                "stale": False,
            })
            self.assertIn("invalid artifact path", self.state.validate(state))
            with self.assertRaises(ValueError):
                self.state.save(project, state)


if __name__ == "__main__": unittest.main()
