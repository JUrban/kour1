#!/usr/bin/env python3
"""Stronger three-variable targets for a possible rank-two proof."""
import hashlib
import json
import math
from pathlib import Path


def run():
    for label in ['a2', 'b2', 'g2']:
        source = Path('results/19.62-' + label + '-monomial-input.json')
        original = json.loads(source.read_text())
        roots = original['roots']
        cases = {}
        for r, s, k, i, j, c in original['rules']:
            p = roots.index([-v for v in roots[k]])
            key = p, tuple(sorted([(p, 2), (r, i), (s, j)]))
            cases[key] = math.gcd(cases.get(key, 0), c)
        result = dict(type=label, roots=roots, rules=original['rules'],
                      cases=[dict(root=p, variables=v, coefficient=c)
                             for (p, v), c in sorted(cases.items())],
                      source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        path = Path('results/19.62-' + label + '-rank-two-input.json')
        assert not path.exists()
        path.write_text(json.dumps(result, indent=2) + '\n')
        with path.with_suffix('.txt').open('w') as out:
            out.write(str(len(roots)) + ' ' + str(len(result['rules'])) + '\n')
            for row in result['rules']:
                out.write(' '.join(map(str, row)) + '\n')
            out.write(str(len(result['cases'])) + '\n')
            for case in result['cases']:
                row = [case['root'], case['coefficient'], len(case['variables'])]
                row += [v for item in case['variables'] for v in item]
                out.write(' '.join(map(str, row)) + '\n')
        print('PREPARED_1962_RANK_TWO', label, len(result['cases']), flush=True)


if __name__ == '__main__':
    run()
