#!/usr/bin/env python3
"""Compare the independent complete state searches and audit the frozen packet."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inspect(name,command,marker):
    stem=ROOT/('results/17.39-'+name)
    record=json.loads(Path(str(stem)+'-process.json').read_text())
    out=Path(str(stem)+'.log');err=Path(str(stem)+'.stderr')
    assert record['command']==command and record['actual_returncode']==0 and record['accepted'] is True and record['timed_out'] is False
    assert not err.read_bytes() and sha(err)==record['stderr_sha256'] and sha(out)==record['stdout_sha256']
    assert sha(ROOT/command[-1])==record['script_sha256'] and out.read_bytes().count(marker)==1
    return out.read_text()

def summary():
    gap=inspect('native',['bin/gap','-o','2g','scripts/verify_17_39.g'],b'PASS_17_39_NATIVE')
    words=inspect('words',['python3','scripts/verify_17_39.py'],b'PASS_17_39_WORDS')
    def rows(t):return [json.loads(line.split(' ',1)[1]) for line in t.strip().splitlines() if line.startswith('ROW1739 ')]
    a,b=rows(gap),rows(words)
    assert a==b and len(a)==7
    assert [r[:2] for r in a]==[[3,1],[3,2],[3,3],[3,4],[5,1],[5,2],[7,1]]
    for p,d,order,size,normalizers,pairs,mins,hist,chain in a:
        assert order==2*p**(2*d+1) and size==2*p**d and normalizers==p**(d+1)
        assert pairs==2+(p**d-1)//(p-1)
        assert mins==chain==[2*p**d]+[p**(d-j) for j in range(1,d+1)]
        assert len(hist)==d+1 and all(count>0 for layer in hist for size,count in layer)
        assert [min(size for size,count in layer) for layer in hist]==mins
    checks=json.loads(next(line for line in words.splitlines() if line.startswith('CHECK1739 ')).split(' ',1)[1])
    assert checks==dict(associativity_triples=157464,elements_checked=51466,graph_basis_checks=185048)
    source=json.loads((ROOT/'results/17.39-source-statement.json').read_text())
    assert source['id']=='17.39' and source['starred_heading'] is False and source['contains_editorial_star'] is False
    return dict(models=7,all_normalizers=sum(r[4] for r in a),largest_minimum=5,
                new_complete_candidates_added=1,priority='unestablished',**checks)

def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');p.add_argument('--summary-only',action='store_true');args=p.parse_args()
    result=summary()
    if args.summary_only:print(json.dumps(result,sort_keys=True));return
    packet=json.loads((ROOT/'results/17.39-packet.json').read_text())
    assert packet['summary']==result and packet['outside_reviews']==0
    def bindings():
        assert len({r['path'] for r in packet['files']})==len(packet['files'])
        for row in packet['files']:
            f=ROOT/row['path'];assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],f
    bindings()
    if args.replay:
        for name,command in [('native',['bin/gap','-o','2g','scripts/verify_17_39.g']),('words',['python3','scripts/verify_17_39.py'])]:
            x=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
            assert x.returncode==0 and not x.stderr
            assert x.stdout==(ROOT/('results/17.39-'+name+'.log')).read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,**result),sort_keys=True))
    print('PASS_17_39_PACKET')

if __name__=='__main__':main()
