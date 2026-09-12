#!/usr/bin/env python3
"""Hash audit, deterministic reconstruction, and matrix replay for G2 pilot."""
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def run():
    manifest=json.loads((ROOT/'results/19.61-g2-summary.json').read_text())
    for path,digest in manifest['sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    obs=json.loads((ROOT/'results/19.61-g2-process-observations.json').read_text())
    assert len(obs['processes'])==7
    assert all(p['exit_code']==0 and p['tool_chunk'] for p in obs['processes'])
    for label,count,order in [('g2p2',174,12096),('g2p3',217,4245696)]:
        output=(ROOT/f'results/19.61-{label}-search.log').read_text()
        assert not re.search(r'Error|Syntax warning|Traceback|CANDIDATE_',output)
        values=re.findall(r'PASS_1961_SEARCH '+label+r'\s*(\[[^\]]+\])',output)
        assert len(values)==output.count('PASS_1961_SEARCH')==1
        assert ast.literal_eval(values[0])==[count,0,0]
        assert f'PASS_1961_AMBIENT {label} order={order}' in output
        assert not (ROOT/f'results/19.61-{label}-changes.grows').read_bytes()
        orders=[ast.literal_eval(s) for s in (ROOT/f'results/19.61-{label}-orders.grows').read_text().splitlines()]
        assert [x[0] for x in orders]==list(range(1,count+1))
        assert all(order%x[1]==0 for x in orders)
        output=(ROOT/f'results/19.61-{label}-orders.log').read_text()
        assert output.strip()==f'PASS_1961_ORDERS {label} {count}'
    prep=module('prepare1961g2','scripts/prepare_19_61_g2.py')
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp);Path('results').mkdir()
            name='results/19.61-g2-integral.grows';shutil.copyfile(ROOT/name,name)
            with contextlib.redirect_stdout(io.StringIO()):prep.main()
            for label in ['g2p2','g2p3']:
                name=f'results/19.61-{label}-input.g'
                assert Path(name).read_bytes()==(ROOT/name).read_bytes()
                name=f'results/19.61-{label}-preparation.json'
                a=json.loads(Path(name).read_text());b=json.loads((ROOT/name).read_text())
                a.pop('elapsed_seconds');b.pop('elapsed_seconds');assert a==b
    finally:
        os.chdir(ROOT)
    checker=module('check1961g2','scripts/check_19_61_g2.py')
    assert checker.run()==json.loads((ROOT/'results/19.61-g2-controls.json').read_text())
    print('PASS_1961_G2_PACKET',len(manifest['sha256']),'carpets=391 matrix_cases=390 full_cases=1')


if __name__=='__main__':run()
