#!/usr/bin/env python3
"""Check review links and historical hashes; do not rerun mathematical tests.

This is an inventory audit, not a proof verifier. Historical expected hashes
are read from existing manifests and never rewritten by this program.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
PATH_FIELDS = (
    "principal_proofs", "review_or_source_scope", "reports",
    "evidence_entry_points",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="results/candidate-handoff-integrity.json")
    args = parser.parse_args()
    started = time.monotonic()
    ledger_path = ROOT / "research/complete-candidate-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    candidates = ledger["candidates"]
    assert ledger["candidate_count"] == len(candidates) == 46
    assert len({row["problem"] for row in candidates}) == len(candidates)
    assert [row["candidate_number"] for row in candidates] == list(range(1, 47))
    assert all(row["outside_reviews"] == 0 for row in candidates)
    statements = {
        row["id"]: row for row in
        json.loads((ROOT / "research/problem-index.json").read_text())
    }
    tracked = set(subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode().split("\0"))
    cache = {}
    missing = set()
    untracked = set()
    mismatches = []
    bindings = []
    manifest_paths = set()
    manifest_counts = {}
    candidate_rows = []

    def inspect(path):
        if path in cache:
            return cache[path]
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Non-repository path in manifest: {path}")
        target = ROOT / relative
        if not target.is_file():
            missing.add(path)
            cache[path] = None
            return None
        if path not in tracked:
            untracked.add(path)
        digest = hashlib.sha256()
        size = 0
        with target.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
                size += len(block)
        result = {"path": path, "bytes": size, "sha256": digest.hexdigest()}
        cache[path] = result
        return result

    def audit_manifest(path):
        if path in manifest_paths:
            return manifest_counts[path]
        observed = inspect(path)
        if observed is None or not path.endswith(".json"):
            return 0
        obj = json.loads((ROOT / path).read_text())
        if not isinstance(obj, dict):
            return 0
        expected = []
        if isinstance(obj.get("sha256"), dict):
            expected.extend(
                {"path": name, "sha256": digest}
                for name, digest in obj["sha256"].items()
                if isinstance(digest, str)
            )
        if isinstance(obj.get("files"), list):
            expected.extend(
                entry for entry in obj["files"]
                if isinstance(entry, dict) and
                isinstance(entry.get("path"), str) and
                isinstance(entry.get("sha256"), str)
            )
        if not expected:
            return 0
        manifest_paths.add(path)
        manifest_counts[path] = len(expected)
        for entry in expected:
            current = inspect(entry["path"])
            record = {"manifest": path, "path": entry["path"],
                      "expected_sha256": entry["sha256"]}
            if "bytes" in entry:
                record["expected_bytes"] = entry["bytes"]
            record["matches"] = (
                current is not None and
                current["sha256"] == entry["sha256"] and
                ("bytes" not in entry or current["bytes"] == entry["bytes"])
            )
            bindings.append(record)
            if not record["matches"]:
                mismatches.append({**record, "observed": current})
            name = entry["path"]
            if name.endswith(("-packet.json", "-summary.json", "-provenance.json")):
                audit_manifest(name)
        return len(expected)

    for row in candidates:
        source = statements[row["problem"]]
        assert row["original_statement"] == source["text"], row["problem"]
        assert row["statement_index_pdf_page"] == source["pdf_page"], row["problem"]
        paths = sorted({path for field in PATH_FIELDS for path in row[field]})
        for path in paths:
            inspect(path)
        counts = {
            path: audit_manifest(path) for path in row["evidence_entry_points"]
        }
        latest = subprocess.check_output(
            ["git", "log", "-1", "--format=%H", "--", *row["principal_proofs"]],
            cwd=ROOT,
        ).decode().strip()
        assert latest, row["problem"]
        candidate_rows.append({
            "problem": row["problem"],
            "covered_subparts": row["covered_subparts"],
            "linked_paths": paths,
            "historical_binding_counts_at_entry_points": counts,
            "has_historical_manifest": any(counts.values()),
            "latest_principal_proof_commit": latest,
        })
    for path in ("docs/21tkt.pdf", "research/problem-index.json"):
        inspect(path)
    ok = not missing and not mismatches and not untracked
    result = {
        "status": "PASS" if ok else "FAIL",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "scope": "Inventory links, statement-index agreement, tracked-file availability, and historical hash bindings only. No mathematical verifier was rerun, no new PDF visual audit was performed, and no outside review or priority certification is implied.",
        "candidate_count": len(candidates),
        "outside_reviews": 0,
        "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        "auditor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "historical_manifests": sorted(manifest_paths),
        "historical_binding_count": len(bindings),
        "candidates_with_historical_manifests": sum(
            row["has_historical_manifest"] for row in candidate_rows),
        "unique_files_hashed": sum(value is not None for value in cache.values()),
        "unique_bytes_hashed": sum(value["bytes"] for value in cache.values() if value),
        "missing_paths": sorted(missing),
        "untracked_paths": sorted(untracked),
        "historical_mismatches": mismatches,
        "candidates": candidate_rows,
        "current_file_observations": [cache[name] for name in sorted(cache) if cache[name]],
        "historical_bindings": bindings,
    }
    output = ROOT / args.output
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "candidate_count", "historical_binding_count",
        "candidates_with_historical_manifests", "unique_files_hashed",
        "unique_bytes_hashed", "missing_paths", "untracked_paths",
        "historical_mismatches", "elapsed_seconds",
    )}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
