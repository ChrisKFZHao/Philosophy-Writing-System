"""Tests for reader-serve.py."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import io
import json
import tempfile
import threading
import unittest
from contextlib import redirect_stderr
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "Scripts" / "reader-serve.py"
STEM = "Author_2019_Title"
GOOD_STEM = "Srinivasan_2018_The-Aptness-of-Anger"


def load_module():
    spec = importlib.util.spec_from_file_location("reader_serve", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SERVE = load_module()
BUILD = SERVE.load_reader_build()


def anno(uid="urn:uuid:one", source="u1"):
    return {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "type": "Annotation",
        "id": uid,
        "created": "2026-01-01T00:00:00Z",
        "motivation": "highlighting",
        "body": [],
        "target": {"source": source, "layer": "zh"},
    }


def collection(items, source="KEY-1"):
    return {"@context": "http://www.w3.org/ns/anno.jsonld",
            "type": "AnnotationCollection", "source": source, "items": items}


class ReaderServeTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name)

        template = self.root / "Framework/Workflow/Templates/Reader/reader.html"
        template.parent.mkdir(parents=True)
        template.write_text(
            '<!doctype html><meta charset="utf-8"><title>t</title>'
            'READER-TEMPLATE-OK<script id="reader-data" type="application/json">'
            '__READER_DATA__</script>', encoding="utf-8")

        bibliography = self.root / "Private/Bibliography"
        extract = bibliography / "Extract" / STEM
        self.reader = bibliography / "Reader" / STEM
        extract.mkdir(parents=True)
        self.reader.mkdir(parents=True)

        block = {"unit_id": "u1", "text_span": "one", "unit_sha256": "hash",
                 "locator": {"kind": "page", "value": "10"},
                 "layout": {"kind": "body"}}
        (extract / "blocks.jsonl").write_text(json.dumps(block) + "\n", encoding="utf-8")
        translation = {"unit_id": "u1", "unit_sha256": "hash", "zh": "一",
                       "model": "m", "glossary": "g"}
        (self.reader / "translation-part1.jsonl").write_text(
            json.dumps(translation, ensure_ascii=False) + "\n", encoding="utf-8")

        self.notes = self.reader / "user-notes.json"
        self.out = self.reader / "reader.html"
        self.server = SERVE.ReaderServer(("127.0.0.1", 0), self.root, STEM, BUILD,
                                         self.out, self.notes)
        self.port = self.server.server_port
        thread = threading.Thread(
            target=lambda: self.server.serve_forever(poll_interval=0.02), daemon=True)
        thread.start()
        # addCleanup runs in reverse order: shutdown, close, then join.
        self.addCleanup(thread.join, 5)
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)

    # -- helpers -----------------------------------------------------------
    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def put(self, items, source="KEY-1", if_match="", extra=None):
        headers = {"Content-Type": "application/json", "X-Phil-Reader": "1",
                   "If-Match": if_match}
        headers.update(extra or {})
        body = json.dumps(collection(items, source), ensure_ascii=False).encode("utf-8")
        return self.request("PUT", "/api/notes", body=body, headers=headers)

    # -- tests -------------------------------------------------------------
    def test_get_notes_absent(self):
        status, headers, data = self.request("GET", "/api/notes")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(data), {"etag": "", "items": []})

    def test_put_success_and_file(self):
        item = anno()
        status, headers, data = self.put([item])
        self.assertEqual(status, 200)
        etag = json.loads(data)["etag"]
        self.assertTrue(self.notes.is_file())
        raw = self.notes.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), etag)
        stored = json.loads(raw.decode("utf-8"))
        self.assertEqual(stored["type"], "AnnotationCollection")
        self.assertEqual(stored["source"], "KEY-1")
        self.assertEqual(stored["items"], [item])
        # A later GET reflects the file.
        status, _, data = self.request("GET", "/api/notes")
        current = json.loads(data)
        self.assertEqual(current["etag"], etag)
        self.assertEqual(current["items"], [item])

    def test_put_without_header_forbidden(self):
        body = json.dumps(collection([anno()])).encode("utf-8")
        status, _, _ = self.request("PUT", "/api/notes", body=body,
                                    headers={"Content-Type": "application/json",
                                             "If-Match": ""})
        self.assertEqual(status, 403)
        self.assertFalse(self.notes.exists())

    def test_wrong_host_forbidden(self):
        status, _, _ = self.request("GET", "/api/notes",
                                    headers={"Host": "evil.example"})
        self.assertEqual(status, 403)

    def test_foreign_origin_forbidden(self):
        body = json.dumps(collection([anno()])).encode("utf-8")
        status, _, _ = self.request("PUT", "/api/notes", body=body, headers={
            "Content-Type": "application/json", "X-Phil-Reader": "1",
            "If-Match": "", "Origin": "http://evil.example"})
        self.assertEqual(status, 403)
        self.assertFalse(self.notes.exists())

    def test_stale_if_match_conflict(self):
        first = anno("urn:uuid:first")
        status, _, data = self.put([first])
        self.assertEqual(status, 200)
        current_etag = json.loads(data)["etag"]

        status, _, data = self.put([anno("urn:uuid:second")], if_match="0" * 64)
        self.assertEqual(status, 409)
        payload = json.loads(data)
        self.assertEqual(payload["etag"], current_etag)
        self.assertEqual([item["id"] for item in payload["items"]],
                         ["urn:uuid:first"])

    def test_invalid_item_rejected(self):
        bad = {"type": "Annotation", "id": "urn:uuid:bad"}  # no target
        status, _, _ = self.put([bad])
        self.assertEqual(status, 400)
        self.assertFalse(self.notes.exists())

    def test_oversize_body(self):
        body = b"x" * (SERVE.MAX_BODY + 1)
        status, _, _ = self.request("PUT", "/api/notes", body=body, headers={
            "Content-Type": "application/json", "X-Phil-Reader": "1", "If-Match": ""})
        self.assertEqual(status, 413)

    def test_get_root_serves_html(self):
        status, headers, data = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", headers.get("Content-Type", ""))
        self.assertIn(b"READER-TEMPLATE-OK", data)
        self.assertNotIn(b"__READER_DATA__", data)
        self.assertTrue(self.out.is_file())

    def test_unknown_path_is_404(self):
        status, _, _ = self.request("GET", "/nope")
        self.assertEqual(status, 404)

    def test_options_is_405(self):
        status, _, _ = self.request("OPTIONS", "/api/notes")
        self.assertEqual(status, 405)

    def test_open_server_forced_port_is_exact(self):
        calls = []

        def make(port):
            calls.append(port)
            return {"port": port}

        self.assertEqual(SERVE.open_server(9000, make), {"port": 9000})
        self.assertEqual(calls, [9000])

    def test_open_server_falls_back_past_busy_ports(self):
        def make(port):
            if port in (8411, 8412):
                raise OSError("in use")
            return {"port": port}

        result = SERVE.open_server(None, make, ports=[8411, 8412, 8413])
        self.assertEqual(result, {"port": 8413})

    def test_open_server_all_busy_raises(self):
        def make(port):
            raise OSError("in use")

        with self.assertRaises(OSError):
            SERVE.open_server(None, make, ports=[8411, 8412])
        with self.assertRaises(OSError):  # a forced port never falls back
            SERVE.open_server(8411, make)

    def test_default_port_range(self):
        self.assertEqual(SERVE.DEFAULT_PORT_START, 8411)
        self.assertEqual(SERVE.DEFAULT_PORT_TRIES, 10)

    def test_bad_stem_rejected(self):
        for stem in ("", "../escape", "a/b", "a\\b", "with space"):
            self.assertIsNotNone(SERVE.validate_stem(stem), stem)
        self.assertIsNone(SERVE.validate_stem(GOOD_STEM))

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = SERVE.main(["../escape", "--no-browser", "--root", str(self.root)])
        self.assertEqual(code, 2)
        self.assertIn("invalid stem", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
