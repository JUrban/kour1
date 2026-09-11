#!/usr/bin/env python3
"""Check retained coverage, completion records, and packet hashes."""
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

root=Path(__file__).resolve().parents[1]
controls=json.loads((root/'results/9.45-controls.json').read_text())
coverage=json.loads((root/'results/9.45-coverage.json').read_text())
actual=Counter((len(c['r']),c['m']) for c in controls['cases'])
expected_pairs={(n,m) for n,bound in controls['ranges'] for m in range(1,bound+1)}
assert set(actual)==expected_pairs
for record in coverage['coverage']:
    n,m=record['n'],record['m']
    # Count primitive vectors by an independent divisor/Mobius calculation.
    primes=[p for p in range(2,m+1) if m%p==0 and
            all(p%d for d in range(2,math.isqrt(p)+1))]
    primitive=m**n
    phi=m
    for p in primes:
        primitive=primitive//(p**n)*(p**n-1)
        phi=phi//p*(p-1)
    assert record['primitive_vectors']==primitive and record['units']==phi
    assert record['expected']==record['actual']==actual[n,m]==primitive//phi
assert coverage['pairs']==len(actual)==85
assert coverage['cases']==sum(actual.values())==3520
assert len({(c['m'],tuple(c['r'])) for c in controls['cases']})==3520
for path in ['results/9.45-gap-status.json','results/9.45-summary.json']:
    p=root/path
    if not p.exists():
        assert path.endswith('summary.json')
        continue
    data=json.loads(p.read_text())
    for name,digest in data['sha256'].items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
gap=json.loads((root/'results/9.45-gap-status.json').read_text())
assert gap['status']=='PASS' and gap['returncode']==0
assert gap['clean_log'] and gap['completion_sentinel']
log=(root/'results/9.45-gap.log').read_text()
assert not re.search(r'Error,|Syntax (error|warning)',log)
assert 'PASS_945_GAP' in log
counts={name:int(value) for name,value in re.findall(r'(\w+) := (\d+)',log)}
assert counts==dict(basis_equalities=1198,box_cases=274,box_points=291330,
    box_short_vectors=2698,cases=3520,negative=2921,positive=599,splitting_vectors=3011)
assert 'PASS_945_PYTHON' in (root/'results/9.45-python.log').read_text()
assert controls['counts']==dict(cases=3520,negative=2921,positive=599,
    prime_power_controls=1371,search_nodes=40980,short_vectors=93238)
print('PASS_945_PACKET 3520 cases; 85 orbit counts; completion and hashes verified')
