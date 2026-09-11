#!/usr/bin/env python3
"""Integrity audit and replay of the prior-consequence packet."""
import hashlib
import json
from pathlib import Path

from check_7_58 import run_controls

ROOT = Path(__file__).resolve().parents[1]
summary = json.loads((ROOT/'results/7.58-summary.json').read_text())
assert summary['status'] == 'PRIOR_CONSEQUENCE'
assert summary['complete_candidate_increment'] == 0
for name, digest in summary['sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
stored = json.loads((ROOT/'results/7.58-controls.json').read_text())
assert run_controls() == stored
process = json.loads((ROOT/'results/7.58-controls-process.json').read_text())
assert process['actual_returncode'] == 0 and process['stderr'] == ''
assert process['script_sha256'] == summary['sha256']['scripts/check_7_58.py']
checks = sum(c['membership_checks'] for c in stored['graph_cases'])
assert checks == 82080
assert stored['matrix_case']['membership_checks'] == 54
print(f"PASS_758_PACKET {len(summary['sha256'])} hashes; "
      '82,134 membership checks; prior consequence, no new candidate')
