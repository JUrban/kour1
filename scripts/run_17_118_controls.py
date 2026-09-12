#!/usr/bin/env python3
"""Record actual process results for the independent 17.118 checks."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(name, command, sentinel):
    base = ROOT / ('results/17.118-'+name)
    paths = [Path(str(base)+s) for s in ['.log', '.stderr', '-process.json']]
    assert not any(p.exists() for p in paths), 'preserve previous results'
    started = datetime.now(timezone.utc).isoformat()
    process = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=300,
                             env=dict(os.environ, OMP_NUM_THREADS='1',
                                      OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1'))
    paths[0].write_bytes(process.stdout)
    paths[1].write_bytes(process.stderr)
    record = dict(command=command, started_at=started,
                  finished_at=datetime.now(timezone.utc).isoformat(),
                  actual_returncode=process.returncode,
                  stdout_sha256=hashlib.sha256(process.stdout).hexdigest(),
                  stderr_sha256=hashlib.sha256(process.stderr).hexdigest(),
                  sentinel=sentinel, sentinel_seen=sentinel.encode() in process.stdout)
    paths[2].write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(name=name, **record)), flush=True)
    assert process.returncode == 0 and not process.stderr
    assert record['sentinel_seen'] and b'Error' not in process.stdout


if __name__ == '__main__':
    jobs = [('model', ['python3', 'scripts/verify_17_118_model.py'], 'PASS_17118_MODEL'),
            ('matrices', ['bin/gap', '-o', '512m', 'scripts/check_17_118_matrices.g'],
             'PASS_17118_MATRICES')]
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, *job) for job in jobs]
        for future in futures:
            future.result()
    print('PASS_17118_CONTROL_RUNNER', flush=True)
