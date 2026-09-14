#!/usr/bin/env python3
"""Compile the manuscript with a recorded local Tectonic invocation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-complete", action="store_true")
    args = ap.parse_args()
    command = [sys.executable, str(PAPER / "scripts/make_inventory.py")]
    if args.require_complete:
        command.append("--require-complete")
    subprocess.run(command, cwd=ROOT, check=True)
    tectonic = os.environ.get("PAPER_TECTONIC") or shutil.which("tectonic")
    if not tectonic:
        local = ROOT / "software/paper-toolchain/tectonic"
        if local.is_file():
            tectonic = str(local)
    if not tectonic:
        raise SystemExit("Set PAPER_TECTONIC to a Tectonic binary, or use a normal LaTeX distribution.")
    build = PAPER / "build"
    build.mkdir(exist_ok=True)
    cmd = [tectonic, "--keep-logs", "--keep-intermediates",
           "--outdir", "build", "main.tex"]
    started = datetime.now(timezone.utc)
    with (build / "build-console.log").open("w") as log:
        result = subprocess.run(cmd, cwd=PAPER, stdout=log, stderr=subprocess.STDOUT)
    receipt = {
        "command": cmd, "cwd": str(PAPER), "exit_code": result.returncode,
        "started_utc": started.isoformat(),
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "version": subprocess.check_output([tectonic, "--version"], text=True).strip(),
    }
    pdf = build / "main.pdf"
    if result.returncode == 0 and pdf.is_file():
        receipt.update(pdf_bytes=pdf.stat().st_size,
                       pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())
    (build / "build-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    if result.returncode:
        print((build / "build-console.log").read_text()[-6000:])
        raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
