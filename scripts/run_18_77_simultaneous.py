#!/usr/bin/env python3
import subprocess,time,datetime,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];start=time.monotonic();log=ROOT/'results/18.77-simultaneous-controls.log'
with log.open('w') as f:
 p=subprocess.run([sys.executable,'scripts/check_18_77_simultaneous.py'],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=300)
t=log.read_text();files=['scripts/check_18_77_simultaneous.py','scripts/run_18_77_simultaneous.py','results/18.77-simultaneous-controls.json','results/18.77-simultaneous-controls.log']
r={'actual_returncode':p.returncode,'elapsed_seconds':time.monotonic()-start,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clean_log':'Traceback' not in t,'sentinel':'PASS_1877_SIMULTANEOUS' in t,'sha256':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in files if (ROOT/s).exists()}}
(ROOT/'results/18.77-simultaneous-process.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
assert p.returncode==0 and r['clean_log'] and r['sentinel']
print('PASS_1877_SIMULTANEOUS_RUNNER')
