#!/usr/bin/env python3
"""Run four completed G2 ring inputs with recorded exits and hash binding."""
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
    script=ROOT/'scripts/search_19_61_roots.g';labels=['g2f4','g2dual','g2split','g2z4']
    statepath=ROOT/'results/19.61-g2-rings-search-state.json'
    finalpath=ROOT/'results/19.61-g2-rings-search-summary.json'
    assert not statepath.exists() and not finalpath.exists()
    state=dict(status='RUNNING',started_utc=datetime.now(timezone.utc).isoformat(),
               script_sha256=sha(script),runner_sha256=sha(__file__),workspace_gib_each=1,jobs=[])
    started=time.monotonic();processes=[];handles=[]
    try:
        for label in labels:
            source=ROOT/f'results/19.61-{label}-input.g'
            report=json.loads((ROOT/f'results/19.61-{label}-preparation.json').read_text())
            log=ROOT/f'results/19.61-{label}-search.log';changes=ROOT/f'results/19.61-{label}-changes.grows'
            assert source.exists() and not log.exists() and not changes.exists()
            command=[str(ROOT/'bin/gap'),'-o','1g',str(source),str(script)]
            handle=log.open('w');handles.append(handle)
            p=subprocess.Popen(command,cwd=ROOT,stdin=subprocess.DEVNULL,stdout=handle,stderr=subprocess.STDOUT)
            processes.append(p)
            state['jobs'].append(dict(label=label,pid=p.pid,command=command,returncode=None,
                                      expected_carpets=report['carpets'],expected_order=report['expected_ambient_order'],
                                      input=str(source.relative_to(ROOT)),input_sha256=sha(source),
                                      log=str(log.relative_to(ROOT)),changes=str(changes.relative_to(ROOT))))
        statepath.write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(state),flush=True)
        for p,job in zip(processes,state['jobs']):
            job['returncode']=p.wait();job['observed_completion_utc']=datetime.now(timezone.utc).isoformat()
            statepath.write_text(json.dumps(state,indent=2)+'\n');assert job['returncode']==0
    finally:
        for p in processes:
            if p.poll() is None:p.terminate()
        for p in processes:p.wait()
        for handle in handles:handle.close()
    assert sha(script)==state['script_sha256']
    totals=[0,0,0]
    for job in state['jobs']:
        assert sha(ROOT/job['input'])==job['input_sha256']
        output=(ROOT/job['log']).read_text();label=job['label']
        assert not re.search(r'Error|Syntax warning|Traceback|Assertion failure',output)
        assert f"PASS_1961_AMBIENT {label} order={job['expected_order']}" in output
        matches=re.findall(r'PASS_1961_SEARCH '+label+r'\s*(\[[^\]]+\])',output)
        assert len(matches)==output.count('PASS_1961_SEARCH')==1
        counts=ast.literal_eval(matches[0]);assert counts[0]==job['expected_carpets']
        assert output.count('CANDIDATE_1961')==counts[2]
        rows=[ast.literal_eval(line) for line in (ROOT/job['changes']).read_text().splitlines()]
        assert len(rows)==counts[1] and len({r[0] for r in rows})==len(rows)
        assert sum(bool(r[4]) for r in rows)==counts[2]
        job['counts']=counts;job['log_sha256']=sha(ROOT/job['log']);job['changes_sha256']=sha(ROOT/job['changes'])
        totals=[a+b for a,b in zip(totals,counts)]
    state.update(status='COMPLETE_REQUIRES_CANDIDATE_REVIEW' if totals[2] else 'COMPLETE_NO_FAILURE',
                 counts=totals,elapsed_seconds=time.monotonic()-started,completed_utc=datetime.now(timezone.utc).isoformat())
    statepath.write_text(json.dumps(state,indent=2)+'\n');finalpath.write_text(json.dumps(state,indent=2)+'\n')
    print('PASS_1961_G2_RINGS_SEARCH',json.dumps(totals),flush=True)


if __name__=='__main__':main()
