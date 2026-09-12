#!/usr/bin/env python3
"""Exact affine controls for the separate written proof of 16.38."""
import itertools as it
import json
from fractions import Fraction as F
from pathlib import Path


def add(u, v):
    return tuple(a + b for a, b in zip(u, v))


def neg(u):
    return tuple(-a for a in u)


def scale(k, u):
    return tuple(k * a for a in u)


def matmul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


def act(a, u):
    return tuple(sum(x * y for x, y in zip(row, u)) for row in a)


def closure(gens):
    n = len(gens[0])
    identity = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    elements, seen = [identity], {identity}
    for a in elements:
        for b in gens:
            c = matmul(a, b)
            if c not in seen:
                elements.append(c)
                seen.add(c)
                assert len(elements) < 100
    return elements


def matrix_controls():
    r3 = ((0, -1), (1, -1))
    r4 = ((0, -1), (1, 0))
    swap = ((0, 1), (1, 0))
    t, ti = ((1, 3), (0, 1)), ((1, -3), (0, 1))
    rows = []
    for name, gens, expected_order in [('C3', [r3], 3), ('S3', [r3, swap], 6),
                                       ('C4', [r4], 4), ('D8', [r4, swap], 8)]:
        group = closure([matmul(matmul(t, g), ti) for g in gens])
        assert len(group) == expected_order
        # The representation is deliberately not orthogonal in the given basis.
        assert any(sum(g[i][0] ** 2 for i in range(2)) != 1 for g in group)
        metric = tuple(tuple(sum(sum(g[k][i] * g[k][j] for k in range(2))
                                 for g in group) for j in range(2)) for i in range(2))
        assert metric[0][0] > 0 and metric[0][0] * metric[1][1] > metric[0][1] ** 2
        norm = lambda u: sum(u[i] * metric[i][j] * u[j] for i in range(2) for j in range(2))
        zero = (F(0), F(0))
        cocycles = products = orbit_points = 0
        for numerators in it.product(range(-3, 4), repeat=2):
            v = tuple(F(a, 2) for a in numerators)
            delta = {g: add(v, neg(act(g, v))) for g in group}
            average = tuple(sum(delta[g][i] for g in group) / len(group) for i in range(2))
            for g in group:
                assert delta[g] == add(average, neg(act(g, average)))
                assert norm(act(g, average)) == norm(average)
                orbit_points += 1
                for h in group:
                    gh = matmul(g, h)
                    assert delta[gh] == add(delta[g], act(g, delta[h]))
                    cocycles += 1
            values = set(delta.values())
            assert all(scale(2, u) not in values for u in values if u != zero)
            # A_g=(0,g), B_h=(delta(h),h); compute AB independently.
            pure = set()
            for g, h in it.product(group, repeat=2):
                scalar = matmul(g, h)
                vector = act(g, delta[h])
                products += 1
                if scalar == group[0]:
                    pure.add(vector)
            assert pure == {neg(u) for u in values}
            assert all(scale(2, u) not in pure for u in pure if u != zero)
        rows.append({'group': name, 'order': len(group), 'matrices': group,
                     'averaged_metric': metric, 'cocycles': 49,
                     'cocycle_pairs': cocycles, 'affine_products': products,
                     'orbit_point_checks': orbit_points})
    return rows


def sign_controls():
    # Truncations of C=sum C2 acting by coordinate sign changes on D=sum Z.
    # The infinite cocycle has no coboundary in Q tensor D (finite support).
    rows = []
    for n in range(1, 9):
        delta = [tuple((g >> i) & 1 for i in range(n)) for g in range(2 ** n)]
        action = lambda g, u: tuple((-1 if (g >> i) & 1 else 1) * u[i] for i in range(n))
        pure, pairs = set(), 0
        for g, h in it.product(range(2 ** n), repeat=2):
            assert delta[g ^ h] == add(delta[g], action(g, delta[h]))
            scalar, vector = g ^ h, action(g, delta[h])
            if scalar == 0:
                pure.add(vector)
            pairs += 1
        assert pure == {neg(u) for u in delta}
        assert all(scale(2, u) not in pure for u in pure if any(u))
        rows.append({'rank': n, 'scalar_order': 2 ** n, 'cocycle_and_product_pairs': pairs,
                     'pure_translations': len(pure), 'nonzero_translations': len(pure) - 1})
    return rows


def mutation_controls():
    # Without torsion-freeness, a finite orbit can be an entire affine line.
    v = (0, 1, 2)
    images = []
    for shift in range(3):
        gv = v[shift:] + v[:shift]
        images.append(tuple((a - b) % 3 for a, b in zip(v, gv)))
    t = images[1]
    assert any(t) and tuple(2 * a % 3 for a in t) in images
    # Without local finiteness, the cocycle Z->Q, n->n, contains 1 and 2.
    assert 1 + 1 == 2
    return {'torsion_module': 'F3^3 with C3 cyclically permuting coordinates',
            'cocycle_image': images, 'doubling_witness': t,
            'nonlocally_finite_example': 'C=Z acts trivially on Q; delta(n)=n'}


def run():
    return {'status': 'PASS', 'scope': 'Exact finite controls, not an exhaustive proof.',
            'matrix_controls': matrix_controls(), 'sign_controls': sign_controls(),
            'mutations': mutation_controls()}


if __name__ == '__main__':
    result = run()
    Path('results/16.38-controls.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS_1638_AFFINE_CONTROLS', sum(r['cocycle_pairs'] for r in result['matrix_controls']),
          sum(r['cocycle_and_product_pairs'] for r in result['sign_controls']))
