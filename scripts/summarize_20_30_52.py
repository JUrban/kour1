#!/usr/bin/env python3
from pathlib import Path
import json
import re

odd = Path('results/20.52-odd-through1727.log').read_text()
tables = Path('results/20.30-tables.log').read_text()
controls = Path('results/20.30-52-controls.log').read_text()
for log in (odd, tables, controls):
    assert 'Error' not in log and 'Syntax warning' not in log
assert 'DONE groups=2845 nonabelian=1719 distinct_m=103' in odd
assert re.search(r'MISSING\s*\[\s*\]', odd)
rows = [tuple(map(int, row)) for row in re.findall(
    r'GROUP order=(\d+) id=(\d+) classes=(\d+) diff=(\d+)', odd)]
assert len(rows) == 2845
assert len({(n,i) for n,i,k,d in rows}) == len(rows)
assert {n for n,i,k,d in rows} == set(range(3,1728,2))
assert sum(d>0 for n,i,k,d in rows) == 1719
lookup = {(n,i):k for n,i,k,d in rows}
witnesses = {}
for n,i,k,d in rows:
    assert n-k == d and d % 16 == 0
    if d:
        assert 27*k <= 11*n
        m = d//16
        witnesses.setdefault(m, {'order':n,'id':i,'classes':k})
assert len(witnesses) == 103
assert all(m in witnesses for m in range(1,65))
assert 'DONE tables=2750 eligible=340 hits=0' in tables
flat = re.sub(r'\\\n\s*', '', tables)
trows = re.findall(r'TABLE name=(\S+) order=(\d+)\s+max_class=\s*(\d+)', flat)
assert len(trows) == 340
assert all(int(b)**2 >= int(n) for name,n,b in trows)
c52 = re.findall(r'CONTROL52 order=(\d+) id=(\d+) classes=(\d+)', controls)
assert len(c52) == 86
assert all(lookup[int(n),int(i)] == int(k) for n,i,k in c52)
assert len(re.findall(r'^CONTROL30 ', controls,re.M)) == 9
assert 'DONE controls52=86 controls30=9 PASS' in controls
result = {'20.30':{'tables':2750,'eligible':340,'hits':0,'actual_controls':9},
          '20.52':{'max_order':1727,'groups':2845,'nonabelian':1719,
                    'distinct_m':103,'all_m_through':64,'actual_controls':86,
                    'witnesses_through64':{m:witnesses[m] for m in range(1,65)}}}
Path('results/20.30-52-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS 20.30:2750 tables,340 eligible,0 hits;20.52:2845 groups,all m<=64;95 actual controls')
