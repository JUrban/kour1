#!/usr/bin/env python3
"""Audit the complete four-ring result packet and replay its controls."""
import ast
import hashlib
import json
from pathlib import Path
import re
import audit_19_61_g2_rings_preparation as prep_audit
import check_19_61_g2_rings as controls


def run():
    manifest=json.loads(Path('results/19.61-g2-rings-summary.json').read_text())
    for path,digest in manifest['sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    search=json.loads(Path('results/19.61-g2-rings-search-summary.json').read_text())
    assert search['status']=='COMPLETE_NO_FAILURE' and search['counts']==[135700,12492,0]
    expected={'g2f4':[10479,1044,0],'g2dual':[59921,4848,0],'g2split':[47345,6600,0],'g2z4':[17955,0,0]}
    assert {j['label'] for j in search['jobs']}==set(expected)
    for job in search['jobs']:
        label=job['label'];assert job['returncode']==0 and job['counts']==expected[label]
        for key,h in [('input','input_sha256'),('log','log_sha256'),('changes','changes_sha256')]:
            assert hashlib.sha256(Path(job[key]).read_bytes()).hexdigest()==job[h]
        output=Path(job['log']).read_text()
        assert not re.search(r'Error|Syntax warning|Traceback|CANDIDATE_',output)
        matches=re.findall(r'PASS_1961_SEARCH '+label+r'\s*(\[[^\]]+\])',output)
        assert len(matches)==output.count('PASS_1961_SEARCH')==1
        assert ast.literal_eval(matches[0])==expected[label]
        rows=[ast.literal_eval(line) for line in Path(job['changes']).read_text().splitlines()]
        assert len(rows)==expected[label][1] and len({r[0] for r in rows})==len(rows)
        assert all(1<=r[0]<=expected[label][0] and r[1]!=r[2] and r[4]==[] for r in rows)
    obs=json.loads(Path('results/19.61-g2-rings-process-observations.json').read_text())
    assert all(p['exit_code']==0 and p['tool_chunk'] for p in obs['processes'])
    prep_audit.main()
    replay=json.loads(json.dumps(controls.run()))
    assert replay==json.loads(Path('results/19.61-g2-rings-controls.json').read_text())
    print('PASS_1961_G2_RINGS_PACKET',len(manifest['sha256']),'carpets=135700 controls=2214 expanded=12492')


if __name__=='__main__':run()
