#!/usr/bin/env python3
"""Closed proof-packet hash audit and exact mathematical replay."""
from pathlib import Path
import json,hashlib
from check_14_26_polynomial import run as polynomial_run
from check_14_26_wreath import run as wreath_run
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={
 'docs/21tkt.pdf',
 'research/14.26-polynomial-plan.md','research/14.26-polynomial-draft.md',
 'research/14.26-proof.md','research/14.26-sources.md',
 'research/14.26-review.md','research/14.26-report.md',
 'scripts/check_14_26_polynomial.py','scripts/check_14_26_wreath.py',
 'scripts/run_14_26_controls.py','scripts/audit_14_26.py',
 'results/14.26-polynomial-controls.json','results/14.26-polynomial-controls.log',
 'results/14.26-wreath-controls.json','results/14.26-wreath-controls.log',
 'results/14.26-controls-process.json','results/14.26-runner-observation.json',
 'references/cache/jennings-1955-group-ring.pdf','references/cache/jennings-1955-group-ring.txt',
 'references/cache/jennings-1955-p182.png','references/cache/notebook-14.26-p75.png',
 'references/cache/gul-weiss-unitriangular.pdf','references/cache/gul-weiss-unitriangular.txt',
}
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def clean(v):
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items() if k!='elapsed_seconds'}
 if isinstance(v,list):return [clean(x) for x in v]
 return v

def audit():
 summary=json.loads((ROOT/'results/14.26-summary.json').read_text())
 assert summary['problem']=='14.26' and summary['candidate_number']==37
 assert summary['status']=='COMPLETE_AFFIRMATIVE_CANDIDATE'
 assert summary['novelty']=='pending' and summary['outside_reviews']==0
 assert set(summary['sha256'])==REQUIRED and len(REQUIRED)==23
 for p,h in summary['sha256'].items():assert sha(p)==h,p
 process=json.loads((ROOT/'results/14.26-controls-process.json').read_text())
 assert [r['label'] for r in process['runs']]==['polynomial','wreath']
 for r in process['runs']:
  assert r['returncode']==0
  for p,h in r['sha256'].items():assert sha(p)==h,p
  log=(ROOT/r['log']).read_text()
  assert log.splitlines()[-1]==r['sentinel'] and 'Traceback' not in log
 obs=json.loads((ROOT/'results/14.26-runner-observation.json').read_text())
 assert obs['actual_tool_exit_code']==0 and obs['completion_chunk_id']=='6c9036'
 assert obs['process_sha256']==sha('results/14.26-controls-process.json')
 poly=json.loads((ROOT/'results/14.26-polynomial-controls.json').read_text())
 assert poly['status']=='PASS'
 expected=[(1,2,[-1,0,1]),(2,1,[0,1]),(2,2,[-1,0,1]),(3,1,[0,1])]
 assert [(r['c'],r['R'],r['I']) for r in poly['cases']]==expected
 for args,r in zip(expected,poly['cases']):assert clean(polynomial_run(*args))==clean(r)
 assert [r['quotient_dimension'] for r in poly['cases']]==[4,8,14,21]
 wreath=json.loads((ROOT/'results/14.26-wreath-controls.json').read_text())
 assert clean(wreath_run())==clean(wreath)
 assert wreath['elements']==37 and wreath['multiplication_relations']==319 and wreath['separated_pairs']==666
 print(json.dumps({'status':'PASS','problem':'14.26','candidate_number':37,'hashed_files':len(REQUIRED),'polynomial_cases':4,'wreath_relations':319,'wreath_separations':666}))
 print('PASS_14_26_AUDIT')
if __name__=='__main__':audit()
