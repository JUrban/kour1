#!/usr/bin/env python3
"""Check exact extension coverage and replay both independent table packets."""
import hashlib,json
from pathlib import Path
from audit_16_45_pilot import REQUIRED as PILOT_REQUIRED,audit as pilot_audit
from check_16_45_extension import run
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=PILOT_REQUIRED|{
 'results/16.45-pilot-summary.json','results/16.45-audit-observation.json',
 'research/16.45-extension-plan.md','research/16.45-extension-report.md',
 'scripts/screen_16_45_extension.g','scripts/run_16_45_extension.py',
 'scripts/export_16_45_extension_controls.g','scripts/check_16_45_extension.py',
 'scripts/run_16_45_extension_controls.py','scripts/audit_16_45_extension.py',
 'results/16.45-extension.json','results/16.45-extension.log','results/16.45-extension-process.json',
 'results/16.45-extension-control-inputs.json','results/16.45-extension-catalogue-counts.json',
 'results/16.45-extension-export.log','results/16.45-extension-controls.json',
 'results/16.45-extension-controls.log','results/16.45-extension-controls-process.json',
 'results/16.45-extension-runner-observations.json',
}
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def audit():
 m=read('results/16.45-extension-summary.json')
 assert m['status']=='BOUNDED_SUFFICIENT_CERTIFICATES' and m['candidate_increment']==0
 assert set(m['sha256'])==REQUIRED
 for p,h in m['sha256'].items():assert sha(p)==h,p
 pilot_audit()
 d=read('results/16.45-extension.json');counts=[[81,15],[125,5],[128,2328],[243,67],[343,5],[625,15]]
 assert read('results/16.45-extension-catalogue-counts.json')==counts
 assert d['orders']==[n for n,c in counts] and d['groups']==2435 and d['unresolved']==0
 assert len(d['rows'])==2435
 assert {(r['order'],r['id']) for r in d['rows']}=={(n,i) for n,c in counts for i in range(1,c+1)}
 for r in d['rows']:
  assert sum(v for k,v in r['rank_frequencies'])==r['subgroup_classes']
  assert max(k for k,v in r['rank_frequencies'])==r['rank']
  assert sum(v for k,v in r['rank_frequencies'] if k==r['rank'])==r['top_rank_classes']
  assert 0<r['normal_frattini_witness_classes']<=r['top_rank_classes']
  assert 0<=r['abelian_witness_classes']<=r['top_rank_classes']
 totals={k:sum(r[k] for r in d['rows']) for k in ['subgroup_classes','subgroups','top_rank_classes','abelian_witness_classes','normal_frattini_witness_classes']}
 assert totals=={'subgroup_classes':619438,'subgroups':1108458,'top_rank_classes':15257,'abelian_witness_classes':5376,'normal_frattini_witness_classes':15128}
 assert sum(not r['abelian_witness_classes'] for r in d['rows'])==1010
 p=read('results/16.45-extension-process.json')
 assert p['actual_returncode']==0 and not p['timed_out'] and p['clean_log'] and p['sentinel']
 for q,h in p['sha256'].items():assert sha(q)==h
 for p in read('results/16.45-extension-controls-process.json')['runs']:
  assert p['actual_returncode']==0 and p['clean_log'] and p['sentinel']
  for q,h in p['sha256'].items():assert sha(q)==h
 obs=read('results/16.45-extension-runner-observations.json')
 assert obs['screen']['actual_outer_returncode']==obs['controls']['actual_outer_returncode']==0
 assert obs['screen']['completion_chunk_id']=='dd4aaa' and obs['controls']['completion_chunk_id']=='cbd907'
 controls=read('results/16.45-extension-controls.json')
 assert json.loads(json.dumps(run()))==controls
 assert [(r['order'],r['id']) for r in controls]==[(81,14),(125,3),(128,133),(128,990),(128,163),(243,19),(343,3),(625,14)]
 assert sum(r['subgroups'] for r in controls)==474
 assert sum(r['associativity_triples'] for r in controls)==307619161
 print('PASS_1645_EXTENSION_PACKET',len(REQUIRED),'hashes; 2435 new groups; 1108458 subgroups; 8 new table controls; general question unresolved')
if __name__=='__main__':audit()
