#!/usr/bin/env python3
"""Full source, coverage, root-system and arithmetic replay for 19.62."""
import ast
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import check_19_62_g2_integer_constants as g2_constants
import check_19_62_symplectic as symplectic
import prepare_19_62_types as preparation
import verify_19_62_monomial_certificates as g2_certificates
import verify_19_62_types as certificates

ROOT=Path(__file__).resolve().parents[1]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def root_system(label):
    roots,powers,adj,cartan=ast.literal_eval((ROOT/('results/19.62-'+label+'-integral.grows')).read_text())
    n=int(label[1:]);expected=[[2*int(i==j)-int(abs(i-j)==1) for j in range(n)] for i in range(n)]
    if label.startswith('b'):expected[n-2][n-1]=-2
    if label.startswith('c'):expected[n-1][n-2]=-2
    if label=='d4':expected=[[2,-1,0,0],[-1,2,-1,-1],[0,-1,2,0],[0,-1,0,2]]
    if label=='f4':expected=[[2,0,-1,0],[0,2,0,-1],[-1,0,2,-1],[0,-1,-2,2]]
    assert cartan==expected
    known=set(map(tuple,cartan));pending=list(known)
    for v in pending:
        for i,simple in enumerate(cartan):
            w=tuple(x-v[i]*y for x,y in zip(v,simple))
            if w not in known:known.add(w);pending.append(w);assert len(known)<200
    assert known==set(map(tuple,roots)) and len(known)==len(roots)


def run():
    packet=json.loads((ROOT/'results/19.62-all-types-packet.json').read_text())
    for p,h in packet['sha256'].items():assert sha(ROOT/p)==h,p
    for name in ['results/19.62-types-completed-manifest.json','results/19.62-types-launch-manifest.json',
                 'results/19.62-g2-symbolic-packet.json','results/19.61-g2-summary.json']:
        prior=json.loads((ROOT/name).read_text())
        for p,h in prior['sha256'].items():assert sha(ROOT/p)==h,p
    summary=json.loads((ROOT/'results/19.62-types-generation-summary.json').read_text())
    assert summary['status']=='COMPLETE' and len(summary['jobs'])==75
    for label in preparation.TYPES:
        root_system(label)
        data=json.loads((ROOT/('results/19.62-'+label+'-monomial-input.json')).read_text())
        covered=[];parts=[]
        for job in summary['jobs']:
            if job['type']!=label:continue
            assert job['returncode']==0 and job['counts']==[job['first'],job['last'],job['last']-job['first']+1,0]
            for p,h in job['sha256'].items():assert sha(ROOT/p)==h,p
            covered.extend(range(job['first'],job['last']+1));parts.append((ROOT/job['certificate']).read_bytes())
        assert covered==list(range(1,len(data['cases'])+1))
        assert b''.join(parts)==(ROOT/('results/19.62-'+label+'-monomial-certificates.jsonl')).read_bytes()
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp);Path('results').mkdir()
            for label in preparation.TYPES:
                source='results/19.62-'+label+'-integral.grows';shutil.copyfile(ROOT/source,source)
                with contextlib.redirect_stdout(io.StringIO()):preparation.prepare(label)
                for extension in ['json','txt']:
                    name='results/19.62-'+label+'-monomial-input.'+extension
                    assert Path(name).read_bytes()==(ROOT/name).read_bytes(),name
                print('PASS_1962_FULL_PREPARATION_REPLAY',label,flush=True)
    finally:os.chdir(ROOT)
    assert g2_constants.run()==json.loads(Path('results/19.62-g2-integer-constants.json').read_text())
    g2=g2_certificates.run();assert g2==json.loads(Path('results/19.62-g2-monomial-verification.json').read_text())
    rest=certificates.run();assert rest==json.loads(Path('results/19.62-types-verification.json').read_text())
    assert symplectic.run()==json.loads(Path('results/19.62-symplectic-controls.json').read_text())
    assert g2['cases']+rest['cases']==71056 and g2['derivation_nodes']+rest['derivation_nodes']==974165
    print('PASS_1962_ALL_TYPES_PACKET',len(packet['sha256']),'targets=71056 nodes=974165',flush=True)


if __name__=='__main__':run()
