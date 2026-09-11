#!/usr/bin/env python3
"""Export bounded word-function cosets; independently check their operations."""
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software/coset-python'))
import numpy as np

CASES = ([(16, i) for i in [7, 8, 9]] + [(27, i) for i in [3, 4]]
         + [(32, i) for i in [6, 7, 8, 9, 10, 11, 13, 14, 15, 18, 19, 20,
                                  39, 40, 41, 42, 43, 44]]
         + [(64, i) for i in [4, 5, 6, 7, 8, 32, 34, 52, 53, 54]])
CAP = 4096
TIMEOUT = 180


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(data):
    n = data['n']
    old = np.asarray(data['table'], dtype=np.int64) - 1
    unit = data['identity'] - 1
    inv = np.asarray(data['inverse']) - 1
    oi = np.asarray(data['orbit_index']) - 1
    transporters = np.asarray(data['transporters']) - 1
    reps = np.asarray(data['representatives']) - 1
    assert old.shape == (n, n)
    assert np.array_equal(old[unit], np.arange(n))
    assert np.array_equal(old[:, unit], np.arange(n))
    # Check every stored transporter is an automorphism of the original table
    # and sends its representative to its designated ordered pair.
    for index, perm in enumerate(transporters):
        assert sorted(perm.tolist()) == list(range(n))
        assert np.array_equal(perm[old], old[perm[:, None], perm])
        assert tuple(perm[reps[oi[index]]]) == divmod(index, n)
    funcs = np.asarray(data['word_functions']) - 1
    assert funcs.shape == (data['normalized_count'], data['pair_orbits'])
    assert len({tuple(v) for v in funcs}) == data['normalized_count']
    assert data['function_group_order'] == len(funcs) * data['exponent'] ** 2
    associative = []
    first_bad = None
    found_original = False
    found_opposite = False
    for index, coord in enumerate(funcs):
        op = transporters[np.arange(n*n), coord[oi]].reshape(n, n)
        assert np.array_equal(op[unit], np.arange(n))
        assert np.array_equal(op[:, unit], np.arange(n))
        assert np.all(op[np.arange(n), inv] == unit)
        assert np.all(op[inv, np.arange(n)] == unit)
        # Every power, including intermediate powers, agrees before any
        # associativity assumption. This follows from exponent sums.
        powers_old = np.full(n, unit)
        powers_new = np.full(n, unit)
        for _ in range(data['exponent']):
            powers_old = old[powers_old, np.arange(n)]
            powers_new = op[powers_new, np.arange(n)]
            assert np.array_equal(powers_old, powers_new)
        left = op[op[:, :, None], np.arange(n)[None, None, :]]
        right = op[np.arange(n)[:, None, None], op[None, :, :]]
        if np.array_equal(left, right):
            associative.append({'function_index': index, 'table': (op+1).tolist()})
            found_original |= np.array_equal(op, old)
            found_opposite |= np.array_equal(op, old.T)
        elif first_bad is None:
            triple = tuple(int(i) for i in np.argwhere(left != right)[0])
            a, b, c = triple
            first_bad = {'function_index': index, 'triple_zero_based': triple,
                         'left': int(op[op[a,b],c])+1,
                         'right': int(op[a,op[b,c]])+1}
    assert found_original and found_opposite
    return {'status': 'PASS', 'normalized_operations': len(funcs),
            'associative_count': len(associative),
            'checked_triples': len(funcs)*n**3,
            'transporter_checks': n*n,
            'original_and_opposite_present': True,
            'first_nonassociative_witness': first_bad,
            'associative_operations': associative}


def main():
    records = []
    for n, ident in CASES:
        stem = ROOT / f'results/6.47-extension-{n}-{ident}'
        script = stem.with_suffix(stem.suffix + '.g')
        output = stem.with_suffix(stem.suffix + '.json')
        log = stem.with_suffix(stem.suffix + '.log')
        process = stem.with_suffix(stem.suffix + '-process.json')
        controls = stem.with_suffix(stem.suffix + '-controls.json')
        script.write_text('Read("scripts/export_6_47.g");;\n'
                          f'Run647({n},{ident},{CAP},"{output.relative_to(ROOT)}");;\n'
                          'QUIT_GAP(0);\n')
        start = time.monotonic()
        timed_out = False
        with log.open('w') as stream:
            proc = subprocess.Popen(['bin/gap', str(script.relative_to(ROOT))],
                                    cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
            try:
                rc = proc.wait(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                timed_out = True
                proc.kill()
                rc = proc.wait()
        content = log.read_text()
        clean = not any(s in content for s in ['Error,', 'Syntax error', 'Syntax warning'])
        sentinel = (content.rstrip().endswith('PASS_647_EXPORT') or
                    content.rstrip().endswith('PASS_647_EXPORT_SKIPPED'))
        record = {'n': n, 'id': ident, 'actual_returncode': rc,
                  'timed_out': timed_out, 'timeout_seconds': TIMEOUT,
                  'elapsed_seconds': time.monotonic()-start,
                  'clean_log': clean, 'sentinel': sentinel,
                  'observed_utc': datetime.now(timezone.utc).isoformat(),
                  'sha256': {str(p.relative_to(ROOT)): digest(p)
                             for p in [script, log, ROOT/'scripts/export_6_47.g']}}
        process.write_text(json.dumps(record, indent=2)+'\n')
        if timed_out:
            record['status'] = 'TIMEOUT'
        else:
            assert rc == 0 and clean and sentinel, record
            data = json.loads(output.read_text())
            record['status'] = data['status']
            if data['status'] == 'EXPORTED':
                result = check(data)
                controls.write_text(json.dumps(result, indent=2)+'\n')
                record['associative_count'] = result['associative_count']
                record['normalized_count'] = result['normalized_operations']
        records.append(record)
        print(json.dumps({k: v for k, v in record.items() if k != 'sha256'}), flush=True)
    summary = {'status': 'PASS_BOUNDED_EXTENSION', 'cap': CAP, 'cases': records,
               'scope': 'Associativity and elementary controls only; no variety nonmembership claimed.'}
    (ROOT/'results/6.47-extension-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print('PASS_647_EXTENSION', flush=True)


if __name__ == '__main__':
    main()
