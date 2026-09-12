#!/usr/bin/env python3
"""Preserve streaming output and actual completion, including timeouts."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(name, command, sentinel):
    base = ROOT / ("results/17.113-" + name)
    stdout = Path(str(base) + ".log")
    stderr = Path(str(base) + ".stderr")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    timed_out = False
    with stdout.open("w") as out, stderr.open("w") as err:
        process = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=err)
        try:
            returncode = process.wait(timeout=180)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.terminate()
            try:
                returncode = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                returncode = process.wait()
    record = dict(command=command, started_at=started,
                  finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  actual_returncode=returncode, timed_out=timed_out,
                  stdout_sha256=hashlib.sha256(stdout.read_bytes()).hexdigest(),
                  stderr_sha256=hashlib.sha256(stderr.read_bytes()).hexdigest(),
                  sentinel=sentinel, sentinel_seen=sentinel in stdout.read_text())
    Path(str(base) + "-process.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record), flush=True)
    assert not timed_out and returncode == 0 and not stderr.read_bytes()
    assert record["sentinel_seen"] and "Error" not in stdout.read_text()


if __name__ == "__main__":
    run("coordinates", ["python3", "scripts/check_17_113.py"], "PASS_17113_COORDINATES")
    run("gap", ["bin/gap", "-o", "512m", "scripts/check_17_113.g"], "PASS_17113_GAP cases=28")
    print("PASS_17113_RUNNER")
