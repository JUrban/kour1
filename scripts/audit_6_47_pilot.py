#!/usr/bin/env python3
"""Audit frozen hashes and replay all exported pilot tables."""
import hashlib
import json
from pathlib import Path

from run_6_47_pilot import check
from classify_6_47_tables import classify

ROOT = Path(__file__).resolve().parents[1]
summary = json.loads((ROOT / 'results/6.47-pilot-packet.json').read_text())
assert summary['scope'] == 'bounded_pilot_and_class_two_partial'
assert summary['complete_candidate_increment'] == 0
for name, value in summary['sha256'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == value, name
pilot = json.loads((ROOT / 'results/6.47-pilot-summary.json').read_text())
assert [(r['n'], r['id']) for r in pilot['cases']] == [
    (6,1), (8,3), (12,3), (16,6), (24,3), (32,2)]
outer = json.loads((ROOT / 'results/6.47-pilot-outer-process.json').read_text())
assert outer['actual_returncode'] == 0
assert outer['completion_sentinel'] == 'PASS_647_PILOT'
assert outer['summary_sha256'] == hashlib.sha256(
    (ROOT / 'results/6.47-pilot-summary.json').read_bytes()).hexdigest()
initial = json.loads((ROOT / 'results/6.47-pilot-initial-process.json').read_text())
assert initial['actual_returncode'] == 1
total_operations = total_triples = total_associative = 0
for record in pilot['cases']:
    stem = ROOT / f"results/6.47-pilot-{record['n']}-{record['id']}"
    path = lambda suffix: stem.with_name(stem.name + suffix)
    process = json.loads(path('-process.json').read_text())
    assert process['actual_returncode'] == 0 and not process['timed_out']
    assert process['clean_log'] and process['sentinel']
    content = path('.log').read_text()
    assert not any(s in content for s in ['Error,', 'Syntax error', 'Syntax warning'])
    for name, value in process['sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == value
    data = json.loads(path('.json').read_text())
    if record['status'] == 'SKIP_CAP':
        assert (data['n'], data['id'], data['normalized_count']) == (24,3,8192)
        assert data['normalized_count'] > data['cap'] == 4096
        assert content.rstrip().endswith('PASS_647_EXPORT_SKIPPED')
        continue
    assert data['status'] == record['status'] == 'EXPORTED'
    assert content.rstrip().endswith('PASS_647_EXPORT')
    replay = check(data)
    stored = json.loads(path('-controls.json').read_text())
    # JSON normalizes tuple-valued witness coordinates to lists.
    assert json.loads(json.dumps(replay)) == stored
    assert stored['associative_count'] == 2
    old = data['table']
    opposite = [list(row) for row in zip(*old)]
    assert all(r['table'] in (old, opposite)
               for r in stored['associative_operations'])
    assert classify(data, stored)['all_variety_memberships_certified']
    total_operations += stored['normalized_operations']
    total_triples += stored['checked_triples']
    total_associative += stored['associative_count']
assert (total_operations, total_triples, total_associative) == (289,522952,10)
print(f"PASS_647_PILOT_PACKET {len(summary['sha256'])} hashes; "
      f"{total_operations} operations; {total_triples} triples; "
      'five complete finite cases, one cap omission; no general solution')
