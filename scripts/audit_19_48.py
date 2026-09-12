#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run():
    root=Path.cwd()
    packet=json.loads(Path('results/19.48-packet.json').read_text())
    for path,digest in packet['sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    assert packet['new_candidate_increment']==0
    for name in ['prepare','controls','gap']:
        r=json.loads(Path('results/19.48-'+name+'-process.json').read_text())
        assert r['returncode']==0 and r['sentinel_present'] and r['stderr']==''
        assert r['script_sha256']==packet['sha256'][r['command'][-1]]
        assert r['stdout']==Path('results/19.48-'+name+'.log').read_text()
        assert r['log_sha256']==packet['sha256']['results/19.48-'+name+'.log']
        assert not re.search(r'Error|Syntax warning|Traceback',r['stdout'])
    old=json.loads(Path('results/19.48-initial-controls/19.48-controls-process.json').read_text())
    assert old['script_sha256']==packet['sha256']['results/19.48-initial-controls/check_19_48.py']
    assert old['returncode']==0 and old['stderr']=='' and old['sentinel_present']
    with tempfile.TemporaryDirectory(prefix='1948-audit-') as temp:
        temp=Path(temp)
        r=subprocess.run(['python3',str(root/'scripts/prepare_19_48.py'),'--output',
                          str(temp/'word.json'),'--table',str(temp/'table.md')],capture_output=True,text=True)
        assert r.returncode==0 and r.stderr=='' and 'PASS_1948_PREPARATION' in r.stdout
        assert (temp/'word.json').read_bytes()==Path('results/19.48-word.json').read_bytes()
        assert (temp/'table.md').read_bytes()==Path('research/19.48-word-table.md').read_bytes()
        r=subprocess.run([str(root/'bin/gap'),'-o','512m',str(root/'scripts/check_19_48.g')],
                         cwd=temp,capture_output=True,text=True)
        assert r.returncode==0 and r.stderr=='' and 'PASS_1948_GAP' in r.stdout
        assert not re.search(r'Error|Syntax warning',r.stdout)
    sys.path.insert(0,str(root/'scripts'))
    spec=importlib.util.spec_from_file_location('check1948',root/'scripts/check_19_48.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    controls=m.run()
    assert controls==json.loads(Path('results/19.48-controls.json').read_text())
    assert controls['basis_product_controls']==3024 and controls['prior_cubic_integer_matrix_controls']=='PASS'
    print('PASS_1948_PACKET',len(packet['sha256']),'word_factors=9 module_products=3024 prior_cubic=PASS new_candidates=0')


if __name__=='__main__':
    run()
