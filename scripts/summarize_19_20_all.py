#!/usr/bin/env python3
"""Combine three disjoint completed ranges; never promote an incomplete run."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
paths = ['results/19.20-summary.json', 'results/19.20-order256-summary.json',
         'results/19.20-orders257-511-summary.json']
a, b, c = [json.loads((ROOT/p).read_text()) for p in paths]
assert a['status'] == 'complete through order255, excluding trivial group'
assert b['status'] == c['status'] == 'COMPLETE_BOUNDED_SEARCH'
assert b['order'] == 256 and c['orders'] == [257, 511]
assert a['completed_groups'] == 7011 and a['abelian_equality_controls'] == 493
assert b['nonabelian_counted'] == 56070 and c['nonabelian_counted'] == 29186
count = a['completed_groups'] - a['abelian_equality_controls'] + b['nonabelian_counted'] + c['nonabelian_counted']
assert count == 91774
r = dict(status='COMPLETE_NONABELIAN_COVERAGE_THROUGH_ORDER_511',
         observed_utc=datetime.now(timezone.utc).isoformat(),
         nonabelian_counted=count,
         nonabelian_equalities=a['nonabelian_equality_hits']+b['nonabelian_equalities']+c['nonabelian_equalities'],
         reverse_inequalities=len(a['reverse_inequalities'])+b['reverse_inequalities']+c['reverse_inequalities'],
         initial_abelian_equality_controls=493,
         independently_reconstructed_abelian_skips=len(b['skipped_abelian_ids'])+c['independently_reconstructed_abelian'],
         source_summaries={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
         scope='Every nonabelian group through order511 is in the covered SmallGroups catalogue. '
         'This is exact bounded computational evidence, not a proof of the general equality question. '
         'Separate larger structural examples are not included in these totals.')
(ROOT/'results/19.20-through511-summary.json').write_text(json.dumps(r, indent=2)+'\n')
print(json.dumps(r, indent=2))
