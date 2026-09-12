#!/usr/bin/env python3
"""Observe actual child exits and freeze exact-control provenance."""
from pathlib import Path
import subprocess,sys,hashlib,json,time,datetime
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
records=[]
for label,script,sentinel in [('polynomial','scripts/check_14_26_polynomial.py','PASS_14_26_POLYNOMIAL'),('wreath','scripts/check_14_26_wreath.py','PASS_14_26_WREATH')]:
 log=f'results/14.26-{label}-controls.log';output=f'results/14.26-{label}-controls.json';start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (ROOT/log).open('w') as f:p=subprocess.run([sys.executable,script],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=120)
 text=(ROOT/log).read_text();record={'label':label,'script':script,'command':[sys.executable,script],'started_utc':utc,'elapsed_seconds':time.monotonic()-start,'returncode':p.returncode,'log':log,'output':output,'sentinel':sentinel,'sha256':{s:sha(s) for s in [script,log,output] if (ROOT/s).exists()}}
 records.append(record)
 (ROOT/'results/14.26-controls-process.json').write_text(json.dumps({'runs':records},indent=2)+'\n')
 assert p.returncode==0 and text.splitlines()[-1]==sentinel and 'Traceback' not in text
 assert json.loads((ROOT/output).read_text())['status']=='PASS'
print('PASS_14_26_RUNNER')
