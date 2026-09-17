#!/usr/bin/env python3
"""Check manuscript structure and recorded evidence, not mathematical truth."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

PAPER = Path(__file__).resolve().parents[1]


def main():
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    receipt = json.loads((PAPER / "build/build-receipt.json").read_text())
    assert receipt["exit_code"] == 0
    assert sha(PAPER / "build/main.pdf") == receipt["pdf_sha256"]
    for name, expected in receipt["source_sha256"].items():
        assert sha(PAPER / name) == expected, ("stale build", name)

    paths = [PAPER / "main.tex"] + sorted((PAPER / "sections").rglob("*.tex"))
    paths += sorted((PAPER / "appendices").rglob("*.tex"))
    content = "\n".join(path.read_text() for path in paths)
    labels = re.findall(r"\\label\{([^}]+)\}", content)
    duplicates = [k for k, n in collections.Counter(labels).items() if n > 1]
    assert not duplicates, duplicates
    refs = set(re.findall(r"\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}", content))
    assert not refs - set(labels), refs - set(labels)
    cites = {key.strip()
             for group in re.findall(r"\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}", content)
             for key in group.split(",")}
    bibkeys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,",
                         (PAPER / "references.bib").read_text())
    assert len(bibkeys) == len(set(bibkeys)), "duplicate bibliography keys"
    assert not cites - set(bibkeys), cites - set(bibkeys)
    for target in re.findall(r"\\input\{([^}]+)\}", content):
        assert (PAPER / (target + ".tex")).is_file(), target

    frozen = json.loads((PAPER / "data/frozen-candidate-ledger.json").read_text())
    review = json.loads((PAPER / "reviews/candidate-review-ledger.json").read_text())
    assert len(frozen["candidates"]) == len(review["entries"]) == 46
    assert {r["problem"] for r in frozen["candidates"]} == {
        r["problem"] for r in review["entries"]}
    assert all(r["final_pass"] == "passed_internal_review" and
               r["final_pass_notes"] and r["outside_reviews"] == 0 and
               r["priority"] == "unestablished" for r in review["entries"])
    special = {"21.106": "subsec:concise", "21.68": "subsec:semiabelian",
               "20.108": "subsec:holomorph"}
    assert all(special.get(r["problem"], "cand:" + r["problem"]) in labels
               for r in frozen["candidates"])
    assert not re.search(r"\b(?:TODO|TBD|FIXME)\b", content)
    for log in ["main.log", "main.blg"]:
        text = (PAPER / "build" / log).read_text()
        assert not re.search(r"undefined|multiply defined|Overfull|Warning--|LaTeX Warning",
                             text, re.I), log

    ancillary = PAPER / "ancillary"
    manifest = json.loads((ancillary / "manifest.json").read_text())
    assert len(manifest["files"]) == 24
    for row in manifest["files"]:
        path = ancillary / row["path"]
        assert path.stat().st_size == row["bytes"] and sha(path) == row["sha256"]
    assert (PAPER / "appendices/carpet-tables.tex").read_text().count(
        r"\begin{minipage}") == 19
    info = subprocess.check_output(["pdfinfo", str(PAPER / "build/main.pdf")], text=True)
    result = {
        "status": "PASS", "checked_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Structure, source/build binding, recorded review completeness, and artifact integrity only; not an automated mathematical proof check.",
        "candidate_entries": 46, "tex_files": len(paths),
        "labels": len(labels), "cited_works": len(cites),
        "bibliography_entries": len(bibkeys),
        "ancillary_original_files": 24, "printed_carpet_derivations": 19,
        "pages": int(re.search(r"Pages:\s+(\d+)", info)[1]),
        "pdf_sha256": receipt["pdf_sha256"],
        "undistributed_large_artifacts": ["20.100-n7-certificate.g.gz"],
    }
    (PAPER / "reviews/structure-audit.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
