#!/usr/bin/env python3
"""Exact controls and boundary examples for the written infinite-group proof."""
from fractions import Fraction as F
from itertools import permutations, product
import json
from pathlib import Path


def mat(n, entry):
    return tuple(tuple(F(entry(i, j)) for j in range(n)) for i in range(n))


def eye(n):
    return mat(n, lambda i, j: i == j)


def unit(n, a, b):
    return mat(n, lambda i, j: i == a and j == b)


def add(a, b):
    return tuple(tuple(x+y for x, y in zip(r, s)) for r, s in zip(a, b))


def scale(a, c):
    return tuple(tuple(c*x for x in r) for r in a)


def mul(a, b):
    n = len(a)
    return mat(n, lambda i, j: sum(a[i][k]*b[k][j] for k in range(n)))


def power(a, e):
    r = eye(len(a))
    while e:
        if e % 2:
            r = mul(r, a)
        e //= 2
        if e:
            a = mul(a, a)
    return r


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def flat(a):
    return tuple(x for r in a for x in r)


def original_basis(rows):
    echelon, originals = {}, []
    for original in rows:
        row = list(map(F, original))
        for pivot, v in sorted(echelon.items()):
            c = row[pivot]
            row = [x-c*y for x, y in zip(row, v)]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            c = row[pivot]
            echelon[pivot] = [x/c for x in row]
            originals.append(original)
    return originals


def rank(rows):
    return len(original_basis(rows))


def algebra_controls(basis, expected_radical):
    n, d = len(basis[0]), len(basis)
    assert rank([flat(a) for a in basis]) == d
    gram = [[trace(mul(a, b)) for b in basis] for a in basis]
    assert rank(gram) == d-len(expected_radical)
    assert rank([flat(a) for a in expected_radical]) == len(expected_radical)
    for a in expected_radical:
        assert all(trace(mul(a, b)) == 0 for b in basis)
        assert power(a, n) == scale(a, 0)
    return {'dimension': d, 'trace_rank': rank(gram),
            'radical_dimension': len(expected_radical)}


root_count = 0
max_denominator = 0
for n in range(2, 6):
    ident = eye(n)
    nil = mat(n, lambda i, j: j == i+1)
    target = add(ident, nil)
    for r in [2, 3, 5]:
        for k in range(1, 7):
            m = r**k
            root, nilpower, coefficient = ident, ident, F(1)
            for j in range(1, n):
                nilpower = mul(nilpower, nil)
                coefficient *= (F(1, m)-j+1)/j
                root = add(root, scale(nilpower, coefficient))
            assert power(root, m) == target
            max_denominator = max(max_denominator, *(x.denominator for x in flat(root)))
            root_count += 1
assert max_denominator > 10**10

# Semisimple root towers are allowed: order-three eigenvalues need not be 1.
rotation = ((F(0), F(-1)), (F(1), F(-1)))
assert power(rotation, 3) == eye(2) and rotation != eye(2)
for k in range(1, 25):
    root = power(rotation, pow(2**k, -1, 3))
    assert power(root, 2**k) == rotation

triangular = []
for n in range(1, 7):
    basis = [unit(n, i, j) for i in range(n) for j in range(i, n)]
    radical = [unit(n, i, j) for i in range(n) for j in range(i+1, n)]
    item = algebra_controls(basis, radical)
    item['n'] = n
    # Matrix units give all radical-power dimensions, including sharp R^n=0.
    item['radical_power_dimensions'] = [sum(j-i >= k for i in range(n)
                                              for j in range(n))
                                           for k in range(1, n+1)]
    assert item['radical_power_dimensions'][-1] == 0
    if n > 1:
        nil = mat(n, lambda i, j: j == i+1)
        assert power(nil, n-1) == unit(n, 0, n-1)
    triangular.append(item)

# An actual infinite finite-orbit example: A5 x (Q,+) in degree seven.
perms = list(permutations(range(5)))
even = [p for p in perms if sum(p[i] > p[j] for i in range(5)
                               for j in range(i+1, 5)) % 2 == 0]
assert len(even) == 60


def permutation_matrix(p, q=F(0)):
    return mat(7, lambda i, j: (p[i] == j) if i < 5 and j < 5
               else (i == j) if i >= 5 and j >= 5 and (i, j) != (5, 6)
               else q if (i, j) == (5, 6) else 0)


group_matrices = [permutation_matrix(p) for p in even]
transvection = add(eye(7), unit(7, 5, 6))
originals = original_basis([flat(a) for a in group_matrices+[transvection]])
basis = [tuple(tuple(row[7*i:7*i+7]) for i in range(7)) for row in originals]
a5q = algebra_controls(basis, [unit(7, 5, 6)])
assert a5q == {'dimension': 18, 'trace_rank': 17, 'radical_dimension': 1}
tuples = {}
for p, q in product(even, [F(-2), F(-1, 3), F(0), F(1, 2), F(3)]):
    g = permutation_matrix(p, q)
    value = tuple(trace(mul(g, b)) for b in basis)
    if p in tuples:
        assert tuples[p] == value
    else:
        tuples[p] = value
assert len(set(tuples.values())) == 60
a5q['distinct_quotient_tuples'] = len(set(tuples.values()))
a5q['sampled_group_elements'] = 300

# Check the conjugation subgroup S5 has exactly four orbits on A5.
def compose(p, q):
    return tuple(p[q[i]] for i in range(5))


remaining, orbit_sizes = set(even), []
while remaining:
    p = min(remaining)
    orbit = set()
    for s in perms:
        inv = tuple(s.index(i) for i in range(5))
        orbit.add(compose(compose(s, p), inv))
    assert orbit <= remaining
    remaining -= orbit
    orbit_sizes.append(len(orbit))
assert sorted(orbit_sizes) == [1, 15, 20, 24]
a5q['S5_orbit_sizes_on_A5'] = sorted(orbit_sizes)
a5q['infinite_example_automorphism_orbit_upper_bound'] = 2*len(orbit_sizes)

# Negative control: checking only unipotent generators would be invalid.
upper = add(eye(2), unit(2, 0, 1))
lower = add(eye(2), unit(2, 1, 0))
assert trace(upper) == trace(lower) == 2
assert trace(mul(upper, lower)) == 3
full_matrix = algebra_controls([unit(2, i, j) for i in range(2)
                                for j in range(2)], [])
assert full_matrix['trace_rank'] == 4

result = {'status': 'PASS', 'rational_unipotent_root_towers': root_count,
          'largest_root_entry_denominator': max_denominator,
          'nontrivial_finite_order_root_controls': 24,
          'triangular_algebras': triangular, 'A5_times_Q': a5q,
          'unipotent_generators_negative_control': 'PASS',
          'note': 'Finite exact controls; the arbitrary-group theorem rests on the written proof.'}
Path('results/21.40-python-controls.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
