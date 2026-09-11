#!/usr/bin/env python3
"""Export retained exact cases, run GAP, and retain actual process status."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'results/9.45-controls.json').read_text())
rows=[]
for case in data['cases']:
    row=[case['r'],case['m'],case['splitting'],case['independent_basis'],case['short_vectors']]
    rows.append(json.dumps(row,separators=(',',':')).replace('null','fail'))
export=root/'results/9.45-cases.g'
export.write_text('Cases945 := [\n'+',\n'.join(rows)+'\n];\n')
log=root/'results/9.45-gap.log'
start=time.monotonic()
with log.open('w') as output:
    run=subprocess.run([str(root/'bin/gap'),'scripts/verify_9_45.g'],cwd=root,
                       stdout=output,stderr=subprocess.STDOUT)
text=log.read_text()
clean=not any(word in text for word in ['Error,','Syntax error','Syntax warning','Traceback'])
sentinel='PASS_945_GAP' in text
status=dict(returncode=run.returncode,clean_log=clean,completion_sentinel=sentinel,
            seconds=time.monotonic()-start,
            status='PASS' if run.returncode==0 and clean and sentinel else 'FAIL',
            sha256={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [export,log,root/'scripts/verify_9_45.g',
                              root/'results/9.45-controls.json']})
(root/'results/9.45-gap-status.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status,indent=2))
raise SystemExit(0 if status['status']=='PASS' else 1)
