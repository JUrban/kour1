#!/usr/bin/env python3
"""Eight independent bounded jobs; retain each actual exit before aggregation."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


jobs = []
for order in [256,2187]:
    for shard in range(4):
        base = ROOT/f'results/21.100-order{order}-shard{shard}'
        config = f'SearchOrder21100:={order};SearchShard21100:={shard};SearchShards21100:=4;'
        command = ['bin/gap','-o','3g','-c',config,'scripts/screen_21_100.g']
        out,err = Path(str(base)+'.log').open('wb'),Path(str(base)+'.stderr').open('wb')
        p = subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err)
        row = dict(order=order,shard=shard,shards=4,pid=p.pid,command=command,
                   started_utc=now(),actual_returncode=None)
        jobs.append((p,out,err,base,row))
        Path(str(base)+'-live.json').write_text(json.dumps(row,indent=2)+'\n')
state = ROOT/'results/21.100-shards-state.json'


def save():
    state.write_text(json.dumps(dict(observed_utc=now(),jobs=[x[4] for x in jobs]),indent=2)+'\n')


save()
started = time.monotonic()
pending = set(range(len(jobs)))
while pending:
    for i in list(pending):
        p,out,err,base,row = jobs[i]
        rc = p.poll()
        if rc is None:
            if time.monotonic()-started > 7200:
                p.terminate()
            continue
        out.close(); err.close()
        stdout,stderr = Path(str(base)+'.log').read_bytes(),Path(str(base)+'.stderr').read_bytes()
        row.update(ended_utc=now(),actual_returncode=rc,
                   stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                   stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                   sentinel_seen=stdout.count(b'PASS_21100_SHARD ') == 1)
        Path(str(base)+'-process.json').write_text(json.dumps(row,indent=2)+'\n')
        pending.remove(i)
        save()
        print('JOB_DONE',row['order'],row['shard'],rc,row['sentinel_seen'],flush=True)
    if pending:
        time.sleep(1)
for p,out,err,base,row in jobs:
    assert row['actual_returncode'] == 0 and row['sentinel_seen'],row
    assert not Path(str(base)+'.stderr').read_bytes()
    assert b'Error' not in Path(str(base)+'.log').read_bytes()
print('PASS_21100_SHARD_RUNNER jobs=8',flush=True)
