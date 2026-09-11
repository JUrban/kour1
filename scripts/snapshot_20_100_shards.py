#!/usr/bin/env python3
"""Read live shard evidence without decompressing an already hashed certificate again."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re

import summarize_20_100 as reporter

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('n', type=int)
args = parser.parse_args()
n = args.n
prefix = ROOT/f'results/20.100-n{n}'
integrity = json.loads(Path(str(prefix)+'-integrity.json').read_text())
state = json.loads(Path(str(prefix)+'-shards-state.json').read_text())
expected_rows = [json.loads(line) for line in Path(str(prefix)+'-generator.log').read_text().splitlines()
                 if line.startswith('{') and 'CERTIFICATE_COMPLETE_PENDING_VERIFICATION' in line]
assert len(expected_rows)==1
expected = expected_rows[0]
assert integrity['status']=='INTEGRITY_CHECKED_PENDING_MATHEMATICAL_VERIFICATION'
assert integrity['n']==n and integrity['prime_bound']==n+1
for key in ['states','leaves','edges']:
    assert integrity[key]==expected[key]
digest = reporter.sha256(Path(str(prefix)+'-certificate.g.gz'))
assert digest==expected['compressed_sha256']==integrity['certificate_sha256']==state['certificate_sha256']
assert integrity['uncompressed_sha256']==state['uncompressed_sha256']
assert reporter.sha256(ROOT/'scripts/run_20_100_shards.py')==state['runner_sha256']
assert integrity['shards']==len(state['jobs'])
assert integrity['workspace_gib_each']==state['workspace_gib_each']
assert len(state['jobs'])*state['workspace_gib_each']<=84
audit = reporter.inspect_shards(n, expected, integrity['uncompressed_sha256'], prefix)
assert audit is not None
workers = []
for job in state['jobs']:
    assert job['command'][job['command'].index('-o')+1]==f"{state['workspace_gib_each']}g"
    live = reporter.recorded_job_is_live(job)
    text = Path(job['log']).read_text()
    matches = re.findall(r'CHECK_SHARD index=\s*(\d+) nodes=\s*(\d+) last_id=\s*(\d+) '
                         r'edges=\s*(\d+) cpu_ms=\s*(\d+)', ' '.join(text.split()))
    row = dict(index=job['index'],pid=job['pid'],verified_live=live,returncode=job.get('returncode'))
    if matches:
        values = list(map(int,matches[-1]))
        assert values[0]==job['index']
        row['last_progress'] = dict(zip(['index','checked_nodes','last_id','edges','cpu_ms'],values))
    if live:
        try:
            status = Path(f"/proc/{job['pid']}/status").read_text()
            row['rss_kib'] = int(re.search(r'^VmRSS:\s+(\d+) kB$',status,re.M)[1])
        except FileNotFoundError:
            row['rss_read_raced_process_exit'] = True
    workers.append(row)
if audit['status']=='VERIFIED':
    assert state['status']=='VERIFIED' and all(j.get('returncode')==0 for j in state['jobs'])
result = dict(observed_utc=datetime.now(timezone.utc).isoformat(),n=n,**audit,
              certificate_states=expected['states'],certificate_edges=expected['edges'],
              certificate_sha256=digest,workspace_gib_each=state['workspace_gib_each'],
              combined_workspace_gib=len(workers)*state['workspace_gib_each'],workers=workers,
              verified_live_rss_kib=sum(w.get('rss_kib',0) for w in workers),
              scope='Progress snapshot. A complete certificate has no proof status until every shard and the aggregate pass. Integrity is bound to the prior full gzip read by the checked compressed SHA256.')
Path(str(prefix)+'-shards-progress.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
