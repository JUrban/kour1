#!/usr/bin/env python3
"""Check complete runs, independent agreement, exact coverage and source hashes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256((root/path).read_bytes()).hexdigest()


log = (root/'results/19.56-gap.log').read_text()
assert not any(s in log for s in ('Error', 'Syntax warning', 'Assertion failure'))
assert log.strip().endswith('PASS_19_56') and log.count('PASS_19_56') == 1
run = json.loads((root/'results/19.56-gap-run.json').read_text())
assert run['returncode'] == 0
assert run['script_sha256'] == sha('scripts/verify_19_56.g')
assert run['log_sha256'] == sha('results/19.56-gap.log')
initial = json.loads((root/'results/19.56-initial-gap-run.json').read_text())
assert initial['script_sha256'] == sha('results/19.56-initial-control.g')
assert initial['log_sha256'] == sha('results/19.56-initial-gap.log')
oldlog = (root/'results/19.56-initial-gap.log').read_text()
assert 'Error, SylowSubgroup: <p> must be a prime' in oldlog
assert 'PASS_19_56' not in oldlog

coverage = [list(map(int, m)) for m in re.findall(r'^ORDER_DONE (\d+) (\d+)$', log, re.M)]
assert [r[0] for r in coverage] == list(range(1, 65))
assert sum(r[1] for r in coverage) == 586
m = re.search(r'PASS_GROUPS (.*?)\nPASS_MATRICES', log, re.S)
assert m and log.count('PASS_GROUPS ') == 1
rows = json.loads(m[1])
assert len(rows) == 593
expected_names = [f'small_{n}_{i}' for n, count in coverage for i in range(1, count+1)]
assert [r[0] for r in rows[:-7]] == expected_names
assert [r[0] for r in rows[-7:]] == ['S3', 'A4', 'S4', 'A5', 'SL2_5', 'PSL2_7', 'A6']
assert sum(len(r[6]) for r in rows) == 843
assert sum(r[3] for r in rows) == 159220
assert sum(r[4] for r in rows) == 582
assert all(r[4] == r[5] for r in rows)
assert all(h[2] == h[3] for r in rows for h in r[6])
assert all((r[7] == []) == r[4] for r in rows)
assert all(r[7][2] < r[7][0]*r[7][1] for r in rows if not r[4])

py = json.loads((root/'results/19.56-python.json').read_text())
assert py == json.loads((root/'results/19.56-python.log').read_text())
assert py['status'] == 'PASS' and py['multiplication_entries'] == 176580
assert len(py['odd_matrix_controls']) == 12
assert [r['row'] for r in py['groups']] == [r[:7] for r in rows[-7:]]
assert [r['violation_pairs'] == 0 for r in py['groups']] == [r[4] for r in rows[-7:]]

m = re.search(r'^PASS_MATRICES (.*?) additive_checks=(\d+)$', log, re.M)
assert m and log.count('PASS_MATRICES ') == 1
matrix = json.loads(m[1])
assert len(matrix) == 24 and int(m[2]) == 17472
assert [r[1] for r in matrix if r[0] == 'odd_PSL2'] == [3,5,7,9,11,13,17,19,23,25,27,31,49,81,125]
assert [r[1] for r in matrix if r[0] == 'even_PSL2'] == [4,8,16,32,64]
assert [r[1] for r in matrix if r[0] == 'Suzuki'] == [8,32,128]
assert [r for r in matrix if r[0] == 'PSL3'] == [['PSL3',3,4,12]]
m = re.search(r'^PASS_LIFTS (.*?)$', log, re.M)
assert m and log.count('PASS_LIFTS ') == 1
lifts = json.loads(m[1])
assert lifts == [[5,120,4,3,4,5,5,5,4], [7,336,4,3,4,3,3,3,4], [9,720,4,3,4,3,3,3,4]]

files = [
    'research/19.56-proof.md', 'research/19.56-review.md', 'research/19.56-plan.md',
    'scripts/verify_19_56.g', 'scripts/verify_19_56.py', 'scripts/summarize_19_56.py',
    'results/19.56-gap.log', 'results/19.56-gap-run.json',
    'results/19.56-python.json', 'results/19.56-python.log',
    'results/19.56-initial-control.g', 'results/19.56-initial-gap.log',
    'results/19.56-initial-gap-run.json', 'bin/gap', 'docs/21tkt.pdf',
    'references/cache/notebook-page139-1956.png',
    'references/cache/bcglo-extensions-published.pdf',
    'references/cache/broto-castellana-grodal-levi-oliver-extensions.pdf',
    'references/cache/bray-baarnhielm-suzuki-2017.pdf',
    'references/cache/guralnick-malle-variations-baer-suzuki.pdf',
    'references/cache/guo-revin-minimal-nonsolvable.pdf',
    'references/cache/monakhov-derived-nilpotency-2017.pdf',
    'references/cache/monakhov-star-metanilpotency-2017.pdf',
    'references/cache/bastos-monetta-coprime-2018.pdf',
    'references/cache/li-lei-gao-products-2022.pdf',
]
report = dict(
    status='PASS', observed_utc=datetime.now(timezone.utc).isoformat(), problem='19.56',
    conclusion='Complete affirmative candidate under even the primary-output-only inequality',
    small_group_cases=586, named_cases=rows[-7:], group_cases=593,
    hyperfocal_checks=843, primary_input_pairs=159220, satisfying_cases=582,
    violating_cases=11, matrix_cases=matrix, suzuki_additive_checks=17472,
    central_lift_cases=lifts, independent_python=py, gap_process=run,
    excluded_initial_run=dict(record=initial, status='FAILED',
                              reason='GAP reported an invalid prime and did not complete, despite OS returncode zero'),
    scope='General proof imports hyperfocal, minimal-simple classification and Baer-Suzuki. Bounded controls corroborate only the checked constructions. Outside review and broader priority checking pending.',
    sha256={p: sha(p) for p in files})
(root/'results/19.56-summary.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k: report[k] for k in ('status', 'observed_utc', 'problem', 'group_cases',
                                       'hyperfocal_checks', 'primary_input_pairs')}, indent=2))
