#!/usr/bin/env python3
"""Record the actual completion and output hashes of the bounded GAP screen."""
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
start = time.monotonic()
logpath = ROOT/'results/12.40-table-screen.log'
with logpath.open('w') as stream:
    proc = subprocess.run(['bin/gap','scripts/screen_12_40.g'], cwd=ROOT,
                          stdout=stream, stderr=subprocess.STDOUT)
log = logpath.read_text()
record = {'actual_returncode':proc.returncode,
          'elapsed_seconds':time.monotonic()-start,
          'observed_utc':datetime.now(timezone.utc).isoformat(),
          'clean_log':not any(s in log for s in ['Error,','Syntax error','Syntax warning']),
          'sentinel':log.rstrip().endswith('PASS_1240_TABLE_SCREEN'),
          'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [ROOT/'scripts/screen_12_40.g',logpath,
                              ROOT/'results/12.40-table-degrees.txt',
                              ROOT/'results/12.40-table-catalog.json'] if p.exists()}}
(ROOT/'results/12.40-table-screen-process.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
assert proc.returncode == 0 and record['clean_log'] and record['sentinel']
