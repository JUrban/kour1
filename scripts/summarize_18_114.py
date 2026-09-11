#!/usr/bin/env python3
"""Check completed valid logs, excluding the preserved failed cache runs."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
files = ['18.114-dim1-3.log', '18.114-dim4.log', '18.114-dim5-6.log']
all_groups, dimensions = [], []
for name in files:
    raw = (root/'results'/name).read_text()
    assert not re.search(r'Error|Syntax', raw), name
    data = re.sub(r'\s+', '', raw)
    groups = [dict(zip(('n', 'd', 'k', 'order', 'cyclic', 'classes', 'ms'),
                      (int(n), int(d), int(k), int(o), c == 'true', int(kv), int(ms))))
              for n, d, k, o, c, kv, ms in re.findall(
                  r'GROUPn=(\d+)d=(\d+)k=(\d+)order=(\d+)cyclic=(true|false)'
                  r'affine_classes=(\d+)ms=(\d+)', data)]
    assert len(groups) == data.count('GROUPn='), name
    ids = [(g['n'], g['d'], g['k']) for g in groups]
    assert len(set(ids)) == len(ids), name
    localdims = []
    for n, total, eligible, eq, hits in re.findall(
            r'DONE_DIMn=(\d+)total=(\d+)eligible=(\d+)equalities=(\d+)hits=(\d+)', data):
        n, total, eligible, eq, hits = map(int, (n,total,eligible,eq,hits))
        subset = [g for g in groups if g['n'] == n]
        assert len(subset) == eligible <= total
        assert sum(g['classes'] == 5**n for g in subset) == eq
        assert sum(g['classes'] == 5**n and not g['cyclic'] for g in subset) == hits
        assert all(g['order'] % 5 and g['classes'] <= 5**n for g in subset)
        assert all(g['classes'] == g['order']+(5**n-1)//g['order']
                   for g in subset if g['cyclic'])
        localdims.append(dict(n=n,total=total,eligible=eligible,equalities=eq,
                              noncyclic_hits=hits,cyclic=sum(g['cyclic'] for g in subset)))
    done = re.findall(r'DONEtotal=(\d+)eligible=(\d+)equalities=(\d+)noncyclic_hits=(\d+)', data)
    assert len(done) == 1
    assert list(map(int,done[0])) == [sum(d[k] for d in localdims)
                                    for k in ('total','eligible','equalities','noncyclic_hits')]
    dimensions.extend(localdims)
    all_groups.extend(groups)
assert sorted(d['n'] for d in dimensions) == list(range(1,7))
control = re.sub(r'\s+', '', (root/'results/18.114-controls.log').read_text())
assert 'ALLPASScontrols=57noncyclic_equality_controls=3commuting_pair_controls=37' in control
assert control.count('PASSp=') == 57
assert 'Error' not in control and 'Syntax' not in control
report = dict(status='PASS',field=5,dimensions=sorted(dimensions,key=lambda d:d['n']),
              total=sum(d['total'] for d in dimensions),eligible=len(all_groups),
              cyclic=sum(g['cyclic'] for g in all_groups),
              equalities=[g for g in all_groups if g['classes'] == 5**g['n']],
              noncyclic_hits=sum(d['noncyclic_hits'] for d in dimensions),
              independent_controls=57,noncyclic_positive_controls=3,
              commuting_pair_controls=37,
              scope='IRREDSOL soluble irreducible subgroups only, n=1,...,6',
              excluded_logs='All *-invalid-cache.log files are invalid diagnostic runs.')
(root/'results/18.114-summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('equalities',)},indent=2))
