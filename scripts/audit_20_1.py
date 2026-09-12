#!/usr/bin/env python3
import hashlib
import importlib.util
import json
from pathlib import Path
import re

m = json.loads(Path('results/20.1-summary.json').read_text())
assert m['status'] == 'COMPLETE_CANDIDATE_PENDING_REVIEW'
for path, digest in m['sha256'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
for name in ('gap', 'controls'):
    r = json.loads(Path('results/20.1-' + name + '-process.json').read_text())
    assert r['returncode'] == 0 and r['sentinel_present'] and r['stderr'] == ''
    assert r['script_sha256'] == m['sha256'][r['command'][-1]]
    text = Path('results/20.1-' + name + '.log').read_text()
    assert text == r['stdout']
    assert r['log_sha256'] == m['sha256']['results/20.1-' + name + '.log']
    assert not re.search(r'Error|Syntax warning', text)
text = Path('results/20.1-gap.log').read_text()
rows = re.findall(r'PRODUCT_CONTROL (\w+) cases=(\d+)', text)
assert rows == [('C2_C3', '10'), ('Q8_C3', '67'), ('S3_C5', '47'), ('A4_C5', '53')]
assert 'PASS_201_GAP cases=177' in text
assert 'J1_TABLE_ORDER 175560 PRODUCT_ORDER 2282280' in text
spec = importlib.util.spec_from_file_location('control201', 'scripts/check_20_1.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
replayed = json.loads(json.dumps(module.run()))
assert replayed == json.loads(Path('results/20.1-controls.json').read_text())
assert replayed['cases'] == 177 and replayed['maximum_degree'] == 60
print('PASS_201_PACKET', len(m['sha256']))
