#!/usr/bin/env python3
"""Maintain the source-backed philosopher database and its private review queue."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_REPO_ROOT = SCRIPT_PATH.parent.parent.parent.parent
SUBSTANTIVE_ROLES = {"author", "core-target", "supporting", "opposition"}
CENTRAL_DOMAIN_ROLES = {"author", "core-target"}
VALID_ROLES = SUBSTANTIVE_ROLES | {"background", "passing-mention"}
CLAIM_CATEGORIES = {
    "identity", "tradition", "work", "position", "argument",
    "relevance", "relationship", "other",
}
LEGACY_CATEGORY = {
    "Tradition": "tradition",
    "Major Works": "work",
    "Key Positions": "position",
    "Key Arguments": "argument",
    "Relevance": "relevance",
    "Related": "relationship",
}
DOMAIN_REGISTRY = {
    "registry_version": "1.0",
    "domains": [
        {
            "domain_id": "general",
            "label": "General Philosophy / Methodology",
            "topic_keywords": [
                "methodology", "conceptual analysis", "epistemology",
                "philosophy of language", "philosophy of mind",
                "political philosophy", "logic", "pragmatism",
            ],
        },
        {
            "domain_id": "metaphysics",
            "label": "Metaphysics",
            "topic_keywords": [
                "metaphysics", "ontology", "grounding", "fundamentality",
                "identity", "persistence", "modality", "possible worlds",
                "causation", "laws of nature", "natural kind", "properties",
                "time", "mereology", "philosophy of physics",
            ],
        },
        {
            "domain_id": "metaethics",
            "label": "Metaethics",
            "topic_keywords": [
                "metaethics", "moral realism", "moral anti-realism",
                "moral semantics", "normativity", "normative reasons",
                "moral psychology", "moral disagreement",
                "moral epistemology", "moral supervenience", "expressivism",
            ],
        },
    ],
}


class PhilosopherDBError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_hash(*parts: Any, length: int = 12) -> str:
    payload = json.dumps(parts, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length].upper()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ascii_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")


def clean_person_name(value: str) -> str:
    value = re.sub(r"\s*\([^)]*(?:ed\.?|eds\.?|editor|编辑)[^)]*\)\s*$", "", value, flags=re.I)
    value = re.sub(r"\s+", " ", value).strip(" ,;\t")
    if value.count(",") == 1 and " & " not in value and " and " not in value.lower():
        surname, given = [part.strip() for part in value.split(",", 1)]
        if surname and given:
            value = f"{given} {surname}"
    return value


def split_authors(value: str) -> list[str]:
    value = re.sub(r"\s*\((?:eds?\.?|editors?)\)\s*", "", value, flags=re.I)
    value = re.sub(r"\s+et\s+al\.?$", "", value, flags=re.I)
    parts = re.split(r"\s+(?:&|and)\s+|\s*;\s*", value)
    return [clean_person_name(part) for part in parts if clean_person_name(part)]


def name_key(value: str) -> str:
    return ascii_slug(clean_person_name(value))


def paths_for(repo_root: Path) -> dict[str, Path]:
    db_root = repo_root / "Shared/Philosophers-DB"
    queue_root = repo_root / "Private/Bibliography/Philosopher-Queue"
    return {
        "repo": repo_root,
        "db": db_root,
        "profiles": db_root / "Profiles",
        "domains": db_root / "Domains",
        "domain_registry": db_root / "Domains/registry.json",
        "queue": queue_root,
        "observations": queue_root / "Observations",
        "state": queue_root / "state.json",
    }


def load_profiles(profiles_root: Path) -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    if not profiles_root.exists():
        return profiles
    for path in sorted(profiles_root.glob("*.json")):
        profile = read_json(path)
        profiles[profile["person_id"]] = profile
    return profiles


def profile_alias_map(profiles: dict[str, dict[str, Any]]) -> tuple[dict[str, str], set[str]]:
    candidates: dict[str, set[str]] = defaultdict(set)
    for person_id, profile in profiles.items():
        identity = profile["identity"]
        values = [person_id, identity["display_name"], identity["canonical_name"], *identity["aliases"]]
        for legacy_path in identity.get("legacy_paths", []):
            values.append(Path(legacy_path).stem)
        for value in values:
            key = name_key(value)
            if key:
                candidates[key].add(person_id)
    ambiguous = {key for key, ids in candidates.items() if len(ids) > 1}
    aliases = {key: next(iter(ids)) for key, ids in candidates.items() if len(ids) == 1}
    return aliases, ambiguous


def resolve_person(value: str, profiles: dict[str, dict[str, Any]]) -> tuple[str | None, bool]:
    aliases, ambiguous = profile_alias_map(profiles)
    key = name_key(value)
    return aliases.get(key), key in ambiguous


def validate_evidence(evidence: dict[str, Any], context: str) -> list[str]:
    failures: list[str] = []
    required = {"bib_key", "source_type", "analysis_level", "locator", "approved_at"}
    missing = required - evidence.keys()
    if missing:
        failures.append(f"{context}: missing evidence fields {sorted(missing)}")
    if evidence.get("source_type") not in {"primary", "secondary"}:
        failures.append(f"{context}: invalid source_type")
    if evidence.get("analysis_level") not in {0.5, 1, 2, 3}:
        failures.append(f"{context}: invalid analysis_level")
    if not evidence.get("bib_key") or not evidence.get("locator"):
        failures.append(f"{context}: evidence must identify a bibliography KEY and locator")
    if any(key in evidence for key in ("source_location", "pdf_path", "project")):
        failures.append(f"{context}: private paths/project data cannot enter shared evidence")
    return failures


def validate_profile(profile: dict[str, Any], expected_path: Path | None = None) -> list[str]:
    failures: list[str] = []
    required = {"profile_version", "person_id", "identity", "claims", "domains", "relations", "created_at", "updated_at"}
    missing = required - profile.keys()
    if missing:
        return [f"profile missing fields {sorted(missing)}"]
    person_id = profile["person_id"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", person_id):
        failures.append(f"{person_id}: invalid person_id")
    if expected_path and expected_path.stem != person_id:
        failures.append(f"{person_id}: filename must match person_id")
    claim_ids: set[str] = set()
    for claim in profile["claims"]:
        claim_id = claim.get("claim_id", "<missing>")
        if claim_id in claim_ids:
            failures.append(f"{person_id}: duplicate claim_id {claim_id}")
        claim_ids.add(claim_id)
        if claim.get("category") not in CLAIM_CATEGORIES:
            failures.append(f"{person_id}/{claim_id}: invalid category")
        evidence = claim.get("evidence", [])
        if claim.get("support_status") == "prompt-only" and evidence:
            failures.append(f"{person_id}/{claim_id}: prompt-only claim carries evidence")
        elif claim.get("support_status") == "source-backed" and not evidence:
            failures.append(f"{person_id}/{claim_id}: source-backed claim lacks evidence")
        elif claim.get("support_status") not in {"source-backed", "prompt-only"}:
            failures.append(f"{person_id}/{claim_id}: invalid support_status")
        for item in evidence:
            failures.extend(validate_evidence(item, f"{person_id}/{claim_id}"))
    seen_domains: set[str] = set()
    for domain in profile["domains"]:
        domain_id = domain.get("domain_id", "")
        if domain_id in seen_domains:
            failures.append(f"{person_id}: duplicate domain {domain_id}")
        seen_domains.add(domain_id)
        evidence = domain.get("evidence", [])
        if domain.get("support_status") == "prompt-only" and evidence:
            failures.append(f"{person_id}/{domain_id}: prompt-only domain carries evidence")
        if domain.get("support_status") == "source-backed" and not evidence:
            failures.append(f"{person_id}/{domain_id}: source-backed domain lacks evidence")
        for item in evidence:
            failures.extend(validate_evidence(item, f"{person_id}/{domain_id}"))
    return failures


def validate_database(paths: dict[str, Path]) -> list[str]:
    failures: list[str] = []
    profiles = load_profiles(paths["profiles"])
    if not profiles:
        failures.append("no canonical profiles found")
    aliases, ambiguous = profile_alias_map(profiles)
    if ambiguous:
        failures.append(f"ambiguous profile aliases: {sorted(ambiguous)}")
    for person_id, profile in profiles.items():
        failures.extend(validate_profile(profile, paths["profiles"] / f"{person_id}.json"))
    if not paths["domain_registry"].exists():
        failures.append("missing domain registry")
    elif read_json(paths["domain_registry"]).get("registry_version") != "1.0":
        failures.append("invalid domain registry version")
    return failures


def parse_legacy_profile(path: Path, migrated_at: str) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        raise PhilosopherDBError(f"legacy profile has no heading: {path}")
    heading = lines[0][2:].strip()
    match = re.match(r"^(.*?)(?:\s+\(([^()]*)\))?$", heading)
    assert match
    heading_name = match.group(1).strip()
    life = match.group(2)
    display_name = clean_person_name(heading_name)
    person_id = ascii_slug(display_name)
    claim_values: list[tuple[str, str]] = []
    if life:
        claim_values.append(("identity", f"Life: {life}"))
    current_category: str | None = None
    for line in lines[1:]:
        top = re.match(r"^- \*\*(.+?)\*\*:\s*(.*)$", line)
        if top:
            current_category = LEGACY_CATEGORY.get(top.group(1), "other")
            if top.group(2).strip():
                claim_values.append((current_category, top.group(2).strip()))
            continue
        nested = re.match(r"^\s+-\s+(.*)$", line)
        if nested and current_category:
            claim_values.append((current_category, nested.group(1).strip()))
            continue
        if line.strip() and current_category and claim_values and not line.startswith("*"):
            category, statement = claim_values[-1]
            claim_values[-1] = (category, f"{statement}\n{line.strip()}")
    claims = []
    for index, (category, statement) in enumerate(claim_values, start=1):
        claims.append({
            "claim_id": f"P-{person_id}-C{index:04d}",
            "category": category,
            "statement": statement,
            "support_status": "prompt-only",
            "dispute_status": "unmarked",
            "status": "active",
            "evidence": [],
        })
    legacy_relative = path.relative_to(path.parents[2]).as_posix()
    aliases = sorted({display_name, heading_name, path.stem})
    return {
        "profile_version": "1.0",
        "person_id": person_id,
        "identity": {
            "display_name": display_name,
            "canonical_name": display_name,
            "aliases": aliases,
            "legacy_paths": [legacy_relative],
        },
        "claims": claims,
        "domains": [{
            "domain_id": path.parent.name.lower(),
            "support_status": "prompt-only",
            "evidence": [],
        }],
        "relations": [],
        "created_at": migrated_at,
        "updated_at": migrated_at,
    }


def legacy_paths(db_root: Path) -> list[Path]:
    paths: list[Path] = []
    for domain in ("General", "Metaphysics", "Metaethics"):
        paths.extend(sorted((db_root / domain).glob("*.md")))
    return paths


def migrate_legacy(paths: dict[str, Path], apply: bool) -> dict[str, Any]:
    source_paths = legacy_paths(paths["db"])
    if not source_paths:
        profiles = load_profiles(paths["profiles"])
        return {"legacy_files": 0, "profiles": len(profiles), "already_migrated": bool(profiles)}
    migrated_at = now_iso()
    profiles = [parse_legacy_profile(path, migrated_at) for path in source_paths]
    ids = [profile["person_id"] for profile in profiles]
    if len(ids) != len(set(ids)):
        raise PhilosopherDBError("legacy migration produced duplicate person IDs")
    failures = [failure for profile in profiles for failure in validate_profile(profile)]
    if failures:
        raise PhilosopherDBError("migration validation failed:\n- " + "\n- ".join(failures))
    report = {
        "legacy_files": len(source_paths),
        "profiles": len(profiles),
        "prompt_only_claims": sum(len(profile["claims"]) for profile in profiles),
        "source_backed_claims": 0,
        "apply": apply,
    }
    if not apply:
        return report
    paths["profiles"].mkdir(parents=True, exist_ok=True)
    paths["domains"].mkdir(parents=True, exist_ok=True)
    write_json(paths["domain_registry"], DOMAIN_REGISTRY)
    for profile in profiles:
        write_json(paths["profiles"] / f"{profile['person_id']}.json", profile)
    post_failures = validate_database(paths)
    if post_failures:
        raise PhilosopherDBError("written profiles failed validation:\n- " + "\n- ".join(post_failures))
    render_views(paths)
    for path in source_paths:
        path.unlink()
    for domain in ("General", "Metaphysics", "Metaethics"):
        directory = paths["db"] / domain
        if directory.exists() and not any(directory.iterdir()):
            directory.rmdir()
    return report


def load_domain_registry(paths: dict[str, Path]) -> dict[str, Any]:
    if paths["domain_registry"].exists():
        return read_json(paths["domain_registry"])
    return DOMAIN_REGISTRY


def render_views(paths: dict[str, Path]) -> None:
    profiles = load_profiles(paths["profiles"])
    registry = load_domain_registry(paths)
    paths["domains"].mkdir(parents=True, exist_ok=True)
    known_domain_files = set()
    for domain in registry["domains"]:
        domain_id = domain["domain_id"]
        known_domain_files.add(f"{domain_id}.md")
        backed: list[dict[str, Any]] = []
        prompted: list[dict[str, Any]] = []
        for profile in profiles.values():
            link = next((item for item in profile["domains"] if item["domain_id"] == domain_id), None)
            if not link:
                continue
            (backed if link["support_status"] == "source-backed" else prompted).append(profile)
        lines = [
            f"# {domain['label']}",
            "",
            "> Generated from canonical profiles. This view contains links only.",
            "",
            "## Source-backed connections",
            "",
        ]
        if backed:
            for profile in sorted(backed, key=lambda item: item["identity"]["display_name"]):
                lines.append(f"- [{profile['identity']['display_name']}](../Profiles/{profile['person_id']}.json)")
        else:
            lines.append("- None")
        lines.extend(["", "## Prompt-only connections", "", "> [source unverified] Discovery hints only.", ""])
        if prompted:
            for profile in sorted(prompted, key=lambda item: item["identity"]["display_name"]):
                lines.append(f"- [{profile['identity']['display_name']}](../Profiles/{profile['person_id']}.json)")
        else:
            lines.append("- None")
        (paths["domains"] / f"{domain_id}.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    for path in paths["domains"].glob("*.md"):
        if path.name not in known_domain_files:
            path.unlink()
    index_lines = [
        "# Philosophers Reference Database",
        "",
        "> Canonical v2 database. Read this index first, then load only the required profile.",
        "> `source-backed` routes to bibliography evidence; `prompt-only` is `[source unverified]` and cannot support manuscript assertions.",
        "",
        f"Profiles: {len(profiles)}. Domains: {len(registry['domains'])}.",
        "",
        "## Domain views",
        "",
    ]
    for domain in registry["domains"]:
        index_lines.append(f"- [{domain['label']}](Domains/{domain['domain_id']}.md)")
    index_lines.extend([
        "",
        "## Profiles",
        "",
        "| Philosopher | Person ID | Source-backed claims | Prompt-only claims | Domains |",
        "|---|---|---:|---:|---|",
    ])
    for profile in sorted(profiles.values(), key=lambda item: item["identity"]["display_name"]):
        counts = Counter(claim["support_status"] for claim in profile["claims"] if claim["status"] == "active")
        domain_labels = []
        for link in profile["domains"]:
            marker = "supported" if link["support_status"] == "source-backed" else "prompt"
            domain_labels.append(f"{link['domain_id']} ({marker})")
        index_lines.append(
            f"| [{profile['identity']['display_name']}](Profiles/{profile['person_id']}.json) "
            f"| `{profile['person_id']}` | {counts['source-backed']} | {counts['prompt-only']} "
            f"| {', '.join(domain_labels) or '—'} |"
        )
    (paths["db"] / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8", newline="\n")


def empty_state() -> dict[str, Any]:
    return {
        "record_type": "queue-state",
        "queue_version": "1.0",
        "processed_artifacts": {},
        "people": {},
        "candidates": {},
        "updated_at": now_iso(),
    }


def load_state(path: Path) -> dict[str, Any]:
    return read_json(path) if path.exists() else empty_state()


def extract_embedded_json(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if not blocks:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise PhilosopherDBError(f"no embedded JSON in {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise PhilosopherDBError(f"JSON input must be an object: {path}")
        return data
    return json.loads(blocks[-1])


def public_citation(metadata: dict[str, Any]) -> str:
    author = metadata.get("author", "Unknown")
    year = metadata.get("year", "nd")
    title = metadata.get("title", "Untitled")
    return f"{author} ({year}), {title}"


def normalize_observed_person(item: dict[str, Any]) -> dict[str, Any]:
    role = item.get("role", "background")
    if role not in VALID_ROLES:
        raise PhilosopherDBError(f"invalid philosopher role: {role}")
    canonical = clean_person_name(item.get("canonical_name") or item.get("display_name", ""))
    if not canonical:
        raise PhilosopherDBError("philosopher observation lacks a name")
    claims = []
    for raw_claim in item.get("claims", [])[:2]:
        statement = str(raw_claim.get("statement", "")).strip()
        locator = str(raw_claim.get("locator", "")).strip()
        if not statement or not locator:
            continue
        category = raw_claim.get("category", "other")
        if category not in CLAIM_CATEGORIES:
            category = "other"
        claim = {"statement": statement, "category": category, "locator": locator}
        if raw_claim.get("candidate_type"):
            claim["candidate_type"] = raw_claim["candidate_type"]
        if raw_claim.get("claim_id"):
            claim["claim_id"] = raw_claim["claim_id"]
        claims.append(claim)
    substantive = role in SUBSTANTIVE_ROLES and bool(item.get("substantive", True))
    return {
        **({"person_id": item["person_id"]} if item.get("person_id") else {}),
        "display_name": item.get("display_name") or canonical,
        "canonical_name": canonical,
        "aliases": sorted(set(item.get("aliases", []))),
        "role": role,
        "substantive": substantive,
        "claims": claims,
    }


def build_observation(data: dict[str, Any], input_path: Path, analysis_level: float | None = None) -> dict[str, Any]:
    if data.get("record_type") == "observation-batch":
        return data
    artifact_type = "summary" if "summary_id" in data else "analysis"
    artifact_id = data.get("summary_id") or data.get("report_id") or input_path.stem
    bib_key = data.get("bib_key") or data.get("source_bib_key")
    if not bib_key:
        raise PhilosopherDBError(f"artifact has no bibliography KEY: {input_path}")
    metadata = dict(data.get("source_metadata") or {})
    people = [normalize_observed_person(item) for item in data.get("philosopher_observations", [])]
    present = {(name_key(item["canonical_name"]), item["role"]) for item in people}
    core_thesis = str(data.get("core_thesis", "")).strip()
    for author in split_authors(str(metadata.get("author", ""))):
        if (name_key(author), "author") in present:
            continue
        claims = []
        if core_thesis:
            claims.append({"statement": core_thesis, "category": "position", "locator": "summary:core_thesis"})
        people.append({
            "display_name": author,
            "canonical_name": author,
            "aliases": [],
            "role": "author",
            "substantive": True,
            "claims": claims,
        })
    canonical_payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    artifact_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
    level = analysis_level if analysis_level is not None else (0.5 if artifact_type == "summary" else 1)
    generated_at = str(data.get("generated_at") or now_iso())
    return {
        "record_type": "observation-batch",
        "observation_id": f"PHO-{stable_hash(artifact_id, artifact_hash)}",
        "bib_key": bib_key,
        "artifact_id": artifact_id,
        "artifact_hash": artifact_hash,
        "artifact_type": artifact_type,
        "analysis_level": level,
        "source_metadata": {key: value for key, value in metadata.items() if key != "source_location"},
        "topics": list(data.get("topics") or data.get("domain_classification", {}).get("secondary_domains") or []),
        "people": people,
        "generated_at": generated_at,
    }


def observation_filename(observation: dict[str, Any]) -> str:
    stem = ascii_slug(observation["artifact_id"])[:80] or "artifact"
    return f"{stem}-{stable_hash(observation['artifact_id'], length=8)}.json"


def mapped_domains(topics: Iterable[str], registry: dict[str, Any]) -> set[str]:
    normalized_topics = [topic.lower().strip() for topic in topics]
    domains: set[str] = set()
    for domain in registry["domains"]:
        for keyword in domain["topic_keywords"]:
            keyword = keyword.lower()
            if any(keyword == topic or keyword in topic for topic in normalized_topics):
                domains.add(domain["domain_id"])
                break
    return domains


def load_observations(observations_root: Path) -> list[dict[str, Any]]:
    if not observations_root.exists():
        return []
    return [read_json(path) for path in sorted(observations_root.glob("*.json"))]


def candidate_id(candidate_type: str, name: str, artifact_id: str = "", statement: str = "", domain: str = "") -> str:
    return f"PHC-{stable_hash(candidate_type, name_key(name), artifact_id, statement, domain)}"


def evidence_from(
    observation: dict[str, Any],
    person: dict[str, Any],
    locator: str,
    approved: bool = False,
) -> dict[str, Any]:
    evidence = {
        "bib_key": observation["bib_key"],
        "source_type": "primary" if person["role"] == "author" else "secondary",
        "analysis_level": observation["analysis_level"],
        "locator": locator,
        "public_citation": public_citation(observation["source_metadata"]),
    }
    evidence["approved_at" if approved else "observed_at"] = now_iso()
    return evidence


def rebuild_queue(
    paths: dict[str, Path],
    previous: dict[str, Any],
    changed_artifacts: set[str] | None = None,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    changed_artifacts = changed_artifacts or set()
    profiles = load_profiles(paths["profiles"])
    aliases, ambiguous_aliases = profile_alias_map(profiles)
    registry = load_domain_registry(paths)
    observations = load_observations(paths["observations"])
    people_state: dict[str, dict[str, Any]] = {}
    resolved_observations: list[tuple[dict[str, Any], dict[str, Any], str, str | None, bool]] = []
    for observation in observations:
        domains = mapped_domains(observation["topics"], registry)
        for person in observation["people"]:
            key = name_key(person.get("canonical_name") or person["display_name"])
            explicit_id = person.get("person_id")
            person_id = explicit_id if explicit_id in profiles else aliases.get(key)
            ambiguous = key in ambiguous_aliases
            state_key = person_id or key
            entry = people_state.setdefault(state_key, {
                "person_id": person_id,
                "name_key": key,
                "display_name": person["display_name"],
                "ambiguous": ambiguous,
                "source_keys": set(),
                "substantive_source_keys": set(),
                "role_counts": Counter(),
                "domains": defaultdict(lambda: {"source_keys": set(), "central_source_keys": set()}),
            })
            entry["source_keys"].add(observation["bib_key"])
            entry["role_counts"][person["role"]] += 1
            if person["substantive"]:
                entry["substantive_source_keys"].add(observation["bib_key"])
            for domain in domains:
                entry["domains"][domain]["source_keys"].add(observation["bib_key"])
                if person["role"] in CENTRAL_DOMAIN_ROLES:
                    entry["domains"][domain]["central_source_keys"].add(observation["bib_key"])
            resolved_observations.append((observation, person, key, person_id, ambiguous))
    serial_people: dict[str, Any] = {}
    for state_key, entry in people_state.items():
        serial_people[state_key] = {
            "person_id": entry["person_id"],
            "name_key": entry["name_key"],
            "display_name": entry["display_name"],
            "ambiguous": entry["ambiguous"],
            "source_keys": sorted(entry["source_keys"]),
            "substantive_source_keys": sorted(entry["substantive_source_keys"]),
            "role_counts": dict(sorted(entry["role_counts"].items())),
            "domains": {
                domain: {
                    "source_keys": sorted(values["source_keys"]),
                    "central_source_keys": sorted(values["central_source_keys"]),
                }
                for domain, values in sorted(entry["domains"].items())
            },
        }
    candidates = dict(previous.get("candidates", {}))
    for candidate in candidates.values():
        if candidate.get("artifact_id") in changed_artifacts and candidate["status"] == "pending":
            candidate["status"] = "superseded"
            candidate["updated_at"] = now_iso()
    timestamp = now_iso()
    for observation, person, key, person_id, ambiguous in resolved_observations:
        if not person_id or not person["substantive"]:
            continue
        for claim in person["claims"]:
            kind = claim.get("candidate_type", "new-claim")
            cid = candidate_id(kind, person_id, observation["artifact_id"], claim["statement"])
            if cid in candidates:
                if candidates[cid]["status"] == "superseded":
                    candidates[cid]["status"] = "pending"
                    candidates[cid]["evidence"] = evidence_from(observation, person, claim["locator"])
                    candidates[cid]["updated_at"] = timestamp
                continue
            candidates[cid] = {
                "candidate_id": cid,
                "candidate_type": kind,
                "status": "pending",
                "person_id": person_id,
                "name_key": key,
                "display_name": person["display_name"],
                "artifact_id": observation["artifact_id"],
                "source_keys": [observation["bib_key"]],
                "claim": claim,
                "evidence": evidence_from(observation, person, claim["locator"]),
                "created_at": timestamp,
                "updated_at": timestamp,
            }
    for entry in serial_people.values():
        if entry["person_id"] or entry["ambiguous"]:
            continue
        if len(entry["source_keys"]) < 5 or len(entry["substantive_source_keys"]) < 3:
            continue
        cid = candidate_id("new-person", entry["display_name"])
        if cid not in candidates:
            candidates[cid] = {
                "candidate_id": cid,
                "candidate_type": "new-person",
                "status": "pending",
                "name_key": entry["name_key"],
                "display_name": entry["display_name"],
                "source_keys": entry["source_keys"],
                "created_at": timestamp,
                "updated_at": timestamp,
            }
        elif candidates[cid]["status"] == "pending":
            candidates[cid]["source_keys"] = entry["source_keys"]
            candidates[cid]["updated_at"] = timestamp
    processed = {
        observation["artifact_id"]: {
            "artifact_hash": observation["artifact_hash"],
            "observation_file": observation_filename(observation),
            "bib_key": observation["bib_key"],
        }
        for observation in observations
    }
    state = {
        "record_type": "queue-state",
        "queue_version": "1.0",
        "processed_artifacts": processed,
        "people": serial_people,
        "candidates": dict(sorted(candidates.items())),
        "updated_at": timestamp,
    }
    return state, profiles


def synchronize_domains(
    paths: dict[str, Path],
    state: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
) -> int:
    observations = load_observations(paths["observations"])
    by_key: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    aliases, _ = profile_alias_map(profiles)
    for observation in observations:
        for person in observation["people"]:
            key = name_key(person.get("canonical_name") or person["display_name"])
            person_id = person.get("person_id") or aliases.get(key)
            if person_id:
                by_key[person_id].append((observation, person))
    updated = 0
    for entry in state["people"].values():
        person_id = entry.get("person_id")
        if not person_id or person_id not in profiles:
            continue
        profile = profiles[person_id]
        for domain_id, domain_state in entry["domains"].items():
            if len(domain_state["source_keys"]) < 2 or not domain_state["central_source_keys"]:
                continue
            evidence: list[dict[str, Any]] = []
            seen_keys: set[str] = set()
            link = next((item for item in profile["domains"] if item["domain_id"] == domain_id), None)
            existing_approved = {
                (item["bib_key"], item["locator"]): item["approved_at"]
                for item in (link or {}).get("evidence", [])
            }
            for observation, person in by_key[person_id]:
                if observation["bib_key"] not in domain_state["source_keys"] or observation["bib_key"] in seen_keys:
                    continue
                item = evidence_from(observation, person, "topics/domain classification", approved=True)
                item["approved_at"] = existing_approved.get(
                    (item["bib_key"], item["locator"]), item["approved_at"]
                )
                evidence.append(item)
                seen_keys.add(observation["bib_key"])
            if link and link["support_status"] == "source-backed" and link["evidence"] == evidence:
                continue
            if link:
                link["support_status"] = "source-backed"
                link["evidence"] = evidence
            else:
                profile["domains"].append({"domain_id": domain_id, "support_status": "source-backed", "evidence": evidence})
            profile["domains"].sort(key=lambda item: item["domain_id"])
            profile["updated_at"] = now_iso()
            updated += 1
        write_json(paths["profiles"] / f"{person_id}.json", profile)
    return updated


def observe(paths: dict[str, Path], inputs: list[Path], dry_run: bool, analysis_level: float | None) -> dict[str, Any]:
    observations = [build_observation(extract_embedded_json(path), path, analysis_level) for path in inputs]
    previous = load_state(paths["state"])
    changed: set[str] = set()
    unchanged = 0
    for observation in observations:
        prior = previous["processed_artifacts"].get(observation["artifact_id"])
        if prior and prior.get("artifact_hash") == observation["artifact_hash"]:
            unchanged += 1
        else:
            changed.add(observation["artifact_id"])
    if dry_run:
        return {"inputs": len(inputs), "changed": len(changed), "unchanged": unchanged, "dry_run": True}
    paths["observations"].mkdir(parents=True, exist_ok=True)
    for observation in observations:
        write_json(paths["observations"] / observation_filename(observation), observation)
    state, profiles = rebuild_queue(paths, previous, changed)
    domain_updates = synchronize_domains(paths, state, profiles)
    write_json(paths["state"], state)
    if domain_updates:
        render_views(paths)
    return {
        "inputs": len(inputs),
        "changed": len(changed),
        "unchanged": unchanged,
        "pending_candidates": sum(item["status"] == "pending" for item in state["candidates"].values()),
        "domain_updates": domain_updates,
        "dry_run": False,
    }


def next_claim_id(profile: dict[str, Any]) -> str:
    numbers = []
    prefix = f"P-{profile['person_id']}-C"
    for claim in profile["claims"]:
        if claim["claim_id"].startswith(prefix):
            try:
                numbers.append(int(claim["claim_id"][len(prefix):]))
            except ValueError:
                pass
    return f"{prefix}{max(numbers, default=0) + 1:04d}"


def approve_candidate(
    paths: dict[str, Path],
    cid: str,
    person_id_override: str | None = None,
    statement_override: str | None = None,
    category_override: str | None = None,
    merge_claim_id: str | None = None,
) -> dict[str, Any]:
    state = load_state(paths["state"])
    candidate = state["candidates"].get(cid)
    if not candidate:
        raise PhilosopherDBError(f"unknown candidate: {cid}")
    if candidate["status"] != "pending":
        raise PhilosopherDBError(f"candidate is not pending: {cid}")
    profiles = load_profiles(paths["profiles"])
    if candidate["candidate_type"] == "new-person":
        person_id = person_id_override or ascii_slug(candidate["display_name"])
        if person_id in profiles:
            raise PhilosopherDBError(f"profile already exists: {person_id}")
        timestamp = now_iso()
        profile = {
            "profile_version": "1.0",
            "person_id": person_id,
            "identity": {
                "display_name": candidate["display_name"],
                "canonical_name": candidate["display_name"],
                "aliases": [candidate["display_name"]],
                "legacy_paths": [],
            },
            "claims": [],
            "domains": [],
            "relations": [],
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        write_json(paths["profiles"] / f"{person_id}.json", profile)
        candidate["person_id"] = person_id
    else:
        person_id = person_id_override or candidate.get("person_id")
        if not person_id or person_id not in profiles:
            raise PhilosopherDBError("claim candidate has no resolvable profile")
        profile = profiles[person_id]
        observed_evidence = candidate.get("evidence")
        if not observed_evidence:
            raise PhilosopherDBError("claim candidate has no evidence")
        evidence = {key: value for key, value in observed_evidence.items() if key != "observed_at"}
        evidence["approved_at"] = now_iso()
        statement = statement_override or candidate.get("claim", {}).get("statement")
        category = category_override or candidate.get("claim", {}).get("category", "other")
        if not statement or category not in CLAIM_CATEGORIES:
            raise PhilosopherDBError("approved claim needs a valid statement and category")
        target_claim_id = merge_claim_id or candidate.get("claim", {}).get("claim_id")
        if candidate["candidate_type"] == "additional-evidence" and not target_claim_id:
            raise PhilosopherDBError("additional-evidence approval requires --merge-claim-id")
        if target_claim_id:
            target = next((item for item in profile["claims"] if item["claim_id"] == target_claim_id), None)
            if not target:
                raise PhilosopherDBError(f"unknown merge claim: {target_claim_id}")
            if not any(item["bib_key"] == evidence["bib_key"] and item["locator"] == evidence["locator"] for item in target["evidence"]):
                target["evidence"].append(evidence)
            target["support_status"] = "source-backed"
            if candidate["candidate_type"] == "conflict":
                target["dispute_status"] = "contested"
        else:
            profile["claims"].append({
                "claim_id": next_claim_id(profile),
                "category": category,
                "statement": statement,
                "support_status": "source-backed",
                "dispute_status": "contested" if candidate["candidate_type"] == "conflict" else "unmarked",
                "status": "active",
                "evidence": [evidence],
            })
        profile["updated_at"] = now_iso()
        failures = validate_profile(profile)
        if failures:
            raise PhilosopherDBError("approval would create an invalid profile:\n- " + "\n- ".join(failures))
        write_json(paths["profiles"] / f"{person_id}.json", profile)
    candidate["status"] = "approved"
    candidate["updated_at"] = now_iso()
    state["updated_at"] = now_iso()
    if candidate["candidate_type"] == "new-person":
        state, profiles = rebuild_queue(paths, state)
        synchronize_domains(paths, state, profiles)
        candidate = state["candidates"][cid]
    write_json(paths["state"], state)
    render_views(paths)
    return candidate


def change_candidate_status(paths: dict[str, Path], cid: str, action: str) -> dict[str, Any]:
    state = load_state(paths["state"])
    candidate = state["candidates"].get(cid)
    if not candidate:
        raise PhilosopherDBError(f"unknown candidate: {cid}")
    if action == "reject":
        if candidate["status"] != "pending":
            raise PhilosopherDBError("only pending candidates can be rejected")
        candidate["status"] = "rejected"
    elif action == "reopen":
        if candidate["status"] not in {"rejected", "superseded"}:
            raise PhilosopherDBError("only rejected or superseded candidates can be reopened")
        candidate["status"] = "pending"
    candidate["updated_at"] = now_iso()
    state["updated_at"] = now_iso()
    write_json(paths["state"], state)
    return candidate


def status_report(paths: dict[str, Path], person: str | None = None) -> dict[str, Any]:
    state = load_state(paths["state"])
    candidates = list(state["candidates"].values())
    if person:
        key = name_key(person)
        candidates = [
            item for item in candidates
            if item.get("person_id") == person or item.get("name_key") == key or name_key(item["display_name"]) == key
        ]
    return {
        "processed_artifacts": len(state["processed_artifacts"]),
        "observed_people": len(state["people"]),
        "candidate_counts": dict(sorted(Counter(item["status"] for item in candidates).items())),
        "candidates": sorted(candidates, key=lambda item: (item["status"], item["candidate_type"], item["candidate_id"])),
        "updated_at": state["updated_at"],
    }


def init_queue(paths: dict[str, Path]) -> dict[str, Any]:
    paths["observations"].mkdir(parents=True, exist_ok=True)
    if not paths["state"].exists():
        write_json(paths["state"], empty_state())
    return status_report(paths)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    migrate = sub.add_parser("migrate", help="convert legacy Markdown profiles")
    migrate.add_argument("--apply", action="store_true")
    sub.add_parser("init-queue", help="create the private staging queue")
    observe_parser = sub.add_parser("observe", help="batch observations from summaries/analyses")
    observe_parser.add_argument("--input", type=Path, action="append", required=True)
    observe_parser.add_argument("--analysis-level", type=float, choices=[0.5, 1, 2, 3])
    observe_parser.add_argument("--dry-run", action="store_true")
    status = sub.add_parser("status", help="show compact queue status")
    status.add_argument("--person")
    status.add_argument("--json", action="store_true")
    approve = sub.add_parser("approve", help="apply an approved candidate")
    approve.add_argument("candidate_id")
    approve.add_argument("--person-id")
    approve.add_argument("--statement")
    approve.add_argument("--category", choices=sorted(CLAIM_CATEGORIES))
    approve.add_argument("--merge-claim-id")
    reject = sub.add_parser("reject", help="reject a pending candidate")
    reject.add_argument("candidate_id")
    reopen = sub.add_parser("reopen", help="reopen a rejected/superseded candidate")
    reopen.add_argument("candidate_id")
    sub.add_parser("rebuild", help="validate profiles and regenerate views")
    sub.add_parser("validate", help="validate canonical profiles")
    resolve = sub.add_parser("resolve", help="resolve a name or legacy alias")
    resolve.add_argument("name")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    paths = paths_for(args.repo_root.resolve())
    try:
        if args.command == "migrate":
            result = migrate_legacy(paths, args.apply)
        elif args.command == "init-queue":
            result = init_queue(paths)
        elif args.command == "observe":
            result = observe(paths, [path.resolve() for path in args.input], args.dry_run, args.analysis_level)
        elif args.command == "status":
            result = status_report(paths, args.person)
        elif args.command == "approve":
            result = approve_candidate(
                paths, args.candidate_id, args.person_id, args.statement,
                args.category, args.merge_claim_id,
            )
        elif args.command in {"reject", "reopen"}:
            result = change_candidate_status(paths, args.candidate_id, args.command)
        elif args.command == "rebuild":
            failures = validate_database(paths)
            if failures:
                raise PhilosopherDBError("validation failed:\n- " + "\n- ".join(failures))
            render_views(paths)
            result = {"profiles": len(load_profiles(paths["profiles"])), "views": "rebuilt"}
        elif args.command == "validate":
            failures = validate_database(paths)
            if failures:
                raise PhilosopherDBError("validation failed:\n- " + "\n- ".join(failures))
            result = {"profiles": len(load_profiles(paths["profiles"])), "status": "valid"}
        elif args.command == "resolve":
            profiles = load_profiles(paths["profiles"])
            person_id, ambiguous = resolve_person(args.name, profiles)
            result = {"query": args.name, "person_id": person_id, "ambiguous": ambiguous}
        else:
            raise AssertionError(args.command)
    except (OSError, json.JSONDecodeError, PhilosopherDBError) as exc:
        print(f"philosopher-db: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
