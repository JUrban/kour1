#!/usr/bin/env python3
"""Independent integer/permutation certificate for Kourovka20.108(a),(b)."""
from itertools import product
from math import prod
import hashlib

P, Q, L = 11, 5, 3
POINTS = list(product(range(P), range(P), range(Q)))
INDEX = {v: i for i, v in enumerate(POINTS)}
LP = [pow(L, i, P) for i in range(Q)]


def mul(v, w):
    x, y, k = v
    a, b, c = w
    return ((x + LP[k] * a) % P, (y + LP[2*k % Q] * b) % P, (k+c) % Q)


def theta(v):
    x, y, k = v
    return (y, LP[-k % Q]*x % P, 2*k % Q)


def hol(v, par):
    a, b, c, d, e, f, j = par
    x, y, k = v
    return ((a*x+b+c*LP[k]) % P,
            (d*y+e+f*LP[2*k % Q]) % P, (k+j) % Q)


def conjugated_parameters(par):
    a, b, c, d, e, f, j = par
    z = LP[-j % Q]
    return (d, e, f, z*a % P, z*c % P, z*b % P, 2*j % Q)


def permutation(fn):
    return tuple(INDEX[fn(v)] for v in POINTS)


def compose(a, b):
    return tuple(a[j] for j in b)


def fit_hol(h):
    out = [POINTS[i] for i in h]
    c = out[INDEX[(0, 0, 0)]][2]
    if any(w[2] != (v[2]+c) % Q for v, w in zip(POINTS, out)):
        return None
    z0 = out[INDEX[(0, 0, 0)]]
    z1 = out[INDEX[(0, 0, 1)]]
    a = (out[INDEX[(1, 0, 0)]][0]-z0[0]) % P
    d = (out[INDEX[(0, 1, 0)]][1]-z0[1]) % P
    if not a or not d:
        return None
    cc = (z1[0]-z0[0])*pow(L-1, -1, P) % P
    f = (z1[1]-z0[1])*pow(L*L-1, -1, P) % P
    par = (a, (z0[0]-cc) % P, cc, d, (z0[1]-f) % P, f, c)
    return par if permutation(lambda v: hol(v, par)) == h else None


gens = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
center = [v for v in POINTS if all(mul(v, g) == mul(g, v) for g in gens)]
assert center == [(0, 0, 0)]

# Enumerate every invertible 2x2 matrix and every possible induced C5 automorphism.
normalizers = {u: 0 for u in range(1, Q)}
matrices = 0
for a, b, c, d in product(range(P), repeat=4):
    if (a*d-b*c) % P == 0:
        continue
    matrices += 1
    for u in range(1, Q):
        # M diag(L,L^2) = diag(L^u,L^(2u)) M.
        if ((a*L-LP[u]*a) % P == 0 and
            (b*L*L-LP[u]*b) % P == 0 and
            (c*L-LP[2*u % Q]*c) % P == 0 and
            (d*L*L-LP[2*u % Q]*d) % P == 0):
            normalizers[u] += 1
assert matrices == 13200
assert normalizers == {1: 100, 2: 0, 3: 0, 4: 0}
print('AUTOMORPHISMS GL2_matrices=13200 quotient_units=4 counts=', normalizers)

t = permutation(theta)
t2 = compose(t, t)
t3 = compose(t, t2)
assert compose(t, t3) == tuple(range(605))
assert fit_hol(t2) is None
assert all(POINTS[t2[i]][2] == -v[2] % Q for i, v in enumerate(POINTS))

holgens = [(2,0,0,1,0,0,0), (1,1,0,1,0,0,0), (1,0,1,1,0,0,0),
           (1,0,0,2,0,0,0), (1,0,0,1,1,0,0), (1,0,0,1,0,1,0),
           (1,0,0,1,0,0,1)]
for par in holgens:
    h = permutation(lambda v: hol(v, par))
    actual = compose(t, compose(h, t3))
    assert fit_hol(actual) == conjugated_parameters(par)

# Every quotient shift and both nonzero scales; all binary coefficient choices.
# These 8000 controls test the full formula beyond the generator check.
checks = 0
for j, a, d in product(range(Q), range(1, P), range(1, P)):
    for b, c, e, f in product(range(2), repeat=4):
        par = (a,b,c,d,e,f,j)
        h = permutation(lambda v: hol(v, par))
        actual = compose(t, compose(h, t3))
        expected = permutation(lambda v: hol(v, conjugated_parameters(par)))
        assert actual == expected
        checks += 1
assert checks == 8000

# Omitting the k-dependent multiplier must fail the normalizer check.
bad = permutation(lambda v: (v[1], v[0], 2*v[2] % Q))
bad_inv = compose(bad, compose(bad, bad))
bad_failures = 0
for par in holgens:
    h = permutation(lambda v: hol(v, par))
    bad_failures += fit_hol(compose(bad, compose(h, bad_inv))) is None
assert bad_failures > 0
print('PERMUTATIONS points=605 generators=7 mixed_parameter_checks=8000',
      'negative_control_failures=', bad_failures)
print('THETA sha256=', hashlib.sha256(repr(t).encode()).hexdigest())
print('DONE center=1 automorphism_order=12100 holomorph_order=7320500',
      'theta_order=4 theta_square_outside_holomorph=true PASS')
