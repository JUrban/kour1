#!/usr/bin/env python3
"""Audit and hash-bind the completed 18.18 controls."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
py = json.loads((root/'results/18.18-python.json').read_text())
assert py == json.loads((root/'results/18.18-python.log').read_text())
assert py['status'] == 'PASS'
assert [py[k] for k in ('finite_groups', 'table_associativity_checks',
                        'main_centralizers', 'padded_centralizers')] == [14, 3624, 14, 28]
log = (root/'results/18.18-gap.log').read_text()
assert not any(s in log for s in ('Error', 'Syntax warning', 'Assertion failure'))
pattern = r'^PASS_SIGMA positives=(.*) negatives=(.*)$'
m = re.search(pattern, log, re.M)
assert m and log.count('PASS_SIGMA ') == 1
positive, negative = json.loads(m[1]), json.loads(m[2])
assert len(positive) == 6 and len(negative) == 12
assert all(r[1][0] for r in positive) and not any(r[1][0] for r in negative)
assert [[n]+details[2:] for n, details in positive] == [
    [r[0]]+r[2:] for r in py['incidence']]
assert set(r[0] for r in negative) == {'S4', 'A4', 'A5', 'A6', 'D10', 'SL2_5', 'S5xC2'}
m = re.search(r'^PASS_CENTRALIZERS groups=14 padded_cases=28 rows=(.*)$', log, re.M)
assert m and log.count('PASS_CENTRALIZERS ') == 1
centralizers = json.loads(m[1])
expected = [[h, i, n, h] for h, count in enumerate([0, 1, 1, 1, 2, 1, 2, 1, 5])
            for i in range(1, count+1) for n in [2*h*h+3, 2*h*h+4]]
assert centralizers == expected
assert Counter((h, n, size) for h, _, n, size in centralizers) == Counter(
    (h, n, size) for _, h, n, size in py['centralizer_rows'])
files = ['research/18.18-proof.md', 'research/18.18-review.md',
         'scripts/verify_18_18.g', 'scripts/verify_18_18.py',
         'scripts/summarize_18_18.py', 'results/18.18-gap.log',
         'results/18.18-python.json', 'results/18.18-python.log',
         'results/18.18-initial-control-run.json',
         'results/18.18-initial-control-stopped.log',
         'results/18.18-diagnostic-control-run.json',
         'results/18.18-diagnostic-control-stopped.log',
         'references/cache/shelah-permutation-1973.pdf',
         'references/cache/shelah-permutation-errata-1973.pdf', 'docs/21tkt.pdf']
report = dict(status='PASS', observed_utc=datetime.now(timezone.utc).isoformat(),
              problem='18.18', interpretation='Cofinite up to finite-group isomorphism',
              conclusion='Complete candidate: neither the cofinite theory nor its complement is computably enumerable',
              sigma_positive=positive, sigma_negative=negative,
              centralizers=centralizers, independent_python=py,
              process_evidence='The completed GAP and Python processes were observed to exit zero. Two earlier auxiliary GAP runs were stopped incomplete and observed to exit nonzero; they are not pass evidence.',
              scope='The proof uses Malcev non-enumerability and explicit computable reductions. Exact controls corroborate the finite constructions only. Outside review and further priority checking pending.',
              sha256={p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files})
(root/'results/18.18-summary.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
