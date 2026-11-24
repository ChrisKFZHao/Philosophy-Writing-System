from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = WORKFLOW_ROOT / "Scripts"


def load_script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PhilosopherDBFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = load_script("philosopher-db.py")

    def make_repo(self, root: Path):
        paths = self.database.paths_for(root)
        paths["profiles"].mkdir(parents=True)
        paths["domains"].mkdir(parents=True)
        self.database.write_json(paths["domain_registry"], self.database.DOMAIN_REGISTRY)
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

    def write_index(self, root: Path, keys):
        index = root / "Private/Bibliography/INDEX.md"
        index.parent.mkdir(parents=True, exist_ok=True)
        lines = ["| KEY | Title |", "|---|---|"]
        lines.extend(f"| {key} | {key} |" for key in keys)
        index.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return index

    def observation(self, artifact, bib_key, statement="Approved claim"):
        return {
            "record_type": "observation-batch",
            "observation_id": f"PHO-{artifact}",
            "bib_key": bib_key,
            "artifact_id": artifact,
            "artifact_hash": artifact,
            "artifact_type": "summary",
            "analysis_level": 0.5,
            "source_metadata": {"author": "Test Philosopher", "year": "2026", "title": artifact},
            "topics": ["metaphysics"],
            "people": [{
                "display_name": "Test Philosopher",
                "canonical_name": "Test Philosopher",
                "aliases": [],
                "role": "author",
                "substantive": True,
                "claims": [{"statement": statement, "category": "position", "locator": "summary:core_thesis"}],
            }],
            "generated_at": "2026-07-19T00:00:00Z",
        }

    def add_claim_candidate(self, paths, bib_key="KEY-1", statement="Approved claim"):
        paths["observations"].mkdir(parents=True, exist_ok=True)
        observation = self.observation("A1", bib_key, statement)
        self.database.write_json(paths["observations"] / "1.json", observation)
        state, _ = self.database.rebuild_queue(paths, self.database.empty_state())
        self.database.write_json(paths["state"], state)
        return next(item["candidate_id"] for item in state["candidates"].values() if item["status"] == "pending")

    def test_approve_rejects_path_like_person_id_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root)
            cid = self.add_claim_candidate(paths)
            registry_before = paths["domain_registry"].read_text(encoding="utf-8")
            result = self.database.main(
                ["--repo-root", str(root), "approve", cid, "--person-id", "../Domains/registry"]
            )
            self.assertEqual(result, 1)
            self.assertEqual(registry_before, paths["domain_registry"].read_text(encoding="utf-8"))
            state = self.database.load_state(paths["state"])
            self.assertEqual(state["candidates"][cid]["status"], "pending")

    def test_approve_accepts_indexed_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root)
            index = self.write_index(root, ["KEY-1"])
            cid = self.add_claim_candidate(paths)
            self.database.approve_candidate(paths, cid, bibliography_index=index)
            claims = self.database.load_profiles(paths["profiles"])["test-philosopher"]["claims"]
            self.assertEqual(len(claims), 1)
            self.assertEqual(claims[0]["support_status"], "source-backed")

    def test_approve_rejects_unindexed_evidence_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root)
            index = self.write_index(root, ["OTHER-KEY"])
            cid = self.add_claim_candidate(paths)
            with self.assertRaisesRegex(self.database.PhilosopherDBError, "not registered"):
                self.database.approve_candidate(paths, cid, bibliography_index=index)
            claims = self.database.load_profiles(paths["profiles"])["test-philosopher"]["claims"]
            self.assertEqual(claims, [])
            self.assertEqual(self.database.load_state(paths["state"])["candidates"][cid]["status"], "pending")

    def test_approve_rejects_missing_bibliography_index(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root)
            cid = self.add_claim_candidate(paths)
            with self.assertRaisesRegex(self.database.PhilosopherDBError, "index not found"):
                self.database.approve_candidate(paths, cid)
            claims = self.database.load_profiles(paths["profiles"])["test-philosopher"]["claims"]
            self.assertEqual(claims, [])

    def test_observe_rejects_invalid_analysis_level(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root)
            batch = self.observation("A1", "KEY-1")
            batch["analysis_level"] = 4
            batch_path = root / "batch.json"
            batch_path.write_text(json.dumps(batch), encoding="utf-8")
            with self.assertRaisesRegex(self.database.PhilosopherDBError, "invalid analysis_level"):
                self.database.observe(paths, [batch_path], False, None)
            self.assertFalse(paths["observations"].exists())

    def test_synchronize_domains_validates_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root)
            paths["observations"].mkdir(parents=True)
            self.database.write_json(paths["observations"] / "1.json", self.observation("A1", "KEY-1"))
            self.database.write_json(paths["observations"] / "2.json", self.observation("A2", "KEY-2"))
            profile_path = paths["profiles"] / "test-philosopher.json"
            before = profile_path.read_text(encoding="utf-8")
            profile = self.database.read_json(profile_path)
            del profile["relations"]  # makes validate_profile fail
            profiles = {"test-philosopher": profile}
            state = {
                "people": {
                    "test-philosopher": {
                        "person_id": "test-philosopher",
                        "domains": {
                            "metaphysics": {
                                "source_keys": ["KEY-1", "KEY-2"],
                                "central_source_keys": ["KEY-1"],
                            },
                        },
                    },
                },
            }
            with self.assertRaisesRegex(self.database.PhilosopherDBError, "invalid profile"):
                self.database.synchronize_domains(paths, state, profiles)
            self.assertEqual(before, profile_path.read_text(encoding="utf-8"))

    def test_reapprove_after_interrupted_approve_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.make_repo(root)
            index = self.write_index(root, ["KEY-1"])
            cid = self.add_claim_candidate(paths)
            original_state = self.database.read_json(paths["state"])
            self.database.approve_candidate(paths, cid, bibliography_index=index)
            # Simulate interruption after the profile write but before the state write.
            self.database.write_json(paths["state"], original_state)
            self.database.approve_candidate(paths, cid, bibliography_index=index)
            claims = self.database.load_profiles(paths["profiles"])["test-philosopher"]["claims"]
            self.assertEqual(len(claims), 1)
            self.assertEqual(len(claims[0]["evidence"]), 1)


