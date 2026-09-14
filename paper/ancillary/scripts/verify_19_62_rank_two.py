#!/usr/bin/env python3
"""Reconstruct all three-variable targets and check saved integer proofs."""
import copy
import hashlib
import json
import math
from pathlib import Path
from verify_19_62_monomial_certificates import verify_case


def targets(data):
    roots = data['roots']
    coefficients = {tuple(row[:5]): row[5] for row in data['rules']}
    assert len(coefficients) == len(data['rules'])
    required = {}
    found = set()
    # Solve the root equation independently; do not read the target list.
    for p, point in enumerate(roots):
        for r, left in enumerate(roots):
            for s, right in enumerate(roots):
                if left == right or left == [-v for v in right]:
                    continue
                det = left[0]*right[1]-left[1]*right[0]
                assert det != 0
                ni = -point[0]*right[1]+point[1]*right[0]
                nj = -left[0]*point[1]+left[1]*point[0]
                if ni % det or nj % det:
                    continue
                i, j = ni//det, nj//det
                if i <= 0 or j <= 0:
                    continue
                assert max(i, j) <= 3
                rule = (r, s, roots.index([-v for v in point]), i, j)
                found.add(rule)
                c = coefficients[rule]
                key = p, tuple(sorted([(p, 2), (r, i), (s, j)]))
                required[key] = math.gcd(required.get(key, 0), c)
    assert found == set(coefficients)
    actual = {(v['root'], tuple(map(tuple, v['variables']))): v['coefficient']
              for v in data['cases']}
    assert actual == required and len(actual) == len(data['cases'])


def weyl_coverage(data, label):
    cartan, selected, order = {
        'a2': ([[2, -1], [-1, 2]], [2], 6),
        'b2': ([[2, -2], [-1, 2]], [2, 3], 8),
        'g2': ([[2, -1], [-3, 2]], [3, 5], 12),
    }[label]
    roots = data['roots']
    reflections = []
    for i, simple in enumerate(cartan):
        permutation = tuple(roots.index([x-v[i]*y for x, y in zip(v, simple)]) for v in roots)
        assert sorted(permutation) == list(range(len(roots)))
        assert all(permutation[permutation[r]] == r for r in range(len(roots)))
        reflections.append(permutation)
    known = {tuple(range(len(roots)))}
    group = list(known)
    for permutation in group:
        for reflection in reflections:
            product = tuple(reflection[r] for r in permutation)
            if product not in known:
                known.add(product); group.append(product)
                assert len(group) <= order
    assert len(group) == order
    rules = set(map(tuple, data['rules']))
    for permutation in group:
        transported = {(permutation[r], permutation[s], permutation[k], i, j, c)
                       for r, s, k, i, j, c in rules}
        assert transported == rules
    cases = {(v['root'], tuple(map(tuple, v['variables']))): v['coefficient'] for v in data['cases']}
    for (p, variables), c in cases.items():
        witnesses = [w for w in group if w[p] in selected]
        assert witnesses
        for w in witnesses:
            key = w[p], tuple(sorted((w[r], e) for r, e in variables))
            assert cases[key] == c
    return dict(weyl_order=order, representatives=sum(v['root'] in selected for v in data['cases']))


def run():
    reports = []
    for label, expected in [('a2', 6), ('b2', 20), ('g2', 78)]:
        source = Path('results/19.62-' + label + '-rank-two-input.json')
        data = json.loads(source.read_text())
        original = Path('results/19.62-' + label + '-monomial-input.json')
        reference = json.loads(original.read_text())
        assert data['source_sha256'] == hashlib.sha256(original.read_bytes()).hexdigest()
        assert data['roots'] == reference['roots'] and data['rules'] == reference['rules']
        targets(data)
        coverage = weyl_coverage(data, label)
        certificate = source.with_name('19.62-' + label + '-rank-two-certificate.jsonl')
        seen = set()
        total = largest = 0
        first = None
        for line in certificate.read_text().splitlines():
            index, nodes = json.loads(line)
            assert index not in seen
            seen.add(index)
            size = verify_case(data, index, nodes)
            total += size
            largest = max(largest, size)
            if first is None:
                first = index, nodes
        assert seen == set(range(1, expected+1)) and len(data['cases']) == expected
        short = certificate.with_name('19.62-'+label+'-rank-two-short-certificate.jsonl')
        short_seen = set()
        short_total = short_largest = 0
        for line in short.read_text().splitlines():
            index, nodes = json.loads(line)
            assert index not in short_seen
            short_seen.add(index)
            size = verify_case(data, index, nodes)
            short_total += size; short_largest = max(short_largest, size)
        assert short_seen == seen
        index, nodes = first
        mutants = []
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
                raise AssertionError('corrupt proof accepted')
        result = dict(type=label, cases=expected, derivation_nodes=total,
                      largest_certificate=largest, mutations_rejected=rejected,
                      short_nodes=short_total, short_largest=short_largest, **coverage,
                      input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                      certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest(),
                      short_certificate_sha256=hashlib.sha256(short.read_bytes()).hexdigest())
        reports.append(result)
        print('PASS_1962_RANK_TWO_CERTIFICATES', label, expected, total, largest, rejected, flush=True)
    return dict(types=reports, cases=sum(v['cases'] for v in reports),
                derivation_nodes=sum(v['derivation_nodes'] for v in reports))


if __name__ == '__main__':
    report = run()
    Path('results/19.62-rank-two-verification.json').write_text(json.dumps(report, indent=2)+'\n')
