#!/usr/bin/env python3
"""Run fixed disjoint ID ranges for all groups of order256, with 16 workers.

Each process receives the 4 GiB GAP workspace limit from bin/gap. This runner
refuses to overwrite any existing output: inspect live processes before deciding
to resume a genuinely interrupted range manually.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]
COUNT = 56092
WORKERS = 16
width = (COUNT + WORKERS - 1) // WORKERS
ranges = [(lo, min(lo + width - 1, COUNT)) for lo in range(1, COUNT + 1, width)]
outputs = {pair: ROOT / f"results/19.20-order256-ids{pair[0]}-{pair[1]}.log" for pair in ranges}
assert not any(path.exists() for path in outputs.values()), "Output already exists; inspect before resuming"
lock = threading.Lock()
states = {f"{lo}-{hi}": dict(low=lo, high=hi, status="queued", output=str(outputs[lo,hi]))
          for lo,hi in ranges}


def save():
    (ROOT / "state/19.20-order256-jobs.json").write_text(json.dumps(dict(
        observed_utc=datetime.now(timezone.utc).isoformat(),
        warning="Last observed state only; revalidate process command lines before relying on liveness.",
        jobs=list(states.values())), indent=2) + "\n")


def run(pair):
    lo,hi = pair
    key = f"{lo}-{hi}"
    command = (f"START_ORDER:=256;; END_ORDER:=256;; START_ID:={lo};; END_ID:={hi};; "
               'SKIP_ABELIAN:=true;; LOG_ALL:=true;; Read("scripts/search_19_20.g");\n')
    with outputs[pair].open("x") as out:
        proc = subprocess.Popen([str(ROOT / "bin/gap")], cwd=ROOT,
                                stdin=subprocess.PIPE, stdout=out, stderr=subprocess.STDOUT, text=True)
        with lock:
            states[key].update(status="running", pid=proc.pid)
            save()
        proc.communicate(command)
    content = outputs[pair].read_text()
    valid = proc.returncode == 0 and "DONE checked=" in content and "Error" not in content
    with lock:
        states[key].update(status="completed" if valid else "failed_or_interrupted", returncode=proc.returncode)
        save()
    print(json.dumps(states[key]), flush=True)


with ThreadPoolExecutor(max_workers=WORKERS) as pool:
    list(pool.map(run,ranges))
