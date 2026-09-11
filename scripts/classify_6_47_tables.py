#!/usr/bin/env python3
"""Check explicit power-map isomorphisms on completed 6.47 table exports."""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software/coset-python'))
import numpy as np


def classify(data, controls):
    n, exponent = data['n'], data['exponent']
    old = np.asarray(data['table'], dtype=np.int64) - 1
    unit = data['identity'] - 1
    powers = [np.full(n, unit)]
    for _ in range(exponent):
        powers.append(old[powers[-1], np.arange(n)])
    assert np.array_equal(powers[-1], powers[0])
    records = []
    for item in controls['associative_operations']:
        op = np.asarray(item['table'], dtype=np.int64) - 1
        matches = []
        for k in range(1, exponent):
            if math.gcd(k, exponent) != 1:
                continue
            perm = powers[k]
            assert sorted(perm.tolist()) == list(range(n))
            if np.array_equal(perm[op], old[perm[:, None], perm]):
                matches.append(k)
        abelian = np.array_equal(op, op.T)
        records.append({
            'function_index': item['function_index'],
            'power_map_isomorphisms': matches,
            'abelian': bool(abelian),
            'variety_membership_certified': bool(matches or abelian),
            'certificate': ('explicit_power_map_isomorphism' if matches else
                            'abelian_with_same_exponent' if abelian else
                            'UNRESOLVED'),
        })
    return {'n': n, 'id': data['id'], 'operations': records,
            'all_variety_memberships_certified': all(
                r['variety_membership_certified'] for r in records)}


def main():
    records = []
    for name in sys.argv[1:]:
        source = ROOT / name
        controls = json.loads(source.read_text())
        data = json.loads(source.with_name(
            source.name.replace('-controls.json', '.json')).read_text())
        result = classify(data, controls)
        result['controls_file'] = str(source.relative_to(ROOT))
        records.append(result)
    print(json.dumps({'status': 'PASS_EXPLICIT_CERTIFICATE_CHECKS',
                      'cases': records}, indent=2))


if __name__ == '__main__':
    main()
