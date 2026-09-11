#!/usr/bin/env python3
"""Bound ACE and its GAP parent in one process group; preserve inconclusive runs."""
import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path

root=Path(__file__).resolve().parents[1]
template=(root/'scripts/explore_11_18_ace.g').read_text()
results=[]
for a,b,strategy in [(2,2,'hard'),(2,3,'hard'),(2,3,'hlt'),(3,3,'hard')]:
    p=root/f'results/11.18-ace-{a}-{b}-{strategy}.g'
    p.write_text(template.replace('PARAM_A',str(a)).replace('PARAM_B',str(b)).replace('PARAM_STRATEGY',strategy))
    log=p.with_suffix('.log');start=time.monotonic()
    with log.open('w') as out:
        proc=subprocess.Popen([str(root/'bin/gap'),str(p)],cwd=root,
            stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
        try:
            code=proc.wait(timeout=30);timedout=False
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL)
            code=proc.wait();timedout=True
    text=log.read_text()
    row=dict(a=a,b=b,strategy=strategy,returncode=code,timeout=timedout,
        seconds=time.monotonic()-start,complete='DONE_1118_ACE' in text,
        clean_log=not any(s in text for s in ('Error,','Syntax warning','Syntax error')),
        sha256={str(q.relative_to(root)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (p,log)})
    results.append(row)
    (root/'results/11.18-ace-summary.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(row),flush=True)
