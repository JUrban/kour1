#!/usr/bin/env python3
"""Exact rational polynomial controls; no GAP data or symbolic libraries."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

N = 4
Z = (0,)*N


class P(dict):
    def __init__(self, value=0):
        if isinstance(value, dict):
            super().__init__((m, F(c)) for m, c in value.items() if c)
        else:
            super().__init__({Z: F(value)} if value else {})

    def __add__(self, other):
        other = P(other)
        return P({m: self.get(m, 0)+other.get(m, 0) for m in self.keys() | other.keys()})

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for a, x in self.items():
            for b, y in P(other).items():
                m = tuple(i+j for i, j in zip(a, b))
                out[m] = out.get(m, 0)+x*y
        return P(out)

    __rmul__ = __mul__

    def degree(self):
        return max(map(sum, self), default=-1)

    def evaluate(self, a, p):
        out = 0
        for m, c in self.items():
            v = c.numerator*pow(c.denominator, -1, p)
            for t, j in zip(a, m):
                v = v*pow(t, j, p) % p
            out = (out+v) % p
        return out


variables = [P({tuple(int(i == j) for j in range(N)): 1}) for i in range(N)]


def zero(n):
    return [[P() for _ in range(n)] for _ in range(n)]


def identity(n):
    return [[P(int(i == j)) for j in range(n)] for i in range(n)]


def add(a, b):
    return [[x+y for x, y in zip(u, v)] for u, v in zip(a, b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def mul(a, b):
    n = len(a)
    return [[sum((a[i][r]*b[r][j] for r in range(n)), P())
             for j in range(n)] for i in range(n)]


def exp(a):
    out = power = identity(len(a))
    fact = 1
    for j in range(1, len(a)):
        power = mul(power, a)
        fact *= j
        out = add(out, scale(F(1, fact), power))
    assert mul(power, a) == zero(len(a))
    return out


def log(a):
    n = len(a)
    t = add(a, scale(-1, identity(n)))
    out, power = zero(n), identity(n)
    for j in range(1, n):
        power = mul(power, t)
        out = add(out, scale(F((-1)**(j+1), j), power))
    assert mul(power, t) == zero(n)
    return out


def check(name, left):
    def X(a):
        out = zero(N+1)
        mat = left(a)
        for i in range(N):
            for j in range(N):
                out[i][j] = P(mat[i][j])
            out[i][N] = P(a[i])
        return out

    def W(a):
        return [row[N] for row in exp(X(a))[:N]]

    def C(a, b):
        matrix = log(mul(exp(X(a)), exp(X(b))))
        column = [row[N] for row in matrix[:N]]
        assert matrix == X(column), 'formal BCH closure'
        return column

    basis = [[P(int(i == j)) for j in range(N)] for i in range(N)]
    ls = [left(x) for x in basis]
    for i, j in product(range(N), repeat=2):
        bracket = add(mul(ls[i], ls[j]), scale(-1, mul(ls[j], ls[i])))
        vector = [ls[i][r][j]-ls[j][r][i] for r in range(N)]
        assert bracket == left(vector), 'pre-Lie identity on basis'
    x = [P() for _ in range(N)]
    stages = []
    for i in range(1, N+1):
        r = [a-b for a, b in zip(variables, W(x))]
        assert all(not q for q in r[N+1-i:]), 'residual in flag'
        x = C(x, r)
        stages.append(max(q.degree() for q in x))
    assert W(x) == variables, 'formal polynomial right inverse'
    lam = [row[:N] for row in exp(X(x))[:N]]
    poly = add(lam, scale(-1, identity(N)))
    assert [[P({m: c for m, c in q.items() if sum(m) == 1}) for q in row]
            for row in poly] == left(variables)
    assert all(q.get(Z, 0) == 0 for row in poly for q in row)
    d = max(q.degree() for row in poly for q in row)
    # Rational polynomial sum: record exactly which homogeneous degrees
    # survive each base-2 average after reduction to the finite field.
    modular = []
    for p in [5, 7, 11, 17, 31, 127]:
        order = 1
        while pow(2, order, p) != 1:
            order += 1
        average = []
        for row in poly:
            resultrow = []
            for q in row:
                r = {}
                for m, c in q.items():
                    coeff = c.numerator*pow(c.denominator, -1, p) % p
                    factor = -sum(pow(2, i*(sum(m)-1), p) for i in range(p-1)) % p
                    if coeff*factor % p:
                        r[m] = coeff*factor % p
                resultrow.append(r)
            average.append(resultrow)
        target = [[{m: c.numerator*pow(c.denominator, -1, p) % p
                    for m, c in q.items() if c.numerator % p}
                   for q in row] for row in left(variables)]
        equal = average == target
        if order > d:
            assert equal
        # Literal evaluations separately check the sign, endpoints, and
        # repeated orbit in the printed formula (including nonprimitive 2).
        points = list(product(range(3), repeat=N))
        comparisons, failures = 0, 0
        for a in points:
            for row, targetrow in zip(poly, left(a)):
                for q, expected in zip(row, targetrow):
                    total = -sum(pow(2, -i, p)*q.evaluate(
                        tuple(pow(2, i, p)*v % p for v in a), p)
                                 for i in range(p-1)) % p
                    failures += total != P(expected).evaluate(a, p)
                    comparisons += 1
        if equal:
            assert failures == 0
        modular.append(dict(p=p, order_of_2=order, formal_average_equal=equal,
                            evaluated_entries=comparisons, failed_entries=failures))
    return dict(name=name, correction_degrees=stages, lambda_degree=d,
                omega_terms=[len(q) for q in x], basis_pre_lie_pairs=N*N,
                modular=modular,
                omega=[[[list(m), str(c)] for m, c in sorted(q.items())] for q in x])


def psnz(a, j=0, k=0, y=1):
    # Example 7.2, basis S,P,Q,R, column convention.
    s, u, v, w = a
    out = zero(N)
    out[0][1] = y*w
    out[0][2] = -y*v
    out[0][3] = y*u+k*w
    out[1][2] = -s
    out[1][3] = j*w
    out[2][3] = -s
    return out


def associative(a):
    # Ideal (t) in Q[t]/(t^5), basis t^4,t^3,t^2,t.
    return [[P(a[3-j+i]) if i < j else P() for j in range(N)] for i in range(N)]


rows = [check('PSNZ_j0_k0_y1', psnz),
        check('PSNZ_j2_k3_y2', lambda a: psnz(a, 2, 3, 2)),
        check('associative_truncated_polynomials', associative)]
out = dict(status='PASS', method='exact rational sparse polynomials and modular evaluation',
           rows=rows)
path = Path(__file__).resolve().parents[1]/'results/20.92a-python.json'
path.write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out), flush=True)
