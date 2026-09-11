#!/usr/bin/env python3
"""Run the final audits once every search worker has exited successfully."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--seconds', type=int, default=3600)
args = parser.parse_args()
assert 0 < args.seconds <= 3600
deadline = time.monotonic() + args.seconds
print('WAIT_FOR_FINAL_AUDIT', datetime.now(timezone.utc).isoformat(), flush=True)
while time.monotonic() < deadline:
    state = json.loads((ROOT/'state/19.20-orders257-511-jobs.json').read_text())
    jobs = state['jobs']
    if any(j['status'] in ['failed', 'stopped_at_bound', 'not_started_at_bound'] for j in jobs):
        raise SystemExit('Search did not complete successfully; final audits not run.')
    if all(j['status'] == 'completed' and j.get('returncode') == 0 for j in jobs):
        for script in ['run_19_20_extension.py', 'finalize_19_20_extension.py', 'summarize_19_20_all.py']:
            command = [sys.executable, str(ROOT/'scripts'/script)]
            if script == 'run_19_20_extension.py': command.append('--snapshot')
            subprocess.run(command, cwd=ROOT, check=True)
        print('FINAL_AUDITS_PASS', datetime.now(timezone.utc).isoformat(), flush=True)
        break
    time.sleep(min(15, max(0, deadline-time.monotonic())))
else:
    raise SystemExit('Wait bound reached; no completed range claimed by this runner.')
