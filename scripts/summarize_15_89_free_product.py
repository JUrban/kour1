#!/usr/bin/env python3
"""Bind the candidate proof and the completed exact control artifacts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
result = json.loads((root/'results/15.89-free-product-python.json').read_text())
assert result == json.loads((root/'results/15.89-free-product-python.log').read_text())
assert result['status'] == 'PASS'
assert [result[k] for k in ('degree', 'inverse_support', 'tested_vertices',
                           'basis_coordinate_checks', 'distinct_power_controls')] == [4, 9, 50, 1500, 101]
assert result['omitted_edge_rejected'] is True
gap = (root/'results/15.89-free-product-gap.log').read_text()
assert not any(x in gap for x in ('Error', 'Assertion failure', 'Syntax warning'))
assert gap.count('PASS_PROJECTIVE') == gap.count('PASS_FINITE_GRAPHS') == 1
assert ('PASS_PROJECTIVE matrices=4 inverse_support=9 two_sided_products=2 '
        'power_controls=101') in gap
assert re.search(r'PASS_FINITE_GRAPHS rows=\[ \[ 3, 12, 12 \], \[ 5, 60, 60 \], '
                 r'\[ 7, 168, 168 \] \] identity_entries=63936', gap)
files = ['research/15.89-proof.md', 'research/15.89-review.md',
         'scripts/verify_15_89_free_product.py', 'scripts/verify_15_89_free_product.g',
         'scripts/summarize_15_89_free_product.py',
         'results/15.89-free-product-python.json', 'results/15.89-free-product-python.log',
         'results/15.89-free-product-gap.log',
         'references/cache/trofimov-adjacency-2022.pdf',
         'references/cache/rvw-zigzag-2002.pdf',
         'references/cache/cavaleri-dangeli-donno-2019.pdf', 'docs/21tkt.pdf']
report = dict(status='PASS', observed_utc=datetime.now(timezone.utc).isoformat(),
              group='C3*C2', degree=4, inverse_support=9,
              python=result, gap=dict(projective_two_sided_products=2,
                                     finite_graph_orders=[12, 60, 168],
                                     finite_identity_entries=63936),
              process_evidence='Python and GAP actual exit statuses0 were observed through the execution tool; this summarizer additionally checks all retained markers and counts.',
              scope='Complete candidate negative answer to15.89. The proof covers all functions; finite controls are not extrapolated to infinity. Outside review and further novelty checking pending.',
              sha256={p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files})
(root/'results/15.89-free-product-summary.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
