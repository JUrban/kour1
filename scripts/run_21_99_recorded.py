#!/usr/bin/env python3
"""Record a named command, keeping real process status separate from sentinels."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('sentinel')
    parser.add_argument('command',nargs=argparse.REMAINDER)
    args = parser.parse_args()
    assert args.command and '/' not in args.name
    base = ROOT/('results/21.99-'+args.name)
    now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    start = time.monotonic()
    record = dict(command=args.command,started_utc=now())
    with Path(str(base)+'.log').open('wb') as out,Path(str(base)+'.stderr').open('wb') as err:
        p = subprocess.Popen(args.command,cwd=ROOT,stdout=out,stderr=err)
        record['pid'] = p.pid
        Path(str(base)+'-live.json').write_text(json.dumps(record,indent=2)+'\n')
        rc = p.wait()
    stdout,stderr = Path(str(base)+'.log').read_bytes(),Path(str(base)+'.stderr').read_bytes()
    record.update(ended_utc=now(),elapsed_seconds=time.monotonic()-start,actual_returncode=rc,
                  stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                  stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                  sentinel_seen=stdout.count(args.sentinel.encode()) == 1)
    Path(str(base)+'-process.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2),flush=True)
    assert rc == 0 and not stderr and record['sentinel_seen']


if __name__ == '__main__':
    main()
