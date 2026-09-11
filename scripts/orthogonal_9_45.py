#!/usr/bin/env python3
"""Exact coordinate criterion for S(r/m); see research/9.45-proof.md."""
from fractions import Fraction
from itertools import product
from math import gcd, lcm


def normalize(coordinates):
    a = [Fraction(x) for x in coordinates]
    if not a:
        raise ValueError("positive dimension required")
    m = lcm(*(x.denominator for x in a))
    return tuple(int(x * m) % m for x in a), m


def splitting_vectors(r, m):
    """Return positive-first representatives w=m*b of all splitting lines.

    r is reduced modulo m and m is the least denominator. No floats,
    factorization, orthogonality search, or lattice reduction is used.
    """
    r = tuple(r)
    n = len(r)
    if not n or m < 1 or any(not 0 <= x < m for x in r):
        raise ValueError("invalid residue input")
    if gcd(m, *r) != 1:
        raise ValueError("denominator is not minimal")
    answer = []
    for j, x in enumerate(r):
        if x == 0:
            w = [0] * n
            w[j] = m
            answer.append(tuple(w))
    for k in range(1, m):
        s = [(k * x) % m for x in r]
        ties = sum(2 * x == m for x in s)
        if ties > 2:
            continue
        choices = [(-x, x) if 2 * x == m else
                   (x if 2 * x < m else x - m,) for x in s]
        for w in product(*choices):
            if next(x for x in w if x) < 0:
                continue
            q = sum(x * x for x in w)
            if all(m * x % q == 0 for x in w) and \
                    sum(x * y for x, y in zip(r, w)) % q == 0:
                answer.append(w)
    return answer


def orthogonal_basis(coordinates):
    """Return an orthogonal rational basis, or None if none exists."""
    r, m = normalize(coordinates)
    vectors = splitting_vectors(r, m)
    if len(vectors) != len(r):
        return None
    return [[Fraction(x, m) for x in w] for w in vectors]
