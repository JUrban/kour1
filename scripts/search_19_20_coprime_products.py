#!/usr/bin/env python3
"""Search recorded exact counts for a coprime direct-product equality."""
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from math import gcd
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
counts, sources = {}, {}
pattern = r'COUNTS id=\[\s*(\d+),\s*(\d+)\s*\] end=(\d+) piso=(\d+)'
for path in sorted((root/'results').glob('19.20-*.log')):
    content = path.read_bytes()
    matches = re.findall(pattern, content.decode())
    if not matches:
        continue
    sources[str(path.relative_to(root))] = hashlib.sha256(content).hexdigest()
    for n, i, end, piso in matches:
        key, value = (int(n), int(i)), (int(end), int(piso))
        assert max(value) > 0 and min(value) > 0
        assert key not in counts or counts[key] == value
        counts[key] = value
ratios = defaultdict(list)
for key, (end, piso) in counts.items():
    if end != piso:
        d = gcd(end, piso)
        ratios[(end//d, piso//d)].append(key)
hits = []
for (end, piso), groups in sorted(ratios.items()):
    if end <= piso:
        continue
    for left in groups:
        for right in ratios.get((piso, end), []):
            if gcd(left[0], right[0]) == 1:
                hits.append(dict(left=left, right=right, left_counts=counts[left],
                                 right_counts=counts[right], product_order=left[0]*right[0]))
result = dict(status='COMPLETE', observed_utc=datetime.now(timezone.utc).isoformat(),
              distinct_recorded_groups=len(counts), distinct_nonunit_ratios=len(ratios),
              recorded_reverse_groups=sum(e>p for e,p in counts.values()),
              maximum_recorded_order=max(n for n,i in counts), hits=hits,
              source_sha256=sources,
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              scope='Search only the explicit COUNTS records in retained logs, deduplicated by SmallGroup ID. Some earlier searches did not log all per-group counts, so this is not the entire completed through511 catalogue. Coprime pairs only; no assertion about larger factors or products of three or more nonabelian groups.')
(root/'results/19.20-coprime-products-summary.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))
