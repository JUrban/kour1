#!/usr/bin/env python3
"""Run the bounded sufficient-certificate screen; preserve incomplete runs."""
import hashlib,json,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parents[1]
start=time.monotonic()
with (root/'results/16.45-pilot.log').open('w') as stream:
    proc=subprocess.Popen(['bin/gap','scripts/screen_16_45.g'],cwd=root,
                          stdout=stream,stderr=subprocess.STDOUT)
    timed_out=False
    try: code=proc.wait(timeout=1200)
    except subprocess.TimeoutExpired:
        timed_out=True;proc.kill();code=proc.wait()
log=(root/'results/16.45-pilot.log').read_text()
record={'actual_returncode':code,'timed_out':timed_out,
        'elapsed_seconds':time.monotonic()-start,
        'observed_utc':datetime.now(timezone.utc).isoformat(),
        'clean_log':not any(s in log for s in ('Error,','Syntax error','Syntax warning')),
        'sentinel':log.rstrip().endswith('PASS_1645_PILOT'),
        'sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
          for name in ('scripts/screen_16_45.g','scripts/run_16_45_pilot.py',
                       'results/16.45-pilot.log','results/16.45-pilot.json')
          if (root/name).exists()}}
(root/'results/16.45-pilot-process.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
assert code==0 and not timed_out and record['clean_log'] and record['sentinel']
