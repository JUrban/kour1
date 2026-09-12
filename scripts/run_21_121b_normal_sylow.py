#!/usr/bin/env python3
"""Preserve one bounded control invocation and its actual terminal status."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time

root=pathlib.Path(__file__).resolve().parents[1]
name=sys.argv[1]
command=sys.argv[2:]
stem=root/("results/21.121b-normal-sylow-"+name)
script=next(root/x for x in command if pathlib.Path(x).suffix in ('.py','.g') and (root/x).is_file())
start=datetime.datetime.now(datetime.timezone.utc)
tick=time.monotonic()
try:
    result=subprocess.run(command,cwd=root,capture_output=True,timeout=180)
    code,out,err=result.returncode,result.stdout,result.stderr
    timed_out=False
except subprocess.TimeoutExpired as failure:
    code,out,err=None,failure.stdout or b'',failure.stderr or b''
    timed_out=True
accepted=code==0 and not err and out.count(b'PASS_21_121B_')==1
sha=lambda data:hashlib.sha256(data).hexdigest()
pathlib.Path(str(stem)+'.log').write_bytes(out)
pathlib.Path(str(stem)+'.stderr').write_bytes(err)
record=dict(command=command,started_utc=start.isoformat(),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,actual_returncode=code,timed_out=timed_out,accepted=accepted,script_sha256=sha(script.read_bytes()),stdout_sha256=sha(out),stderr_sha256=sha(err))
pathlib.Path(str(stem)+'-process.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,sort_keys=True))
print(out.decode(errors='replace'))
print(err.decode(errors='replace'))
sys.exit(0 if accepted else 1)
