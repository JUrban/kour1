#!/usr/bin/env python3
"""Exact coordinate checks for 16.87; no GAP or external packages.

The all-ranks theorem is in research/16.87-proof.md. Here we independently
evaluate generator substitutions, without using the claimed action formula.
"""
from fractions import Fraction
from itertools import combinations, product
from math import gcd, lcm
import json
import random


def null_row(rows, rank):
    a = [[Fraction(x) for x in row] for row in rows]
    pivots = []
    for col in range(rank):
        j = next((j for j in range(len(pivots), len(a)) if a[j][col]), None)
        if j is None:
            continue
        i = len(pivots)
        a[i], a[j] = a[j], a[i]
        d = a[i][col]
        a[i] = [x/d for x in a[i]]
        for j in range(len(a)):
            if j != i:
                d = a[j][col]
                a[j] = [x-d*y for x, y in zip(a[j], a[i])]
        pivots.append(col)
    free = next(j for j in range(rank) if j not in pivots)
    w = [Fraction(int(j == free)) for j in range(rank)]
    for i, j in enumerate(pivots):
        w[j] = -a[i][free]
    scale = lcm(*(x.denominator for x in w))
    w = [int(scale*x) for x in w]
    divisor = gcd(*w)
    w = tuple(x//divisor for x in w)
    assert gcd(*w) == 1
    assert all(sum(x*y for x, y in zip(w, v)) == 0 for v in rows)
    return w


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    out = Fraction(1)
    for i in range(len(a)):
        j = next((j for j in range(i, len(a)) if a[j][i]), None)
        if j is None:
            return 0
        if i != j:
            a[i], a[j] = a[j], a[i]
            out = -out
        d = a[i][i]
        out *= d
        for j in range(i+1, len(a)):
            q = a[j][i]/d
            a[j] = [x-q*y for x, y in zip(a[j], a[i])]
    assert out.denominator == 1
    return int(out)


class Model:
    def __init__(self, rank, prime):
        self.r, self.p = rank, prime
        self.pairs = list(combinations(range(rank), 2))
        self.one = ((0,)*rank, (0,)*len(self.pairs))
        self.gens = [(tuple(int(i == j) for j in range(rank)), self.one[1])
                     for i in range(rank)]

    def mul(self, x, y):
        a, c = x
        b, d = y
        return (tuple(u+v for u, v in zip(a, b)),
                tuple((u+v+a[i]*b[j]) % self.p
                      for u, v, (i, j) in zip(c, d, self.pairs)))

    def inv(self, x):
        a, c = x
        return (tuple(-u for u in a),
                tuple((-u+a[i]*a[j]) % self.p
                      for u, (i, j) in zip(c, self.pairs)))

    def power(self, x, n):
        if n < 0:
            x, n = self.inv(x), -n
        out = self.one
        while n:
            if n & 1:
                out = self.mul(out, x)
            x, n = self.mul(x, x), n//2
        return out

    def comm(self, x, y):
        return self.mul(self.mul(self.mul(self.inv(x), self.inv(y)), x), y)

    def substitute(self, g, images):
        # Independently collect the reverse-ordered word, then commutators.
        out = self.one
        for i in reversed(range(self.r)):
            out = self.mul(out, self.power(images[i], g[0][i]))
        for exponent, (i, j) in zip(g[1], self.pairs):
            out = self.mul(out, self.power(self.comm(images[i], images[j]), exponent))
        return out

    def random_element(self, rng):
        return (tuple(rng.randrange(-9, 10) for _ in range(self.r)),
                tuple(rng.randrange(self.p) for _ in self.pairs))


rng = random.Random(1687)
totals = dict(target_sets=0, fixed_elements=0, substitution_comparisons=0,
              homomorphism_checks=0, associativity_checks=0,
              determinant_checks=0, central_power_checks=0)
records = []
for p in (2, 3, 5):
    for r in (1, 2, 3, 4, 6, 8):
        g = Model(r, p)
        before = totals.copy()
        for _ in range(40):
            a, b, c = (g.random_element(rng) for _ in range(3))
            assert g.mul(g.mul(a, b), c) == g.mul(a, g.mul(b, c))
            assert g.mul(a, g.inv(a)) == g.one
            assert g.comm(g.comm(a, b), c) == g.one
            assert g.power(g.comm(a, b), p) == g.one
            assert g.substitute(a, g.gens) == a
            totals['associativity_checks'] += 1
            for x in g.gens:
                assert g.comm(g.power(x, p), a) == g.one
                totals['central_power_checks'] += 1
        if r >= 2:
            assert g.comm(g.gens[0], g.gens[1]) != g.one
        sets = [[]]
        for k in range(1, r):
            sets.extend([[g.random_element(rng) for _ in range(k)]
                         for _ in range(12)])
        if r == 2:
            sets.extend([[(v, (c,))] for v in product(range(-3, 4), repeat=2)
                         for c in range(p)])
        for targets in sets:
            w = null_row([s[0] for s in targets], r)
            i = next(i for i in range(r) if w[i])
            epsilon = 1 if w[i] > 0 else -1
            c = g.power(g.gens[i], p*epsilon)
            images = [g.mul(x, g.power(c, wj)) for x, wj in zip(g.gens, w)]
            matrix = [[images[col][0][row] for col in range(r)] for row in range(r)]
            assert determinant(matrix) == 1+p*abs(w[i]) > 1
            totals['determinant_checks'] += 1
            f = lambda h: sum(a*b for a, b in zip(w, h[0]))
            for s in targets:
                assert g.substitute(s, images) == s
                totals['fixed_elements'] += 1
            for _ in range(3):
                a, b = g.random_element(rng), g.random_element(rng)
                actual = g.substitute(a, images)
                assert actual == g.mul(a, g.power(c, f(a)))
                assert f(actual) == (1+p*abs(w[i]))*f(a)
                assert g.substitute(g.mul(a, b), images) == g.mul(actual, g.substitute(b, images))
                totals['substitution_comparisons'] += 1
                totals['homomorphism_checks'] += 1
            totals['target_sets'] += 1
        records.append(dict(prime=p, rank=r,
                            checks={k: totals[k]-before[k] for k in totals}))
print(json.dumps(dict(status='PASS', seed=1687, totals=totals, cases=records,
                     limitation='Exact finite sanity checks; the universal proof is separate.'), indent=2))
