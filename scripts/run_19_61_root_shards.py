#!/usr/bin/env python3
"""Shard complete carpet inputs and bind aggregate changes to catalogue indices."""
import argparse
import ast
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('label',choices=['f4','g2f9'])
    args=parser.parse_args();label=args.label
    count,order={ 'f4':(2515,979200),'g2f9':(40105,22594320403200)}[label]
    source=ROOT/f'results/19.61-{label}-input.g';script=ROOT/'scripts/search_19_61_roots_shard.g'
    summary=ROOT/f'results/19.61-{label}-sharded-summary.json';assert not summary.exists()
    state=dict(status='RUNNING',label=label,carpets=count,expected_order=order,shards=4,
               workspace_gib_each=2,started_utc=datetime.now(timezone.utc).isoformat(),
               input_sha256=sha(source),script_sha256=sha(script),runner_sha256=sha(__file__),jobs=[])
    processes=[];handles=[];started=time.monotonic()
    try:
        for i in range(4):
            tag=f'{label}-shard{i}';log=ROOT/f'results/19.61-{tag}-search.log'
            changes=ROOT/f'results/19.61-{tag}-changes.grows'
            setup=ROOT/f'results/19.61-{tag}-setup.g'
            assert not any(p.exists() for p in [log,changes,setup])
            setup.write_text(f'RingLabel1961:="{tag}";ShardIndex1961:={i};ShardCount1961:=4;ExpectedOrder1961:={order};\n')
            command=[str(ROOT/'bin/gap'),'-o','2g',str(source),str(setup),str(script)]
            handle=log.open('w');handles.append(handle)
            p=subprocess.Popen(command,cwd=ROOT,stdin=subprocess.DEVNULL,stdout=handle,stderr=subprocess.STDOUT)
            processes.append(p)
            state['jobs'].append(dict(index=i,pid=p.pid,tag=tag,command=command,returncode=None,
                                      setup=str(setup.relative_to(ROOT)),log=str(log.relative_to(ROOT)),changes=str(changes.relative_to(ROOT))))
        print(json.dumps(state),flush=True)
        for p,job in zip(processes,state['jobs']):
            job['returncode']=p.wait();assert job['returncode']==0
            job['observed_completion_utc']=datetime.now(timezone.utc).isoformat()
    finally:
        for p in processes:
            if p.poll() is None:p.terminate()
        for p in processes:p.wait()
        for handle in handles:handle.close()
    assert sha(source)==state['input_sha256'] and sha(script)==state['script_sha256']
    allrows=[];totals=[0,0,0]
    for job in state['jobs']:
        i=job['index'];output=(ROOT/job['log']).read_text();tag=job['tag']
        assert not re.search(r'Error|Syntax warning|Traceback|Assertion failure',output)
        assert f'PASS_1961_AMBIENT {tag} order={order}' in output
        matches=re.findall(r'PASS_1961_SEARCH '+tag+r'\s*(\[[^\]]+\])',output)
        assert len(matches)==output.count('PASS_1961_SEARCH')==1
        counts=ast.literal_eval(matches[0]);assert counts[0]==(count-1-i)//4+1
        rows=[ast.literal_eval(line) for line in (ROOT/job['changes']).read_text().splitlines()]
        assert len(rows)==counts[1] and len({r[0] for r in rows})==len(rows)
        assert all(1<=r[0]<=count and (r[0]-1)%4==i for r in rows)
        assert counts[2]==sum(bool(r[4]) for r in rows)==output.count('CANDIDATE_1961')
        allrows+=rows;totals=[a+b for a,b in zip(totals,counts)]
        job['counts']=counts;job['sha256']={p:sha(ROOT/p) for p in [job['setup'],job['log'],job['changes']]}
    assert totals[0]==count
    if label=='f4':
        baseline=[ast.literal_eval(line) for line in (ROOT/'results/19.61-f4-changes.grows').read_text().splitlines()]
        assert sorted(allrows)==sorted(baseline) and totals==[2515,576,0]
    state.update(status='COMPLETE_CANDIDATE_REQUIRES_REVIEW' if totals[2] else 'COMPLETE_NO_FAILURE',counts=totals,
                 elapsed_seconds=time.monotonic()-started,completed_utc=datetime.now(timezone.utc).isoformat())
    summary.write_text(json.dumps(state,indent=2)+'\n')
    print('PASS_1961_SHARDS',label,json.dumps(totals),flush=True)


if __name__=='__main__':main()
