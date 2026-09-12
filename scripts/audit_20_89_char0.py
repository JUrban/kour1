#!/usr/bin/env python3
"""Audit exact independent agreement and a hash-bound proof packet."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
COMMANDS={'native':['bin/gap','-o','2g','scripts/verify_20_89_char0.g'],'words':['python3','scripts/verify_20_89_char0.py']}
def inspect(name):
    command=COMMANDS[name];stem=ROOT/('results/20.89-char0-'+name)
    record=json.loads(Path(str(stem)+'-process.json').read_text())
    out=Path(str(stem)+'.log');err=Path(str(stem)+'.stderr')
    assert record['command']==command and record['actual_returncode']==0 and record['accepted'] is True and record['timed_out'] is False
    assert not err.read_bytes() and sha(err)==record['stderr_sha256'] and sha(out)==record['stdout_sha256']
    assert sha(ROOT/command[-1])==record['script_sha256'] and out.read_bytes().count(b'PASS_20_89_CHAR0_')==1
    return out.read_text().strip().splitlines()
def parse(lines,prefix):return [json.loads(s.split(' ',1)[1]) for s in lines if s.startswith(prefix+' ')]
def summary():
    a,b=inspect('native'),inspect('words')
    rows=parse(a,'ROW2089C');assert rows==parse(b,'ROW2089C') and len(rows)==720
    assert [r[0] for r in rows]==list(range(720))
    count=0
    for i,chain in rows:
        assert len(chain)==3
        for el in chain:
            assert len(el)==4 and all(len(q)==2 and q[1]>0 for q in el[:3]) and sorted(el[3])==[1,2,3,4]
        assert chain[2][:3]==[[0,1]]*3
        assert sum(chain[2][3][i]>chain[2][3][j] for i in range(4) for j in range(i+1,4))%2==0
        count+=chain[1][2][0]!=0
    sa=parse(a,'SUMMARY2089C');sb=parse(b,'SUMMARY2089C');assert len(sa)==1 and sa==sb
    expected=dict(pairs=720,commutators=2160,nonzero_second_commutators=480,excluded_dilations=[[-4,21],[-3,21],[-2,21],[-1,40],[1,21],[2,21],[3,21],[4,21]],s4_sink_histogram=[[1,4],[4,8],[5,12]],s4_sink_union=12,nonsplit_checks=246,nonsplit_torsion=6,central_torsion_orders=[3**r for r in range(1,9)])
    assert sa[0]==expected and count==480
    assert parse(b,'INDEPENDENT2089C')==[dict(associativity_triples=729,inverse_checks=9)]
    for name in ['native','words']:
        stem=ROOT/('results/20.89-char0-'+name+'-initial')
        rec=json.loads(Path(str(stem)+'-process.json').read_text());ext='g' if name=='native' else 'py'
        assert rec['script_sha256']==sha(ROOT/('scripts/verify_20_89_char0_initial.'+ext))
        assert rec['stdout_sha256']==sha(Path(str(stem)+'.log')) and rec['stderr_sha256']==sha(Path(str(stem)+'.stderr'))
        assert rec['actual_returncode']==0 and rec['accepted']==(name=='words')
    assert b"'Encode' is read only" in (ROOT/'results/20.89-char0-native-initial.stderr').read_bytes()
    source=json.loads((ROOT/'results/20.89-statements.json').read_text())
    assert [r['id'] for r in source]==['19.83','20.89'] and all(not r['starred_heading'] for r in source)
    return dict(**expected,associativity_triples=729,inverse_checks=9,new_complete_candidates_added=0,scope='characteristic zero; positive characteristic unresolved',priority='unestablished')
def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');p.add_argument('--summary-only',action='store_true');args=p.parse_args()
    result=summary()
    if args.summary_only:print(json.dumps(result,sort_keys=True));return
    packet=json.loads((ROOT/'results/20.89-char0-packet.json').read_text())
    assert packet['summary']==result and packet['outside_reviews']==0
    def bindings():
        assert len({r['path'] for r in packet['files']})==len(packet['files'])
        for row in packet['files']:
            f=ROOT/row['path'];assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],f
    bindings()
    if args.replay:
        for name,command in COMMANDS.items():
            x=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
            assert x.returncode==0 and not x.stderr
            assert x.stdout==(ROOT/('results/20.89-char0-'+name+'.log')).read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,**result),sort_keys=True))
    print('PASS_20_89_CHAR0_PACKET')
if __name__=='__main__':main()
