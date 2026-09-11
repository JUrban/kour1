#!/usr/bin/env python3
"""Finite controls for the quasigroup isotope obstruction, using no GAP."""
import itertools
import json
import math


def latin_squares(n):
    rows = list(itertools.permutations(range(n)))

    def extend(table):
        if len(table) == n:
            yield table
            return
        for row in rows:
            if all(row[j] not in [r[j] for r in table] for j in range(n)):
                yield from extend(table + [row])

    yield from extend([])


def factorial_controls():
    records = []
    for n, expected in [(1, 1), (2, 2), (3, 12), (4, 576)]:
        count = checks = 0
        for table in latin_squares(n):
            count += 1
            for x in range(n):
                for y in range(n):
                    value = y
                    for _ in range(math.factorial(n)):
                        value = table[x][value]
                    assert value == y, (n, table, x, y)
                    checks += 1
        assert count == expected
        records.append({'n': n, 'latin_squares': count,
                        'factorial_identity_assignments': checks})
    return records


def affine_control(p, m):
    vectors = list(itertools.product(range(p), repeat=m))
    index = {v: i for i, v in enumerate(vectors)}
    n = len(vectors)
    shift = lambda v: v[-1:] + v[:-1]
    unshift = lambda v: v[1:] + v[:1]
    plus = lambda a, b: tuple((x+y) % p for x, y in zip(a, b))
    minus = lambda a, b: tuple((x-y) % p for x, y in zip(a, b))
    op = [[index[plus(a, shift(b))] for b in vectors] for a in vectors]
    left = [[index[unshift(minus(c, a))] for c in vectors] for a in vectors]
    right = [[index[minus(c, shift(b))] for b in vectors] for c in vectors]
    target = list(range(n))
    for x in range(n):
        assert sorted(op[x]) == target
        assert sorted(op[y][x] for y in range(n)) == target
        for y in range(n):
            assert op[x][left[x][y]] == y
            assert left[x][op[x][y]] == y
            assert op[right[x][y]][y] == x
            assert right[op[x][y]][y] == x

    # Independently encode a vector as a base-p integer, with e_0 = 1.
    def encode(v):
        return sum(c * p**i for i, c in enumerate(v))

    def rotate_integer(b):
        return (b % p**(m-1)) * p + b // p**(m-1)

    def add_integer(a, b):
        answer = 0
        for i in range(m):
            answer += ((a // p**i + b // p**i) % p) * p**i
        return answer

    for a, row in zip(vectors, op):
        for b, value in zip(vectors, row):
            assert encode(vectors[value]) == add_integer(
                encode(a), rotate_integer(encode(b)))

    zero = index[(0,)*m]
    seed = index[(1,)+(0,)*(m-1)]
    orbit = []
    value = seed
    while value not in orbit:
        orbit.append(value)
        value = op[zero][value]
    assert value == seed and len(orbit) == m

    # Compute closure with division operations obtained from the Latin
    # square itself, independently of the affine division formulas.
    raw_left = [[op[x].index(y) for y in range(n)] for x in range(n)]
    raw_right = [[next(x for x in range(n) if op[x][y] == z)
                  for y in range(n)] for z in range(n)]
    assert raw_left == left and raw_right == right
    generated = {seed}
    rounds = 0
    while True:
        old = set(generated)
        for x, y in itertools.product(old, repeat=2):
            generated.update([op[x][y], raw_left[x][y], raw_right[x][y]])
        rounds += 1
        if generated == old:
            break
    assert len(generated) == n

    boolean_checks = 0
    if p == 2:
        for x, y, z in itertools.product(range(n), repeat=3):
            assert right[op[x][y]][z] == right[op[x][z]][y]
            boolean_checks += 1
    return {'p': p, 'm': m, 'order': n, 'left_zero_orbit': orbit,
            'left_zero_orbit_length': m, 'axiom_checks': 4*n*n,
            'independent_product_checks': n*n,
            'boolean_identity_checks': boolean_checks,
            'monogenic_closure_order': len(generated), 'closure_rounds': rounds}


def separating_controls():
    out = []
    for bound in range(1, 11):
        # Any prime m > bound avoids every prime factor of bound!.
        m = bound + 1
        while any(m % d == 0 for d in range(2, math.isqrt(m)+1)):
            m += 1
        nfactorial = math.factorial(bound)
        # Literal iteration on a sparse coordinate label, not a formula
        # using N modulo m. This is the orbit of e_0 under left zero.
        position = 0
        for _ in range(nfactorial):
            position += 1
            if position == m:
                position = 0
        assert position == nfactorial % m and position != 0
        out.append({'generator_size_bound': bound, 'identity_length': nfactorial,
                    'witness_dimension': m, 'witness_order': 2**m,
                    'initial_basis_position': 0, 'final_basis_position': position})
    return out


def run():
    cases = [(2, m) for m in range(1, 8)] + [(3, m) for m in range(1, 4)]
    cases += [(5, m) for m in range(1, 3)]
    return {'status': 'PASS_94_CONTROLS', 'latin': factorial_controls(),
            'affine': [affine_control(p, m) for p, m in cases],
            'separators': separating_controls(),
            'scope': 'Finite formula controls; the general obstruction is proved in prose.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
