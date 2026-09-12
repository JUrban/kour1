#!/usr/bin/env python3
"""Validate and replay the partial 20.89 packet, including a rejected verifier."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def process(name,expected,marker=None,script=None):
    stem=ROOT/('results/20.89-'+name)
    record=json.loads(Path(str(stem)+'-process.json').read_text())
    out=Path(str(stem)+'.log');err=Path(str(stem)+'.stderr')
    assert record['actual_returncode']==expected
    assert record['accepted'] is (expected==0)
    assert sha(out)==record['stdout_sha256'] and sha(err)==record['stderr_sha256']
    if expected==0:
        assert not err.read_bytes() and out.read_bytes().count(marker)==1
    else:
        assert not out.read_bytes() and b'AssertionError' in err.read_bytes()
    if script is not None:assert sha(ROOT/script)==record['script_sha256']
    return out.read_text(),record


def summary():
    process('native',0,b'PASS_20_89_NATIVE')
    process('independent',0,b'PASS_20_89_INDEPENDENT')
    out,_=process('expanded-native',0,b'PASS_20_89_NATIVE','scripts/verify_20_89_native.g')
    match=re.fullmatch(r'\s*FILTRATION_2089 (\[.*\])\s*MIXED_2089 (\[.*\])\s*SINK_2089 (\[.*\])\s*PASS_20_89_NATIVE\s*',out,re.S)
    assert match
    filtration,mixed,sink=[json.loads(match[i]) for i in range(1,4)]
    assert filtration==[216,[1,3,9,27],8424,1053]
    assert mixed==[[r,12*3**r,6*3**r,72*9**r,3**r] for r in range(1,4)]
    assert sink==[72,3,3,9]
    process('expanded-independent',1,script='scripts/verify_20_89_independent_failed_union.py')
    out,_=process('final-independent',0,b'PASS_20_89_INDEPENDENT','scripts/verify_20_89_independent.py')
    result=json.loads(out.splitlines()[0]);assert result['status']=='PASS'
    assert result['filtration']==dict(order=216,layer_orders=[1,3,9,27],products=46656,conjugation_checks=8424,central_checks=1053)
    assert result['mixed_rows'][:3]==mixed and result['mixed_rows'][3]==[4,972,486,472392,81]
    assert result['rational_distinct_iterates']==65 and len(result['rejected_shortcuts'])==6
    assert result['nonnormal_sink']==dict(group_order=72,sink_size=3,sink_group_order=3,normal_closure_order=9,conjugate_union_size=5,product_checks=5184)
    statements=json.loads((ROOT/'results/20.89-statements.json').read_text())
    assert [x['id'] for x in statements]==['19.83','20.89']
    assert all(not x['starred_heading'] and not x['contains_editorial_star'] for x in statements)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true')
    parser.add_argument('--summary-only',action='store_true');args=parser.parse_args()
    result=summary()
    if args.summary_only:print(json.dumps(result,sort_keys=True));return
    packet=json.loads((ROOT/'results/20.89-packet.json').read_text())
    assert packet['summary']==result and packet['new_complete_candidates_added']==0
    assert packet['outside_reviews']==0 and packet['priority_established'] is False
    def bindings():
        assert len({r['path'] for r in packet['files']})==len(packet['files'])
        for r in packet['files']:
            p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],p
    bindings()
    if args.replay:
        for script,name,code,marker in [
            ('verify_20_89_native.g','expanded-native',0,b'PASS_20_89_NATIVE'),
            ('verify_20_89_independent.py','final-independent',0,b'PASS_20_89_INDEPENDENT'),
            ('verify_20_89_independent_failed_union.py','expanded-independent',1,None)]:
            command=([str(ROOT/'bin/gap'),'-o','2g'] if script.endswith('.g') else ['python3'])+[str(ROOT/'scripts'/script)]
            r=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=60)
            assert r.returncode==code
            if code==0:
                assert not r.stderr and r.stdout.count(marker)==1
                assert r.stdout==(ROOT/('results/20.89-'+name+'.log')).read_bytes()
            else:
                assert not r.stdout and b'AssertionError' in r.stderr
                assert b'assert len(normal_closure)==9' in r.stderr
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,
                          new_complete_candidates_added=0,independent_mixed_pairs=531360),sort_keys=True))
    print('PASS_20_89_PACKET')


if __name__=='__main__':main()
