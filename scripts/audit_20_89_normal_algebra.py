#!/usr/bin/env python3
"""Compare complete native/independent finite sinks and frozen bindings."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COMMANDS={'native':['bin/gap','-o','2g','scripts/verify_20_89_normal_algebra.g'],'words':['python3','scripts/verify_20_89_normal_algebra.py']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect(name):
    stem=ROOT/('results/20.89-normal-algebra-'+name);cmd=COMMANDS[name]
    rec=json.loads(Path(str(stem)+'-process.json').read_text());out=Path(str(stem)+'.log');err=Path(str(stem)+'.stderr')
    assert rec['command']==cmd and rec['actual_returncode']==0 and rec['accepted'] is True and rec['timed_out'] is False
    assert not err.read_bytes() and sha(err)==rec['stderr_sha256'] and sha(out)==rec['stdout_sha256']
    assert sha(ROOT/cmd[-1])==rec['script_sha256'] and out.read_bytes().count(b'PASS_20_89_NORMAL_ALGEBRA_')==1
    return out.read_text().strip().splitlines()
def parse(lines,prefix):return [json.loads(s.split(' ',1)[1]) for s in lines if s.startswith(prefix+' ')]
def summary():
    a,b=inspect('native'),inspect('words');rows=parse(a,'ROW2089A')
    assert rows==parse(b,'ROW2089A') and len(rows)==107
    assert len({(p,k,tuple(rep)) for p,k,rep,*_ in rows})==107
    starts=sinkentries=nontrivial=conjugates=0
    for p,kind,rep,order,sink,r,orbit in rows:
        assert p in [2,3,5,7] and kind in ['GL','SL']
        assert order==(p*p-1)*p*(p-1 if kind=='GL' else 1)
        assert sink==sorted(sink) and len({tuple(x) for x in sink})==len(sink)
        assert [1,0,0,1] in sink
        for x in sink:
            assert len(x)==4 and all(isinstance(t,int) and 0<=t<p for t in x)
            assert (x[0]*x[3]-x[1]*x[2])%p!=0
        if len(sink)>1:
            assert len(sink)>=r+1 and len(orbit)==r and len({tuple(x) for x in orbit})==r
            assert [1,0,0,1] not in orbit and all(x in sink for x in orbit)
            nontrivial+=1;conjugates+=r
        else:assert not orbit
        starts+=order;sinkentries+=len(sink)
    assert (starts,nontrivial,conjugates)==(112692,83,423)
    sa=parse(a,'SUMMARY2089A');assert len(sa)==1 and sa==parse(b,'SUMMARY2089A')
    assert sa[0]==dict(groups=8,classes=107,nontrivial_sinks=83,parameter_conjugates=423,group_rows=[[2,'GL',6,3,3,3],[2,'SL',6,3,3,3],[3,'GL',48,8,4,5],[3,'SL',24,5,4,4],[5,'GL',480,24,6,13],[5,'SL',120,7,6,13],[7,'GL',2016,48,9,25],[7,'SL',336,9,9,25]])
    control=[7,[[0,6,1,6],[1,0,0,1],[6,1,6,0]],5,[0,1,6,6]]
    assert parse(a,'CONTROL2089A')==parse(b,'CONTROL2089A')==[control]
    initial=ROOT/'results/20.89-normal-algebra-native-initial';rec=json.loads(Path(str(initial)+'-process.json').read_text())
    assert rec['actual_returncode']==0 and rec['accepted'] is False
    assert rec['script_sha256']==sha(ROOT/'scripts/verify_20_89_normal_algebra_initial.g')
    assert rec['stdout_sha256']==sha(Path(str(initial)+'.log')) and rec['stderr_sha256']==sha(Path(str(initial)+'.stderr'))
    assert Path(str(initial)+'.stderr').read_bytes().count(b'Syntax warning:')==8
    assert parse(Path(str(initial)+'.log').read_text().strip().splitlines(),'ROW2089A')==rows
    return dict(**sa[0],starting_matrices=starts,sink_entries=sinkentries,normality_counterexample=True,new_complete_candidates_added=0,priority='unestablished')
def main():
    p=argparse.ArgumentParser();p.add_argument('--summary-only',action='store_true');p.add_argument('--replay',action='store_true');args=p.parse_args();result=summary()
    if args.summary_only:print(json.dumps(result,sort_keys=True));return
    packet=json.loads((ROOT/'results/20.89-normal-algebra-packet.json').read_text())
    assert packet['summary']==result and packet['outside_reviews']==0
    def bindings():
        assert len({r['path'] for r in packet['files']})==len(packet['files'])
        for row in packet['files']:
            f=ROOT/row['path'];assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],f
    bindings()
    if args.replay:
        for name,cmd in COMMANDS.items():
            x=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=120)
            assert x.returncode==0 and not x.stderr and x.stdout==(ROOT/('results/20.89-normal-algebra-'+name+'.log')).read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,**result),sort_keys=True));print('PASS_20_89_NORMAL_ALGEBRA_PACKET')
if __name__=='__main__':main()
