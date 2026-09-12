#!/usr/bin/env python3
"""Bind and replay the infinite-rank partial result for20.124."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def process(name,command,marker):
    stem=ROOT/('results/20.124-'+name)
    record=json.loads(Path(str(stem)+'-process.json').read_text())
    out=Path(str(stem)+'.log');err=Path(str(stem)+'.stderr')
    assert record['command']==command and record['actual_returncode']==0 and record['accepted'] is True
    assert not err.read_bytes() and sha(err)==record['stderr_sha256'] and sha(out)==record['stdout_sha256']
    assert out.read_bytes().count(marker)==1 and sha(ROOT/command[-1])==record['script_sha256']
    return out.read_text()


def summary():
    native=process('native',['bin/gap','-o','2g','scripts/verify_20_124_native.g'],b'PASS_20_124_NATIVE')
    match=re.fullmatch(r'\s*FREE_RB_20124 (\[.*\])\s*PASS_20_124_NATIVE\s*',native,re.S)
    assert match and json.loads(match[1])==[76,13849,4240,64,[1,2,3,4,5],388]
    out=process('words',['python3','scripts/verify_20_124_words.py'],b'PASS_20_124_WORDS')
    result=json.loads(out.splitlines()[0]);assert result['status']=='PASS'
    assert [result[k] for k in ['generators','words','rbpairs','image_witnesses','depths','maximum_output_length']]==[76,13849,4240,64,[1,2,3,4,5],388]
    assert len(result['rejected_mutations'])==4
    statement=json.loads((ROOT/'results/20.124-statement.json').read_text())
    assert statement['id']=='20.124' and statement['pdf_page']==165
    assert not statement['starred_heading'] and not statement['contains_editorial_star']
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true')
    p.add_argument('--summary-only',action='store_true');args=p.parse_args()
    result=summary()
    if args.summary_only:print(json.dumps(result,sort_keys=True));return
    packet=json.loads((ROOT/'results/20.124-packet.json').read_text())
    assert packet['summary']==result and packet['new_complete_candidates_added']==0
    assert packet['scope']=='all infinite ranks; finite rank unresolved'
    assert packet['outside_reviews']==0 and packet['priority_established'] is False
    def bindings():
        assert len({r['path'] for r in packet['files']})==len(packet['files'])
        for r in packet['files']:
            f=ROOT/r['path'];assert f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],f
    bindings()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='20.124-replay-') as directory:
            tmp=Path(directory);(tmp/'results').mkdir()
            r=subprocess.run(['python3',str(ROOT/'scripts/make_20_124_fixture.py')],cwd=tmp,capture_output=True,timeout=30)
            assert r.returncode==0 and not r.stderr and r.stdout.count(b'PASS_20_124_FIXTURE')==1
            assert json.loads(r.stdout.splitlines()[0])==dict(generators=76,words=13849,rbpairs=4240,image_witnesses=64)
            for extension in ['json','g']:
                name='results/20.124-fixture.'+extension
                assert (tmp/name).read_bytes()==(ROOT/name).read_bytes()
            r=subprocess.run([str(ROOT/'bin/gap'),'-o','2g',str(ROOT/'scripts/verify_20_124_native.g')],cwd=tmp,capture_output=True,timeout=60)
            assert r.returncode==0 and not r.stderr
            assert r.stdout==(ROOT/'results/20.124-native.log').read_bytes()
            r=subprocess.run(['python3',str(ROOT/'scripts/verify_20_124_words.py')],cwd=ROOT,capture_output=True,timeout=60)
            assert r.returncode==0 and not r.stderr
            assert r.stdout==(ROOT/'results/20.124-words.log').read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,
                          new_complete_candidates_added=0,scope=packet['scope']),sort_keys=True))
    print('PASS_20_124_PACKET')


if __name__=='__main__':main()
