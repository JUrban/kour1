#!/usr/bin/env python3
"""Bind coverage, original run records and independently reconstructed lattices."""
import hashlib,json
from pathlib import Path
from check_16_45 import run
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={
 'docs/21tkt.pdf','research/16.45-plan.md','research/16.45-report.md',
 'scripts/screen_16_45.g','scripts/run_16_45_pilot.py',
 'scripts/screen_16_45_initial.g','scripts/run_16_45_pilot_initial.py',
 'scripts/export_16_45_controls.g','scripts/check_16_45.py','scripts/audit_16_45_pilot.py',
 'results/16.45-pilot.json','results/16.45-pilot.log','results/16.45-pilot-process.json',
 'results/16.45-pilot-initial.json','results/16.45-pilot-initial.log',
 'results/16.45-pilot-initial-process.json','results/16.45-pilot-initial-observation.json',
 'results/16.45-control-inputs.json','results/16.45-export.log','results/16.45-export-process.json',
 'results/16.45-controls.json','results/16.45-controls.log','results/16.45-controls-process.json',
 'results/16.45-runner-observations.json',
 'references/cache/cameron-independence-bases.pdf','references/cache/cameron-independence-bases.txt'
}
def read(name):return json.loads((ROOT/name).read_text())
def audit():
    manifest=read('results/16.45-pilot-summary.json')
    assert manifest['status']=='BOUNDED_SUFFICIENT_CERTIFICATES' and manifest['candidate_increment']==0
    assert set(manifest['sha256'])==REQUIRED
    for name,digest in manifest['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    data=read('results/16.45-pilot.json')
    counts={2:1,3:1,4:2,5:1,7:1,8:5,9:2,16:14,25:2,27:5,32:51,49:2,64:267}
    assert data['orders']==list(counts) and data['groups']==354 and data['unresolved']==0
    assert {(r['order'],r['id']) for r in data['rows']}=={(n,i) for n,c in counts.items() for i in range(1,c+1)}
    assert len(data['rows'])==354
    for row in data['rows']:
        assert sum(v for k,v in row['rank_frequencies'])==row['subgroup_classes']
        assert max(k for k,v in row['rank_frequencies'])==row['rank']
        assert row['normal_frattini_witness_classes']>0
    assert sum(r['subgroup_classes'] for r in data['rows'])==30755
    assert sum(r['subgroups'] for r in data['rows'])==45105
    assert read('results/16.45-pilot-initial.json')==data
    initial=read('results/16.45-pilot-initial-process.json')
    obs=read('results/16.45-pilot-initial-observation.json')
    assert obs['actual_outer_returncode']==1 and initial['actual_returncode']==0
    assert initial['sentinel'] and not initial['clean_log'] and not initial['timed_out']
    assert (ROOT/'results/16.45-pilot-initial.log').read_text().count('Syntax warning:')==5
    for name,digest in initial['sha256'].items():
        assert manifest['sha256'][obs['archive_mapping'][name]]==digest
    for prefix,sentinel in [('pilot','PASS_1645_PILOT'),('export','PASS_1645_EXPORT'),('controls','PASS_1645_CONTROLS')]:
        process=read(f'results/16.45-{prefix}-process.json')
        assert process['actual_returncode']==0 and process['clean_log'] and process['sentinel']
        log=(ROOT/f'results/16.45-{prefix}.log').read_text()
        assert sentinel in log and not any(s in log for s in ['Error,','Syntax warning','Syntax error','Traceback'])
        for name,digest in process.get('sha256',{}).items():assert manifest['sha256'][name]==digest
    outputs=read('results/16.45-controls.json')
    assert json.loads(json.dumps(run()))==outputs
    assert len(outputs)==12 and sum(r['subgroups'] for r in outputs)==3243
    assert sum(r['associativity_triples'] for r in outputs)==1146659
    obs=read('results/16.45-runner-observations.json')
    assert obs['pilot']['actual_outer_returncode']==obs['controls']['actual_outer_returncode']==0
    print('PASS_1645_PACKET',len(REQUIRED),'hashes; 354 groups; 45105 subgroups; 12 independent lattices; general question unresolved')
if __name__=='__main__':audit()
