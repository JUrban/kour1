#!/usr/bin/env python3
"""Bind the finite derived screen to completed root-closure packets and replay it."""
import hashlib
import json
from pathlib import Path
import screen_19_62_derived as screen


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    packet=json.loads(Path('results/19.62-derived-packet.json').read_text())
    for p,h in packet['sha256'].items():assert sha(p)==h,p
    for tag in ['19.61','19.61-g2','19.61-g2-rings','19.61-g2f9']:
        previous=json.loads(Path('results/'+tag+'-summary.json').read_text())
        for p,h in previous['sha256'].items():assert sha(p)==h,p
        observation=json.loads(Path('results/'+tag+'-audit-observation.json').read_text())
        if tag=='19.61':
            assert observation['corrected_exit_code']==0 and observation['initial_exit_code']==1
            for p,h in observation['sha256'].items():assert sha(p)==h,p
        else:
            assert observation['exit_code']==0
            assert observation['summary_sha256']==sha('results/'+tag+'-summary.json')
            assert observation['audit_log_sha256']==sha('results/'+tag+'-audit.log')
    result=screen.run();expected=json.loads(Path('results/19.62-derived-screen.json').read_text())
    assert json.loads(json.dumps(result))==expected
    assert sum(r['carpets'] for r in result['rings'])==193805
    assert sum(r['distinct_derived'] for r in result['rings'])==6999
    assert all(r['hits']==r['square_failures']==[] for r in result['rings'])
    print('PASS_1962_DERIVED_PACKET',len(packet['sha256']),'carpets=193805 derived=6999',flush=True)


if __name__=='__main__':run()
