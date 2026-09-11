#!/usr/bin/env python3
"""Audit the two disjoint completed ranges of an exploratory table screen."""
from pathlib import Path
import gzip
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
old_path = ROOT / 'results/4.55-table-screen-stopped.log.gz'
tail_path = ROOT / 'results/4.55-table-screen-tail.log'
old = gzip.decompress(old_path.read_bytes()).decode()
tail = tail_path.read_text()
checkpoint = 'PROGRESS tables=2600 available=7051\n'
assert old.count(checkpoint) == 1
prefix = old.split(checkpoint)[0] + checkpoint
assert 'Error' not in prefix
assert old.rstrip().endswith('Error, <p> must be a prime')
assert 'DONE' not in old
assert 'START range=2601..2750' in tail
assert 'Error' not in tail
assert re.search(r'DONE tables=150 available=522 rationality_hits=44 '
                 r'parity_hits=20 range=2601\.\.\s*2750\s*$', tail)

def hits(log, kind):
    return re.findall(r'^' + kind + r'_HIT (\S+) p=(\d+)', log, re.M)

rows = []
for label, log, count, available in [
        ('1..2600', prefix, 2600, 7051),
        ('2601..2750', tail, 150, 522)]:
    rh = hits(log, 'RATIONALITY')
    ph = hits(log, 'PARITY')
    assert len(set(rh)) == len(rh)
    assert len(set(ph)) == len(ph)
    rows.append(dict(range=label, tables=count, available_cases=available,
                     rationality_hits=len(rh), parity_hits=len(ph),
                     checked_text_sha256=hashlib.sha256(log.encode()).hexdigest()))
for kind in ['RATIONALITY', 'PARITY']:
    assert not set(hits(prefix, kind)).intersection(hits(tail, kind))
assert rows[1]['rationality_hits'] == 44
assert rows[1]['parity_hits'] == 20
result = dict(
    status='COMPLETE_EXPLORATORY_RANGES', gap_version='4.16.1',
    tables=sum(row['tables'] for row in rows),
    available_cases=sum(row['available_cases'] for row in rows),
    rationality_hits=sum(row['rationality_hits'] for row in rows),
    parity_hits=sum(row['parity_hits'] for row in rows), ranges=rows,
    logs={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in [old_path, tail_path]},
    screen_sha256=hashlib.sha256((ROOT/'scripts/screen_4_55.g').read_bytes()).hexdigest(),
    exclusion='Discard the aborted first run after its table-2600 checkpoint; '
              'the corrected run independently covers tables 2601..2750.',
    limitation='Hits are exploratory constraints, not new examples or proofs. '
               'Only the separate 3.A7 candidate has undergone module reconstruction '
               'and a proof of incompatible indecomposable refinements.')
output = ROOT/'results/4.55-table-screen-summary.json'
output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
