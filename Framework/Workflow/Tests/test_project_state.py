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

    def test_save_is_atomic_and_removes_temp_on_failure(self):
        from unittest import mock
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            data = self.ledger.empty_ledger(project)
            self.ledger.save(project, data)
            target = self.ledger.ledger_path(project)
            before = target.read_bytes()
            data["next_id"] = 2
            with mock.patch.object(self.ledger.os, "replace", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    self.ledger.save(project, data)
            self.assertEqual(target.read_bytes(), before)
            self.assertEqual(list(project.glob("*.tmp")), [])

    def test_transition_appends_status_history(self):
        with tempfile.TemporaryDirectory() as temp:
            data = self.ledger.empty_ledger(Path(temp) / "topic")
            idea, _ = self.ledger.record(data, "A thesis", "user", "parked", "too broad", [], [], [])
            self.ledger.transition(data, idea["id"], "rejected", "counterexample", False, None)
            self.assertEqual(len(idea["status_history"]), 1)
            entry = idea["status_history"][0]
            self.assertEqual(set(entry), {"from_status", "to_status", "from_reason", "superseded_by", "at"})
            self.assertEqual(entry["from_status"], "parked")
            self.assertEqual(entry["to_status"], "rejected")
            self.assertEqual(entry["from_reason"], "too broad")
            self.assertIsNone(entry["superseded_by"])
            self.assertEqual(self.ledger.validate(data), [])

    def test_status_history_records_previous_supersession_value(self):
        with tempfile.TemporaryDirectory() as temp:
            data = self.ledger.empty_ledger(Path(temp) / "topic")
            old, _ = self.ledger.record(data, "Old", "user", "parked", "", [], [], [])
            new, _ = self.ledger.record(data, "New", "user", "parked", "", [], [], [])
            self.ledger.transition(data, old["id"], "superseded", "replaced", False, new["id"])
            self.ledger.transition(data, old["id"], "parked", "revived", False, None)
            self.assertEqual(old["status_history"][1]["from_status"], "superseded")
            self.assertEqual(old["status_history"][1]["superseded_by"], new["id"])
            self.assertEqual(self.ledger.validate(data), [])

    def test_corrupt_ledger_reports_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "topic"
            project.mkdir()
            self.ledger.ledger_path(project).write_text("{not json", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "Scripts/idea-ledger.py"), "--project-dir", str(project), "status"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('"error"', result.stdout)
            self.assertNotIn("Traceback", result.stderr)


class WorkflowStateV2Tests(unittest.TestCase):
    def setUp(self): self.state = load("project-state.py")

    def args(self, command, **kwargs):
        namespace = type("Args", (), {"command": command})()
        defaults = {
            "collaboration": None, "kind": None, "path": None, "stage": None,
            "gate": None, "decision": None, "reason": "", "artifact_path": None,
            "id": None, "severity": None, "target": None, "status": None,
            "review_sha256": "", "note": "", "report": None, "verdict": None,
            "unresolved_high": None, "entrypoint": "phil-full",
        }
        for key, value in defaults.items():
            setattr(namespace, key, kwargs.get(key, value))
        return namespace

    def project(self, temp) -> Path:
        project = Path(temp) / "topic"
        project.mkdir()
        return project

    def test_init_refuses_to_overwrite_unfinished_run_and_allows_after_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            first = self.state.cmd_init(project, self.args("init", entrypoint="phil-full", collaboration="user-led"))
            self.assertEqual(first["action"], "started")
            refused = self.state.cmd_init(project, self.args("init", entrypoint="phil-full"))
            self.assertEqual(refused["action"], "refused")
            self.assertIn("resume", refused["reason"])
            state = self.state.load(project)
            state["status"] = "completed"
            self.state.save(project, state)
            second = self.state.cmd_init(project, self.args("init", entrypoint="phil-write"))
            self.assertEqual(second["action"], "started")
            self.assertNotEqual(second["run_id"], first["run_id"])

    def test_artifact_paths_must_be_posix_relative(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "a.txt").write_text("x", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.state.cmd_artifact(project, self.args("artifact", kind="draft-section", path="..\\outside.txt"))
            with self.assertRaises(ValueError):
                self.state.cmd_artifact(project, self.args("artifact", kind="draft-section", path="sub\\a.txt"))
            recorded = self.state.cmd_artifact(project, self.args("artifact", kind="draft-section", path="a.txt"))
            self.assertEqual(recorded["action"], "recorded")

    def test_resume_rewinds_to_earliest_affected_stage(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "c.txt").write_text("conception", encoding="utf-8")
            (project / "o.txt").write_text("outline", encoding="utf-8")
            self.state.cmd_init(project, self.args("init"))
            self.state.cmd_artifact(project, self.args("artifact", kind="conception", path="c.txt"))
            self.state.cmd_artifact(project, self.args("artifact", kind="outline", path="o.txt"))
            state = self.state.load(project)
            state["stage"] = "draft"
            self.state.save(project, state)
            (project / "c.txt").write_text("changed", encoding="utf-8")
            resumed = self.state.cmd_resume(project, self.args("resume"))
            self.assertEqual(resumed["action"], "stale")
            self.assertEqual(resumed["rewound_to"], "incubation")
            self.assertTrue(resumed["stale_artifacts"])
            self.assertIn("renewed user confirmation", resumed["request"])

    def test_completion_is_blocked_until_gates_close(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "review.txt").write_text("r", encoding="utf-8")
            self.state.cmd_init(project, self.args("init"))
            blocked = self.state.cmd_advance(project, self.args("advance", stage="complete"))
            self.assertEqual(blocked["action"], "refused")
            self.assertIn("outline", blocked["reason"])
            self.state.cmd_approve(project, self.args("approve", gate="outline", decision="waived", reason="user skip instruction"))
            blocked = self.state.cmd_advance(project, self.args("advance", stage="complete"))
            self.assertIn("citation closure", blocked["reason"])
            review_sha = self.state.sha256(project / "review.txt")
            self.state.cmd_finding(project, self.args("finding", id="F1", severity="high", target="s2", status="open", review_sha256=review_sha))
            self.state.cmd_approve(project, self.args("approve", gate="citation_closure", decision="pass", artifact_path="review.txt"))
            self.state.cmd_approve(project, self.args("approve", gate="citation_closure", decision="acknowledge"))
            blocked = self.state.cmd_advance(project, self.args("advance", stage="complete"))
            self.assertIn("F1", blocked["reason"])
            self.state.cmd_finding(project, self.args("finding", id="F1", severity="high", target="s2", status="resolved", review_sha256=review_sha, note="passage rewritten"))
            done = self.state.cmd_advance(project, self.args("advance", stage="complete"))
            self.assertEqual(done["status"], "completed")

    def test_closure_acknowledgement_requires_machine_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            self.state.cmd_init(project, self.args("init"))
            with self.assertRaises(ValueError):
                self.state.cmd_approve(project, self.args("approve", gate="citation_closure", decision="acknowledge"))

    def test_outline_waiver_requires_reason_and_deferral_requires_note(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            self.state.cmd_init(project, self.args("init"))
            with self.assertRaises(ValueError):
                self.state.cmd_approve(project, self.args("approve", gate="outline", decision="waived"))
            self.state.cmd_finding(project, self.args("finding", id="F1", severity="low", target="s1", status="open", review_sha256="0" * 64))
            with self.assertRaises(ValueError):
                self.state.cmd_finding(project, self.args("finding", id="F1", severity="low", target="s1", status="deferred"))

    def test_section_audit_blocks_on_unresolved_high(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "audit.txt").write_text("audit", encoding="utf-8")
            self.state.cmd_init(project, self.args("init"))
            recorded = self.state.cmd_audit(project, self.args("audit", report="audit.txt", verdict="block", unresolved_high=2))
            self.assertEqual(recorded["action"], "recorded")
            state = self.state.load(project)
            state["stage"] = "section_audit"
            self.state.save(project, state)
            self.state.cmd_audit(project, self.args("audit", report="audit.txt", verdict="pass", unresolved_high=0))
            status = self.state.cmd_status(project, self.args("status"))
            self.assertEqual(status["next_action"], "advance to review")

    def test_validation_rejects_bad_enums_and_duplicate_findings(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            state = self.state.empty_state(project)
            state["stage"] = "not-a-stage"
            self.assertIn("invalid stage", self.state.validate(state))
            state = self.state.empty_state(project)
            state["review_findings"] = [
                {"id": "F1", "severity": "high", "target": "s1", "status": "open", "source_review_sha256": "0" * 64},
                {"id": "F1", "severity": "low", "target": "s2", "status": "open", "source_review_sha256": "0" * 64},
            ]
            self.assertIn("duplicate finding id: F1", self.state.validate(state))

    def test_advance_refuses_backwards_movement(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            self.state.cmd_init(project, self.args("init"))
            state = self.state.load(project)
            state["stage"] = "review"
            self.state.save(project, state)
            result = self.state.cmd_advance(project, self.args("advance", stage="draft"))
            self.assertEqual(result["action"], "refused")
            self.assertIn("backwards", result["reason"])

    def test_status_reports_derived_next_action(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            self.state.cmd_init(project, self.args("init"))
            status = self.state.cmd_status(project, self.args("status"))
            self.assertEqual(status["outline_decision"], "pending")
            self.assertTrue(status["next_action"])

    def test_sha256_is_line_ending_stable_for_text_only(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            lf_txt = project / "lf.txt"; lf_txt.write_bytes(b"a\nb\n")
            crlf_txt = project / "crlf.txt"; crlf_txt.write_bytes(b"a\r\nb\r\n")
            self.assertEqual(self.state.sha256(lf_txt), self.state.sha256(crlf_txt))
            lf_pdf = project / "lf.pdf"; lf_pdf.write_bytes(b"a\nb\n")
            crlf_pdf = project / "crlf.pdf"; crlf_pdf.write_bytes(b"a\r\nb\r\n")
            self.assertNotEqual(self.state.sha256(lf_pdf), self.state.sha256(crlf_pdf))

    def test_save_is_atomic_and_removes_temp_on_failure(self):
        from unittest import mock
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            self.state.cmd_init(project, self.args("init"))
            target = self.state.state_path(project)
            before = target.read_bytes()
            state = self.state.load(project)
            state["next_action"] = "changed"
            with mock.patch.object(self.state.os, "replace", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    self.state.save(project, state)
            self.assertEqual(target.read_bytes(), before)
            self.assertEqual(list(project.glob("*.tmp")), [])

    def test_path_guard_rejects_absolute_and_drive_prefixed_forms(self):
        for value in ("/Windows/win.ini", "C:/x.txt", "C:x.txt", "//server/share/x.txt"):
            self.assertFalse(self.state.is_safe_relative_path(value), value)
        self.assertTrue(self.state.is_safe_relative_path("sub/a.txt"))

    def test_approve_records_path_and_stale_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "outline.txt").write_text("outline", encoding="utf-8")
            self.state.cmd_init(project, self.args("init"))
            self.state.cmd_approve(project, self.args(
                "approve", gate="outline", decision="approved", artifact_path="outline.txt"))
            state = self.state.load(project)
            self.assertEqual(state["approvals"]["outline"]["artifact_path"], "outline.txt")
            self.assertEqual(self.state.stale_approvals(project, state), [])
            (project / "outline.txt").write_text("changed", encoding="utf-8")
            self.assertEqual(self.state.stale_approvals(project, state), ["outline"])

            before = self.state.state_path(project).read_bytes()
            status = self.state.cmd_status(project, self.args("status"))
            self.assertEqual(self.state.state_path(project).read_bytes(), before)
            self.assertEqual(status["stale_approvals"], ["outline"])
            self.assertTrue(status["next_action"].startswith(
                "approval stale: outline; renewed confirmation required"))

            refused = self.state.cmd_advance(project, self.args("advance", stage="complete"))
            self.assertEqual(refused["action"], "refused")
            self.assertIn("stale approval: outline", refused["reason"])

            self.state.cmd_approve(project, self.args(
                "approve", gate="outline", decision="approved", artifact_path="outline.txt"))
            self.assertEqual(self.state.stale_approvals(project, self.state.load(project)), [])

    def test_undecided_approval_is_not_stale_and_completed_run_stays_completed(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "outline.txt").write_text("outline", encoding="utf-8")
            self.state.cmd_init(project, self.args("init"))
            self.state.cmd_approve(project, self.args(
                "approve", gate="outline", decision="rejected", artifact_path="outline.txt"))
            (project / "outline.txt").write_text("changed", encoding="utf-8")
            self.assertEqual(self.state.stale_approvals(project, self.state.load(project)), [])

            self.state.cmd_approve(project, self.args(
                "approve", gate="outline", decision="approved", artifact_path="outline.txt"))
            state = self.state.load(project)
            state["stage"], state["status"] = "complete", "completed"
            self.state.save(project, state)
            (project / "outline.txt").write_text("changed again", encoding="utf-8")
            resumed = self.state.cmd_resume(project, self.args("resume"))
            self.assertNotEqual(resumed.get("action"), "stale")
            self.assertEqual(self.state.load(project)["status"], "completed")

    def test_stale_approvals_flags_missing_files_and_skips_unrecorded_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "review.txt").write_text("review", encoding="utf-8")
            self.state.cmd_init(project, self.args("init"))
            self.state.cmd_approve(project, self.args("approve", gate="outline", decision="approved"))
            self.state.cmd_approve(project, self.args(
                "approve", gate="review", decision="accept", artifact_path="review.txt"))
            (project / "review.txt").unlink()
            self.assertEqual(self.state.stale_approvals(project, self.state.load(project)), ["review"])

    def test_resume_marks_stale_when_approval_artifact_changed(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            (project / "outline.txt").write_text("outline", encoding="utf-8")
            self.state.cmd_init(project, self.args("init"))
            self.state.cmd_approve(project, self.args(
                "approve", gate="outline", decision="approved", artifact_path="outline.txt"))
            (project / "outline.txt").write_text("changed", encoding="utf-8")
            resumed = self.state.cmd_resume(project, self.args("resume"))
            self.assertEqual(resumed["action"], "stale")
            self.assertEqual(resumed["stale_approvals"], ["outline"])
            state = self.state.load(project)
            self.assertEqual(state["status"], "stale")
            self.assertIn("approval stale: outline", state["next_action"])

    def test_approval_path_fields_are_optional_but_must_be_safe(self):
        project = Path(tempfile.gettempdir()) / "topic"
        state = self.state.empty_state(project)
        self.assertEqual(self.state.validate(state, "topic"), [])
        state["approvals"]["outline"]["artifact_path"] = "../escape.txt"
        self.assertIn("outline artifact_path must be a safe relative path",
                      self.state.validate(state, "topic"))

    def test_citation_pass_requires_artifact_path(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            self.state.cmd_init(project, self.args("init"))
            with self.assertRaises(ValueError):
                self.state.cmd_approve(project, self.args(
                    "approve", gate="citation_closure", decision="pass"))

    def test_neutralizing_high_finding_requires_note(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.project(temp)
            self.state.cmd_init(project, self.args("init"))
            self.state.cmd_finding(project, self.args(
                "finding", id="F1", severity="high", target="s1", status="open",
                review_sha256="0" * 64))
            with self.assertRaises(ValueError):
                self.state.cmd_finding(project, self.args(
                    "finding", id="F1", severity="medium", target="s1", status="open"))
            with self.assertRaises(ValueError):
                self.state.cmd_finding(project, self.args(
                    "finding", id="F1", severity="high", target="s1", status="rejected"))
            self.state.cmd_finding(project, self.args(
                "finding", id="F1", severity="medium", target="s1", status="open", note="downgraded"))
            self.state.cmd_finding(project, self.args(
                "finding", id="F1", severity="low", target="s1", status="open"))

    def test_validation_requires_finding_target(self):
        project = Path(tempfile.gettempdir()) / "topic"
        state = self.state.empty_state(project)
        state["review_findings"] = [{
            "id": "F1", "severity": "high", "status": "open", "source_review_sha256": "0" * 64,
        }]
        self.assertIn("finding target required", self.state.validate(state, "topic"))

    def test_schema_requires_section_audit_and_allows_empty_outline_reason(self):
        schema = json.loads(
            (ROOT / "Contracts" / "workflow-state.schema.json").read_text(encoding="utf-8"))
        self.assertIn("section_audit", schema["required"])
        self.assertNotIn("minLength", schema["$defs"]["outline_approval"]["properties"]["reason"])


if __name__ == "__main__": unittest.main()
