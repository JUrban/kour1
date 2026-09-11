#!/usr/bin/env python3
"""Match inverse count ratios in retained 19.20 logs; see the research note.

This reads existing rows, not a complete SmallGrp range. It does not replace
the separate catalogue audits or count previously unlogged groups.
"""
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(
    r"(?:COUNTS|CLOSEST|STRONG_INEQUALITY_COUNTEREXAMPLE) "
    r"id=\[ (\d+), (\d+) \] end=(\d+) piso=(\d+)"
)


def main():
    rows = {}
    hashes = {}
    for path in sorted((ROOT / "results").glob("19.20-*.log")):
        raw = path.read_bytes()
        found = PATTERN.findall(raw.decode())
        if found:
            hashes[str(path.relative_to(ROOT))] = sha256(raw).hexdigest()
        for n, i, end, piso in found:
            key, value = (int(n), int(i)), (int(end), int(piso))
            assert key not in rows or rows[key] == value, (path, key)
            rows[key] = value

    ratios = defaultdict(list)
    for key, (end, piso) in sorted(rows.items()):
        assert end > 0 and piso > 0
        if end != piso:
            ratios[Fraction(end, piso)].append(key)
    hits, inadmissible = [], []
    for ratio, first in sorted(ratios.items()):
        if ratio <= 1:
            continue
        for a in first:
            for b in ratios.get(1 / ratio, []):
                target = hits if gcd(a[0], b[0]) == 1 else inadmissible
                target.append([a, b, str(ratio)])

    smallest = sorted(ratios, key=lambda f: (f.numerator + f.denominator, f))[:20]
    data = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Read-only exploration of retained count rows; not an additional coverage audit",
        "unique_group_rows": len(rows),
        "distinct_nonunit_ratios": len(ratios),
        "coprime_inverse_ratio_pairs": hits,
        "noncoprime_inverse_ratio_pairs": inadmissible,
        "smallest_ratios": [
            {"end_over_piso": str(f), "examples": ratios[f][:5]} for f in smallest
        ],
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": hashes,
    }
    output = ROOT / "results/19.20-coprime-ratio-exploration.json"
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({k: data[k] for k in (
        "unique_group_rows", "distinct_nonunit_ratios",
        "coprime_inverse_ratio_pairs", "noncoprime_inverse_ratio_pairs")}, indent=2))
    print("RATIO_EXPLORATION_DONE")


if __name__ == "__main__":
    main()
