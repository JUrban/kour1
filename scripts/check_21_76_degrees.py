#!/usr/bin/env python3
"""Independent exact polynomial controls for the all-characteristic proof."""
import itertools
import json
from pathlib import Path


def trim(poly, p):
    poly = [a % p if p else a for a in poly]
    while poly and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def add(a, b, p):
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))], p)


def mul(a, b, p):
    out = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out, p)


def mm(a, b, p):
    return tuple(tuple(add(mul(a[i][0], b[0][j], p), mul(a[i][1], b[1][j], p), p)
                       for j in range(2)) for i in range(2))


I = (((1,), ()), ((), (1,)))


def evaluate(coefficients, start, p):
    a = I
    for i, c in enumerate(coefficients):
        factor = (((1,), (0, c)), ((), (1,))) if (i+start) % 2 == 0 else (((1,), ()), ((0, c), (1,)))
        a = mm(a, factor, p)
    return a


def matrix_unit_word(indices, start):
    # Track a literal product E_ab E_cd = delta_bc E_ad.
    current = None
    for i in indices:
        root = (0, 1) if (i+start) % 2 == 0 else (1, 0)
        if current is None:
            current = root
        elif current[1] != root[0]:
            return None
        else:
            current = (current[0], root[1])
    return current


def run():
    structural = 0
    for m in range(2, 101):
        for start in range(2):
            target = (start, start)
            if m % 2 == 0:
                assert matrix_unit_word(range(m), start) == target
                structural += 1
            else:
                assert matrix_unit_word(range(m), start) == (start, 1-start)
                hits = [j for j in range(m) if matrix_unit_word([i for i in range(m) if i != j], start) == target]
                assert hits == [m-1]
                structural += m+1
    rows = []
    total = 0
    for p, bound, alphabet in [(2, 16, [1]), (3, 10, [1, 2]), (5, 6, [1, 2, 3, 4]),
                               (7, 5, [1, 2, 3, 4, 5, 6]), (0, 5, [-2, -1, 1, 2])]:
        count = 0
        for m in range(1, bound+1):
            for coefficients in itertools.product(alphabet, repeat=m):
                for start in range(2):
                    a = evaluate(coefficients, start, p)
                    assert all(add(mul(a[0][0], a[1][1], p),
                                   tuple(-x for x in mul(a[0][1], a[1][0], p)), p) == (1,) for _ in [0])
                    if m >= 2:
                        degree = 2*(m//2)
                        leading = 1
                        for c in coefficients[:degree]:
                            leading *= c
                        if p:
                            leading %= p
                        assert len(a[start][start])-1 == degree
                        assert a[start][start][-1] == leading != 0
                        assert a[start][start] != (1,)
                    else:
                        assert a[0][0] == a[1][1] == (1,)
                    count += 1
        rows.append(dict(characteristic=p, max_length=bound, coefficients=alphabet, cases=count))
        total += count
    # A negative control: allowing constant parameters destroys the degree argument.
    p = 3
    u = (((1,), (1,)), ((), (1,)))
    v = (((1,), ()), ((2,), (1,)))
    w = mm(mm(u, v, p), u, p)
    assert w == (((), (1,)), ((2,), ()))
    assert mm(mm(w, w, p), mm(w, w, p), p) == I
    # The actual polynomial degree witnesses: x^3 is not a scalar multiple of x.
    for p in [0, 2, 3, 5, 7]:
        x3 = mul(mul((0, 1), (0, 1), p), (0, 1), p)
        assert x3 == (0, 0, 0, 1)
    return dict(status='PASS', word_cases=total, rows=rows,
                matrix_unit_products=structural, structural_max_length=100,
                negative_constant_parameter_control=True, completion_degree_controls=5,
                scope='Finite independent controls; the proof covers arbitrary word length and every field.')


if __name__ == '__main__':
    result = run()
    Path('results/21.76-degree-controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS_2176_DEGREES', json.dumps(result, sort_keys=True))
