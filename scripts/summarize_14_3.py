#!/usr/bin/env python3
"""Audit both completed table criteria and independent actual-group controls."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    text = (ROOT / path).read_text()
    assert 'Error' not in text and 'Syntax warning' not in text
    return text
def fields(line):
    return {k: int(v) for k, v in re.findall(r'(\w+)=(\d+)(?=\s|$)', line)}

names = [x[5:] for x in read('results/14.2-table-manifest.log').splitlines()
         if x.startswith('NAME ')]
log_path = 'results/14.3-real-character-screen.log'
log = read(log_path)
rows = [x for x in log.splitlines() if x.startswith('TABLE143 ')]
assert len(rows) == len(names) == 2750
flagged = {}
for index, (name, row) in enumerate(zip(names, rows), 1):
    f = fields(row)
    assert f['index'] == index and f' name={name} order=' in row
    assert 0 <= f['surviving_elements'] <= f['central_classes'] - f['central_squares']
    assert f['central_classes'] % f['central_squares'] == 0
    if f['surviving_elements']:
        flagged[name] = f['surviving_elements']
flags = {}
for line in log.splitlines():
    if not line.startswith('FLAG143 '): continue
    m = re.fullmatch(r'FLAG143 name=(.*?) central_indices=\[([\d, ]*)\] orders=\[[\d, ]*\]', line)
    assert m and m[1] not in flags
    flags[m[1]] = [int(x) for x in m[2].replace(',', ' ').split()]
assert {k: len(v) for k, v in flags.items()} == flagged
assert log.rstrip().endswith('DONE143 tables=2750 criterion_passed=2739 '
                            'flagged_tables=11 surviving_elements=13')
assert len(flagged) == 11 and sum(flagged.values()) == 13

ref_path = 'results/14.3-refinement.log'
ref = read(ref_path)
refined = {}
elements = set()
for line in ref.splitlines():
    if line.startswith('REFINED143 '):
        name = re.search(r'name=(.*?) candidates=', line)[1]
        f = fields(line)
        assert name not in refined and f['surviving_elements'] == 0
        refined[name] = f['candidates']
    if line.startswith('ELEMENT143 '):
        m = re.fullmatch(r'ELEMENT143 name=(.*?) central_index=(\d+) odd_root_classes=\[ *\]', line)
        assert m
        pair = (m[1], int(m[2])); assert pair not in elements
        elements.add(pair)
assert refined == flagged
assert elements == {(name, z) for name, zs in flags.items() for z in zs}
assert ref.rstrip().endswith('DONE_REFINE143 tables=11 candidates=13 '
                            'flagged_tables=0 surviving_elements=0')

control_path = 'results/14.3-controls.log'
control = read(control_path)
controls = [fields(x) for x in control.splitlines() if x.startswith('CONTROL143 ')]
assert len(controls) == 19
assert sum(x['classes'] for x in controls) == 187
assert sum(x['nonsquares'] for x in controls) == 84
assert control.rstrip().endswith('PASS143 groups=19 indicator_checks=187 '
    'nonsquares=84 real_rejected=81 odd_root_rejected=3 surviving_elements=0')
paths = [log_path, ref_path, control_path, 'scripts/screen_14_3.g',
         'scripts/refine_14_3.g', 'scripts/verify_14_3.g',
         'references/cache/bakshi-maheshwary-passi-rs-2018.pdf',
         'research/14.3-reduction.md']
result = dict(status='COMPLETE_COMBINED_CRITERION_SCREEN', tables=2750,
              real_criterion_passed=2739, real_criterion_flags=flags,
              odd_root_rejections=13, combined_surviving_elements=0,
              independent_controls=fields(control.splitlines()[-1]),
              sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
              limitation='The proved necessary conditions imply the desired '
              'factorization for the finite groups represented by these table names. '
              'Tables may duplicate isomorphism types. No arbitrary-group conclusion '
              'or novelty claim; this is not enumeration of central units.')
(ROOT/'results/14.3-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
