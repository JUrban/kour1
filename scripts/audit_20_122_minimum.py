#!/usr/bin/env python3
"""Bind and replay the full 20.122 minimum-order counterexample."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def process(name,command,marker):
    stem=ROOT/('results/20.122-'+name)
    r=json.loads(Path(str(stem)+'-process.json').read_text())
    out,err=Path(str(stem)+'.log'),Path(str(stem)+'.stderr')
    assert r['command']==command and r['actual_returncode']==0 and r['accepted'] is True
    assert not err.read_bytes() and sha(err)==r['stderr_sha256'] and sha(out)==r['stdout_sha256']
    assert out.read_bytes().count(marker)==1
    return out.read_text()


def summarize():
    out=process('minimum-native',['bin/gap','-o','2g','scripts/verify_20_122_minimum_native.g'],
                b'PASS_20_122_MINIMUM_NATIVE pairs=81')
    m=re.fullmatch(r'\s*MINIMUM_20122\s*(\[.*\])\s*PASS_20_122_MINIMUM_NATIVE pairs=81\s*',out,re.S)
    assert m and json.loads(m[1])==[36864,72,16,2048,512,9,10,5,16,16]
    out=process('minimum-independent',['python3','scripts/verify_20_122_minimum_permutations.py'],
                b'PASS_20_122_MINIMUM_PERMUTATIONS rejected_corruptions=6')
    summary=json.loads((ROOT/'results/20.122-minimum-permutations-summary.json').read_text())
    assert json.loads(out.splitlines()[0])==summary and summary['status']=='PASS'
    assert summary['orders']==[36864,72,16,2048,512]
    assert summary['minimum_order']==2 and summary['minimum_members']==5
    assert summary['min_generated_order']==summary['Min_generated_order']==16
    assert Counter(summary['pair_orders'])=={2:64,4:16,8:1}
    assert Counter(summary['quotient_normal_closure_orders'])=={18:9,36:30}
    assert summary['orbit_generator_edges']==117 and len(summary['rejected_corruptions'])==6
    out=process('affine-grid',['python3','scripts/search_20_122_affine_grid.py'],b'PASS_20_122_AFFINE_GRID')
    grid=json.loads((ROOT/'results/20.122-affine-grid-summary.json').read_text())
    assert json.loads(out.splitlines()[0])=={k:v for k,v in grid.items() if k!='hits'}
    assert grid['status']=='COMPLETE_SUFFICIENT_COORDINATE_SCREEN' and grid['triples']==120
    assert len(grid['hits'])==11 and grid['hits'][0]['masks']==[1,6,6]
    statement=json.loads((ROOT/'results/20.122-statement.json').read_text())
    assert statement['id']=='20.122' and statement['pdf_page']==165
    assert not statement['contains_editorial_star'] and not statement['starred_heading']
    return dict(independent=summary,exploratory_grid_triples=120,exploratory_grid_hits=11,
                complete_parts=['a','b','c-minimum-order','c-inclusion-minimal'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--summary-only',action='store_true')
    p.add_argument('--replay',action='store_true');args=p.parse_args()
    summary=summarize()
    if args.summary_only:print(json.dumps(summary,indent=2));return
    packet=json.loads((ROOT/'results/20.122-minimum-packet.json').read_text())
    assert packet['summary']==summary and packet['new_complete_candidates_added']==0
    assert packet['completed_existing_candidate']=='20.122'
    assert packet['outside_reviews']==0 and packet['priority_established'] is False

    def bindings():
        assert len({r['path'] for r in packet['files']})==len(packet['files'])
        for r in packet['files']:
            p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],p

    bindings()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='20.122-minimum-replay-') as directory:
            tmp=Path(directory);(tmp/'results').mkdir()
            r=subprocess.run([str(ROOT/'bin/gap'),'-o','2g',str(ROOT/'scripts/verify_20_122_minimum_native.g')],
                             cwd=tmp,capture_output=True,timeout=60)
            assert r.returncode==0 and not r.stderr
            assert r.stdout==(ROOT/'results/20.122-minimum-native.log').read_bytes()
            assert (tmp/'results/20.122-minimum-native-model.json').read_bytes()==(ROOT/'results/20.122-minimum-native-model.json').read_bytes()
            r=subprocess.run(['python3',str(ROOT/'scripts/verify_20_122_minimum_permutations.py')],
                             cwd=ROOT,capture_output=True,timeout=60)
            assert r.returncode==0 and not r.stderr
            assert r.stdout==(ROOT/'results/20.122-minimum-independent.log').read_bytes()
            r=subprocess.run(['python3',str(ROOT/'scripts/search_20_122_affine_grid.py')],
                             cwd=tmp,capture_output=True,timeout=60)
            assert r.returncode==0 and not r.stderr
            assert r.stdout==(ROOT/'results/20.122-affine-grid.log').read_bytes()
            assert (tmp/'results/20.122-affine-grid-summary.json').read_bytes()==(ROOT/'results/20.122-affine-grid-summary.json').read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,
                          completed_parts=summary['complete_parts'],group_order=36864),sort_keys=True))
    print('PASS_20_122_MINIMUM_PACKET')


if __name__=='__main__':main()
