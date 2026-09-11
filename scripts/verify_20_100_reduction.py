#!/usr/bin/env python3
"""Exact independent controls in the Klein bottle group and H_11 x Klein."""
from itertools import permutations
from math import gcd
from random import Random
import json

rng = Random(20100)
zero = (0, 0)


def kmul(a, b):
    return a[0] + (-1 if a[1] % 2 else 1)*b[0], a[1]+b[1]


def power(a, n, op, identity):
    out = identity
    for _ in range(n):
        out = op(out, a)
    return out


def length(a):
    r, s = a
    if s % 2 or r == 0:
        return abs(s)
    return gcd(abs(r), abs(s))


pool = [(r, s) for r in range(-5, 6) for s in range(-5, 6) if (r, s) != zero]
tf_cases = 0
for _ in range(1000):
    n = rng.randrange(2, 31)
    # Include repeated elements and repeated roots; the theorem permits both.
    points = sorted(rng.choices(pool, k=n), key=length)
    exponents = sorted(rng.sample(range(1, 101), n))
    values = [power(a, e, kmul, zero) for a, e in zip(points, exponents)]
    assert all(length(v) == e*length(a) for a, e, v in zip(points, exponents, values))
    assert len(set(values)) == n
    tf_cases += 1
roots = [(-2, 1), (0, 1), (3, 1)]
assert len(set(roots)) == 3
assert len({power(a, 2, kmul, zero) for a in roots}) == 1

prime = 11
hzero = (0, 0, 0)


def hmul(a, b):
    return ((a[0]+b[0]) % prime, (a[1]+b[1]) % prime,
            (a[2]+b[2]+a[0]*b[1]) % prime)


def gmul(a, b):
    return hmul(a[0], b[0]), kmul(a[1], b[1])


identity = (hzero, zero)
hpool = [(a, b, c) for a in range(prime) for b in range(prime) for c in range(prime)]
assert hmul((1, 0, 0), (0, 1, 0)) != hmul((0, 1, 0), (1, 0, 0))
classes = {}
for a in hpool:
    if a == hzero:
        continue
    orbit = [power(a, k, hmul, hzero) for k in range(1, prime)]
    base = min(orbit)
    powers = [power(base, k, hmul, hzero) for k in range(prime)]
    classes[a] = (base, powers.index(a))
assert len({base for base, _ in classes.values()}) == 133

mixed_cases = 0
permutations_checked = 0
for n in range(2, 7):
    for trial in range(80):
        finite_count = trial % (n+1)
        finite = [(a, zero) for a in rng.sample(hpool, finite_count)]
        infinite = []
        while len(infinite) < n-finite_count:
            a = (rng.choice(hpool), rng.choice(pool))
            if a not in infinite:
                infinite.append(a)
        points = finite + infinite
        bases = sorted({classes[a][0] for a, _ in finite if a != hzero})
        dimension = len(bases)+1
        model = []
        for a, _ in finite:
            v = [0]*dimension
            if a != hzero:
                base, exponent = classes[a]
                v[bases.index(base)] = exponent
            model.append(tuple(v))
        for j in range(len(infinite)):
            model.append((0,)*(dimension-1)+(j+1,))
        assert len(set(model)) == n
        actual_powers = [[power(a, e, gmul, identity) for e in range(1, n+1)] for a in points]
        chosen = None
        for assignment in permutations(range(1, n+1)):
            modeled = [tuple((v[k]*e) % (13 if k == dimension-1 else 11)
                             for k in range(dimension)) for v, e in zip(model, assignment)]
            for i in range(finite_count):
                for j in range(i):
                    assert (modeled[i] == modeled[j]) == (actual_powers[i][assignment[i]-1] == actual_powers[j][assignment[j]-1])
            if chosen is None and len(set(modeled)) == n:
                chosen = assignment
            permutations_checked += 1
        assert chosen is not None
        finite_values = [actual_powers[i][chosen[i]-1] for i in range(finite_count)]
        remaining = sorted(chosen[finite_count:])
        infinite = sorted(infinite, key=lambda a: length(a[1]))
        values = finite_values + [power(a, e, gmul, identity) for a, e in zip(infinite, remaining)]
        assert len(set(values)) == n
        mixed_cases += 1

# Direct negative control: all four nonzero residues modulo5.
assert all(len({a*e % 5 for a, e in zip(range(1, 5), assignment)}) < 4
           for assignment in permutations(range(1, 5)))
print(json.dumps({"torsion_free_cases": tf_cases, "distinct_common_square_roots": 3,
                  "H11_cyclic_subgroups": 133, "mixed_group_cases": mixed_cases,
                  "all_assignments_checked_for_finite_power_collisions": permutations_checked,
                  "C5_negative_control_assignments": 24, "status": "PASS"}, indent=2, sort_keys=True))
