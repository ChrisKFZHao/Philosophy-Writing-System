#!/usr/bin/env python3
"""Serve a reader page locally and save annotations straight into user-notes.json.

``reader-serve.py STEM`` binds ``127.0.0.1`` only, rebuilds the page on each
``GET /``, and lets the page read and write its annotations through a small
JSON API:

* ``GET  /api/notes`` -> ``{"etag": <sha256 of the file bytes or "">, "items": [...]}``
* ``PUT  /api/notes`` -> stores the AnnotationCollection the export button
  produces, guarded by ``X-Phil-Reader``, ``Content-Type``, ``If-Match``.

Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


SCRIPT_DIR = Path(__file__).resolve().parent
STEM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ANNO_CONTEXT = "http://www.w3.org/ns/anno.jsonld"
MAX_BODY = 2 * 1024 * 1024
READER_HEADER = "X-Phil-Reader"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def load_reader_build():
    """Load ``reader-build.py`` from this directory as a module."""
    path = SCRIPT_DIR / "reader-build.py"
    spec = importlib.util.spec_from_file_location("reader_build_serve", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_stem(stem: str) -> str | None:
    """Return an error message for an unsafe stem, else ``None``."""
    if not stem or len(stem) > 200:
        return "empty or too long"
    if "/" in stem or "\\" in stem:
        return "contains a path separator"
    if ".." in stem:
        return "contains a parent reference"
    if not STEM_RE.match(stem):
        return "contains unexpected characters"
    return None


def etag_of(path: Path) -> str:
    """SHA-256 of the file bytes, or ``""`` when the file is absent."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except FileNotFoundError:
        return ""


def load_items(path: Path, reader_build) -> list:
    """Read the on-disk notes in either accepted shape."""
    if not path.is_file():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return reader_build.user_notes_of(raw)


def validate_items(items) -> str | None:
    """Return an error message for an invalid ``items`` list, else ``None``."""
    if not isinstance(items, list):
        return "items must be a list"
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            return f"item {index} is not an object"
        if item.get("type") != "Annotation":
            return f"item {index} has no Annotation type"
        if not isinstance(item.get("id"), str) or not item["id"]:
            return f"item {index} has no string id"
        target = item.get("target")
        if not isinstance(target, dict):
            return f"item {index} has no target object"
        if not isinstance(target.get("source"), str) or not target["source"]:
            return f"item {index} has no target source"
    return None


def store_items(path: Path, items: list, source: str) -> str:
    """Atomically write the notes and return the new etag."""
    payload = {
        "@context": ANNO_CONTEXT,
        "type": "AnnotationCollection",
        "source": source,
        "items": items,
    }
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    fd, temp_name = tempfile.mkstemp(prefix=".user-notes-", suffix=".tmp",
                                     dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------

class ReaderServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, root: Path, stem: str, reader_build, out_path: Path,
                 notes_path: Path):
        super().__init__(address, ReaderHandler)
        self.root = root
        self.stem = stem
        self.reader_build = reader_build
        self.out_path = out_path
        self.notes_path = notes_path
        self.build_lock = threading.Lock()


