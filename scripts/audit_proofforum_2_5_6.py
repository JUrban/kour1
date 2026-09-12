#!/usr/bin/env python3
"""Verify source bindings, saved process results, and independent controls.

This checks evidence integrity and bounded calculations, not the universal
mathematical proofs or the imported topological/homological theorems.
"""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(text):
    pattern = (r"CASE p=(\d+) n=(\d+) size=(\d+) class=(\d+) "
               r"abelian=(\[[^]]*\]) lower_sizes=\s*(\[[^]]*\])")
    result = {}
    for match in re.finditer(pattern, text):
        p, n, order, nilclass = map(int, match.groups()[:4])
        abelian, lower = map(ast.literal_eval, match.groups()[4:])
        assert (p, n) not in result
        assert order == p ** (2*n+1) and nilclass == n+1
        assert abelian == [p, p**n]
        assert lower == [order] + [p**(n+1-r) for r in range(1, n+2)]
        result[p, n] = (order, nilclass, abelian, lower)
    return result


def main():
    manifest = json.loads((ROOT / "results/proofforum-2-5-6-packet.json").read_text())
    assert manifest["new_candidates_added"] == 0
    for item in manifest["files"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"]
        assert digest(path) == item["sha256"], path
    for name in ["proofforum-2-5-6-source-downloads", "19.1-dependency-downloads"]:
        for item in json.loads((ROOT / ("results/" + name + ".json")).read_text()):
            path = ROOT / item["path"]
            assert item["status"] == 200
            assert item["bytes"] == path.stat().st_size
            assert item["sha256"] == digest(path)
    for name in ["coordinates", "gap"]:
        base = ROOT / ("results/17.113-" + name)
        record = json.loads(Path(str(base) + "-process.json").read_text())
        out, err = Path(str(base) + ".log"), Path(str(base) + ".stderr")
        assert record["actual_returncode"] == 0 and not record["timed_out"]
        assert record["stdout_sha256"] == digest(out)
        assert record["stderr_sha256"] == digest(err)
        assert not err.read_bytes() and "Error" not in out.read_text()
        assert record["sentinel_seen"] and record["sentinel"] in out.read_text()

    expected = {(p, n) for p in [2, 3, 5, 7, 11]
                for n in range(1, 5 if p == 11 else 7)}
    gap_rows = rows((ROOT / "results/17.113-gap.log").read_text())
    assert set(gap_rows) == expected and len(gap_rows) == 28
    stopped = ROOT / "results/17.113-stopped-run"
    record = json.loads((stopped / "17.113-gap-process.json").read_text())
    assert record["actual_returncode"] == 1 and not record["sentinel_seen"]
    assert record["stdout_sha256"] == digest(stopped / "17.113-gap.log")
    assert record["stderr_sha256"] == digest(stopped / "17.113-gap.stderr")
    assert "PASS_17113_GAP" not in (stopped / "17.113-gap.log").read_text()
    assert rows((stopped / "17.113-gap.log").read_text()) == gap_rows

    run = subprocess.run(["python3", "scripts/check_17_113.py"], cwd=ROOT,
                         capture_output=True, timeout=30)
    assert run.returncode == 0 and not run.stderr
    assert run.stdout == (ROOT / "results/17.113-coordinates.log").read_bytes()
    coordinates = json.loads(run.stdout.decode().split("\nPASS_")[0])
    assert {(r["p"], r["n"]) for r in coordinates} == {
        (p, n) for p in [2, 3, 5, 7, 11] for n in range(1, 4)}
    assert sum(r["projection_pairs"] for r in coordinates) == 507074
    assert sum(r["associativity_controls"] for r in coordinates) == 15000
    for row in coordinates:
        a = gap_rows[row["p"], row["n"]]
        assert (row["size"], row["nilpotency_class"], row["abelian_invariants"]) == a[:3]
    print("PASS_PROOFFORUM_2_5_6_PACKET files=%d gap_cases=28 coordinate_cases=15 "
          "projection_pairs=507074 new_candidates=0" % len(manifest["files"]))


if __name__ == "__main__":
    main()
