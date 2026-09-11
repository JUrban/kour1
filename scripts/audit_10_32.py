#!/usr/bin/env python3
"""Audit retained evidence integrity, not the imported general theorems."""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
summary = json.loads((root/'results/10.32-summary.json').read_text())
status = json.loads((root/'results/10.32-gap-status.json').read_text())
replay = json.loads((root/'results/10.32-replay-summary.json').read_text())
assert summary['candidate_number'] == 30
assert summary['novelty'] == 'pending' and summary['outside_reviews'] == 0
for packet in (summary, status):
    for name, digest in packet['sha256'].items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, name
assert status['status'] == 'PASS' and status['returncode'] == 0
assert status['clean_log'] and status['complete']
log = (root/'results/10.32-gap.log').read_text()
assert log.rstrip().endswith('PASS_1032_WITNESSES')
assert not any(x in log for x in ('Error,', 'Syntax warning', 'Syntax error', 'Traceback'))
assert re.search(r'witnesses=6143\s+positive_genus_checks=3040\s+transpositions=7\s+root_identities=\s*49144', log)
assert replay['status'] == 'PASS' and replay['witnesses'] == 6143
assert replay['degree_prime_pairs'] == 7 and replay['exact_rational_margins'] == 6
assert replay['counts'] == dict(root_identities=49144, even=3096, odd=3047)
assert replay['certificate_sha256'] == summary['sha256']['results/10.32-witnesses.json']
assert len(json.loads((root/'results/10.32-witnesses.json').read_text())) == 6143
failed = json.loads((root/'results/10.32-first-failed-status.json').read_text())
assert failed['status'] == 'FAIL' and not failed['clean_log']
try:
    json.loads((root/'results/10.32-second-format-witnesses.txt').read_text())
except json.JSONDecodeError:
    pass
else:
    raise AssertionError('second attempt must preserve its serialization defect')
assert 'research/10.32-proof.md' in summary['sha256']
assert 'research/10.32-review.md' in summary['sha256']
assert 'scripts/audit_10_32.py' in summary['sha256']
print(f"PASS_1032_PACKET {len(summary['sha256'])} hashes; 6143 witnesses; general inputs imported")
