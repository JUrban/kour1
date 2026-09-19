#!/usr/bin/env python3
"""Exact polynomial checks supporting three comparisons; no external packages.

This verifies identities, not the surrounding infinite-group theorems or Lean.
"""
import json
from collections import defaultdict


class P(dict):
    """Integral polynomials in commuting indeterminates."""
    def __add__(self, other):
        other = const(other) if isinstance(other, int) else other
        out = defaultdict(int, self)
        for m, c in other.items():
            out[m] += c
        return P({m: c for m, c in out.items() if c})

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.items()})

    def __sub__(self, other):
        return self + -(const(other) if isinstance(other, int) else other)

    def __rsub__(self, other):
        return const(other) + -self

    def __mul__(self, other):
        other = const(other) if isinstance(other, int) else other
        out = defaultdict(int)
        for m, c in self.items():
            for n, d in other.items():
                out[tuple(sorted(m + n))] += c * d
        return P({m: c for m, c in out.items() if c})

    __rmul__ = __mul__


def const(n):
    return P({(): n}) if n else P()


def var(s):
    return P({(s,): 1})


def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]


def tensor_mul(a, b):
    """Two free associative algebras commute with each other, not internally."""
    out = defaultdict(int)
    for (p, q), c in a.items():
        for (r, s), d in b.items():
            out[p + r, q + s] += c * d
    return {m: c for m, c in out.items() if c}


def tensor_add(*terms):
    out = defaultdict(int)
    for a in terms:
        for m, c in a.items():
            out[m] += c
    return {m: c for m, c in out.items() if c}


def main():
    vectors = [[var(name + str(i)) for i in (1, 2)] for name in 'abrs']
    a, b, r, s = vectors
    assert (determinant(a, b) * determinant(r, s)
            - determinant(r, a) * determinant(s, b)
            - determinant(r, b) * determinant(a, s)) == {}

    # The eigenvector defect is precisely the characteristic polynomial.
    s, lam = var('s'), var('lambda')
    matrix = [[4*s, const(-2)], [2*s*s-2, -s]]
    vector = [const(2), 4*s-lam]
    defect = [sum(matrix[i][j]*vector[j] for j in (0, 1))
              - lam*vector[i] for i in (0, 1)]
    assert defect == [P(), lam*lam-3*s*lam-4]
    assert ((lam-matrix[0][0])*(lam-matrix[1][1])
            - matrix[0][1]*matrix[1][0]) == lam*lam-3*s*lam-4

    # 18.76: delta f = -C_ours-C_alternative for f(x,y)=alpha(x) beta(y).
    def p(t): return {((t,), ()): 1}
    def q(t): return {((), (t,)): 1}
    x, ax, ax1, y, by, by1 = p('x'), p('alpha(x)'), p('alpha(x1)'), q('y'), q('beta(y)'), q('beta(y1)')
    mul, add = tensor_mul, tensor_add
    f_g = mul(ax, by)
    f_gh = mul(add(ax, mul(x, ax1)), add(by, mul(y, by1)))
    g_f_h = mul(mul(x, y), mul(ax1, by1))
    ours = mul(mul(x, by), ax1)
    alternative = mul(mul(ax, y), by1)
    assert add(g_f_h, {m: -c for m, c in f_gh.items()}, f_g, ours, alternative) == {}
    print(json.dumps({'status': 'PASS', 'checks': [
        '21.106: determinant identity over the universal commutative polynomial ring',
        '15.89: characteristic polynomial and eigenvector defect',
        '18.76: cocycle comparison in a tensor product of free associative algebras'
    ], 'scope': 'Exact algebraic identities; no Lean replay or full theorem certification.'}, indent=2))


if __name__ == '__main__':
    main()
