#!/usr/bin/env python3
"""Exploratory targets for adjoining an opposite-root square term."""
import hashlib
import json
import math
from pathlib import Path


def run():
    for label in ['a2', 'b2', 'g2']:
        source = Path('results/19.62-'+label+'-monomial-input.json')
        original = json.loads(source.read_text())
        roots = original['roots']; cases = {}
        for rr, ss, p, ii, jj, c in original['rules']:
            # Retain the original constant when changing either argument.
            # G2 can have different constants after reversing the source pair.
            for r, s, i, j in [(rr, ss, ii, jj), (ss, rr, jj, ii)]:
                opposite = roots.index([-v for v in roots[r]])
                for k in range(1, i+1):
                    variables = [(r, 2*k), (opposite, k), (s, j)]
                    if i != k:
                        variables.append((r, i-k))
                    key = p, tuple(sorted(variables))
                    cases[key] = math.gcd(cases.get(key, 0), c*math.comb(i, k))
        result = dict(type=label, roots=roots, rules=original['rules'],
                      cases=[dict(root=p, variables=v, coefficient=c)
                             for (p, v), c in sorted(cases.items())],
                      source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        path = Path('results/19.61-'+label+'-square-completion-input.json')
        assert not path.exists()
        path.write_text(json.dumps(result, indent=2)+'\n')
        with path.with_suffix('.txt').open('w') as out:
            out.write(str(len(roots))+' '+str(len(result['rules']))+'\n')
            for row in result['rules']:
                out.write(' '.join(map(str, row))+'\n')
            out.write(str(len(result['cases']))+'\n')
            for case in result['cases']:
                row = [case['root'], case['coefficient'], len(case['variables'])]
                row += [v for item in case['variables'] for v in item]
                out.write(' '.join(map(str, row))+'\n')
        print('PREPARED_1961_SQUARE_COMPLETION', label, len(result['cases']), flush=True)


if __name__ == '__main__':
    run()
