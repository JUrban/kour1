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
    subprocess.run([sys.executable, str(PAPER / "scripts/render_review_changes.py"), "--check"], cwd=ROOT, check=True)
    correspondence = json.loads((PAPER / "external-reviews/manifest.json").read_text())
    for record in correspondence["documents"]:
        for path_key, hash_key in [("path", "sha256"), ("rendered_path", "rendered_sha256")]:
            if path_key in record:
                actual = hashlib.sha256((PAPER / record[path_key]).read_bytes()).hexdigest()
                assert actual == record[hash_key], ("stale correspondence", record[path_key])
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
        "source_sha256": {
            str(path.relative_to(PAPER)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(
                [PAPER / "main.tex", PAPER / "references.bib",
                 PAPER / "figures/trajectory.pdf"]
                + list((PAPER / "sections").rglob("*.tex"))
                + list((PAPER / "appendices").rglob("*.tex"))
                + [p for p in (PAPER / "external-reviews").iterdir() if p.is_file()])
        },
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
