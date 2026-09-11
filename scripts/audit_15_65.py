#!/usr/bin/env python3
"""Audit the retained packet; the analytic proof is reviewed separately."""
from pathlib import Path
import hashlib,json,re
from fractions import Fraction
root=Path(__file__).resolve().parents[1]
pkt=json.loads((root/'results/15.65-summary.json').read_text())
assert pkt['candidate_number']==31
assert pkt['novelty']=='pending' and pkt['outside_reviews']==0
for name,digest in pkt['sha256'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
r=json.loads((root/'results/15.65-controls.json').read_text())
assert r['status']=='PASS' and r['actual_gap_exit']==0
for name,digest in r['hashes'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
assert r['series_degree']==80 and len(r['coefficients'])==81
assert r['published_coefficients_checked']==13 and r['mod_two_GL_checks']==81
expected={(2,n) for n in range(1,5)}|{(q,n) for q in (3,4) for n in range(1,4)}|{(q,n) for q in (5,7) for n in (1,2)}
assert {(x['q'],x['n']) for x in r['finite_cases']}==expected
assert len(r['finite_cases'])==14 and r['class_minpoly_rank_checks']==426
log=(root/'results/15.65-unitary-controls.log').read_text()
assert log.rstrip().endswith('UNITARY_CONTROLS_DONE')
assert not re.search(r'Error|Syntax warning|Syntax error|Traceback',log)
rows=[tuple(map(int,m)) for m in re.findall(r'^UNITARY_CONTROL (\d+) (\d+) (\d+) (\d+) (\d+)$',log,re.M)]
assert len(rows)==14
for row,case in zip(rows,r['finite_cases']):
    assert row==tuple(case[k] for k in ('q','n','order','cyclic','classes'))
    assert Fraction(row[3],row[2])==Fraction(case['proportion'])
assert (root/'results/15.65-controls-runner.log').read_text().strip()=='15_65_CONTROLS_DONE 14 426'
assert pkt['outer_python_exit']==0
print('PASS_15_65_PACKET',len(pkt['sha256']),'hashes; 14 finite cases; analytic proof separate')
