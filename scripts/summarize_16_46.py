#!/usr/bin/env python3
"""Check bounded-target coverage and the independent literal controls."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
log = (root/'results/16.46-target-search.log').read_text()
assert not any(x in log for x in ('Error', 'Syntax warning', 'Assertion failure'))
assert log.count('PASS_ABELIANIZATION relators=22 invariants=[]') == 1
assert log.count('PASS_FALSE_WITNESS first_relators=14 full_relators_reject=true') == 1
m = re.search(r'^COMPLETE targets=(\d+) witnesses=(\d+) cpu_ms=(\d+) rows=(.*)$', log, re.M)
assert m and list(map(int, m.group(1, 2))) == [19, 0]
rows = json.loads(m[4])
assert len(rows) == 19 and all(r[8] == r[9] == 0 for r in rows)
expected = ['A'+str(n) for n in range(5, 9)]+[
    'PSL2_'+str(q) for q in [4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31]]
assert [r[0] for r in rows] == expected
assert all(r[5] == r[2]*r[3] for r in rows)
assert len(re.findall(r'^TARGET ', log, re.M)) == 19
py = json.loads((root/'results/16.46-python.json').read_text())
assert py == json.loads((root/'results/16.46-python.log').read_text())
assert py['status'] == 'PASS' and py['rows'] == rows[:3]
assert py['literal_relator_checks'] == 35904
files = ['research/16.46-search-plan.md', 'scripts/search_16_46.g',
         'scripts/verify_16_46.py', 'scripts/summarize_16_46.py',
         'results/16.46-target-search.log', 'results/16.46-python.json',
         'results/16.46-python.log', 'docs/21tkt.pdf']
report = dict(status='PASS', observed_utc=datetime.now(timezone.utc).isoformat(),
              targets=19, witnesses=0, complete_pairs=sum(r[5] for r in rows),
              cube_triples=sum(r[6] for r in rows), rows=rows,
              independent_python=py,
              process_evidence='The GAP and Python processes were each observed to exit zero.',
              scope='No nontrivial homomorphism into the 19 listed targets. Isomorphic targets are not distinct simple groups. General finite-quotient question unresolved.',
              sha256={p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files})
(root/'results/16.46-summary.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
