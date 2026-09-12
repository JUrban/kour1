#!/usr/bin/env python3
"""Exact rational polynomial paths, independently checked at integer inputs."""
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import random


def trim(p):
    p = list(map(Q, p))
    while p and not p[-1]:
        p.pop()
    return tuple(p)


def add(a, b):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, q):
    return trim([x*q for x in a])


def mul(a, b):
    c = [Q(0)]*(len(a)+len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def ev(a, t):
    v = Q(0)
    for c in reversed(a):
        v = v*t+c
    return v


def matadd(a, b):
    return {ij: p for ij in a.keys() | b.keys()
            if (p := add(a.get(ij, ()), b.get(ij, ())))}


def matscale(a, q):
    return {ij: p for ij, v in a.items() if (p := scale(v, q))}


def matmul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            if j == k:
                out[i, l] = add(out.get((i, l), ()), mul(x, y))
    return {ij: x for ij, x in out.items() if x}


def identity(n):
    return {(i, i): (Q(1),) for i in range(n)}


def inverse(a, n):
    I = identity(n)
    z = matadd(a, matscale(I, -1))
    result, term = I, I
    for k in range(1, n):
        term = matmul(term, z)
        result = matadd(result, matscale(term, (-1)**k))
    return result


def logarithm(a, n):
    z = matadd(a, matscale(identity(n), -1))
    result, term = {}, identity(n)
    for k in range(1, n):
        term = matmul(term, z)
        result = matadd(result, matscale(term, Q((-1)**(k+1), k)))
    return result


def power_polynomial(a, t, n):
    z = matadd(a, matscale(identity(n), -1))
    result, term, choose = identity(n), identity(n), (Q(1),)
    for k in range(1, n):
        term = matmul(term, z)
        choose = scale(mul(choose, add(t, (Q(1-k),))), Q(1, k))
        result = matadd(result, {ij: mul(p, choose) for ij, p in term.items()})
    return result


def invword(w):
    return [-x for x in reversed(w)]


def commword(u, v):
    return invword(u)+invword(v)+u+v


def word_value(w, xs, n):
    invs = [inverse(x, n) for x in xs]
    out = identity(n)
    for letter in w:
        out = matmul(out, (xs if letter > 0 else invs)[abs(letter)-1])
    return out


# This dense numeric implementation uses no polynomial arithmetic.
def densemul(a, b):
    n = len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def denseeye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def denseinverse(a):
    n = len(a)
    # Back substitution, distinct from the producer's geometric series.
    b = denseeye(n)
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            b[i][j] = -sum(a[i][k]*b[k][j] for k in range(i+1, j+1))
    return b


def densepower(a, k):
    if k < 0:
        a, k = denseinverse(a), -k
    out = denseeye(len(a))
    while k:
        if k % 2:
            out = densemul(out, a)
        a = densemul(a, a)
        k //= 2
    return out


def denseword(w, xs):
    out = denseeye(len(xs[0]))
    for letter in w:
        x = xs[abs(letter)-1]
        out = densemul(out, x if letter > 0 else denseinverse(x))
    return out


def dense(a, n, t=0):
    return [[ev(a.get((i,j), ()), t) for j in range(n)] for i in range(n)]


def path(w, a, b, n):
    xs = [matmul(power_polynomial(x, (Q(1), Q(-1)), n),
                 power_polynomial(y, (Q(0), Q(1)), n)) for x, y in zip(a, b)]
    return word_value(w, xs, n)


def main():
    rng = random.Random(2198)
    delta = commword(commword([1], [2]), commword([3], [4]))
    gamma4 = commword(commword(commword([1], [2]), [3]), [4])
    words = [[1,1], [1,1,-2,-2,-2], commword([1],[2]),
             commword(commword([1],[2]),[2]), delta, gamma4]
    counts, points, degree = 0, 0, 0
    for n in [3,4,5,6]:
        for w in words:
            for _ in range(2):
                a, b = [], []
                for dest in [a, b]:
                    for _ in range(4):
                        g = identity(n)
                        for i in range(n):
                            for j in range(i+1,n):
                                v = rng.randrange(-2,3)
                                if v:
                                    g[i,j] = (Q(v),)
                        dest.append(g)
                P = path(w,a,b,n)
                F = logarithm(P,n)
                degree = max(degree, max((len(p)-1 for p in F.values()),default=0))
                for t in range(-3,5):
                    xs = [densemul(densepower(dense(x,n),1-t),
                                   densepower(dense(y,n),t)) for x,y in zip(a,b)]
                    assert dense(P,n,t) == denseword(w,xs)
                    points += 1
                assert dense(P,n,0) == denseword(w,[dense(x,n) for x in a])
                assert dense(P,n,1) == denseword(w,[dense(x,n) for x in b])
                counts += 1
    a = [{**identity(6),(j,j+1):(Q(1),)} for j in range(4)]
    b = [{**identity(6),(j+1,j+2):(Q(1),)} for j in range(4)]
    F = logarithm(path(delta,a,b,6),6)
    assert F[0,4] == tuple(map(Q,[1,-4,6,-4,1]))
    assert F[1,5] == tuple(map(Q,[0,0,0,0,1]))
    directions = {tuple(ev(F.get(ij,()),t)/ev(F[0,4],t)
                        for ij in [(0,4),(1,5),(0,5)]) for t in range(2,102)}
    assert len(directions) == 100
    record = dict(random_paths=counts, integer_evaluations=points,
                  dimensions=[3,4,5,6], words=len(words), maximum_log_degree=degree,
                  explicit_delta2_log={str((i+1,j+1)): [str(c) for c in p]
                                       for (i,j),p in sorted(F.items())},
                  distinct_explicit_directions=100)
    Path('results/21.98-path-controls.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True))
    print('PASS_2198_PATH_PYTHON paths=48 integer_evaluations=384 directions=100')


if __name__ == '__main__':
    main()
