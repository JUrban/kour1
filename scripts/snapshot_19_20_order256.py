#!/usr/bin/env python3
"""Read live order-256 logs and process identities; save an honest snapshot.

Does not start, stop, or restart jobs. A PID alone is not treated as evidence
of liveness: both the executable command and its range-specific stdout file
must match. Log completion is recorded separately from process liveness.
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
metadata = json.loads((ROOT / 'state/19.20-order256-jobs.json').read_text())
workers = []
for job in metadata['jobs']:
    proc = Path('/proc') / str(job['pid'])
    try:
        command = (proc / 'cmdline').read_bytes().replace(b'\0', b' ').decode()
        stdout = os.readlink(proc / 'fd/1')
    except (FileNotFoundError, ProcessLookupError):
        command, stdout = '', ''
    content = Path(job['output']).read_text()
    counts = re.findall(r'^COUNTS id=\[ 256, (\d+) \] end=(\d+) piso=(\d+)$', content, re.M)
    ids = [int(i) for i, _, _ in counts]
    all_in_range = all(job['low'] <= i <= job['high'] for i in ids)
    unique_ids = len(ids) == len(set(ids))
    counts_well_formed = len(counts) == len(re.findall(r'^COUNTS', content, re.M))
    equalities = sum(int(e) == int(p) for _, e, p in counts)
    reversals = sum(int(e) > int(p) for _, e, p in counts)
    workers.append({
        'low': job['low'], 'high': job['high'], 'pid': job['pid'],
        'live_gap': 'gap-4.16.1/gap' in command and stdout == job['output'],
        'stdout_matches_range_log': stdout == job['output'],
        'counted': len(counts),
        'equalities': equalities,
        'reversals': reversals,
        'all_ids_in_range': all_in_range,
        'unique_ids': unique_ids,
        'counts_well_formed': counts_well_formed,
        'errors': bool(re.search(r'Error|Syntax', content)),
        'done': 'DONE checked=' in content,
        'last_counted_id': ids[-1] if ids else None,
    })

result = {
    'observed_utc': datetime.now(timezone.utc).isoformat(),
    'workers': workers,
    'total_counted': sum(w['counted'] for w in workers),
    'total_equalities': sum(w['equalities'] for w in workers),
    'total_reversals': sum(w['reversals'] for w in workers),
    'live_workers': sum(w['live_gap'] for w in workers),
    'completed_workers': sum(w['done'] for w in workers),
    'all_log_checks_pass': all(not w['errors'] and w['all_ids_in_range']
                               and w['unique_ids'] and w['counts_well_formed']
                               for w in workers),
}
(ROOT / 'results/19.20-order256-progress.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'workers'}, indent=2))
