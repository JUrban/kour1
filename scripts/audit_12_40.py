#!/usr/bin/env python3
"""Audit the complete frozen packet and replay the independent integer checks."""
import hashlib
import json
from math import gcd, prod
from pathlib import Path

from check_12_40 import run as arithmetic
from analyze_12_40_tables import run as tables

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    'docs/21tkt.pdf','bin/gap',
    'research/12.40-plan.md','research/12.40-proof.md',
    'research/12.40-review.md','research/12.40-report.md',
    'scripts/check_12_40.py','scripts/analyze_12_40_tables.py',
    'scripts/analyze_12_40_tables_initial.py','scripts/check_12_40_modules.g',
    'scripts/run_12_40_modules.py','scripts/run_12_40_screen.py',
    'scripts/screen_12_40.g','scripts/audit_12_40.py',
    'results/12.40-arithmetic.json','results/12.40-arithmetic.log',
    'results/12.40-arithmetic-process.json','results/12.40-table-degrees.txt',
    'results/12.40-table-catalog.json','results/12.40-table-screen.log',
    'results/12.40-table-screen-process.json','results/12.40-table-analysis.json',
    'results/12.40-table-analysis.log','results/12.40-table-analysis-process.json',
    'results/12.40-table-analysis-initial.log',
    'results/12.40-table-analysis-initial-process.json',
    'results/12.40-modules.json','results/12.40-modules.log',
    'results/12.40-modules-process.json','results/12.40-gap-environment.json',
    'results/12.40-gap-environment-decoded.json','results/12.40-runner-observations.json',
    'references/cache/bray-2-dimensional-cohomology-2007.pdf',
    'references/cache/bray-2-dimensional-cohomology-2007.txt',
    'references/cache/bray-2-dimensional-cohomology-2007-p2.png',
    'references/cache/bray-2-dimensional-cohomology-2007-p3.png',
    'references/cache/notebook-12.40-p60.png',
}


def read(name):
    return json.loads((ROOT/name).read_text())


def audit():
    summary = read('results/12.40-summary.json')
    assert summary['candidate_number'] == 35
    assert summary['status'] == 'COMPLETE_NEGATIVE_CANDIDATE'
    assert summary['novelty'] == 'pending' and summary['outside_reviews'] == 0
    assert set(summary['sha256']) == REQUIRED
    for name,digest in summary['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,name
    a = arithmetic()
    assert a == read('results/12.40-arithmetic.json')
    assert len(a['lifts']) == 510 and len(a['exact_integer_cases']) == 8
    assert sum(x['root_candidates'] for x in a['exhaustive']) == 16383
    assert sum(x['exponent_candidates'] for x in a['exhaustive']) == 32766
    t = tables()
    assert t == read('results/12.40-table-analysis.json')
    assert (t['table_names'],t['available_tables'],t['missing_tables'],t['degrees_checked']) == (2750,7573,2277,352440)
    assert len(t['excess']) == 21
    assert sum(len(e['degrees']) for e in t['excess']) == 32
    for stem in ('arithmetic','table-analysis','table-screen','modules'):
        process = read('results/12.40-'+stem+'-process.json')
        assert process['actual_returncode'] == 0
        for name,digest in process['sha256'].items():
            assert summary['sha256'][name] == digest
        log = (ROOT/('results/12.40-'+stem+'.log')).read_text()
        assert not any(s in log for s in ('Traceback','Error,','Syntax error','Syntax warning'))
        if stem in ('table-screen','modules'):
            assert process['clean_log'] and process['sentinel']
            sentinel = 'PASS_1240_TABLE_SCREEN' if stem == 'table-screen' else 'PASS_1240_MODULES'
            assert log.rstrip().endswith(sentinel)
        else:
            assert log.startswith('PASS_1240_')
    assert not read('results/12.40-modules-process.json')['timed_out']
    failed = read('results/12.40-table-analysis-initial-process.json')
    assert failed['actual_returncode'] == 1 and 'Reconstructed' in failed['record_provenance']
    for original,archived in {
        'scripts/analyze_12_40_tables.py':'scripts/analyze_12_40_tables_initial.py',
        'results/12.40-table-analysis.log':'results/12.40-table-analysis-initial.log',
    }.items():
        assert failed['sha256'][original] == summary['sha256'][archived]
    assert "{'Alt(2)'}" in (ROOT/'results/12.40-table-analysis-initial.log').read_text()
    modules = read('results/12.40-modules.json')
    assert [(m['n'],m['q']) for m in modules] == [(4,3),(4,5),(6,3)]
    for m in modules:
        n,q = m['n'],m['q']
        assert m['projective_degree'] == (q**n-1)//(q-1)
        assert m['order'] == prod(q**n-q**i for i in range(n))//((q-1)*gcd(n,q-1))
        assert m['composition_dimensions'] == [1,1,m['projective_degree']-2]
        assert m['all_absolutely_irreducible'] is True
    raw = (ROOT/'results/12.40-gap-environment.json').read_text()
    env = json.loads(raw.replace('\\\n',''))
    assert env == read('results/12.40-gap-environment-decoded.json')['environment']
    assert env == {'gap_version':'4.16.1','ctbllib_version':'1.3.11','workspace_gib':4,'seed':1240}
    observations = read('results/12.40-runner-observations.json')
    assert [x['actual_outer_returncode'] for x in observations] == [0,0,1,0,0]
    assert [x['label'] for x in observations] == ['arithmetic','table-screen','table-analysis-initial','table-analysis','modules']
    print('PASS_1240_PACKET',len(REQUIRED),'hashes; 510 lifts; 8 exact integer cases; '
          '3 GAP modules; 352,440 table degrees; initial audit failure retained; '
          'priority and outside review pending')


if __name__ == '__main__':
    audit()
