#!/usr/bin/env python3
"""Audit vector certificates, finite tables, exceptional maps and prior packets."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from word_vectors_6_47 import verify_certificate, normalized_export
from run_6_47_vectors import CASES
from run_6_47_extension import check
from classify_6_47_tables import classify
from check_6_47_exceptional_iso import verify
from replay_6_47_vectors import run as regression

ROOT = Path(__file__).resolve().parents[1]
read = lambda name: json.loads((ROOT/name).read_text())
packet = read('results/6.47-vector-packet.json')
assert packet['scope'] == 'bounded_coordinate_enumeration'
assert packet['complete_candidate_increment'] == 0
for name, digest in packet['sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
required = set(packet['fixed_files'])
assert required == {
    'docs/21tkt.pdf', 'research/6.47-vector-plan.md', 'research/6.47-vector-report.md',
    'scripts/word_vectors_6_47.py', 'scripts/replay_6_47_vectors.py',
    'scripts/run_6_47_vectors.py', 'scripts/export_6_47_input.g',
    'scripts/audit_6_47_vectors.py', 'scripts/check_6_47_exceptional_iso.py',
    'scripts/run_6_47_extension.py', 'scripts/classify_6_47_tables.py',
    'scripts/audit_6_47_extension.py', 'results/6.47-extension-packet.json',
    'results/6.47-vector-summary.json', 'results/6.47-vector-outer-process.json',
    'results/6.47-vector-regression.json', 'results/6.47-vector-regression.log',
    'results/6.47-vector-regression-process.json',
}
summary = read('results/6.47-vector-summary.json')
assert summary['status'] == 'PASS_647_VECTOR_RUN' and summary['cap'] == 4096
assert [(r['n'],r['id']) for r in summary['cases']] == CASES
outer = read('results/6.47-vector-outer-process.json')
assert outer['actual_returncode'] == 0 and outer['completion_sentinel'] == 'PASS_647_VECTOR_RUN'
assert outer['summary_sha256'] == packet['sha256']['results/6.47-vector-summary.json']
assert outer['numpy_version'] == '2.5.3'
totals = dict(nodes=0, associative=0, triples=0, power_certificates=0)
for record in summary['cases']:
    stem = f"results/6.47-vector-{record['n']}-{record['id']}"
    suffixes = ['.g', '.log', '-process.json', '-input.json', '-certificate.json',
                '-certificate-check.json', '.json', '-controls.json', '-classification.json']
    required.update(stem+s for s in suffixes)
    process = read(stem+'-process.json')
    assert all(record[k] == v for k,v in process.items())
    assert process['actual_gap_returncode'] == 0 and not process['gap_timed_out']
    assert process['gap_sentinel'] and process['clean_gap_log']
    log = (ROOT/(stem+'.log')).read_text()
    assert log.rstrip().endswith('PASS_647_INPUT')
    assert not any(s in log for s in ['Error,', 'Syntax error', 'Syntax warning'])
    assert all(packet['sha256'][p] == d for p,d in process['sha256'].items())
    data, certificate = read(stem+'-input.json'), read(stem+'-certificate.json')
    replay = verify_certificate(data, certificate)
    assert replay == read(stem+'-certificate-check.json') and replay['complete']
    export = normalized_export(data, certificate)
    assert export == read(stem+'.json')
    controls = json.loads(json.dumps(check(export)))
    assert controls == read(stem+'-controls.json')
    classification = classify(export, controls)
    assert classification == read(stem+'-classification.json')
    assert record['derived_nodes'] == replay['nodes']
    assert record['associative_count'] == controls['associative_count']
    assert record['triples'] == controls['checked_triples']
    assert record['all_variety_memberships_certified'] == classification['all_variety_memberships_certified']
    failures = [r['function_index'] for r in classification['operations'] if not r['variety_membership_certified']]
    assert failures == ([1,2] if (record['n'],record['id']) == (64,34) else [])
    totals['nodes'] += replay['nodes']
    totals['associative'] += controls['associative_count']
    totals['triples'] += controls['checked_triples']
    totals['power_certificates'] += sum(bool(r['power_map_isomorphisms']) for r in classification['operations'])
assert totals == dict(nodes=3296, associative=80, triples=856686592, power_certificates=78)
stem = 'results/6.47-vector-64-34-isomorphism'
required.update(stem+s for s in ['.g','.log','.json','-process.json','-check.json'])
process = read(stem+'-process.json')
assert process['actual_gap_returncode'] == 0 and process['clean_log'] and process['sentinel']
assert all(packet['sha256'][p] == d for p,d in process['sha256'].items())
log = (ROOT/(stem+'.log')).read_text()
assert log.rstrip().endswith('PASS_647_EXCEPTIONAL_GAP')
assert not any(s in log for s in ['Error,','Syntax error','Syntax warning'])
assert verify(read('results/6.47-vector-64-34.json'),
              read('results/6.47-vector-64-34-controls.json'), read(stem+'.json')) == read(stem+'-check.json')
assert regression() == read('results/6.47-vector-regression.json')
process = read('results/6.47-vector-regression-process.json')
assert process['actual_returncode'] == 0
assert all(packet['sha256'][p] == d for p,d in process['sha256'].items())
assert (ROOT/'results/6.47-vector-regression.log').read_text() == ''
assert set(packet['sha256']) == required
prior = subprocess.run([sys.executable, 'scripts/audit_6_47_extension.py'],
                       cwd=ROOT, capture_output=True, text=True, timeout=60)
assert prior.returncode == 0 and not prior.stderr
assert 'PASS_647_EXTENSION_PACKET' in prior.stdout
print(prior.stdout.strip())
print(f'PASS_647_VECTOR_PACKET {len(required)} hashes; 12 new cases; 3296 functions; '
      '856686592 triples; all 80 associative outputs isomorphic to their original groups; no general solution')
