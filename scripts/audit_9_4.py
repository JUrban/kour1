#!/usr/bin/env python3
"""Verify frozen files and replay finite controls, not mathematical priority."""
import hashlib
import json
from pathlib import Path

from check_9_4 import run

ROOT = Path(__file__).resolve().parents[1]
summary = json.loads((ROOT/'results/9.4-summary.json').read_text())
assert summary['problem'] == '9.4'
assert summary['candidate_number'] == 34
assert summary['status'] == 'COMPLETE_NEGATIVE_CANDIDATE'
assert summary['novelty'] == 'pending' and summary['outside_reviews'] == 0
required = {
    'docs/21tkt.pdf',
    'research/9.4-plan.md', 'research/9.4-proof.md', 'research/9.4-review.md',
    'scripts/check_9_4.py', 'scripts/audit_9_4.py',
    'results/9.4-controls.json', 'results/9.4-controls.log',
    'results/9.4-controls-process.json',
    'references/cache/notebook-9.4-p32.png',
    'references/cache/gvaramiya-quasivarieties-1985.pdf',
    'references/cache/gvaramiya-quasivarieties-1985.txt',
    'references/cache/gvaramiya-quasivarieties-1985-p326.png',
    'references/cache/gvaramiya-quasivarieties-1985-p328.png',
    'references/cache/krapez-marinkovic-isotopy-2016.pdf',
    'references/cache/krapez-marinkovic-isotopy-2016.txt',
    'references/cache/krapez-marinkovic-isotopy-2016-check-02.png',
    'references/cache/krapez-marinkovic-isotopy-2016-check-03.png',
}
assert set(summary['sha256']) == required
for name, digest in summary['sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
stored = json.loads((ROOT/'results/9.4-controls.json').read_text())
assert run() == stored
process = json.loads((ROOT/'results/9.4-controls-process.json').read_text())
assert process['actual_returncode'] == 0
assert (ROOT/'results/9.4-controls.log').read_bytes() == b''
for name, digest in process['sha256'].items():
    assert summary['sha256'][name] == digest
assert sum(r['latin_squares'] for r in stored['latin']) == 591
assert len(stored['affine']) == 12
assert sum(r['axiom_checks'] for r in stored['affine']) == 93252
assert sum(r['boolean_identity_checks'] for r in stored['affine']) == 2396744
assert len(stored['separators']) == 10
print('PASS_94_PACKET 18 hashes; 591 Latin squares; 12 affine models; '
      '93,252 axiom checks; 2,396,744 Boolean identity checks; '
      '10 finite separating witnesses; priority and outside review pending')
