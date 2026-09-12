#!/usr/bin/env python3
"""Record a bounded verifier process, preserving all bytes and its actual exit."""
import datetime, hashlib, json, subprocess, sys, time
from pathlib import Path
root=Path(__file__).resolve().parents[1]
name=sys.argv[1];command=sys.argv[2:]
script=next(x for x in command if Path(x).suffix in ('.py','.g') and (root/x).is_file())
stem=root/('results/17.39-'+name)
sha=lambda b:hashlib.sha256(b).hexdigest()
start=datetime.datetime.now(datetime.timezone.utc);tick=time.monotonic()
try:
    x=subprocess.run(command,cwd=root,capture_output=True,timeout=180)
    code=x.returncode;out=x.stdout;err=x.stderr;timed_out=False
except subprocess.TimeoutExpired as x:
    code=None;out=x.stdout or b'';err=x.stderr or b'';timed_out=True
accepted=code==0 and not err and out.count(b'PASS_17_39_')==1
Path(str(stem)+'.log').write_bytes(out);Path(str(stem)+'.stderr').write_bytes(err)
record=dict(command=command,started_utc=start.isoformat(),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,actual_returncode=code,timed_out=timed_out,accepted=accepted,script_sha256=sha((root/script).read_bytes()),stdout_sha256=sha(out),stderr_sha256=sha(err))
Path(str(stem)+'-process.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,sort_keys=True));print(out.decode(errors='replace'));print(err.decode(errors='replace'))
sys.exit(0 if accepted else 1)
