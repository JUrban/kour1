#!/usr/bin/env python3
import hashlib
import importlib.util
import json
from pathlib import Path
import re

m = json.loads(Path('results/19.93-summary.json').read_text())
assert m['status'] == 'COMPLETE_CANDIDATE_PENDING_REVIEW'
for path, digest in m['sha256'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
for name in ('gap', 'controls'):
    r = json.loads(Path('results/19.93-'+name+'-process.json').read_text())
    assert r['returncode'] == 0 and r['sentinel_present'] and r['stderr'] == ''
    assert r['script_sha256'] == m['sha256'][r['command'][-1]]
    text = Path('results/19.93-'+name+'.log').read_text()
    assert text == r['stdout']
    assert r['log_sha256'] == m['sha256']['results/19.93-'+name+'.log']
    assert not re.search(r'Error|Syntax warning', text)
text = Path('results/19.93-gap.log').read_text()
rows = re.findall(r'TRIANGLE p=7 class=(\d+) log_order=(\d+) widths=\[([^]]+)\]', text)
assert len(rows) == 7
widths = [2, 1, 2, 3, 6, 9, 17, 28]
for (cl, order, ws), expected_cl in zip(rows, range(2, 9)):
    actual = [int(x.strip()) for x in ws.split(',')]
    assert int(cl) == expected_cl and actual == widths[:expected_cl]
    assert int(order) == sum(actual)
assert 'generating_torsion_pairs=8 bad=0' in text
assert 'generating_torsion_pairs=648 bad=0' in text
spec = importlib.util.spec_from_file_location('control1993', 'scripts/check_19_93.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.run() == json.loads(Path('results/19.93-controls.json').read_text())
print('PASS_1993_PACKET', len(m['sha256']))
