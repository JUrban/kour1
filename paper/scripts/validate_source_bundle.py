#!/usr/bin/env python3
"""Extract and test both locally generated archives outside the repository."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from datetime import datetime, timezone

PAPER = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest(root, name):
    manifest = json.loads((root / name).read_text())
    for relative, row in manifest.items():
        path = root / relative
        assert path.is_file(), relative
        assert path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], relative
    return manifest


def main():
    tectonic = os.environ.get("PAPER_TECTONIC") or shutil.which("tectonic")
    if not tectonic:
        tectonic = str(PAPER.parent / "software/paper-toolchain/tectonic")
    tectonic = str(Path(tectonic).resolve())
    build = PAPER / "build"
    commands = []

    def run(command, cwd, logname):
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        (build / logname).write_text(result.stdout + result.stderr)
        commands.append({"command": command, "location": cwd.name,
                         "exit_code": result.returncode, "log": logname})
        if result.returncode:
            raise RuntimeError(f"{command}: {result.stdout[-2000:]} {result.stderr[-2000:]}")
        return result.stdout

    with tempfile.TemporaryDirectory(prefix="kourovka-paper-") as temporary:
        root = Path(temporary)
        assert PAPER.parent not in root.parents
        arxiv, full = root / "arxiv", root / "full"
        arxiv.mkdir()
        full.mkdir()
        with tarfile.open(PAPER / "dist/kourovka-experiment-arxiv-source.tar.gz") as archive:
            assert all(not Path(m.name).is_absolute() and ".." not in Path(m.name).parts
                       and m.isfile() for m in archive.getmembers())
            archive.extractall(arxiv, filter="data")
        with zipfile.ZipFile(PAPER / "dist/kourovka-experiment-full-source.zip") as archive:
            assert all(not Path(n).is_absolute() and ".." not in Path(n).parts
                       for n in archive.namelist())
            archive.extractall(full)
        arxiv_manifest = check_manifest(arxiv, "anc/SOURCE-MANIFEST.json")
        full_manifest = check_manifest(full, "SOURCE-MANIFEST.json")
        inventory = {name: sha(full / name) for name in
                     ["sections/inventory.tex", "sections/candidate-proofs.tex"]}
        run([sys.executable, "scripts/make_inventory.py", "--require-complete"],
            full, "portable-inventory.log")
        assert all(sha(full / name) == expected for name, expected in inventory.items())
        run([sys.executable, "scripts/render_review_changes.py", "--check"],
            full, "portable-change-record.log")
        run([sys.executable, "scripts/audit_reader_revision.py"],
            full, "portable-reader-preservation.log")
        run([tectonic, "--only-cached", "--keep-logs", "main.tex"],
            arxiv, "portable-tex.log")
        log = (arxiv / "main.log").read_text()
        assert not re.search(r"undefined|multiply defined|Overfull|LaTeX Warning",
                             log, re.I)
        source_text = subprocess.check_output(
            ["pdftotext", "-layout", str(build / "main.pdf"), "-"])
        portable_text = subprocess.check_output(
            ["pdftotext", "-layout", str(arxiv / "main.pdf"), "-"])
        assert portable_text == source_text, "portable PDF text differs"
        info = subprocess.check_output(["pdfinfo", str(arxiv / "main.pdf")], text=True)
        for script in ["verify_19_62_rank_two.py", "verify_19_61_square_completion.py",
                       "check_19_62_g2_integer_constants.py", "verify_19_62_monomial_certificates.py"]:
            run([sys.executable, "scripts/" + script], arxiv / "anc",
                "portable-" + script.removesuffix(".py") + ".log")
        # Checkers may write receipts but must preserve all original proof files.
        original = json.loads((arxiv / "anc/manifest.json").read_text())
        assert all(sha(arxiv / "anc" / r["path"]) == r["sha256"]
                   for r in original["files"])
        # Bind this replay to the mathematical inputs, not to changing review notes.
        core_hashes = {n: r["sha256"] for n, r in arxiv_manifest.items()
                       if n.endswith((".tex", ".bib", ".bbl")) or
                       n == "figures/trajectory.pdf" or n.startswith("external-reviews/")}
        result = {
            "status": "PASS",
            "checked_utc": datetime.now(timezone.utc).isoformat(),
            "scope": "Both archives extracted outside the repository; manifests checked; standalone cached TeX build; PDF text equality; portable inventory and change-record checks; mathematical-source preservation; all four ancillary proof checks.",
            "arxiv_members_checked": len(arxiv_manifest),
            "full_members_checked": len(full_manifest),
            "pages": int(re.search(r"Pages:\s+(\d+)", info)[1]),
            "tex_input_sha256": core_hashes,
            "ancillary_original_manifest_sha256": sha(arxiv / "anc/manifest.json"),
            "pdf_text_sha256": hashlib.sha256(portable_text).hexdigest(),
            "commands": commands,
        }
    (PAPER / "reviews/portable-validation.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"tex_input_sha256", "commands"}}, indent=2))
    print("All eight execution commands exited zero.")


if __name__ == "__main__":
    main()
