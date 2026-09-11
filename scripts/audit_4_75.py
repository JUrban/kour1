#!/usr/bin/env python3
"""Check the 4.75 packet and its frozen 10.62 dependency, not geometry."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
summary = json.loads((root / 'results/4.75-summary.json').read_text())
assert summary['problem'] == '4.75'
assert summary['candidate_number'] == 33
assert summary['outside_reviews'] == 0
assert summary['novelty'] == 'pending'
assert summary['dependency'] == 'results/10.62-summary.json'
required = {
    'docs/21tkt.pdf',
    'research/4.75-plan.md',
    'research/4.75-proof.md',
    'research/4.75-review.md',
    'results/10.62-summary.json',
    'research/10.62-proof.md',
    'research/10.62-review.md',
    'scripts/audit_10_62.py',
    'scripts/audit_4_75.py',
    'references/cache/notebook-4.75-p14.png',
    'references/cache/durakov-2-rank-one-2019.pdf',
    'references/cache/durakov-2-rank-one-2019.txt',
    'references/cache/durakov-2-rank-one-2019-p65.png',
}
assert set(summary['sha256']) == required
for name, digest in summary['sha256'].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
dependency = subprocess.run(
    [sys.executable, 'scripts/audit_10_62.py'], cwd=root,
    capture_output=True, text=True, timeout=60,
)
assert dependency.returncode == 0, (dependency.returncode, dependency.stderr)
assert dependency.stdout.startswith('PASS_1062_PACKET '), dependency.stdout
assert not dependency.stderr, dependency.stderr
print(dependency.stdout.strip())
print(f"PASS_475_PACKET {len(required)} hashes; frozen dependency passed; "
      'elementary deduction and imported geometry require mathematical review')
