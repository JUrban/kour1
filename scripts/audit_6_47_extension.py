#!/usr/bin/env python3
"""Replay completed extension cases while retaining every timeout as incomplete."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from run_6_47_extension import CASES, check
from classify_6_47_tables import classify

ROOT = Path(__file__).resolve().parents[1]
packet = json.loads((ROOT/'results/6.47-extension-packet.json').read_text())
assert packet['scope'] == 'bounded_extension_with_explicit_variety_certificates'
assert packet['complete_candidate_increment'] == 0
for name, digest in packet['sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
summary = json.loads((ROOT/'results/6.47-extension-summary.json').read_text())
assert summary['status'] == 'PASS_BOUNDED_EXTENSION' and summary['cap'] == 4096
assert len(CASES) == 33
assert [(r['n'], r['id']) for r in summary['cases']] == CASES
outer = json.loads((ROOT/'results/6.47-extension-outer-process.json').read_text())
assert outer['actual_returncode'] == 0
assert outer['completion_sentinel'] == 'PASS_647_EXTENSION'
assert outer['summary_sha256'] == packet['sha256']['results/6.47-extension-summary.json']
assert outer['numpy_version'] == '2.5.3'

complete = timeouts = operations = associative = triples = 0
classifications = []
required = {
    'docs/21tkt.pdf', 'research/6.47-extension-report.md',
    'scripts/run_6_47_extension.py', 'scripts/export_6_47.g',
    'scripts/classify_6_47_tables.py', 'scripts/audit_6_47_extension.py',
    'scripts/audit_6_47_pilot.py', 'results/6.47-pilot-packet.json',
    'results/6.47-extension-summary.json', 'results/6.47-extension-outer-process.json',
    'results/6.47-extension-classification.json',
    'results/6.47-extension-classification-process.json',
    'results/6.47-class-catalog.g', 'results/6.47-class-catalog.log',
    'results/6.47-class-catalog-process.json',
    'results/6.47-first-table-classification.json',
    'results/6.47-second-table-classification.json',
}
for record in summary['cases']:
    stem = f"results/6.47-extension-{record['n']}-{record['id']}"
    path = lambda suffix: ROOT/(stem+suffix)
    required.update(stem+s for s in ['.g', '.log', '-process.json'])
    process = json.loads(path('-process.json').read_text())
    for key, value in process.items():
        assert record[key] == value, (stem, key)
    for name, digest in process['sha256'].items():
        assert packet['sha256'][name] == digest
    content = path('.log').read_text()
    assert not any(s in content for s in ['Error,', 'Syntax error', 'Syntax warning'])
    assert process['clean_log']
    if record['status'] == 'TIMEOUT':
        assert process['timed_out'] and process['actual_returncode'] == -9
        assert process['timeout_seconds'] == 180
        assert not process['sentinel']
        assert not path('.json').exists() and not path('-controls.json').exists()
        timeouts += 1
        continue
    assert record['status'] == 'EXPORTED'
    assert process['actual_returncode'] == 0 and not process['timed_out']
    assert process['sentinel'] and content.rstrip().endswith('PASS_647_EXPORT')
    required.update(stem+s for s in ['.json', '-controls.json'])
    data = json.loads(path('.json').read_text())
    controls = json.loads(path('-controls.json').read_text())
    assert json.loads(json.dumps(check(data))) == controls
    result = classify(data, controls)
    assert result['all_variety_memberships_certified']
    result['controls_file'] = stem+'-controls.json'
    classifications.append(result)
    complete += 1
    operations += controls['normalized_operations']
    associative += controls['associative_count']
    triples += controls['checked_triples']

stored = json.loads((ROOT/'results/6.47-extension-classification.json').read_text())
assert stored == {'status': 'PASS_EXPLICIT_CERTIFICATE_CHECKS', 'cases': classifications}
classification_process = json.loads(
    (ROOT/'results/6.47-extension-classification-process.json').read_text())
assert classification_process['actual_returncode'] == 0
assert classification_process['stderr'] == ''
assert classification_process['output_sha256'] == packet['sha256'][
    'results/6.47-extension-classification.json']
catalog = json.loads((ROOT/'results/6.47-class-catalog-process.json').read_text())
assert catalog['actual_returncode'] == 0
catalog_log = (ROOT/'results/6.47-class-catalog.log').read_text()
assert catalog_log.rstrip().endswith('PASS_647_CATALOG')
assert not any(s in catalog_log for s in ['Error,', 'Syntax error', 'Syntax warning'])
assert set(packet['sha256']) == required
assert (complete, timeouts, operations, associative, triples) == (21,12,622,88,18926930)

for name in ['first', 'second']:
    diagnostic = json.loads((ROOT/f'results/6.47-{name}-table-classification.json').read_text())
    assert diagnostic['status'] == 'PASS_EXPLICIT_CERTIFICATE_CHECKS'
    for row in diagnostic['cases']:
        control_path = ROOT/row['controls_file']
        data_path = control_path.with_name(
            control_path.name.replace('-controls.json', '.json'))
        checked = classify(json.loads(data_path.read_text()),
                           json.loads(control_path.read_text()))
        checked['controls_file'] = row['controls_file']
        assert checked == row

pilot = subprocess.run([sys.executable, 'scripts/audit_6_47_pilot.py'],
                       cwd=ROOT, capture_output=True, text=True, timeout=60)
assert pilot.returncode == 0 and not pilot.stderr
assert pilot.stdout.startswith('PASS_647_PILOT_PACKET ')
print(pilot.stdout.strip())
print(f"PASS_647_EXTENSION_PACKET {len(required)} hashes; 21 complete cases; "
      '12 timeouts; 622 operations; 18,926,930 triples; '
      'all 88 associative outputs certified in var(G); no general solution')
