#!/usr/bin/env python3
"""Four bounded exporters, with independent screens gated on actual success."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
ORDERS = [36,48,54,60,72,96,108,120,144,162,192]
LOCK = threading.Lock()
LIVE = {}


def now():
    return datetime.now(timezone.utc).isoformat()


def record_live(key, value):
    with LOCK:
        LIVE[key] = value
        (ROOT/'results/20.122-pilot-live.json').write_text(json.dumps(
            dict(observed_utc=now(),controller_pid=os.getpid(),jobs=LIVE),indent=2)+'\n')


def run(order, name, command, marker):
    stem = ROOT/f'results/20.122-order{order}-{name}'
    start = time.monotonic(); rec = dict(command=command,started_utc=now(),timeout_seconds=180)
    p = subprocess.Popen(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    rec['pid'] = p.pid; record_live(f'{order}-{name}',dict(pid=p.pid,status='running',command=command))
    stopped = False
    try:
        out,err = p.communicate(timeout=180)
    except subprocess.TimeoutExpired:
        stopped = True; os.killpg(p.pid,signal.SIGTERM)
        try:
            out,err = p.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGKILL);out,err = p.communicate()
    Path(str(stem)+'.log').write_bytes(out);Path(str(stem)+'.stderr').write_bytes(err)
    accepted = p.returncode == 0 and not err and marker in out and not stopped
    rec.update(actual_returncode=p.returncode,ended_utc=now(),elapsed_seconds=time.monotonic()-start,
               bounded_stop=stopped,stdout_sha256=hashlib.sha256(out).hexdigest(),
               stderr_sha256=hashlib.sha256(err).hexdigest(),sentinel_seen=marker in out,accepted=accepted)
    Path(str(stem)+'-process.json').write_text(json.dumps(rec,indent=2)+'\n')
    record_live(f'{order}-{name}',dict(pid=p.pid,status='terminal',actual_returncode=p.returncode,accepted=accepted))
    return rec


def job(order):
    input_name = f'results/20.122-order{order}-input.g'
    model_name = f'results/20.122-order{order}-models.json'
    summary_name = f'results/20.122-order{order}-summary.json'
    (ROOT/input_name).write_text(f'PILOT_ORDER:={order};;\nPILOT_OUTPUT:="{model_name}";;\nRead("scripts/export_20_122.g");\n')
    export = run(order,'export',['bin/gap','-o','2g',input_name],f'PASS_20_122_EXPORT order={order} '.encode())
    result = dict(order=order,export=export,complete=False)
    if export['accepted']:
        result['screen'] = run(order,'screen',['python3','scripts/screen_20_122.py',model_name,summary_name],
                               f'PASS_20_122_SCREEN order={order} '.encode())
        result['complete'] = result['screen']['accepted']
        if result['complete']:
            summary = json.loads((ROOT/summary_name).read_text())
            result['stats'] = summary['stats'];result['hits'] = summary['hits']
    print(json.dumps(dict(order=order,complete=result['complete'],hits=len(result.get('hits',[])))),flush=True)
    return result


def main():
    resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(job,ORDERS))
    result = dict(observed_utc=now(),orders=ORDERS,max_workers=4,per_process_address_limit=8*1024**3,rows=rows)
    (ROOT/'results/20.122-pilot-processes.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_20_122_PILOT_RECORDING complete='+str(sum(r['complete'] for r in rows)),flush=True)


if __name__ == '__main__':
    main()
