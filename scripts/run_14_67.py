#!/usr/bin/env python3
"""One bounded exact search, retaining command, source hashes and actual exit."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
state_path = ROOT / 'state/14.67-search.json'
log_path = ROOT / 'results/14.67-search.log'
assert not state_path.exists() and not log_path.exists(), 'Preserve existing run first'
sources = ['scripts/run_14_67.py', 'scripts/search_14_67.g', 'scripts/lib_14_67.g']
state = dict(status='STARTING', started_utc=datetime.now(timezone.utc).isoformat(),
             seconds_bound=3600, first_order=2, last_order=511,
             command=[str(ROOT/'bin/gap'), str(ROOT/'scripts/search_14_67.g')],
             output=str(log_path),
             source_sha256={f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                            for f in sources})


def save():
    temporary = state_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, indent=2)+'\n')
    temporary.replace(state_path)


save()
with log_path.open('x') as log:
    log.write(json.dumps(state)+'\n')
    log.flush()
    process = subprocess.Popen(state['command'], cwd=ROOT, stdout=log,
                               stderr=subprocess.STDOUT)
    state.update(status='RUNNING', pid=process.pid)
    save()
    try:
        code = process.wait(timeout=state['seconds_bound'])
        state.update(status='EXITED_PENDING_AUDIT', returncode=code)
    except subprocess.TimeoutExpired:
        process.terminate()
        try:
            code = process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            code = process.wait()
        state.update(status='TIME_BOUND_REACHED', returncode=code)
    state['ended_utc'] = datetime.now(timezone.utc).isoformat()
    save()
print(json.dumps(state, indent=2))
raise SystemExit(0 if state['status']=='EXITED_PENDING_AUDIT' and
                 state['returncode']==0 else 1)
