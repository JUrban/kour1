#!/usr/bin/env python3
"""Run bounded catalogue shards with recorded exits and exact aggregate coverage."""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('order', type=int, choices=[96,768])
    parser.add_argument('--shards', type=int, default=8)
    parser.add_argument('--tag', default='')
    args = parser.parse_args()
    assert 1 <= args.shards <= 8
    n, count = args.order, {96:231,768:1090235}[args.order]
    assert re.fullmatch(r'[a-z0-9-]*',args.tag)
    prefix = ROOT / (f'results/20.21-order{n}'+('-'+args.tag if args.tag else ''))
    script = ROOT / 'scripts/search_20_21_shard.g'
    script_hash = sha(script)
    state_file = Path(str(prefix)+'-state.json')
    final_file = Path(str(prefix)+'-summary.json')
    assert not state_file.exists() and not final_file.exists()
    targets = [Path(f'{prefix}-shard{i}{suffix}') for i in range(args.shards)
               for suffix in ['.log','.grows']]
    assert not any(p.exists() for p in targets), 'preserve previous runs'
    state = dict(status='RUNNING',order=n,total_groups=count,shards=args.shards,
                 workspace_gib_each=1,controller_pid=os.getpid(),
                 started_utc=datetime.now(timezone.utc).isoformat(),
                 script_sha256=script_hash,runner_sha256=sha(__file__),jobs=[])
    started = time.monotonic()
    processes, handles = [], []
    try:
        for i in range(args.shards):
            log, rows = Path(f'{prefix}-shard{i}.log'),Path(f'{prefix}-shard{i}.grows')
            code = (f'SearchOrder2021:={n};SearchIndex2021:={i};'
                    f'SearchShards2021:={args.shards};SearchRows2021:={json.dumps(str(rows))};')
            command = [str(ROOT/'gap-4.16.1/gap'),'-l',str(ROOT/'gap-4.16.1'),
                       '-q','-b','-T','-m','128m','-o','1g','-c',code,str(script)]
            handle = log.open('w')
            process = subprocess.Popen(command,cwd=ROOT,stdin=subprocess.DEVNULL,
                                       stdout=handle,stderr=subprocess.STDOUT)
            processes.append(process);handles.append(handle)
            state['jobs'].append(dict(index=i,pid=process.pid,command=command,
                                      log=str(log.relative_to(ROOT)),rows=str(rows.relative_to(ROOT)),
                                      returncode=None))
        state_file.write_text(json.dumps(state,indent=2)+'\n')
        print(json.dumps(state),flush=True)
        for process,job in zip(processes,state['jobs']):
            job['returncode'] = process.wait()
            job['observed_completion_utc'] = datetime.now(timezone.utc).isoformat()
            state_file.write_text(json.dumps(state,indent=2)+'\n')
            assert job['returncode'] == 0
    finally:
        for process in processes:
            if process.poll() is None: process.terminate()
        for process in processes: process.wait()
        for handle in handles: handle.close()
    assert sha(script) == script_hash
    summaries, all_rows = [], []
    for job in state['jobs']:
        output = (ROOT/job['log']).read_text()
        assert not re.search(r'Error|Syntax warning|Traceback|Assertion failure',output)
        matches = re.findall(r'PASS_2021_SHARD\s*(\[[^\]]+\])',output)
        assert len(matches) == output.count('PASS_2021_SHARD') == 1
        values = ast.literal_eval(matches[0])
        i = job['index']
        assert values[:3] == [n,i,args.shards]
        assert values[3] == (count-1-i)//args.shards+1
        rows = [ast.literal_eval(line) for line in (ROOT/job['rows']).read_text().splitlines()]
        assert len(rows) == values[5]
        hits = 0
        for nn,index,cs,aa in rows:
            assert nn == n and 1 <= index <= count and (index-1)%args.shards == i
            assert cs and aa and all(k[0] == n//12 for k in cs+aa)
            hits += sum(a == b for a in cs for b in aa)
        assert hits == values[6] == output.count('CANDIDATE_2021_SHARD')
        job['sha256'] = {p:sha(ROOT/p) for p in (job['log'],job['rows'])}
        all_rows.extend(rows);summaries.append(values)
    assert len({tuple(row[:2]) for row in all_rows}) == len(all_rows)
    totals = [sum(row[j] for row in summaries) for j in range(3,7)]
    assert totals[0] == count
    if n == 96:
        baseline = [ast.literal_eval(line) for line in (ROOT/'results/20.21-kernels.grows').read_text().splitlines()
                    if ast.literal_eval(line)[0] == 96]
        assert sorted(all_rows) == sorted(baseline)
        assert totals == [231,31,4,0]
    state.update(status='COMPLETE_CANDIDATE_REQUIRES_REVIEW' if totals[3] else 'COMPLETE_NO_CANDIDATE',
                 completed_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-started,
                 totals=dict(zip(['tested','eligible','both','hits'],totals)),shard_counts=summaries)
    final_file.write_text(json.dumps(state,indent=2)+'\n')
    state_file.write_text(json.dumps(state,indent=2)+'\n')
    print('PASS_2021_SHARDS',json.dumps(state['totals']),flush=True)


if __name__ == '__main__':
    main()
