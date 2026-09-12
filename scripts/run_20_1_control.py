#!/usr/bin/env python3
from pathlib import Path
import subprocess
import hashlib
import json
import sys
import time

name = sys.argv[1]
cmd, sentinel = {
    'gap': (['bin/gap', '-o', '2g', 'scripts/check_20_1_gap.g'], 'PASS_201_GAP'),
    'controls': (['python3', 'scripts/check_20_1.py'], 'PASS_201_CONTROLS'),
}[name]
start = time.monotonic()
r = subprocess.run(cmd, capture_output=True, text=True)
path = Path('results/20.1-'+name+'.log')
path.write_text(r.stdout+r.stderr)
row = dict(command=cmd, returncode=r.returncode,
           elapsed_seconds=time.monotonic()-start, stdout=r.stdout, stderr=r.stderr,
           sentinel_present=sentinel in r.stdout,
           script_sha256=hashlib.sha256(Path(cmd[-1]).read_bytes()).hexdigest(),
           log_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
Path('results/20.1-'+name+'-process.json').write_text(json.dumps(row, indent=2)+'\n')
assert r.returncode == 0 and sentinel in r.stdout and not r.stderr, row
assert 'Error' not in r.stdout and 'Syntax warning' not in r.stdout, row
print('PASS_201_PROCESS', name, r.returncode, row['elapsed_seconds'])
