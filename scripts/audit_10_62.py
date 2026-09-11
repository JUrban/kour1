#!/usr/bin/env python3
"""Check packet integrity and retained completion; does not verify geometry."""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
summary = json.loads((root/'results/10.62-summary.json').read_text())
status = json.loads((root/'results/10.62-gap-status.json').read_text())
assert summary['candidate_number'] == 29
assert summary['outside_reviews'] == 0
assert summary['novelty'] == 'pending'
assert status['returncode'] == 0 and status['status'] == 'PASS'
assert status['clean_log'] and status['completion_sentinel']
for packet in [summary, status]:
    for name, digest in packet['sha256'].items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, name
content = (root/'results/10.62-gap.log').read_text()
assert not any(x in content for x in
               ['Error,', 'Syntax error', 'Syntax warning', 'Traceback'])
assert content.rstrip().endswith('PASS_1062_GAP')
counts = {key: int(value) for key, value in re.findall(r'(\w+)=(\d+)', content)}
assert counts == summary['finite_controls']
assert counts['odd_presentations'] == counts['even_presentations'] == 50
assert counts['c2_assignments'] == 8
assert counts['dihedral_pairs'] == sum(n*(n-1) for n in range(3, 41))
assert counts['odd_pairs'] + counts['even_pairs'] == counts['dihedral_pairs']
assert 'research/10.62-proof.md' in summary['sha256']
assert 'research/10.62-review.md' in summary['sha256']
assert 'references/cache/amelio-bounded-exponent-2025-v2.pdf' in summary['sha256']
assert 'scripts/audit_10_62.py' in summary['sha256']
print(f"PASS_1062_PACKET {len(summary['sha256'])} hashes; "
      f"{counts['dihedral_pairs']} finite pairs; geometry imported")
