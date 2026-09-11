#!/usr/bin/env python3
"""Verify the frozen proof packet and replay exact model controls."""
import hashlib
import json
from pathlib import Path
from check_13_42 import run

ROOT=Path(__file__).resolve().parents[1]
REQUIRED={
    'docs/21tkt.pdf',
    'research/13.42-plan.md','research/13.42-proof.md',
    'research/13.42-review.md','research/13.42-report.md',
    'scripts/model_13_42.py','scripts/check_13_42.py','scripts/audit_13_42.py',
    'results/13.42-controls.json','results/13.42-controls.log',
    'results/13.42-controls-process.json','results/13.42-runner-observation.json',
    'references/cache/myasnikov-remeslennikov-exponential-groups-2.pdf',
    'references/cache/myasnikov-remeslennikov-exponential-groups-2.txt',
    'references/cache/myasnikov-remeslennikov-exponential-groups-2-p1.png',
    'references/cache/myasnikov-remeslennikov-exponential-groups-2-p3.png',
    'references/cache/notebook-13.42-p69.png',
}


def audit():
    summary=json.loads((ROOT/'results/13.42-summary.json').read_text())
    assert summary['problem']=='13.42' and summary['candidate_number']==36
    assert summary['status']=='COMPLETE_AFFIRMATIVE_CANDIDATE'
    assert summary['novelty']=='pending' and summary['outside_reviews']==0
    assert set(summary['sha256'])==REQUIRED
    for name,digest in summary['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    data=json.loads((ROOT/'results/13.42-controls.json').read_text())
    assert run()==data
    assert data['symbolic']=={'generic_coordinates':10,'truncated_words':15,
        'nonzero_product_coefficients':81,'product_difference_zero':True,
        'commuting_criterion':True,'inverse':True,'conjugacy_coordinates':True}
    assert data['points']==75 and data['polynomials']==10
    assert data['checks']=={'inverse':75,'associativity':75,
        'f_power_compatibility':1875,'conjugation':750,'addition':7500,
        'multiplication':7500,'commuting_products':5250,'commuting_pairs':525}
    assert len(data['witnesses'])==64 and data['source_class_three']
    process=json.loads((ROOT/'results/13.42-controls-process.json').read_text())
    assert process['actual_returncode']==0
    for name,digest in process['sha256'].items():assert summary['sha256'][name]==digest
    log=(ROOT/'results/13.42-controls.log').read_text()
    assert log.startswith('PASS_1342_CONTROLS ') and 'Traceback' not in log
    assert json.loads(log.removeprefix('PASS_1342_CONTROLS '))=={k:v for k,v in data.items() if k!='witnesses'}
    outer=json.loads((ROOT/'results/13.42-runner-observation.json').read_text())
    assert outer['actual_outer_returncode']==0
    print('PASS_1342_PACKET',len(REQUIRED),'hashes; generic 10-variable algebra check; '
          '75 model elements; 525 commuting pairs; 64 nonzero commutators; '
          'priority and outside review pending')


if __name__=='__main__':audit()
