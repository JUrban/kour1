#!/usr/bin/env python3
"""Index the Notebook main body; editorial markers are not open-status proofs."""
import json
import re
from pathlib import Path

source = Path("docs/21tkt.txt").read_text()
pages = source.split("\f")
pattern = re.compile(r"(?m)^\s*(∗\s*)?(\d{1,2}\.\d{1,3})\.\s+")
main_pages = pages[:189]
joined = ""
page_offsets = []
for page_number, page in enumerate(main_pages, 1):
    page_offsets.append((len(joined), page_number))
    joined += page + "\n"
matches = list(pattern.finditer(joined))
records = []
for i, match in enumerate(matches):
    identifier = match.group(2)
    issue = int(identifier.split(".")[0])
    if not 1 <= issue <= 21:
        continue
    page_number = max(p for offset, p in page_offsets if offset <= match.start())
    end = matches[i + 1].start() if i + 1 < len(matches) else len(joined)
    statement = joined[match.end():end].strip()
    records.append({"id": identifier, "issue": issue, "pdf_page": page_number,
                    "starred_heading": bool(match.group(1)),
                    "contains_editorial_star": "∗" in statement,
                    "status": "needs_manual_review", "text": statement})
ids = [r["id"] for r in records]
assert len(ids) == len(set(ids)), "Repeated problem identifiers; inspect parser."
assert len([r for r in records if r["issue"] == 21]) == 150
assert next(r for r in records if r["id"] == "21.106")["pdf_page"] == 183
Path("research/problem-index.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
header = "id\tpdf_page\tstarred_heading\tcontains_editorial_star\tfirst_line\n"
Path("research/problem-index.tsv").write_text(header + "".join(
    f"{r['id']}\t{r['pdf_page']}\t{int(r['starred_heading'])}\t"
    f"{int(r['contains_editorial_star'])}\t{r['text'].splitlines()[0]}\n"
    for r in records))
print(json.dumps({"main_body_problems": len(records),
                  "issue_21_problems": sum(r["issue"] == 21 for r in records),
                  "starred_headings": sum(r["starred_heading"] for r in records)}, sort_keys=True))
