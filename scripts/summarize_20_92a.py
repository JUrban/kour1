#!/usr/bin/env python3
"""Audit actual completion, expected controls, retained failure, and hashes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]


def sha(name):
    return hashlib.sha256((root/name).read_bytes()).hexdigest()


def read(name):
    return json.loads((root/name).read_text())


for kind, ext in [('python', 'py'), ('gap', 'g')]:
    run = read(f'results/20.92a-{kind}-run.json')
    assert run['returncode'] == 0
    assert run['script_sha256'] == sha(f'scripts/verify_20_92a.{ext}')
    assert run['log_sha256'] == sha(f'results/20.92a-{kind}.log')
initial = read('results/20.92a-initial-python-run.json')
assert initial['returncode'] == 1
assert initial['script_sha256'] == sha('scripts/20.92a-initial-control.py')
assert initial['log_sha256'] == sha('results/20.92a-initial-python.log')
assert 'AssertionError: pre-Lie identity on basis' in (root/'results/20.92a-initial-python.log').read_text()

gap = (root/'results/20.92a-gap.log').read_text()
assert not re.search(r'error|syntax warning|assertion fail', gap, re.I)
assert gap.count('PASS_20_92A') == 1 and gap.strip().endswith('PASS_20_92A')
rows = [json.loads(s) for s in re.findall(
    r'FIELD_RESULT\s+(\[.*?\])\s*(?=FIELD_RESULT|PASS_20_92A)', gap, re.S)]
assert [r[:4] for r in rows] == [[5,625,4,400],[7,2401,3,2058],[11,14641,10,0]]
assert [r[4] for r in rows] == [[0,1,0,1],[0,0,1,0],[]]
for p, size, order, fail, witness, inverses, cycle in rows:
    assert size == p**4 and inverses == 101
    assert cycle == [[0,p-1,0,0],[p-1,0,0,0],[0,1,0,0],[1,0,0,0]]

py = read('results/20.92a-python.json')
assert py == read('results/20.92a-python.log') and py['status'] == 'PASS'
assert [r['name'] for r in py['rows']] == [
    'PSNZ_j0_k0_y1','PSNZ_j2_k3_y2','associative_truncated_polynomials']
assert [r['lambda_degree'] for r in py['rows']] == [5,7,1]
assert [r['correction_degrees'] for r in py['rows']] == [[1,9,15,5],[1,9,15,7],[1,4,4,4]]
comparisons = 0
for i, r in enumerate(py['rows']):
    assert r['basis_pre_lie_pairs'] == 16
    assert [t['p'] for t in r['modular']] == [5,7,11,17,31,127]
    assert [t['formal_average_equal'] for t in r['modular']] == [
        [False,False,True,True,True,True],
        [False,False,True,True,False,True],
        [True]*6][i]
    assert [t['failed_entries'] for t in r['modular']] == [
        [42,83,0,0,0,0],[82,162,0,0,108,0],[0]*6][i]
    for t in r['modular']:
        assert t['evaluated_entries'] == 1296
        comparisons += t['evaluated_entries']
assert comparisons == 23328

files = [
    'research/20.92a-plan.md','research/20.92a-proof.md','research/20.92a-review.md',
    'scripts/verify_20_92a.py','scripts/verify_20_92a.g','scripts/summarize_20_92a.py',
    'scripts/20.92a-initial-control.py',
    'results/20.92a-python.json','results/20.92a-python.log','results/20.92a-python-run.json',
    'results/20.92a-gap.log','results/20.92a-gap-run.json',
    'results/20.92a-initial-python.log','results/20.92a-initial-python-run.json',
    'docs/21tkt.pdf','bin/gap','references/cache/notebook-page161-2092.png']
for base in ['lazard-nilpotent-groups-lie-rings-1954',
             'trappeniers-lazard-braces-2024','trappeniers-lazard-braces-2024-v3',
             'puljic-smoktunowicz-zenouz-braces-p4-2022']:
    files += [f'references/cache/{base}.{ext}' for ext in ['pdf','txt']]
out = dict(status='PASS', checked_utc=datetime.now(timezone.utc).isoformat(),
           gap_actual_group_elements=sum(r[1] for r in rows),
           gap_constructive_inverse_inputs=sum(r[5] for r in rows),
           gap_field_results=rows, python_literal_entries=comparisons,
           python_symbolic_examples=3, initial_failed_control_retained=True,
           scope='Complete candidate proof; internal controls pass; outside review and novelty pending.',
           sha256={name:sha(name) for name in files})
(root/'results/20.92a-summary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k != 'sha256'},indent=2))
print('HASHED_FILES',len(files))
