#!/usr/bin/env python3
"""Run bounded algebraic controls, requiring actual exit and clean completion."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
log = root / 'results/10.62-gap.log'
start = time.monotonic()
with log.open('w') as output:
    run = subprocess.run([str(root / 'bin/gap'), 'scripts/verify_10_62.g'],
                         cwd=root, stdout=output, stderr=subprocess.STDOUT)
content = log.read_text()
clean = not any(x in content for x in
                ['Error,', 'Syntax error', 'Syntax warning', 'Traceback'])
sentinel = 'PASS_1062_GAP' in content
result = dict(returncode=run.returncode, clean_log=clean,
              completion_sentinel=sentinel, seconds=time.monotonic()-start,
              status='PASS' if run.returncode == 0 and clean and sentinel else 'FAIL',
              scope='Finite controls only; infinite theorem is imported.',
              sha256={str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [log, root/'scripts/verify_10_62.g']})
(root/'results/10.62-gap-status.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)
