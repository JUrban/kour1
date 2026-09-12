#!/usr/bin/env python3
"""Run the certificate producer and retain actual exit and output hashes."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
base = ROOT/'results/20.112-chain-gap'
command = ['bin/gap', '-o', '2g', 'scripts/check_20_112_chains.g']
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
p = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=600)
Path(str(base)+'.log').write_bytes(p.stdout)
Path(str(base)+'.stderr').write_bytes(p.stderr)
record = dict(command=command, started_utc=start,
              ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              elapsed_seconds=time.monotonic()-t, actual_returncode=p.returncode,
              stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),
              stderr_sha256=hashlib.sha256(p.stderr).hexdigest(),
              sentinel_seen=p.stdout.count(b'PASS_20112_CHAINS groups=') == 1)
Path(str(base)+'-process.json').write_text(json.dumps(record, indent=2)+'\n')
assert p.returncode == 0 and not p.stderr and record['sentinel_seen'], record
assert b'Error' not in p.stdout
print(p.stdout.decode(), end='')
print('PASS_20112_CHAIN_RUNNER')
