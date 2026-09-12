#!/usr/bin/env python3
"""Check both argument substitutions by independent polynomial expansion."""
import collections
import copy
import hashlib
import json
import math
from pathlib import Path
from verify_19_62_monomial_certificates import verify_case


def targets(data):
    roots = data['roots']; required = {}
    substitutions = terms = 0
    for r, s, p, i, j, c in data['rules']:
        for which in [0, 1]:
            changed, other = ([r, s] if which == 0 else [s, r])
            degree, other_degree = ([i, j] if which == 0 else [j, i])
            opposite = roots.index([-v for v in roots[changed]])
            assigned = [changed, changed, opposite, other]
            # Multiply (X0+X1^2 X2)^degree X3^other_degree directly.
            polynomial = {(0, 0, 0, other_degree): c}
            for repetition in range(degree):
                updated = collections.defaultdict(int)
                for exponent, coefficient in polynomial.items():
                    for increment in [(1, 0, 0, 0), (0, 2, 1, 0)]:
                        key = tuple(a+b for a, b in zip(exponent, increment))
                        updated[key] += coefficient
                polynomial = dict(updated)
            substitutions += 1
            for exponents, coefficient in polynomial.items():
                if exponents[2] == 0:
                    continue
                terms += 1
                variables = tuple(sorted((a, e) for a, e in zip(assigned, exponents) if e))
                key = p, variables
                required[key] = math.gcd(required.get(key, 0), coefficient)
    actual = {(v['root'], tuple(map(tuple, v['variables']))): v['coefficient'] for v in data['cases']}
    assert actual == required and len(actual) == len(data['cases'])
    return substitutions, terms


def run():
    reports = []
    for label, expected in [('a2', 12), ('b2', 48), ('g2', 240)]:
        prefix = 'results/19.61-'+label+'-square-completion-'
        source = Path(prefix+'input.json'); data = json.loads(source.read_text())
        original = Path('results/19.62-'+label+'-monomial-input.json')
        reference = json.loads(original.read_text())
        assert data['source_sha256'] == hashlib.sha256(original.read_bytes()).hexdigest()
        assert data['rules'] == reference['rules'] and data['roots'] == reference['roots']
        substitutions, terms = targets(data)
        certificate = Path(prefix+'certificate.jsonl')
        seen = set(); total = largest = 0; first = None
        for line in certificate.read_text().splitlines():
            index, nodes = json.loads(line)
            assert index not in seen; seen.add(index)
            size = verify_case(data, index, nodes); total += size; largest = max(largest, size)
            if first is None:
                first = index, nodes
        assert seen == set(range(1, expected+1)) and len(data['cases']) == expected
        index, nodes = first; mutants = []
        bad = copy.deepcopy(nodes); bad[-1][1] += 1; mutants.append(bad)
        bad = copy.deepcopy(nodes); bad[-1][4][1] = bad[-1][0]; mutants.append(bad)
        bad = copy.deepcopy(nodes); bad[-1][4][0] = (bad[-1][4][0]+1) % len(data['rules']); mutants.append(bad)
        bad = copy.deepcopy(nodes); bad.pop(); mutants.append(bad)
        rejected = 0
        for bad in mutants:
            try:
                verify_case(data, index, bad)
            except (AssertionError, KeyError):
                rejected += 1
            else:
                raise AssertionError('corrupt certificate accepted')
        report = dict(type=label, cases=expected, nodes=total, largest=largest,
                      substitutions=substitutions, polynomial_terms=terms,
                      mutations_rejected=rejected,
                      input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                      certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest())
        reports.append(report)
        print('PASS_1961_SQUARE_COMPLETION_CERTIFICATES', label, expected, total, largest, substitutions, terms, rejected, flush=True)
    return dict(types=reports, cases=sum(v['cases'] for v in reports),
                nodes=sum(v['nodes'] for v in reports))


if __name__ == '__main__':
    Path('results/19.61-square-completion-verification.json').write_text(json.dumps(run(), indent=2)+'\n')
