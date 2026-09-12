#!/usr/bin/env python3
"""Eight workers search explicit generator words, with actual exit collection."""
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
for shard in range(8):
    base = ROOT/f'results/21.99-words-shard{shard}'
    command = ['bin/gap','-o','3g','-c',f'WordShard2199:={shard};WordShards2199:=8;',
               'scripts/search_21_99_words.g']
    out,err = Path(str(base)+'.log').open('wb'),Path(str(base)+'.stderr').open('wb')
    p = subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err)
    record = dict(shard=shard,shards=8,command=command,pid=p.pid,started_utc=now(),actual_returncode=None)
    jobs.append((p,out,err,base,record))
    Path(str(base)+'-live.json').write_text(json.dumps(record,indent=2)+'\n')


def save():
    (ROOT/'results/21.99-words-shards-state.json').write_text(json.dumps(
        dict(observed_utc=now(),jobs=[x[-1] for x in jobs]),indent=2)+'\n')


save()
pending = set(range(8)); start = time.monotonic()
while pending:
    for i in list(pending):
        p,out,err,base,record = jobs[i]
        rc = p.poll()
        if rc is None:
            if time.monotonic()-start > 7200:
                p.terminate()
            continue
        out.close(); err.close()
        stdout,stderr = Path(str(base)+'.log').read_bytes(),Path(str(base)+'.stderr').read_bytes()
        cert = Path(str(base)+'-certificate.jsonl').read_bytes()
        record.update(ended_utc=now(),actual_returncode=rc,
                      stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                      stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                      certificate_sha256=hashlib.sha256(cert).hexdigest(),certificate_bytes=len(cert),
                      sentinel_seen=stdout.count(b'PASS_2199_WORD_SHARD ')==1)
        Path(str(base)+'-process.json').write_text(json.dumps(record,indent=2)+'\n')
        pending.remove(i); save()
        print('JOB_DONE',i,rc,record['sentinel_seen'],flush=True)
    if pending:
        time.sleep(1)
for p,out,err,base,record in jobs:
    assert record['actual_returncode'] == 0 and record['sentinel_seen']
    assert not Path(str(base)+'.stderr').read_bytes()
    assert not Path(str(base)+'-unresolved.jsonl').read_bytes()
print('PASS_2199_WORD_SHARD_RUNNER jobs=8',flush=True)
