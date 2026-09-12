#!/usr/bin/env python3
import hashlib
import importlib.util
import json
from pathlib import Path

manifest = json.loads(Path('results/16.38-summary.json').read_text())
assert manifest['status'] == 'COMPLETE_CANDIDATE_PENDING_REVIEW'
for p, expected in manifest['sha256'].items():
    assert hashlib.sha256(Path(p).read_bytes()).hexdigest() == expected, p
process = json.loads(Path('results/16.38-controls-process.json').read_text())
assert process['returncode'] == 0 and process['sentinel_present']
assert process['stderr'] == ''
assert process['script_sha256'] == manifest['sha256']['scripts/check_16_38.py']
assert process['result_sha256'] == manifest['sha256']['results/16.38-controls.json']
assert Path('results/16.38-controls.log').read_text() == 'PASS_1638_AFFINE_CONTROLS 6125 87380\n'
spec = importlib.util.spec_from_file_location('control1638', 'scripts/check_16_38.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = json.loads(json.dumps(module.run()))
assert result == json.loads(Path('results/16.38-controls.json').read_text())
print('PASS_1638_PACKET', len(manifest['sha256']))