class ReaderHandler(BaseHTTPRequestHandler):
    server_version = "PhilReader/1.0"
    protocol_version = "HTTP/1.1"

    # -- responses ---------------------------------------------------------
    def _send(self, code: int, body: bytes = b"",
              content_type: str = "application/json; charset=utf-8",
              close: bool = False) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if close:
            self.send_header("Connection", "close")
            self.close_connection = True
        self.end_headers()
        if body:
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def _json(self, code: int, obj, close: bool = False) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._send(code, body, "application/json; charset=utf-8", close=close)

    # -- guards ------------------------------------------------------------
    def _host_ok(self) -> bool:
        port = self.server.server_port
        return self.headers.get("Host", "") in (f"127.0.0.1:{port}",
                                                f"localhost:{port}")

    def _origin_ok(self) -> bool:
        origin = self.headers.get("Origin")
        if origin is None:
            return True
        port = self.server.server_port
        return origin in (f"http://127.0.0.1:{port}",
                          f"http://localhost:{port}")

    def log_message(self, fmt: str, *args) -> None:  # quiet by default
        pass

    def _content_length(self) -> int | None:
        raw = self.headers.get("Content-Length")
        try:
            length = int(raw) if raw is not None else -1
        except ValueError:
            return None
        return length if length >= 0 else None

    def _drain(self, length: int | None) -> None:
        """Read and discard a request body so closing the socket is graceful."""
        if not length or length <= 0:
            return
        remaining = min(length, 8 * 1024 * 1024)
        while remaining > 0:
            chunk = self.rfile.read(min(remaining, 65536))
            if not chunk:
                break
            remaining -= len(chunk)

    # -- methods -----------------------------------------------------------
    def do_GET(self) -> None:
        if not self._host_ok():
            return self._json(403, {"error": "unexpected Host header"})
        path = urlsplit(self.path).path
        if path == "/api/notes":
            notes = self.server.notes_path
            return self._json(200, {"etag": etag_of(notes),
                                    "items": load_items(notes, self.server.reader_build)})
        if path == "/":
            return self._serve_page()
        return self._json(404, {"error": "not found"})

    def do_OPTIONS(self) -> None:
        if not self._host_ok():
            return self._json(403, {"error": "unexpected Host header"})
        self._json(405, {"error": "method not allowed"})

    def do_PUT(self) -> None:
        if not self._host_ok():
            return self._json(403, {"error": "unexpected Host header"}, close=True)
        length = self._content_length()
        if not self._origin_ok():
            self._drain(length)
            return self._json(403, {"error": "unexpected Origin header"}, close=True)
        if urlsplit(self.path).path != "/api/notes":
            self._drain(length)
            return self._json(404, {"error": "not found"}, close=True)
        if self.headers.get(READER_HEADER) != "1":
            self._drain(length)
            return self._json(403, {"error": f"missing {READER_HEADER} header"}, close=True)
        content_type = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if content_type != "application/json":
            self._drain(length)
            return self._json(415, {"error": "Content-Type must be application/json"}, close=True)
        if length is None:
            return self._json(411, {"error": "Content-Length required"}, close=True)
        if length > MAX_BODY:
            self._drain(length)
            return self._json(413, {"error": "body too large"}, close=True)

        body = self.rfile.read(length)
        if len(body) != length:
            return self._json(400, {"error": "incomplete body"}, close=True)
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return self._json(400, {"error": "invalid JSON"})
        items = payload.get("items") if isinstance(payload, dict) else None
        error = validate_items(items)
        if error:
            return self._json(400, {"error": error})

        notes = self.server.notes_path
        current = etag_of(notes)
        if_match = self.headers.get("If-Match")
        if if_match is None:
            return self._json(428, {"error": "If-Match required"})
        if if_match != current:
            return self._json(409, {"etag": current,
                                    "items": load_items(notes, self.server.reader_build)})

        source = payload.get("source")
        if not isinstance(source, str) or not source:
            source = self.server.stem
        try:
            new_etag = store_items(notes, items, source)
        except OSError as exc:
            return self._json(500, {"error": f"cannot write notes: {exc}"})

        print(f"PUT /api/notes {len(items)} items -> {new_etag[:12]}", file=sys.stderr)
        self._json(200, {"etag": new_etag})

    # -- page --------------------------------------------------------------
    def _serve_page(self) -> None:
        server = self.server
        try:
            with server.build_lock:
                report, html = server.reader_build.build(server.root, server.stem,
                                                         server.out_path)
                if html is None:
                    raise RuntimeError("; ".join(report.get("errors") or ["build failed"]))
                server.out_path.write_text(html, encoding="utf-8")
            body = html.encode("utf-8")
        except Exception as exc:  # noqa: BLE001 - fall back to the last build
            print(f"reader rebuild failed: {exc}", file=sys.stderr)
            try:
                body = server.out_path.read_bytes()
            except OSError:
                return self._json(500, {"error": "no reader page available"})
        self._send(200, body, "text/html; charset=utf-8")


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

DEFAULT_PORT_START = 8411
DEFAULT_PORT_TRIES = 10


def open_server(forced_port: int | None, make, ports=None):
    """Bind through ``make(port)``; a forced port is exact, else try each candidate."""
    if forced_port is not None:
        return make(forced_port)
    candidates = list(ports if ports is not None else
                      range(DEFAULT_PORT_START, DEFAULT_PORT_START + DEFAULT_PORT_TRIES))
    last_error: OSError | None = None
    for port in candidates:
        try:
            return make(port)
        except OSError as exc:
            last_error = exc
    raise OSError(f"no free port among {candidates[0]}-{candidates[-1]}: {last_error}")


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        description="Serve a reader page and save annotations to user-notes.json.")
    parser.add_argument("stem", help="bibliography stem, e.g. Author_2018_Title")
    parser.add_argument("--root", type=Path, help="repository root")
    parser.add_argument("--port", type=int, default=None,
                        help="port to bind (default: first free of 8411-8420)")
    parser.add_argument("--no-browser", action="store_true",
                        help="do not open the page in a browser")
    args = parser.parse_args(argv)

    error = validate_stem(args.stem)
    if error:
        print(f"invalid stem: {error}", file=sys.stderr)
        return 2

    reader_build = load_reader_build()
    root = (args.root or reader_build.find_root(SCRIPT_DIR) or Path.cwd()).resolve()
    reader_dir = root / "Private/Bibliography/Reader" / args.stem
    if not reader_dir.is_dir():
        print(f"reader directory not found: {reader_dir}", file=sys.stderr)
        return 2

    out_path = reader_dir / "reader.html"
    notes_path = reader_dir / "user-notes.json"
    make = lambda port: ReaderServer(("127.0.0.1", port), root, args.stem, reader_build,
                                     out_path, notes_path)
    try:
        server = open_server(args.port, make)
    except OSError as exc:
        print(f"cannot bind server: {exc}", file=sys.stderr)
        return 1

    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"reader: {url}", flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
