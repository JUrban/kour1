#!/usr/bin/env python3
"""Retain bounded enumeration outcomes including process-level timeouts."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

root=Path(__file__).resolve().parents[1]
template=(root/'scripts/explore_11_18.g').read_text()
records=[]
for a,b in [(2,2),(2,3),(3,3),(5,5)]:
    script=root/f'results/11.18-enumerate-{a}-{b}.g'
    script.write_text(template.replace('PARAM_A',str(a)).replace('PARAM_B',str(b)))
    log=script.with_suffix('.log')
    start=time.monotonic()
    with log.open('w') as out:
        try:
            proc=subprocess.run([str(root/'bin/gap'),str(script)],cwd=root,
                stdout=out,stderr=subprocess.STDOUT,timeout=35)
            code,timedout=proc.returncode,False
        except subprocess.TimeoutExpired:
            code,timedout=None,True
    content=log.read_text()
    clean=not any(s in content for s in ['Error,','Syntax error','Syntax warning'])
    complete='DONE_1118_ENUM' in content
    result=dict(a=a,b=b,returncode=code,timeout=timedout,
        seconds=time.monotonic()-start,clean_log=clean,complete=complete,
        concluded=code==0 and clean and complete and 'COMPLETED_COSET_TABLE' in content,
        sha256={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (script,log)})
    records.append(result)
    (root/'results/11.18-exploration-summary.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(result),flush=True)
