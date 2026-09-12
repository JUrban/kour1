#!/usr/bin/env python3
"""Run one certificate stage and retain its actual return code and output hashes."""
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
    parser.add_argument('name', choices=['conlon-probe','independent-gap','independent-python','audit'])
    args = parser.parse_args()
    commands = {
        'conlon-probe': (['bin/gap','-o','2g','scripts/probe_21_100_conlon.g'],b'PASS_21100_CONLON_DUPLICATES'),
        'independent-gap': (['bin/gap','-o','2g','scripts/export_21_100_controls.g'],b'PASS_21100_EXPORT'),
        'independent-python': (['python3','scripts/verify_21_100_controls.py'],b'PASS_21100_INDEPENDENT'),
        'audit': (['python3','scripts/audit_21_100.py'],b'PASS_21100_PACKET'),
    }
    command,sentinel = commands[args.name]
    base = ROOT/('results/21.100-'+args.name)
    now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = dict(command=command,started_utc=now())
    start = time.monotonic()
    with Path(str(base)+'.log').open('wb') as out, Path(str(base)+'.stderr').open('wb') as err:
        p = subprocess.run(command,cwd=ROOT,stdout=out,stderr=err,timeout=600)
    stdout,stderr = Path(str(base)+'.log').read_bytes(),Path(str(base)+'.stderr').read_bytes()
    record.update(ended_utc=now(),elapsed_seconds=time.monotonic()-start,actual_returncode=p.returncode,
                  stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                  stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                  sentinel_seen=stdout.count(sentinel)==1)
    Path(str(base)+'-process.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2),flush=True)
    assert p.returncode == 0 and not stderr and record['sentinel_seen']


if __name__ == '__main__':
    main()
