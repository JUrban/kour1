#!/usr/bin/env python3
"""Check the finite controls and preserve the exact rank-uniform scope."""
from pathlib import Path
from datetime import datetime, timezone
import re
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
s = (ROOT/'results/14.24-controls.log').read_text()
assert not re.search(r'Error|Syntax|Assertion', s)
rows = re.findall(r'CONTROL1424 r=(\d+) rank=(\d+) alpha_norm=3 beta_norm=2 conjugator_norm=(\d+)', s)
assert [tuple(map(int, row)) for row in rows] == [(r, 2*r-1, r) for r in range(3, 41)]
assert s.rstrip().endswith('PASS1424 cases=38 generator_equations=11172 fixed_lattice_checks=38')
assert 11172 == sum(7*(2*r-1) for r in range(3, 41))
paths = ['research/14.24-uniform.md', 'scripts/verify_14_24.g',
         'results/14.24-controls.log',
         'references/cache/kharlampovich-14-23-uniform-2026.pdf',
         'references/cache/notebook-page75.png']
r = dict(observed_utc=datetime.now(timezone.utc).isoformat(),
         status='VERIFIED_CONTROLS_FOR_RANK_UNIFORM_PRIOR_FAMILY_DEDUCTION',
         cases=38, generator_equations=11172, fixed_lattice_checks=38,
         mathematical_scope='Exact minimum conjugator norm r in rank2r-1, '
         'with input norms3 and2. No fixed-rank impossibility claim and '
         'no new complete-candidate count.',
         sha256={x: hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in paths})
(ROOT/'results/14.24-verification.json').write_text(json.dumps(r, indent=2)+'\n')
print(json.dumps(r, indent=2))
