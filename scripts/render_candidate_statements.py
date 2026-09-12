#!/usr/bin/env python3
"""Render original candidate statements for human scope review, not proof checking."""
import hashlib
import json
import math
import pathlib
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = ROOT / "docs/21tkt.pdf"
OUT = ROOT / "results/pdf-statement-review"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ledger = json.loads((ROOT / "research/complete-candidate-ledger.json").read_text())
    ns = {"h": "http://www.w3.org/1999/xhtml"}
    pages = {}
    rows = []
    for c in ledger["candidates"]:
        number = c["statement_index_pdf_page"]
        if number not in pages:
            xml = OUT / f"page-{number}.html"
            subprocess.run(["pdftotext", "-f", str(number), "-l", str(number),
                            "-bbox-layout", str(PDF), str(xml)], check=True)
            # Poppler may emit literal TeX control characters in word text.
            # Preserve its bytes; remove XML-forbidden controls only in memory.
            xml_text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", xml.read_text())
            page = ET.fromstring(xml_text).find(".//h:page", ns)
            words = list(page.iterfind(".//h:word", ns))
            headings = [w for w in words
                        if float(w.attrib["xMin"]) < 130
                        and re.fullmatch(r"\*?\d+\.\d+\.?", w.text or "")]
            pages[number] = (xml, page, headings)
        xml, page, headings = pages[number]
        starts = [w for w in headings if (w.text or "").lstrip("*").rstrip(".") == c["problem"]]
        if len(starts) != 1:
            raise ValueError((c["problem"], "ambiguous heading", [w.text for w in starts]))
        top = float(starts[0].attrib["yMin"])
        later = [float(w.attrib["yMin"]) for w in headings
                 if float(w.attrib["yMin"]) > top + 5]
        bottom = min(later) - 3 if later else float(page.attrib["height"]) - 10
        # 144 dpi: two pixels per PDF point. Keep the entire text width.
        x, y = 180, math.floor(2 * (top - 5))
        width, height = 810, math.ceil(2 * bottom) - y
        prefix = OUT / f"{c['problem']}-statement"
        subprocess.run(["pdftoppm", "-f", str(number), "-l", str(number),
                        "-r", "144", "-x", str(x), "-y", str(y), "-W", str(width),
                        "-H", str(height), "-singlefile", "-png", str(PDF), str(prefix)],
                       check=True, stdout=subprocess.DEVNULL)
        png = pathlib.Path(str(prefix) + ".png")
        rows.append({"problem": c["problem"], "pdf_page": number,
                     "covered_subparts": c["covered_subparts"],
                     "pixel_crop_at_144_dpi": [x, y, width, height],
                     "next_heading_on_page": bool(later),
                     "coordinate_source": str(xml.relative_to(ROOT)),
                     "coordinate_source_sha256": digest(xml),
                     "image": str(png.relative_to(ROOT)), "image_sha256": digest(png)})
    manifest = {"purpose": "Rendered statements for a human scope review; no mathematical PASS claim",
                "source_pdf": "docs/21tkt.pdf", "source_pdf_sha256": digest(PDF),
                "renderer": subprocess.run(["pdftoppm", "-v"], capture_output=True,
                                           text=True, check=True).stderr.strip(),
                "statements": rows}
    (OUT / "render-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"rendered": len(rows), "pages": len(pages),
                      "without_next_heading": [r["problem"] for r in rows if not r["next_heading_on_page"]]}))


if __name__ == "__main__":
    main()
