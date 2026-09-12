#!/usr/bin/env python3
"""Hash binding, native/independent comparison, and optional fresh replay."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inspect(name,command,marker):
    stem=ROOT/('results/20.89-metabelian-'+name)
    record=json.loads(Path(str(stem)+'-process.json').read_text())
    out=Path(str(stem)+'.log');err=Path(str(stem)+'.stderr')
    assert record['command']==command and record['actual_returncode']==0 and record['accepted'] is True
    assert not err.read_bytes() and sha(err)==record['stderr_sha256'] and sha(out)==record['stdout_sha256']
    assert sha(ROOT/command[-1])==record['script_sha256'] and out.read_bytes().count(marker)==1
    return out.read_text()

def summary():
    py=inspect('words',['python3','scripts/verify_20_89_metabelian.py'],b'PASS_20_89_METABELIAN_WORDS')
    data=json.loads(py.splitlines()[0])
    gap=inspect('native',['bin/gap','-o','2g','scripts/verify_20_89_metabelian.g'],b'PASS_20_89_METABELIAN_NATIVE')
    match=re.fullmatch(r'\s*ROWS20189 (.*?)\nCONTROL20189 (.*?)\nFAMILY20189 (.*?)\nPASS_20_89_METABELIAN_NATIVE\s*',gap,re.S)
    assert match
    for raw,key in zip(match.groups(),['rows','nonmetabelian_control','dihedral_family']):assert json.loads(raw)==data[key],key
    assert len(data['rows'])==8 and len(data['dihedral_family'])==36 and len(data['rejected_mutations'])==4
    assert data['nonmetabelian_control']==['S4',24,12,[[1,4],[4,8],[5,12]],576,13824]
    stem=ROOT/'results/20.89-metabelian-native-initial'
    old=json.loads(Path(str(stem)+'-process.json').read_text())
    assert old['actual_returncode']==0 and old['accepted'] is False
    assert old['script_sha256']==sha(ROOT/'scripts/verify_20_89_metabelian_initial.g')
    for ext,key in [('.log','stdout_sha256'),('.stderr','stderr_sha256')]:assert sha(Path(str(stem)+ext))==old[key]
    assert Path(str(stem)+'.stderr').read_bytes().count(b'Syntax warning: Unbound global variable')==2
    assert Path(str(stem)+'.log').read_bytes()==(ROOT/'results/20.89-metabelian-native.log').read_bytes()
    stem=ROOT/'results/20.89-metabelian-audit-initial'
    old=json.loads(Path(str(stem)+'-process.json').read_text())
    assert old['actual_returncode']==1 and old['accepted'] is False
    assert old['script_sha256']==sha(ROOT/'scripts/audit_20_89_metabelian_initial.py')
    for ext,key in [('.log','stdout_sha256'),('.stderr','stderr_sha256')]:assert sha(Path(str(stem)+ext))==old[key]
    assert b'assert match' in Path(str(stem)+'.stderr').read_bytes()
    return dict(models=8,sink_product_pairs=sum(r[4] for r in data['rows']),
                independent_associativity_triples=sum(r[5] for r in data['rows'])+24**3,
                dihedral_family=36,dihedral_rotation_elements=sum(r[2] for r in data['dihedral_family']),
                nonmetabelian_control='S4: twelve sinks have size5 and fail subgroup closure',
                warning_bearing_initial_run_retained=True,new_complete_candidates_added=0,
                priority='metabelian rediscovery; virtually abelian prior consequence')

def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');p.add_argument('--summary-only',action='store_true');args=p.parse_args()
    result=summary()
    if args.summary_only:print(json.dumps(result,sort_keys=True));return
    packet=json.loads((ROOT/'results/20.89-metabelian-packet.json').read_text())
    assert packet['summary']==result and packet['outside_reviews']==0
    def bindings():
        assert len({r['path'] for r in packet['files']})==len(packet['files'])
        for row in packet['files']:
            f=ROOT/row['path'];assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],f
    bindings()
    if args.replay:
        for name,command in [('native',['bin/gap','-o','2g','scripts/verify_20_89_metabelian.g']),('words',['python3','scripts/verify_20_89_metabelian.py'])]:
            x=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
            assert x.returncode==0 and not x.stderr
            assert x.stdout==(ROOT/('results/20.89-metabelian-'+name+'.log')).read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,**result),sort_keys=True))
    print('PASS_20_89_METABELIAN_PACKET')

if __name__=='__main__':main()
