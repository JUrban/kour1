#!/usr/bin/env python3
"""Bounded eight-worker extension, with exact partition and live-process audits."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'state/19.20-orders257-511-jobs.json'
SUMMARY=ROOT/'results/19.20-orders257-511-progress.json'
CATALOGUE=ROOT/'results/19.20-orders257-511-catalogue.log'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path,value):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2)+'\n')
    temporary.replace(path)


def catalogue():
    content=CATALOGUE.read_text()
    assert not re.search(r'Error|Syntax|Assertion',content)
    rows=[tuple(map(int,m)) for m in re.findall(r'ORDER (\d+) (\d+)',content)]
    assert [n for n,c in rows]==list(range(257,512))
    assert sum(c for n,c in rows)==29700
    return dict(rows)


def inspect_log(job):
    path=Path(job['output'])
    if not path.exists():
        assert job['status'] in ['queued','not_started_at_bound']
        return dict(counted=0,skipped_abelian=0,equalities=0,reversals=0,done=False)
    content=path.read_text()
    assert not re.search(r'Error|Syntax|Assertion',content)
    header=json.loads(content.splitlines()[0])
    assert header['command']==job['command'] and header['source_hashes']==job['source_hashes']
    rows=re.findall(r'^COUNTS id=\[ (\d+), (\d+) \] end=(\d+) piso=(\d+)$',content,re.M)
    skipped=re.findall(r'^ABELIAN_SKIPPED id=\[ (\d+), (\d+) \] reason=known_equality$',content,re.M)
    assert len(rows)==len(re.findall(r'^COUNTS',content,re.M))
    assert len(skipped)==len(re.findall(r'^ABELIAN_SKIPPED',content,re.M))
    seen=set(); counts=[]
    for n,i,e,p in rows:
        n,i,e,p=map(int,(n,i,e,p))
        assert n==job['order'] and job['low']<=i<=job['high'] and i not in seen
        assert e>0 and p>0
        seen.add(i); counts.append((e,p))
    for n,i in skipped:
        n,i=map(int,(n,i))
        assert n==job['order'] and job['low']<=i<=job['high'] and i not in seen
        seen.add(i)
    equalities=sum(e==p for e,p in counts); reversals=sum(e>p for e,p in counts)
    done=re.findall(r'DONE checked=(\d+) abelian=(\d+) hits=(\d+) reversed=(\d+) skipped_abelian=(\d+)',content)
    assert len(done)==content.count('DONE checked=') and len(done)<=1
    if done:
        assert list(map(int,done[0]))==[len(rows),0,equalities,reversals,len(skipped)]
        assert seen==set(range(job['low'],job['high']+1))
    return dict(counted=len(rows),skipped_abelian=len(skipped),equalities=equalities,
                reversals=reversals,done=bool(done))


def is_live(job):
    if 'pid' not in job:
        return False
    proc=Path('/proc')/str(job['pid'])
    try:
        return ((proc/'cmdline').read_bytes().rstrip(b'\0').split(b'\0')==
                [s.encode() for s in job['command']] and
                (proc/'fd/1').resolve()==Path(job['output']).resolve())
    except OSError:
        return False


def snapshot():
    state=json.loads(STATE.read_text()); cat=catalogue(); covered=set(); workers=[]
    for job in state['jobs']:
        for path,sha in job['source_hashes'].items():
            assert digest(ROOT/path)==sha,'Search source changed during the run'
        ids={(job['order'],i) for i in range(job['low'],job['high']+1)}
        assert not covered&ids
        covered |= ids
        try:
            result=inspect_log(job)
            result.update(log_checks_pass=True)
        except (AssertionError,ValueError,OSError) as error:
            result=dict(log_checks_pass=False,error=str(error),done=False,
                        counted=0,skipped_abelian=0,equalities=0,reversals=0)
        result.update(order=job['order'],low=job['low'],high=job['high'],
                      state=job['status'],live=is_live(job),output=job['output'])
        result['complete']=(result['done'] and job['status']=='completed' and job['returncode']==0)
        workers.append(result)
    assert covered=={(n,i) for n,count in cat.items() for i in range(1,count+1)}
    complete=all(w['complete'] for w in workers)
    result=dict(observed_utc=datetime.now(timezone.utc).isoformat(),
                status='COMPLETE_BOUNDED_SEARCH' if complete else 'INCOMPLETE',
                catalogue_groups=29700,jobs=len(workers),
                completed_jobs=sum(w['complete'] for w in workers),
                live_workers=sum(w['live'] for w in workers),
                all_log_checks_pass=all(w['log_checks_pass'] for w in workers),
                **{name:sum(w[name] for w in workers) for name in
                   ['counted','skipped_abelian','equalities','reversals']},workers=workers)
    if complete:
        assert result['counted']+result['skipped_abelian']==29700
        result['log_sha256']={j['output']:digest(Path(j['output'])) for j in state['jobs']}
    save_json(SUMMARY,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['workers','log_sha256']},indent=2))


def run(workers,hours):
    assert 1<=workers<=8 and 0<hours<=33
    assert not STATE.exists(),'Existing run state: inspect and preserve it before resumption'
    cat=catalogue(); hashes={path:digest(ROOT/path) for path in
                           ['scripts/search_19_20.g','scripts/lib_19_20.g']}
    jobs=[]
    for n,count in cat.items():
        for low in range(1,count+1,256):
            high=min(low+255,count)
            output=ROOT/f'results/19.20-extension-order{n}-ids{low}-{high}.log'
            assert not output.exists(),'Refusing to overwrite a search log'
            setup=(f'START_ORDER:={n};;END_ORDER:={n};;START_ID:={low};;END_ID:={high};;'
                   'SKIP_ABELIAN:=true;;LOG_ALL:=true;;')
            command=[str(ROOT/'gap-4.16.1/gap'),'-l',str(ROOT/'gap-4.16.1'),'-q','-b','-T',
                     '-m','128m','-o','4g','-c',setup,str(ROOT/'scripts/search_19_20.g')]
            jobs.append(dict(order=n,low=low,high=high,status='queued',output=str(output),
                             command=command,source_hashes=hashes))
    jobs.sort(key=lambda j:(j['low'],j['order']))
    assert len(jobs)==356
    deadline=time.time()+hours*3600
    state=dict(started_utc=datetime.now(timezone.utc).isoformat(),workers=workers,
               deadline_utc=datetime.fromtimestamp(deadline,timezone.utc).isoformat(),
               workspace_cap_per_worker='4 GiB',jobs=jobs,
               warning='Recorded state is not liveness evidence; snapshot checks /proc command and stdout.')
    lock=threading.Lock()
    save_json(STATE,state)
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')

    def task(job):
        if time.time()>=deadline:
            with lock:
                job['status']='not_started_at_bound'; save_json(STATE,state)
            return
        with Path(job['output']).open('x') as log:
            log.write(json.dumps(dict(command=job['command'],source_hashes=hashes))+'\n');log.flush()
            proc=subprocess.Popen(job['command'],cwd=ROOT,stdin=subprocess.DEVNULL,
                                  stdout=log,stderr=subprocess.STDOUT,env=env)
            with lock:
                job.update(status='running',pid=proc.pid);save_json(STATE,state)
            bounded=False
            try:
                proc.wait(timeout=max(1,deadline-time.time()))
            except subprocess.TimeoutExpired:
                bounded=True;proc.terminate()
                try: proc.wait(timeout=10)
                except subprocess.TimeoutExpired: proc.kill();proc.wait()
        try:
            valid=inspect_log(job)['done'] and proc.returncode==0 and not bounded
        except (AssertionError,ValueError,OSError):
            valid=False
        with lock:
            job.update(status='completed' if valid else 'stopped_at_bound' if bounded else 'failed',
                       returncode=proc.returncode)
            save_json(STATE,state)
        print(json.dumps({k:job[k] for k in ['order','low','high','status','returncode']}),flush=True)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(task,jobs))
    snapshot()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--snapshot',action='store_true')
    parser.add_argument('--workers',type=int,default=8)
    parser.add_argument('--hours',type=float,default=33)
    args=parser.parse_args()
    if args.snapshot: snapshot()
    else: run(args.workers,args.hours)
