#!/usr/bin/env python3
from pathlib import Path
import subprocess,time,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1];start=time.monotonic();log='results/18.120-pilot.log'
with (ROOT/log).open('w') as f:
 p=subprocess.Popen(['bin/gap','scripts/screen_18_120.g'],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT);timeout=False
 try:rc=p.wait(timeout=3600)
 except subprocess.TimeoutExpired:timeout=True;p.kill();rc=p.wait()
t=(ROOT/log).read_text();r={'actual_returncode':rc,'timed_out':timeout,'elapsed_seconds':time.monotonic()-start,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clean_log':not any(x in t for x in ['Error,','Syntax warning','Syntax error']),'sentinel':t.rstrip().endswith('PASS_18120_PILOT'),'sha256':{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in ['scripts/screen_18_120.g','scripts/run_18_120.py',log,'results/18.120-pilot.json'] if (ROOT/x).exists()}}
(ROOT/'results/18.120-pilot-process.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));assert rc==0 and not timeout and r['clean_log'] and r['sentinel']
