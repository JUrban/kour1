#!/usr/bin/env python3
"""Audit bounded coverage, all run hashes, and independent table controls."""
import hashlib,json
from pathlib import Path
from check_18_120 import run as pilot_controls
from check_18_120_256 import run as extension_controls
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={
 'research/18.120-plan.md','research/18.120-partial.md','research/18.120-report.md',
 'scripts/screen_18_120.g','scripts/screen_18_120_256.g',
 'scripts/run_18_120.py','scripts/run_18_120_256.py',
 'scripts/export_18_120_controls.g','scripts/export_18_120_256_controls.g',
 'scripts/check_18_120.py','scripts/check_18_120_256.py',
 'scripts/run_18_120_controls.py','scripts/run_18_120_256_controls.py',
 'scripts/explore_18_120_roots.py','scripts/audit_18_120.py',
 'results/18.120-pilot.json','results/18.120-pilot.log','results/18.120-pilot-process.json',
 'results/18.120-256.json','results/18.120-256.log','results/18.120-256-process.json',
 'results/18.120-control-inputs.json','results/18.120-controls.json',
 'results/18.120-controls.log','results/18.120-export.log','results/18.120-controls-process.json',
 'results/18.120-256-control-inputs.json','results/18.120-256-controls.json',
 'results/18.120-256-controls.log','results/18.120-256-export.log','results/18.120-256-controls-process.json',
 'results/18.120-root-partitions.json','results/18.120-runner-observations.json',
 'references/cache/jabara-2005-factorized-p.pdf','references/cache/jabara-2005-factorized-p.txt',
 'references/cache/mccann-2016-class-two-abelian-p3.pdf','references/cache/mccann-2016-class-two-abelian-p3.txt',
}
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def audit():
 m=read('results/18.120-summary.json')
 assert m['status']=='PARTIAL_THEOREM_AND_BOUNDED_SEARCH' and m['candidate_increment']==0
 assert set(m['sha256'])==REQUIRED
 for p,h in m['sha256'].items():assert sha(p)==h,p
 for stem,counts,total,high,eligible in [
 ('pilot',[(32,51),(64,267),(81,15),(125,5),(128,2328),(243,67),(343,5),(625,15),(729,504)],723,42,16),
 ('256',[(256,56092)],27432,361,221)]:
  d=read(f'results/18.120-{stem}.json')
  assert d['orders']==[n for n,c in counts]
  assert d['groups']==len(d['rows'])==sum(c for n,c in counts)
  assert {(r['order'],r['id']) for r in d['rows']}=={(n,i) for n,c in counts for i in range(1,c+1)}
  assert sum(r['class']>4 for r in d['rows'])==high
  assert sum(bool(r['disjoint_factorizations']) for r in d['rows'])==eligible
  assert d['disjoint_factorizations']==sum(r['disjoint_factorizations'] for r in d['rows'])==total and d['flags']==0
  for r in d['rows']:
   assert r['class']>=1 and r['disjoint_factorizations']>=0
   assert (r['class']>4)==(r['subgroup_classes']>0)
   if r['class']<=4:assert r['disjoint_factorizations']==0
  p=read(f'results/18.120-{stem}-process.json')
  assert p['actual_returncode']==0 and not p['timed_out'] and p['clean_log'] and p['sentinel']
  for q,h in p['sha256'].items():assert sha(q)==h,q
 for stem,run,cases,subs,triples,tests,actual in [
 ('',pilot_controls,[(128,134),(128,995),(729,99),(729,100)],1009,779035282,355,435),
 ('256-',extension_controls,[(256,503),(256,6547)],1782,33554432,896,2816)]:
  for p in read(f'results/18.120-{stem}controls-process.json')['runs']:
   assert p['actual_returncode']==0 and p['clean_log'] and p['sentinel']
   for q,h in p['sha256'].items():assert sha(q)==h,q
  d=read(f'results/18.120-{stem}controls.json');assert run()==d
  assert [(r['order'],r['id']) for r in d]==cases
  for key,value in [('subgroups',subs),('associativity_triples',triples),('factorization_representatives',tests),('actual_factorizations',actual)]:
   assert sum(r[key] for r in d)==value
 roots=read('results/18.120-root-partitions.json')
 assert roots['flags']==[] and [(r['n'],r['root_partitions']) for r in roots['counts']]==[(2,2),(3,5),(4,13),(5,25),(6,25)]
 obs=read('results/18.120-runner-observations.json')
 for label,chunk in [('pilot','4547ef'),('extension','648560'),('controls','21a86a'),('extension_controls','131318'),('roots','566994')]:
  assert obs[label]['actual_outer_returncode']==0 and obs[label]['completion_chunk_id']==chunk
 print('PASS_18120_PACKET',len(REQUIRED),'hashes; 59349 groups; 28155 factorizations; six independent table controls; general question unresolved')
if __name__=='__main__':audit()
