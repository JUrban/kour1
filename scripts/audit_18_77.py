#!/usr/bin/env python3
"""Hash audit and exact replay of the 18.77 partial-result controls."""
import json,hashlib
from pathlib import Path
from check_18_77 import run as first
from check_18_77_simultaneous import run as simultaneous
from check_18_77_valuation import run as valuation
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={
 'research/18.77-plan.md','research/18.77-partial-proof.md','research/18.77-simultaneous.md','research/18.77-sources.md','research/18.77-report.md',
 'scripts/check_18_77.py','scripts/run_18_77.py','scripts/check_18_77_simultaneous.py','scripts/run_18_77_simultaneous.py','scripts/check_18_77_valuation.py','scripts/audit_18_77.py',
 'results/18.77-controls.json','results/18.77-controls.log','results/18.77-process.json',
 'results/18.77-simultaneous-controls.json','results/18.77-simultaneous-controls.log','results/18.77-simultaneous-process.json','results/18.77-valuation-controls.json','results/18.77-runner-observations.json',
 'references/cache/passman-character-problems.pdf','references/cache/passman-character-problems.txt',
 'references/cache/isaacs-passman-1968-char-degrees-II.pdf','references/cache/isaacs-passman-1968-char-degrees-II.txt',
 'references/cache/isaacs-passman-1968-section1-07.png','references/cache/isaacs-passman-1968-section1-08.png',
 'references/cache/boyarchenko-sabitova-orbit.pdf','references/cache/boyarchenko-sabitova-orbit.txt','references/cache/boyarchenko-sabitova-orbit-p12.png',
 'references/cache/obrien-voll-characters.pdf','references/cache/obrien-voll-characters.txt','references/cache/obrien-voll-characters-p7.png','references/cache/notebook-18.77-p126.png',
}
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def audit():
 m=read('results/18.77-summary.json');assert m['status']=='PARTIAL_SMALL_CLASS_AND_PRIOR_CLASS_TWO' and m['candidate_increment']==0
 assert set(m['sha256'])==REQUIRED
 for p,h in m['sha256'].items():assert sha(p)==h,p
 for p in ['results/18.77-process.json','results/18.77-simultaneous-process.json']:
  d=read(p);assert d['actual_returncode']==0 and d['clean_log'] and d['sentinel']
  for q,h in d['sha256'].items():assert sha(q)==h,q
 d=first();assert d==read('results/18.77-controls.json')
 assert len(d['random_pencils'])==63 and sum(r['max_e']<r['p'] for r in d['random_pencils'])==46
 assert sum(r['parameters'] for r in d['random_pencils']+d['sharp_threshold'])+d['ut5_f5']['parameters']==22063
 assert sum(r['independent_images'] for r in d['random_pencils']+d['sharp_threshold'])==476
 assert d['ut5_f5']['max_e']==4 and d['ut5_f5']['maximum_parameters']==10000 and d['ut5_f5']['span_mod_p']==6
 s=simultaneous();assert s==read('results/18.77-simultaneous-controls.json')
 assert len(s)==32 and sum(r['parameter_values'] for r in s)==5772 and sum(r['forbidden_hyperplane_sets'] for r in s)==578
 assert valuation()==read('results/18.77-valuation-controls.json')
 o=read('results/18.77-runner-observations.json')
 for label,chunk in [('first','0dc2e5'),('simultaneous','2f2e30'),('valuation','4fd607')]:assert o[label]['actual_outer_returncode']==0 and o[label]['completion_chunk_id']==chunk
 print('PASS_1877_PACKET',len(REQUIRED),'hashes; all exact controls replayed; general question unresolved; class-two result prior')
if __name__=='__main__':audit()
