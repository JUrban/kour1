#!/usr/bin/env python3
"""Bind the frozen packet and replay exact controls without rewriting it."""
import hashlib
import importlib.util
import json
from pathlib import Path

manifest = json.loads(Path('results/15.76-summary.json').read_text())
assert manifest['status'] == 'COMPLETE_CANDIDATE_PENDING_REVIEW'
for path, expected in manifest['sha256'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
process = json.loads(Path('results/15.76-controls-process.json').read_text())
assert process['returncode'] == 0 and process['sentinel_present']
assert process['stderr'] == ''
assert Path('results/15.76-controls.log').read_text() == 'PASS_1576_EXACT_CONTROLS 2430 2\n'
assert process['script_sha256'] == manifest['sha256']['scripts/check_15_76.py']
assert process['output_sha256'] == manifest['sha256']['results/15.76-controls.json']
spec = importlib.util.spec_from_file_location('control1576', 'scripts/check_15_76.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = json.loads(json.dumps(module.run()))
assert result == json.loads(Path('results/15.76-controls.json').read_text())
print('PASS_1576_PACKET', len(manifest['sha256']))
