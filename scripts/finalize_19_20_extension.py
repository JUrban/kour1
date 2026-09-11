#!/usr/bin/env python3
"""Require closed successful jobs, exact coverage and independent abelian IDs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import run_19_20_extension as runner

ROOT = Path(__file__).resolve().parents[1]
state = json.loads(runner.STATE.read_text())
cat = runner.catalogue()
ab_path = ROOT/'results/19.20-orders257-511-abelian-ids.log'
ab_log = ab_path.read_text()
assert not re.search(r'Error|Syntax|Assertion', ab_log)
assert ab_log.rstrip().endswith('PASS_ABELIAN1920 orders=255 groups=514')
abelian_rows = [tuple(map(int, p)) for p in re.findall(
    r'^ABELIAN_ID1920 order=(\d+) id=(\d+) invariants=', ab_log, re.M)]
assert len(abelian_rows) == len(set(abelian_rows)) == 514
abelian = set(abelian_rows)
orders = [tuple(map(int, p)) for p in re.findall(
    r'^ABELIAN_ORDER1920 order=(\d+) count=(\d+)$', ab_log, re.M)]
assert [n for n, c in orders] == list(range(257, 512))
assert all(sum(a == n for a, i in abelian) == c for n, c in orders)

covered = set(); counted = {}; skipped = set(); logs = {}; parts = []
for job in state['jobs']:
    assert job['status'] == 'completed' and job['returncode'] == 0
    assert not runner.is_live(job)
    for path, sha in job['source_hashes'].items():
        assert runner.digest(ROOT/path) == sha
    r = runner.inspect_log(job); assert r['done']
    interval = {(job['order'], i) for i in range(job['low'], job['high']+1)}
    assert not covered & interval; covered |= interval
    path = Path(job['output']); content = path.read_text()
    local = {(int(n), int(i)): (int(e), int(p)) for n, i, e, p in re.findall(
        r'^COUNTS id=\[ (\d+), (\d+) \] end=(\d+) piso=(\d+)$', content, re.M)}
    omissions = {tuple(map(int, p)) for p in re.findall(
        r'^ABELIAN_SKIPPED id=\[ (\d+), (\d+) \] reason=known_equality$', content, re.M)}
    assert omissions == interval & abelian
    assert set(local) == interval - abelian
    assert not counted.keys() & local.keys() and not skipped & omissions
    counted.update(local); skipped |= omissions
    logs[str(path.relative_to(ROOT))] = runner.digest(path)
    parts.append(dict(order=job['order'], low=job['low'], high=job['high'], **r))
assert covered == {(n, i) for n, c in cat.items() for i in range(1, c+1)}
assert len(parts) == 356 and len(covered) == 29700 and skipped == abelian and len(counted) == 29186
reverse = [dict(order=n, id=i, endomorphisms=e, partial_isomorphisms=p)
           for (n, i), (e, p) in sorted(counted.items()) if e > p]
result = dict(status='COMPLETE_BOUNDED_SEARCH', observed_utc=datetime.now(timezone.utc).isoformat(),
              orders=[257, 511], total_library_groups=29700,
              nonabelian_counted=len(counted), independently_reconstructed_abelian=514,
              nonabelian_equalities=sum(e == p for e, p in counted.values()),
              reverse_inequalities=len(reverse), reversals=reverse,
              partitions=parts, log_sha256=logs,
              abelian_log_sha256=runner.digest(ab_path),
              scope='All nonabelian SmallGroups entries of orders257 through511. '
              'All skipped abelian IDs independently reconstructed from partitions '
              'of prime exponents. No conclusion for arbitrary finite groups.')
(ROOT/'results/19.20-orders257-511-summary.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k not in
                 ['partitions', 'log_sha256', 'reversals']}, indent=2))
