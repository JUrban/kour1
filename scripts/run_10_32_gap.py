#!/usr/bin/env python3
"""Preserve actual exit, clean completion and finite-certificate provenance."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
log = root / 'results/10.32-gap.log'
start = time.monotonic()
with log.open('w') as out:
    run = subprocess.run([str(root/'bin/gap'), 'scripts/verify_10_32.g'],
                         cwd=root, stdout=out, stderr=subprocess.STDOUT)
content = log.read_text()
clean = not any(x in content for x in
                ['Error,', 'Syntax error', 'Syntax warning', 'Traceback'])
complete = 'PASS_1032_WITNESSES' in content
passed = run.returncode == 0 and clean and complete
paths = [log, root/'scripts/verify_10_32.g', root/'results/10.32-witnesses.json']
result = dict(returncode=run.returncode, clean_log=clean, complete=complete,
              status='PASS' if passed else 'FAIL', seconds=time.monotonic()-start,
              scope='Finite permutation witnesses only; general proof separate.',
              sha256={str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in paths if p.exists()})
(root/'results/10.32-gap-status.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if passed else 1)
