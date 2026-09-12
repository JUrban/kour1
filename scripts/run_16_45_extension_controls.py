#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,time,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1]
runs=[]
for label,cmd,files,sentinel in [
 ('export',['bin/gap','scripts/export_16_45_extension_controls.g'],['scripts/export_16_45_extension_controls.g','results/16.45-extension-control-inputs.json','results/16.45-extension-catalogue-counts.json'],'PASS_1645_EXTENSION_EXPORT'),
 ('controls',[sys.executable,'scripts/check_16_45_extension.py'],['scripts/check_16_45_extension.py','results/16.45-extension-controls.json'],'PASS_1645_EXTENSION_CONTROLS')]:
 log=f'results/16.45-extension-{label}.log';start=time.monotonic()
 with (ROOT/log).open('w') as f:p=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=240)
 t=(ROOT/log).read_text();r={'label':label,'command':cmd,'actual_returncode':p.returncode,'elapsed_seconds':time.monotonic()-start,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sentinel':sentinel in t,'clean_log':not any(x in t for x in ['Error,','Syntax warning','Syntax error','Traceback']),'sha256':{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in files+[log] if (ROOT/x).exists()}}
 runs.append(r);(ROOT/'results/16.45-extension-controls-process.json').write_text(json.dumps({'runs':runs},indent=2)+'\n')
 print(json.dumps(r),flush=True)
 assert p.returncode==0 and r['sentinel'] and r['clean_log']
print('PASS_1645_EXTENSION_CONTROL_RUNNER')
