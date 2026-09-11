#!/usr/bin/env python3
"""Require exact ID coverage and all completion records before final aggregation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

root=Path(__file__).resolve().parents[1]
metadata=json.loads((root/'state/19.20-order256-jobs.json').read_text())
abelian_log=(root/'results/19.20-order256-abelian-ids.log').read_text()
assert not re.search(r'Error|Syntax|Assertion',abelian_log)
match=re.search(r'ABELIAN_IDS\s*\[([^]]+)\]',abelian_log)
assert match and 'TOTAL_GROUPS 56092' in abelian_log
abelian=set(map(int,re.findall(r'\d+',match.group(1))))
assert len(abelian)==22

counted={}; ranges=set(); parts=[]; skipped=0
for job in metadata['jobs']:
    low,high=job['low'],job['high']
    interval=set(range(low,high+1))
    assert not ranges&interval
    ranges |= interval
    logfile=Path(job['output'])
    content=logfile.read_text()
    assert not re.search(r'Error|Syntax|Assertion',content)
    rows=re.findall(r'^COUNTS id=\[ 256, (\d+) \] end=(\d+) piso=(\d+)$',content,re.M)
    assert len(rows)==len(re.findall(r'^COUNTS',content,re.M))
    local={}
    for i,e,p in rows:
        i,e,p=int(i),int(e),int(p)
        assert i in interval and i not in local and i not in counted
        assert e>0 and p>0
        local[i]=(e,p)
    assert set(local)==interval-abelian
    normalized=' '.join(content.split())
    done=re.findall(r'DONE checked=(\d+) abelian=(\d+) hits=(\d+) reversed=(\d+) skipped_abelian=(\d+)',normalized)
    assert len(done)==content.count('DONE checked=')==1
    checked,ab,hits,reversals,omitted=map(int,done[0])
    assert checked==len(local) and ab==0
    assert hits==sum(e==p for e,p in local.values())
    assert reversals==sum(e>p for e,p in local.values())
    assert omitted==len(interval&abelian)
    skipped+=omitted; counted.update(local)
    parts.append({'low':low,'high':high,'counted':checked,'skipped_abelian':omitted,
                  'equalities':hits,'reversals':reversals,'log':str(logfile.relative_to(root)),
                  'log_sha256':hashlib.sha256(logfile.read_bytes()).hexdigest()})
assert len(parts)==16 and ranges==set(range(1,56093))
assert set(counted)==ranges-abelian and len(counted)==56070 and skipped==22
result={'status':'COMPLETE_BOUNDED_SEARCH',
        'observed_utc':datetime.now(timezone.utc).isoformat(),
        'order':256,'total_library_groups':56092,'nonabelian_counted':56070,
        'nonabelian_equalities':sum(e==p for e,p in counted.values()),
        'reverse_inequalities':sum(e>p for e,p in counted.values()),
        'skipped_abelian_ids':sorted(abelian),'partitions':parts,
        'scope':'Every nonabelian group of order 256. Abelian IDs independently reconstructed from all 22 partitions of 8; their known equality is not recomputed here.'}
(root/'results/19.20-order256-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='partitions'},indent=2))
