#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,time,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1];runs=[]
for label,cmd,files,sentinel in [
 ('export',['gap-4.16.1/gap','-l',str(ROOT/'gap-4.16.1'),'-q','-b','-T','-m','128m','-o','1g','scripts/export_18_120_256_controls.g'],['scripts/export_18_120_256_controls.g','results/18.120-256-control-inputs.json'],'PASS_18120_256_EXPORT'),
 ('controls',[sys.executable,'scripts/check_18_120_256.py'],['scripts/check_18_120_256.py','results/18.120-256-controls.json'],'PASS_18120_256_CONTROLS')]:
 log=f'results/18.120-256-{label}.log';start=time.monotonic()
 with (ROOT/log).open('w') as f:p=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=300)
 text=(ROOT/log).read_text();r={'label':label,'command':cmd,'actual_returncode':p.returncode,'elapsed_seconds':time.monotonic()-start,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clean_log':not any(x in text for x in ['Error,','Syntax warning','Syntax error','Traceback']),'sentinel':sentinel in text,'sha256':{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in files+[log] if (ROOT/x).exists()}}
 runs.append(r);(ROOT/'results/18.120-256-controls-process.json').write_text(json.dumps({'runs':runs},indent=2)+'\n');print(json.dumps(r),flush=True)
 assert p.returncode==0 and r['clean_log'] and r['sentinel']
print('PASS_18120_256_CONTROL_RUNNER')
