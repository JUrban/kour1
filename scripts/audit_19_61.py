#!/usr/bin/env python3
"""Archive integrity, full preparation replay, and independent matrix controls."""
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def run():
    manifest=json.loads((ROOT/'results/19.61-summary.json').read_text())
    for p,h in manifest['sha256'].items():
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    rings=['f2','f4','dual','split','z4']
    counts=dict(f2=(64,0),f4=(2515,576),dual=(6717,936),split=(6915,1536),z4=(1398,0))
    for ring in rings:
        text=(ROOT/f'results/19.61-{ring}-search.log').read_text()
        assert not re.search(r'Error|Syntax warning|Traceback|CANDIDATE_',text)
        values=re.findall(r'PASS_1961_SEARCH '+ring+r'\s*(\[[^\]]+\])',text)
        assert len(values)==text.count('PASS_1961_SEARCH')==1
        assert ast.literal_eval(values[0])==list(counts[ring])+[0]
        changes=[ast.literal_eval(line) for line in (ROOT/f'results/19.61-{ring}-changes.grows').read_text().splitlines()]
        assert len(changes)==counts[ring][1]
        assert len({r[0] for r in changes})==len(changes)
        assert all(1<=r[0]<=counts[ring][0] and r[1]!=r[2] and r[4]==[] for r in changes)
    processes=json.loads((ROOT/'results/19.61-search-processes.json').read_text())
    assert [p['ring'] for p in processes]==rings[1:]
    for record in processes:
        assert record['returncode']==0
        assert hashlib.sha256((ROOT/f"results/19.61-{record['ring']}-search.log").read_bytes()).hexdigest()==record['log_sha256']
    prep=module('prep1961','scripts/prepare_19_61.py')
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp);Path('results').mkdir()
            with contextlib.redirect_stdout(io.StringIO()):
                for ring in rings:
                    prep.prepare(ring)
                    name=f'results/19.61-{ring}-input.g'
                    assert Path(name).read_bytes()==(ROOT/name).read_bytes()
                    name=f'results/19.61-{ring}-preparation.json'
                    a=json.loads(Path(name).read_text());b=json.loads((ROOT/name).read_text())
                    a.pop('elapsed_seconds');b.pop('elapsed_seconds');assert a==b
    finally:
        os.chdir(ROOT)
    checker=module('check1961','scripts/check_19_61.py')
    # JSON serializes integer histogram keys as strings.
    replay=json.loads(json.dumps(checker.run()))
    assert replay==json.loads((ROOT/'results/19.61-controls.json').read_text())
    print('PASS_1961_PACKET',len(manifest['sha256']),'carpets=17609 controls=1288')


if __name__=='__main__':run()
