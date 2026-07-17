#!/usr/bin/env python3
"""Attach a canonical PDF to a Zotero parent item as a linked_file, via the web API.

Reusable helper for /phil:ingest Step 8 (and the stored->linked migration path in
Framework/Lessons/zotero-integration.md). The zotero MCP has no linked-file-creation
tool, so this fills that gap.

Auth: reads ZOTERO_API_KEY / ZOTERO_LIBRARY_ID / ZOTERO_LIBRARY_TYPE from process
environment variables, then the active runtime's user-level config. The key is NEVER
printed, hardcoded, or passed as an argument. Only the resulting attachment key and
(with --verify) its linkMode/path are printed. Do NOT round-trip keys through a
subagent return value (proxy redaction rewrites `KEY:` lines to `[密钥]`).

Network: api.zotero.org is reached through the local proxy 127.0.0.1:6789 (flaky over
GFW), with per-request retries and exponential backoff. A new-item POST needs no
If-Unmodified-Since-Version header (that is required only for key-based PATCH/DELETE).

Usage:
  # single parent
  python zotero-attach-linked.py --parent <ITEM_KEY> --stem <FILE.pdf> [--verify]
                                 [--content-type application/pdf] [--retries 6]
  # batch: attach the SAME stem to many parents in one POST (edited-collection case:
  # the book item + every bookSection all link to the one volume PDF)
  python zotero-attach-linked.py --parents KEY1,KEY2,KEY3 --stem <FILE.pdf> [--verify]

Prints:
  ATTACHMENT_KEY <parent> <key>   one line per created attachment
  (with --verify) linkMode / path / parentItem / title of each created attachment
  HTTP_ERROR <code> <body>        on a non-transient 4xx (stops immediately)
  ALL_RETRIES_FAILED <type>       if every attempt hit a transient error

--parent and --parents are mutually exclusive. Zotero caps a write batch at 50 items,
so more than 50 parents are split across several POSTs automatically.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import tomllib
except ImportError:  # Python < 3.11 is unsupported for Codex config fallback.
    tomllib = None

DEFAULT_PROXY = "http://127.0.0.1:6789"


def complete_env(env):
    if not env:
        return None
    api_key = env.get("ZOTERO_API_KEY")
    library_id = env.get("ZOTERO_LIBRARY_ID")
    if not api_key or not library_id:
        return None
    return api_key, str(library_id), env.get("ZOTERO_LIBRARY_TYPE", "user")


def config_env(path):
    if not path.is_file():
        return None
    if path.suffix.lower() == ".toml":
        if tomllib is None:
            return None
        with path.open("rb") as handle:
            cfg = tomllib.load(handle)
        return cfg.get("mcp_servers", {}).get("zotero", {}).get("env", {})
    with path.open(encoding="utf-8") as handle:
        cfg = json.load(handle)
    return cfg.get("mcpServers", {}).get("zotero", {}).get("env", {})


def load_env():
    direct = complete_env(os.environ)
    if direct:
        return direct

    explicit = os.environ.get("PHILO_ZOTERO_CONFIG")
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.extend(
        [
            Path.home() / ".claude.json",
            Path.home() / ".codex/config.toml",
        ]
    )
    for path in candidates:
        values = complete_env(config_env(path))
        if values:
            return values
    raise RuntimeError(
        "Zotero credentials not found in environment, ~/.claude.json, or ~/.codex/config.toml"
    )


def opener():
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or DEFAULT_PROXY
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": proxy, "https": proxy})
    )


def request(op, url, api_key, method, data=None, retries=6):
    """One retried request. HTTP 4xx errors are non-transient and stop immediately."""
    last = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Zotero-API-Key", api_key)
        req.add_header("Zotero-API-Version", "3")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            resp = op.open(req, timeout=60)
            return resp.status, resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            print(f"HTTP_ERROR {e.code} {body[:300]}")
            return None, None
        except Exception as e:  # URLError / SSL / timeout — transient
            last = e
            print(f"attempt {attempt} transient error: {type(e).__name__}", file=sys.stderr)
            time.sleep(min(2 * attempt, 15))
    print(f"ALL_RETRIES_FAILED {type(last).__name__ if last else '?'}")
    return None, None


def attachment_payload(parent, stem, content_type):
    return {
        "itemType": "attachment",
        "linkMode": "linked_file",
        "parentItem": parent,
        "path": f"attachments:{stem}",
        "contentType": content_type,
        "title": stem,
    }


def post_batch(op, base, api_key, parents, stem, content_type, retries):
    """POST one batch of attachments (<=50 parents). Returns list of (parent, att_key)
    on success, or None on failure (message already printed)."""
    payload = [attachment_payload(p, stem, content_type) for p in parents]
    _, body = request(op, base, api_key, "POST",
                      data=json.dumps(payload).encode("utf-8"), retries=retries)
    if body is None:
        return None
    obj = json.loads(body)
    failed = obj.get("failed") or {}
    if failed:
        print("FAILED", json.dumps(failed))
        return None
    succ = obj.get("successful") or {}
    # Response keys are batch indices ("0", "1", ...); correlate back to parents by index.
    results = []
    for idx_str, item in succ.items():
        att_key = item.get("key") if isinstance(item, dict) else None
        parent = parents[int(idx_str)] if idx_str.isdigit() and int(idx_str) < len(parents) else None
        results.append((parent, att_key))
    return results


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--parent", help="Zotero parent item key (single)")
    g.add_argument("--parents", help="comma-separated parent item keys (batch — same stem)")
    ap.add_argument("--stem", required=True, help="canonical PDF filename, e.g. Author_2020_Title.pdf")
    ap.add_argument("--content-type", default="application/pdf")
    ap.add_argument("--retries", type=int, default=6)
    ap.add_argument("--verify", action="store_true", help="GET each new attachment back and print linkMode/path")
    args = ap.parse_args()

    parents = [args.parent] if args.parent else [p.strip() for p in args.parents.split(",") if p.strip()]
    if not parents:
        print("ERROR no parent keys given")
        sys.exit(2)

    try:
        api_key, user_id, lib_type = load_env()
    except (KeyError, OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(2)
    if lib_type != "user":
        print(f"ERROR unexpected library type: {lib_type}")
        sys.exit(2)
    base = f"https://api.zotero.org/users/{user_id}/items"
    op = opener()

    all_results = []
    for i in range(0, len(parents), 50):  # Zotero write batch cap = 50 items
        batch = parents[i:i + 50]
        results = post_batch(op, base, api_key, batch, args.stem, args.content_type, args.retries)
        if results is None:
            sys.exit(1)
        all_results.extend(results)

    for parent, att_key in all_results:
        print("ATTACHMENT_KEY", parent, att_key)

    if args.verify:
        for _, att_key in all_results:
            if not att_key:
                continue
            _, vbody = request(op, f"{base}/{att_key}", api_key, "GET", retries=args.retries)
            if vbody:
                d = json.loads(vbody).get("data", {})
                print(f"-- {att_key} --")
                print("linkMode  :", d.get("linkMode"))
                print("path      :", d.get("path"))
                print("parentItem:", d.get("parentItem"))
                print("title     :", d.get("title"))


if __name__ == "__main__":
    main()
