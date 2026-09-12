#!/usr/bin/env python3
"""Exact bounded controls. The proof, not these tests, gives unboundedness."""
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random


def mul(a, b, p):
    v, k = a
    w, l = b
    return (tuple((v[i] + w[(i-k) % p]) % p for i in range(p)), (k+l) % p)


def power(a, n, p):
    out = ((0,)*p, 0)
    for _ in range(n):
        out = mul(out, a, p)
    return out


def wreath_controls():
    rng = random.Random(1993)
    rows = []
    for p in (2, 3, 5, 7, 11):
        exhaustive = p <= 5
        elements = ([(v, k) for v in product(range(p), repeat=p) for k in range(p)]
                    if exhaustive else
                    [(tuple(rng.randrange(p) for _ in range(p)), rng.randrange(p))
                     for _ in range(3000)])
        for g in elements:
            v, k = g
            expected = ((sum(v) % p,)*p if k else (0,)*p, 0)
            assert power(g, p, p) == expected
        # All possible quotient images; a necessary condition for generation
        # is independence in the displayed elementary abelian quotient.
        axes = [(s, a) for s in range(p) for a in range(p) if s*a % p == 0]
        generating = 0
        for s, a in axes:
            for t, b in axes:
                if (s*b-a*t) % p:
                    generating += 1
                    assert (s+t)*(a+b) % p != 0
        assert generating == 2*(p-1)**2
        # Mutation: removing the third relation permits the wreath group.
        e = ((1,) + (0,)*(p-1), 0)
        t = ((0,)*p, 1)
        assert power(e, p, p) == power(t, p, p) == ((0,)*p, 0)
        assert power(mul(e, t, p), p, p) != ((0,)*p, 0)
        rows.append(dict(p=p, norm_tests=len(elements), exhaustive=exhaustive,
                         independent_axis_pairs=generating))
    return rows


def poly_mul(a, b, p, bound):
    c = defaultdict(int)
    for u, x in a.items():
        for v, y in b.items():
            if len(u)+len(v) < bound:
                c[u+v] = (c[u+v]+x*y) % p
    return {w: v for w, v in c.items() if v}


def relations(p):
    z = {'0': 1, '1': 1, '01': 1}
    r = {'': 1}
    for _ in range(p):
        r = poly_mul(r, z, p, 2*p+1)
    assert min(map(len, r)) == p
    assert {w: v for w, v in r.items() if len(w) == p} == {
        ''.join(w): 1 for w in product('01', repeat=p)}
    return [{'0'*p: 1}, {'1'*p: 1}, r]


def rank(rows, p, reverse=False):
    pivots = {}
    for original in rows:
        row = dict(original)
        while row:
            pivot = (max if reverse else min)(row, key=lambda w: (len(w), w))
            if pivot not in pivots:
                inv = pow(row[pivot], -1, p)
                pivots[pivot] = {w: v*inv % p for w, v in row.items()}
                break
            scale = row[pivot]
            for w, v in pivots[pivot].items():
                value = (row.get(w, 0)-scale*v) % p
                if value:
                    row[w] = value
                else:
                    row.pop(w, None)
    return len(pivots)


def algebra_controls():
    p = 7
    rels = relations(p)
    dims = [0]
    records = []
    for n in range(1, 13):
        rows = []
        for total in range(max(0, n-p)):
            for k in range(total+1):
                for letters in product('01', repeat=total):
                    left = ''.join(letters[:k])
                    right = ''.join(letters[k:])
                    for rel in rels:
                        rows.append({left+w+right: v for w, v in rel.items()
                                     if total+len(w) < n})
        r = rank(rows, p)
        # Reversed elimination uses the other end of the degree filtration.
        assert rank(reversed(rows), p, reverse=True) == r
        d = 2**n-1-r
        dims.append(d)
        records.append(dict(truncation=n, relations_spanned=len(rows),
                            ideal_rank=r, dimension=d))
    h = [dims[n+1]-dims[n] for n in range(12)]
    assert h[:7] == [2**i for i in range(7)]
    assert h[7] == 2**7-3
    # Filtered GS bounds cumulative coefficients, not individual coefficients.
    for n in range(len(h)):
        c = dims[n+1]-2*dims[n]+(3*dims[n-6] if n >= 7 else 0)
        assert c >= 1
    tau = Fraction(2, 3)
    value = 1-2*tau+3*tau**7
    assert value == Fraction(-115, 729)
    assert 1-2*tau+3*tau**5 > 0
    return dict(p=p, dimensions=records, hilbert_prefix=h,
                gs_value=str(value), p5_at_same_tau='positive')


def run():
    return dict(wreath=wreath_controls(), algebra=algebra_controls(),
                scope='Bounded exact algebra and wreath controls; no automated proof of unbounded width.')


if __name__ == '__main__':
    result = run()
    Path('results/19.93-controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS_1993_CONTROLS', sum(r['norm_tests'] for r in result['wreath']),
          len(result['algebra']['dimensions']))
