#!/usr/bin/env python3
"""Create deterministic local source archives and a PDF handoff copy."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import tarfile
import zipfile

PAPER = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    dist = PAPER / "dist"
    dist.mkdir(exist_ok=True)
    pdf = PAPER / "build/main.pdf"
    bbl = PAPER / "build/main.bbl"
    receipt = json.loads((PAPER / "build/build-receipt.json").read_text())
    if receipt["exit_code"] or digest(pdf.read_bytes()) != receipt["pdf_sha256"]:
        raise SystemExit("Build receipt does not bind a successful current PDF.")
    if not receipt.get("source_sha256") or any(
            digest((PAPER / name).read_bytes()) != expected
            for name, expected in receipt["source_sha256"].items()):
        raise SystemExit("Manuscript sources changed since the successful build.")
    if not bbl.is_file():
        raise SystemExit("Compile with intermediates retained to supply main.bbl.")

    tex = {"main.tex": (PAPER / "main.tex").read_bytes(),
           "main.bbl": bbl.read_bytes(),
           "references.bib": (PAPER / "references.bib").read_bytes(),
           "figures/trajectory.pdf": (PAPER / "figures/trajectory.pdf").read_bytes()}
    for folder in ("sections", "appendices"):
        for path in sorted((PAPER / folder).rglob("*.tex")):
            tex[str(path.relative_to(PAPER))] = path.read_bytes()

    upload = dict(tex)
    for path in sorted((PAPER / "ancillary").rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            upload["anc/" + str(path.relative_to(PAPER / "ancillary"))] = path.read_bytes()
    upload["anc/SOURCE-README.txt"] = (
        "Compile main.tex from the archive root with XeLaTeX (or pdfLaTeX) "
        "and BibTeX, or with Tectonic. main.bbl and the compiled figure "
        "are included. No shell escape or network retrieval is required "
        "when the TeX packages are installed.\n\n"
        "The anc directory contains the complete portable carpet proof "
        "certificates. Run its three checks from anc; see README.md.\n\n"
        "Author names and affiliations must be supplied by the human "
        "authors before submission. This archive has not been uploaded. "
        "The companion full source archive includes measurements, review "
        "records, and reproducibility scripts.\n"
    ).encode()
    upload["anc/SOURCE-MANIFEST.json"] = json.dumps(
        {name: {"bytes": len(data), "sha256": digest(data)}
         for name, data in sorted(upload.items())}, indent=2).encode() + b"\n"

    target = dist / "kourovka-experiment-arxiv-source.tar.gz"
    with target.open("wb") as stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w") as archive:
                for name, data in sorted(upload.items()):
                    info = tarfile.TarInfo(name)
                    info.size, info.mode, info.mtime = len(data), 0o644, 0
                    archive.addfile(info, io.BytesIO(data))

    full = dict(tex)
    for name in ("README.md", "PLAN.md", "STATUS.md"):
        full[name] = (PAPER / name).read_bytes()
    for folder in ("scripts", "data", "reviews", "ancillary", "figures"):
        for path in sorted((PAPER / folder).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {
                    ".log", ".aux", ".synctex", ".xdv"}:
                full[str(path.relative_to(PAPER))] = path.read_bytes()
    full["SOURCE-MANIFEST.json"] = json.dumps(
        {name: {"bytes": len(data), "sha256": digest(data)}
         for name, data in sorted(full.items())}, indent=2).encode() + b"\n"
    complete = dist / "kourovka-experiment-full-source.zip"
    with zipfile.ZipFile(complete, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for name, data in sorted(full.items()):
            info = zipfile.ZipInfo(name, (2026, 9, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    handoff = dist / "kourovka-experiment.pdf"
    shutil.copyfile(pdf, handoff)
    result = {p.name: {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())}
              for p in (handoff, target, complete)}
    (dist / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