class FakeResponse:
    def __init__(self, status, payload):
        self.status = status
        self._body = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body


class FakeOpener:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.requests = []

    def open(self, req, timeout=60):
        self.requests.append(req)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return FakeResponse(200, outcome)


class ZoteroAttachFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = load_script("zotero-attach-linked.py")

    def test_write_token_is_reused_across_retries(self):
        op = FakeOpener([
            urllib.error.URLError("transient"),
            {"successful": {"0": {"key": "K1"}}, "failed": {}},
        ])
        with mock.patch.object(self.script.time, "sleep", lambda _: None):
            outcome = self.script.post_batch(
                op, "https://api.test/items", "TESTKEY123", ["P1"], "s.pdf", "application/pdf", 2
            )
        self.assertIsNotNone(outcome)
        tokens = [
            next((value for key, value in req.headers.items() if key.lower() == "zotero-write-token"), None)
            for req in op.requests
        ]
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0], tokens[1])
        self.assertRegex(tokens[0], r"^[0-9a-f]{32}$")

    def test_write_token_conflict_reports_and_stops(self):
        error = urllib.error.HTTPError(
            "https://api.test/items", 412, "Precondition Failed", None, io.BytesIO(b"used")
        )
        op = FakeOpener([error])
        with contextlib.redirect_stdout(out := io.StringIO()):
            outcome = self.script.post_batch(
                op, "https://api.test/items", "TESTKEY123", ["P1"], "s.pdf", "application/pdf", 2
            )
        self.assertIsNone(outcome)
        self.assertEqual(len(op.requests), 1)
        conflicts = [line for line in out.getvalue().splitlines() if line.startswith("WRITE_TOKEN_CONFLICT")]
        self.assertEqual(len(conflicts), 1)

    def test_batch_two_failure_keeps_batch_one_keys_printed(self):
        class Opener:
            def __init__(self):
                self.calls = 0

            def open(self, req, timeout=60):
                self.calls += 1
                if self.calls == 1:
                    return FakeResponse(200, {"successful": {"0": {"key": "K1"}}, "failed": {}})
                raise urllib.error.URLError("down")

        op = Opener()
        parents = ",".join(f"P{index}" for index in range(51))
        argv = ["prog", "--parents", parents, "--stem", "s.pdf", "--retries", "1"]
        out = io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(self.script, "load_env", lambda: ("TESTKEY123", "1", "user")), \
                mock.patch.object(self.script, "opener", lambda: op), \
                mock.patch.object(self.script.time, "sleep", lambda _: None), \
                contextlib.redirect_stdout(out):
            with self.assertRaises(SystemExit) as raised:
                self.script.main()
        self.assertEqual(raised.exception.code, 1)
        text = out.getvalue()
        self.assertIn("ATTACHMENT_KEY P0 K1", text)
        self.assertLess(text.index("ATTACHMENT_KEY"), text.index("ALL_RETRIES_FAILED"))

    def test_mixed_successful_and_failed_response_prints_keys_then_fails(self):
        op = FakeOpener([{
            "successful": {"0": {"key": "K1"}},
            "failed": {"1": {"code": 400, "message": "bad"}},
        }])
        argv = ["prog", "--parents", "P0,P1", "--stem", "s.pdf", "--retries", "1"]
        out = io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(self.script, "load_env", lambda: ("TESTKEY123", "1", "user")), \
                mock.patch.object(self.script, "opener", lambda: op), \
                contextlib.redirect_stdout(out):
            with self.assertRaises(SystemExit) as raised:
                self.script.main()
        self.assertEqual(raised.exception.code, 1)
        text = out.getvalue()
        self.assertIn("ATTACHMENT_KEY P0 K1", text)
        self.assertIn("FAILED", text)
        self.assertLess(text.index("ATTACHMENT_KEY"), text.index("FAILED"))

    def test_explicit_empty_proxy_environment_means_direct(self):
        with mock.patch.dict(self.script.os.environ, {"HTTPS_PROXY": ""}, clear=True):
            self.assertEqual(self.script.resolve_proxy(), "")

    def test_stem_with_path_separator_or_parent_is_rejected(self):
        opened = []

        class Opener:
            def open(self, req, timeout=60):
                opened.append(req)
                raise AssertionError("no request should be made")

        for stem in ("../evil.pdf", "dir/file.pdf", "dir\\file.pdf"):
            out = io.StringIO()
            argv = ["prog", "--parents", "P1", "--stem", stem]
            with mock.patch.object(sys, "argv", argv), \
                    mock.patch.object(self.script, "opener", lambda: Opener()), \
                    contextlib.redirect_stdout(out):
                with self.assertRaises(SystemExit) as raised:
                    self.script.main()
            self.assertEqual(raised.exception.code, 2)
            self.assertIn("invalid --stem", out.getvalue())
        self.assertEqual(opened, [])


if __name__ == "__main__":
    unittest.main()
