#!/usr/bin/env python3
"""Run small GAP controls after the table screen has released its worker."""
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
screen = json.loads((ROOT/'results/12.40-table-screen-process.json').read_text())
assert screen['actual_returncode'] == 0 and screen['clean_log'] and screen['sentinel']
start = time.monotonic()
logpath = ROOT/'results/12.40-modules.log'
with logpath.open('w') as stream:
    proc = subprocess.Popen(['bin/gap','scripts/check_12_40_modules.g'],cwd=ROOT,
                            stdout=stream,stderr=subprocess.STDOUT)
    timed_out = False
    try:
        code = proc.wait(timeout=600)
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.kill()
        code = proc.wait()
log = logpath.read_text()
record = {'actual_returncode':code,'timed_out':timed_out,
          'elapsed_seconds':time.monotonic()-start,
          'observed_utc':datetime.now(timezone.utc).isoformat(),
          'clean_log':not any(s in log for s in ('Error,','Syntax error','Syntax warning')),
          'sentinel':log.rstrip().endswith('PASS_1240_MODULES'),
          'sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                    for name in ('scripts/check_12_40_modules.g','results/12.40-modules.log',
                                 'results/12.40-modules.json','results/12.40-gap-environment.json') if (ROOT/name).exists()}}
(ROOT/'results/12.40-modules-process.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
assert code == 0 and record['clean_log'] and record['sentinel'] and not timed_out
