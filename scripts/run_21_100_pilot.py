#!/usr/bin/env python3
"""Retain live progress and trustworthy completion status for the pilot."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
base = ROOT/'results/21.100-pilot'
command = ['bin/gap','-o','3g','scripts/pilot_21_100.g']
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
with Path(str(base)+'.log').open('wb') as out, Path(str(base)+'.stderr').open('wb') as err:
    p = subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err)
    Path(str(base)+'-live.json').write_text(json.dumps(dict(command=command,pid=p.pid,
        started_utc=start),indent=2)+'\n')
    rc = p.wait()
stdout,stderr = Path(str(base)+'.log').read_bytes(),Path(str(base)+'.stderr').read_bytes()
record = dict(command=command,started_utc=start,
    ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    elapsed_seconds=time.monotonic()-t,actual_returncode=rc,
    stdout_sha256=hashlib.sha256(stdout).hexdigest(),stderr_sha256=hashlib.sha256(stderr).hexdigest(),
    sentinel_seen=stdout.count(b'PASS_21100_PILOT ') == 1)
Path(str(base)+'-process.json').write_text(json.dumps(record,indent=2)+'\n')
assert rc == 0 and not stderr and record['sentinel_seen'],record
assert b'Error' not in stdout
print(stdout.decode(),end='')
print('PASS_21100_RUNNER')
