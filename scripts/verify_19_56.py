#!/usr/bin/env python3
"""Independent literal permutation/matrix controls for the 19.56 lemmas.

No GAP output, libraries, or stored group tables are used as input.
"""
import itertools
import json
from math import gcd
from pathlib import Path


def primes(n):
    out = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def permutations(n, alternating=False):
    def even(p):
        return sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2 == 0
    els = [p for p in itertools.permutations(range(n)) if not alternating or even(p)]
    return els, lambda a, b: tuple(b[a[i]] for i in range(n)), tuple(range(n))


def matrices(p, projective=False):
    def canonical(a):
        return min(a, tuple(-x % p for x in a)) if projective else a
    def mul(a, b):
        x, y, z, w = a
        r, s, t, u = b
        return canonical(((x*r+y*t) % p, (x*s+y*u) % p,
                          (z*r+w*t) % p, (z*s+w*u) % p))
    els = sorted({canonical(a) for a in itertools.product(range(p), repeat=4)
                  if (a[0]*a[3]-a[1]*a[2]) % p == 1})
    return els, mul, canonical((1, 0, 0, 1))


def check(name, data):
    els, multiply, one = data
    n = len(els)
    positions = {g: i for i, g in enumerate(els)}
    e = positions[one]
    table = [[positions[multiply(x, y)] for y in els] for x in els]
    inverse = [row.index(e) for row in table]
    assert all(table[inverse[x]][x] == e for x in range(n))
    order = []
    for x in range(n):
        k, v = 1, x
        while v != e:
            k, v = k+1, table[v][x]
            assert k <= n
        assert n % k == 0
        order.append(k)
    ps = [primes(k) for k in order]
    def comm(x, y):
        return table[table[table[inverse[x]][inverse[y]]][x]][y]
    def closure(gens):
        gens = list(gens)
        seen, queue = {e}, [e]
        for x in queue:
            for g in gens:
                y = table[x][g]
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        return seen
    star = {e}
    witnesses = {}
    inputs = 0
    for x in range(n):
        if len(ps[x]) != 1:
            continue
        for y in range(n):
            if len(ps[y]) == 1 and ps[x] != ps[y]:
                a = comm(x, y)
                star.add(a)
                witnesses.setdefault(a, (x, y))
                inputs += 1
    hyper = []
    for p in primes(n):
        target, tmp = 1, n
        while tmp % p == 0:
            tmp //= p
            target *= p
        sylow = {e}
        for x in range(n):
            if len(sylow) == target:
                break
            if ps[x] == [p] and x not in sylow:
                candidate = closure(sylow | {x})
                if primes(len(candidate)) == [p]:
                    sylow = candidate
        assert len(sylow) == target
        residual = closure(x for x in range(n) if order[x] % p != 0)
        generated = closure(star & sylow)
        assert generated == residual & sylow
        hyper.append([p, len(sylow), len(generated), len(generated)])
    good, primarygood = True, True
    violations = 0
    example = None
    for a in star:
        for b in star:
            oa, ob = order[a], order[b]
            if gcd(oa, ob) == 1 and order[table[a][b]] < oa*ob:
                good = False
                if len(ps[a]) == len(ps[b]) == 1:
                    primarygood = False
                violations += 1
                if example is None:
                    x, y = witnesses[a]
                    u, v = witnesses[b]
                    assert comm(x, y) == a and comm(u, v) == b
                    example = dict(a=els[a], b=els[b], x=els[x], y=els[y],
                                   u=els[u], v=els[v],
                                   input_orders=[order[k] for k in (x, y, u, v)],
                                   output_orders=[oa, ob, order[table[a][b]]])
    return dict(row=[name, n, len(star), inputs, good, primarygood, hyper],
                violation_pairs=violations, explicit_example=example,
                multiplication_entries=n*n)


def odd_matrix_controls():
    rows = []
    for p in [3, 5, 7, 11, 13, 17, 19, 23, 31, 43, 59, 101]:
        # These identities need only literal 2-by-2 multiplication.
        def mul(a, b):
            return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) % p
                         for i in range(2) for j in range(2))
        one = (1, 0, 0, 1)
        a, b = next((a, b) for a in range(p) for b in range(p)
                    if (a*a+b*b+1) % p == 0)
        i, j = (0, 1, p-1, 0), (a, b, b, -a % p)
        k = mul(i, j)
        negone = tuple(-x % p for x in one)
        assert all(mul(x, x) == negone for x in (i, j, k))
        inv2 = pow(2, -1, p)
        t = tuple((-one[n]+i[n]+j[n]+k[n])*inv2 % p for n in range(4))
        assert mul(mul(t, t), t) == one and t != one
        assert mul(i, t) == mul(t, j) and mul(j, t) == mul(t, k) and mul(k, t) == mul(t, i)
        assert (t[0]*t[3]-t[1]*t[2]) % p == 1
        rows.append([p, a, b, t])
    return rows


if __name__ == '__main__':
    cases = [('S3', permutations(3)), ('A4', permutations(4, True)),
             ('S4', permutations(4)), ('A5', permutations(5, True)),
             ('SL2_5', matrices(5)), ('PSL2_7', matrices(7, True)),
             ('A6', permutations(6, True))]
    results = [check(name, data) for name, data in cases]
    assert [r['row'][4] for r in results] == [True, True, False, False, False, False, False]
    report = dict(status='PASS', groups=results, odd_matrix_controls=odd_matrix_controls())
    report['multiplication_entries'] = sum(r['multiplication_entries'] for r in results)
    root = Path(__file__).resolve().parents[1]
    (root/'results/19.56-python.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
