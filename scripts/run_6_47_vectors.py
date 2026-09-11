#!/usr/bin/env python3
"""Revisit twelve timed-out cases using direct vector normal-closure orbits."""
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from word_vectors_6_47 import enumerate_derived, verify_certificate, normalized_export
from run_6_47_extension import check
from classify_6_47_tables import classify

ROOT = Path(__file__).resolve().parents[1]
CASES = [(32, 9), (32, 11)] + [(64, i) for i in [4,5,6,7,8,32,34,52,53,54]]
CAP = 4096


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records = []
    for n, ident in CASES:
        stem = f'results/6.47-vector-{n}-{ident}'
        path = lambda suffix: ROOT/(stem+suffix)
        path('.g').write_text('Read("scripts/export_6_47_input.g");;\n'
                             f'Run647Input({n},{ident},"{stem}-input.json");;\n'
                             'QUIT_GAP(0);\n')
        start = time.monotonic()
        timed_out = False
        with path('.log').open('w') as stream:
            proc = subprocess.Popen(['bin/gap', stem+'.g'], cwd=ROOT,
                                    stdout=stream, stderr=subprocess.STDOUT)
            try:
                rc = proc.wait(timeout=180)
            except subprocess.TimeoutExpired:
                timed_out = True
                proc.kill()
                rc = proc.wait()
        log = path('.log').read_text()
        record = {'n': n, 'id': ident, 'actual_gap_returncode': rc,
                  'gap_timed_out': timed_out, 'gap_timeout_seconds': 180,
                  'gap_elapsed_seconds': time.monotonic()-start,
                  'clean_gap_log': not any(s in log for s in
                                          ['Error,', 'Syntax error', 'Syntax warning']),
                  'gap_sentinel': log.rstrip().endswith('PASS_647_INPUT'),
                  'observed_utc': datetime.now(timezone.utc).isoformat(),
                  'sha256': {str(p.relative_to(ROOT)): digest(p) for p in
                             [path('.g'), path('.log'), ROOT/'scripts/export_6_47_input.g']}}
        path('-process.json').write_text(json.dumps(record, indent=2)+'\n')
        if timed_out:
            record['status'] = 'INPUT_TIMEOUT'
            records.append(record)
            print(json.dumps(record), flush=True)
            continue
        assert rc == 0 and record['clean_gap_log'] and record['gap_sentinel'], record
        data = json.loads(path('-input.json').read_text())
        start = time.monotonic()
        certificate = enumerate_derived(data, cap=CAP)
        path('-certificate.json').write_text(json.dumps(certificate, indent=2)+'\n')
        verification = verify_certificate(data, certificate)
        path('-certificate-check.json').write_text(json.dumps(verification, indent=2)+'\n')
        record.update(status=certificate['status'], derived_nodes=certificate['node_count'],
                      nilpotency_class=data['nilpotency_class'],
                      vector_elapsed_seconds=time.monotonic()-start)
        if certificate['status'] == 'COMPLETE':
            export = normalized_export(data, certificate)
            path('.json').write_text(json.dumps(export, indent=2)+'\n')
            controls = check(export)
            path('-controls.json').write_text(json.dumps(controls, indent=2)+'\n')
            classification = classify(export, controls)
            path('-classification.json').write_text(json.dumps(classification, indent=2)+'\n')
            record.update(associative_count=controls['associative_count'],
                          triples=controls['checked_triples'],
                          all_variety_memberships_certified=
                          classification['all_variety_memberships_certified'])
        records.append(record)
        print(json.dumps({k:v for k,v in record.items() if k != 'sha256'}), flush=True)
    summary = {'status': 'PASS_647_VECTOR_RUN', 'cap': CAP, 'cases': records,
               'scope': 'Completed normal closures only; cap and input-timeout omissions retained.'}
    (ROOT/'results/6.47-vector-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print('PASS_647_VECTOR_RUN', flush=True)


if __name__ == '__main__':
    main()
