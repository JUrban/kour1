#!/usr/bin/env python3
"""Audit the finished F9 search and replay independent matrix memberships."""
import ast
import hashlib
import json
from pathlib import Path
import re
import check_19_61_g2_f9 as controls


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    packet=json.loads(Path('results/19.61-g2f9-summary.json').read_text())
    for p,h in packet['sha256'].items():assert sha(p)==h,p
    for name in ['results/19.61-g2f9-launch-manifest.json','results/19.61-g2f9-shard-launch-manifest.json']:
        previous=json.loads(Path(name).read_text())
        for p,h in previous['sha256'].items():assert sha(p)==h,p
    observation=json.loads(Path('results/19.61-g2f9-preparation-audit-observation.json').read_text())
    assert observation['exit_code']==0
    assert sha('results/19.61-g2f9-launch-manifest.json')==observation['manifest_sha256']
    assert sha('results/19.61-g2f9-preparation-audit.log')==observation['audit_log_sha256']
    assert Path('results/19.61-g2f9-preparation-audit.log').read_text().strip()==observation['sentinel']
    search=json.loads(Path('results/19.61-g2f9-sharded-summary.json').read_text())
    assert search['status']=='COMPLETE_NO_FAILURE' and search['counts']==[40105,4032,0]
    assert search['input_sha256']==sha('results/19.61-g2f9-input.g')
    assert search['script_sha256']==sha('scripts/search_19_61_roots_shard.g')
    expected=[[10027,1013,0],[10026,1027,0],[10026,965,0],[10026,1027,0]]
    allrows=[]
    for job in search['jobs']:
        i=job['index'];tag=job['tag'];assert job['returncode']==0 and job['counts']==expected[i]
        for p,h in job['sha256'].items():assert sha(p)==h,p
        output=Path(job['log']).read_text();assert not re.search(r'Error|Syntax warning|Traceback|CANDIDATE_',output)
        values=re.findall(r'PASS_1961_SEARCH '+tag+r'\s*(\[[^\]]+\])',output)
        assert len(values)==output.count('PASS_1961_SEARCH')==1
        assert ast.literal_eval(values[0])==expected[i]
        rows=[ast.literal_eval(s) for s in Path(job['changes']).read_text().splitlines()]
        assert len(rows)==expected[i][1]
        assert all(1<=r[0]<=40105 and (r[0]-1)%4==i and r[1]!=r[2] and r[4]==[] for r in rows)
        allrows.extend(rows)
    assert len(allrows)==len({r[0] for r in allrows})==4032
    obs=json.loads(Path('results/19.61-g2f9-process-observations.json').read_text())
    assert all(p['exit_code']==0 and p['tool_chunk'] for p in obs['successful_processes'])
    assert obs['stopped_serial']['exit_code']==1
    replay=json.loads(json.dumps(controls.run()))
    assert replay==json.loads(Path('results/19.61-g2f9-controls.json').read_text())
    print('PASS_1961_G2_F9_PACKET',len(packet['sha256']),'carpets=40105 expanded=4032 controls=1114')


if __name__=='__main__':run()
