#!/usr/bin/env python3
"""Exact Clifford controls, independent of GAP's spin representations.

Basis e_I, e_i^2=1/2, e_i e_j=-e_j e_i. All arithmetic is rational.
These controls verify the explicit finite identities, not braid linearity,
the homology calculation, or Deligne's theorem.
"""
from fractions import Fraction as Q
import random


def add(a, b):
    out = a.copy()
    for k, v in b.items():
        out[k] = out.get(k, Q(0)) + v
        if not out[k]:
            del out[k]
    return out


def scale(a, q):
    return {k: v*q for k, v in a.items() if v*q}


def mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            swaps = sum((j & ((1 << k)-1)).bit_count()
                        for k in range(i.bit_length()) if i >> k & 1)
            coef = x*y*Q((-1)**swaps, 2**(i & j).bit_count())
            k = i ^ j
            out[k] = out.get(k, Q(0)) + coef
            if not out[k]:
                del out[k]
    return out


def word(gens, indices):
    a = {0: Q(1)}
    for i in indices:
        a = mul(a, gens[i])  # All these generators are involutions.
    return a


def main():
    rng = random.Random(199)
    one = {0: Q(1)}
    neg = {0: Q(-1)}
    total = dict(squares=0, adjacent=0, distant=0,
                 conjugated_relators=0, associativity=0,
                 left_regular_columns=0)
    for n in range(4, 10):
        gens = [{1 << i: Q(1), 1 << (i+1): Q(-1)} for i in range(n-1)]
        for i, a in enumerate(gens):
            assert mul(a, a) == one
            total['squares'] += 1
            for j in range(i+1, n-1):
                b = gens[j]
                if j == i+1:
                    assert add(mul(a, b), mul(b, a)) == neg
                    assert mul(mul(a, b), a) == mul(mul(b, a), b)
                    total['adjacent'] += 1
                else:
                    assert mul(a, b) == scale(mul(b, a), -1)
                    assert word(gens, [i, j, i, j]) == neg
                    total['distant'] += 1
        for _ in range(80):
            w = [rng.randrange(n-1) for _ in range(12)]
            u, inv = word(gens, w), word(gens, w[::-1])
            assert mul(u, inv) == one
            i = rng.randrange(n-2)
            adjacent = [i, i+1, i, i+1, i, i+1]
            assert mul(mul(u, word(gens, adjacent)), inv) == one
            assert mul(mul(u, word(gens, [0, 2, 0, 2])), inv) == neg
            total['conjugated_relators'] += 2
            a, b, c = [word(gens, [rng.randrange(n-1) for _ in range(4)])
                       for _ in range(3)]
            assert mul(mul(a, b), c) == mul(a, mul(b, c))
            total['associativity'] += 1
        # Compare composed left-regular operator columns, including -I.
        a, b = gens[0], gens[2]
        for mask in range(1 << n):
            v = {mask: Q(1)}
            assert mul(a, mul(b, v)) == mul(mul(a, b), v)
            assert mul(a, mul(b, mul(a, mul(b, v)))) == scale(v, -1)
            total['left_regular_columns'] += 1
        print(f'PASS n={n} clifford_dimension={1 << n} '
              f'claimed_tensor_dimension={1+n*(n-1)//2+(1 << n)}')
    print('ALL PASS', total)


if __name__ == '__main__':
    main()
