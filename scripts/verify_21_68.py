#!/usr/bin/env python3
"""Independent exact coordinate certificate for the 21.68 construction.

No GAP, external packages, floating point, or character-table database.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
import json


def compose(p, q):
    return tuple(p[q[j]] for j in range(4))


def inverse_perm(p):
    return tuple(p.index(j) for j in range(4))


def permute(v, p):
    return tuple(v[p.index(j)] for j in range(4))


identity_perm = tuple(range(4))
even_perms = [p for p in permutations(range(4))
              if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0]
even_vectors = [v for v in product(range(2), repeat=4) if sum(v) % 2 == 0]
one = ((0,) * 4, identity_perm)


def mul(a, b):
    v, p = a
    w, q = b
    pw = permute(w, p)
    return tuple((v[i] + pw[i]) % 2 for i in range(4)), compose(p, q)


def inv(a):
    v, p = a
    ip = inverse_perm(p)
    return permute(v, ip), ip


def conj(g, h):
    return mul(mul(g, h), inv(g))


def closure(gens):
    seen = {one}
    todo = [one]
    while todo:
        a = todo.pop()
        for g in gens:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                todo.append(b)
    return seen


def qmul(a, b):
    w, x, y, z = a
    u, v, s, t = b
    return (w*u-x*v-y*s-z*t, w*v+x*u+y*t-z*s,
            w*s-x*t+y*u+z*v, w*t+x*s-y*v+z*u)


K = set(product(even_vectors, even_perms))
x = ((1, 0, 1, 0), (1, 0, 3, 2))
y = ((1, 0, 0, 1), (2, 3, 0, 1))
r = ((0, 0, 0, 0), (0, 2, 3, 1))
z = ((1, 1, 1, 1), identity_perm)
assert len(K) == 96
for a in K:
    assert mul(a, inv(a)) == one
    for b in K:
        assert mul(a, b) in K
assert mul(x, x) == mul(y, y) == mul(mul(x, y), mul(x, y)) == z
assert conj(r, x) == y and conj(r, y) == mul(x, y)
assert mul(mul(r, r), r) == one
Q = closure([x, y])
H = closure([x, y, r])
assert len(Q) == 8 and len(H) == 24
derived = closure([mul(mul(mul(inv(a), inv(b)), a), b) for a in H for b in H])
assert derived == Q  # H has no quotient C2, hence no index-two subgroup.

# Construct and verify the degree-two representation via rational quaternions.
qone = (F(1), F(0), F(0), F(0))
qi = (F(0), F(1), F(0), F(0))
qj = (F(0), F(0), F(1), F(0))
qs = (F(-1, 2),) * 4
rho = {one: qone}
todo = [one]
while todo:
    h = todo.pop()
    for g, qg in [(x, qi), (y, qj), (r, qs)]:
        hg = mul(h, g)
        image = qmul(rho[h], qg)
        if hg in rho:
            assert rho[hg] == image
        else:
            rho[hg] = image
            todo.append(hg)
assert set(rho) == H
for a in H:
    for b in H:
        assert rho[mul(a, b)] == qmul(rho[a], rho[b])
traces = {h: 2*q[0] for h, q in rho.items()}
assert all(v.denominator == 1 for v in traces.values())
traces = {h: int(t) for h, t in traces.items()}
assert sum(t*t for t in traces.values()) == 24

# Enumerate the four left cosets and their induced K-action independently.
representatives = [one]
cosets = [frozenset(H)]
for k in sorted(K):
    if not any(k in c for c in cosets):
        representatives.append(k)
        cosets.append(frozenset(mul(k, h) for h in H))
assert len(cosets) == 4
coset_index = {k: j for j, c in enumerate(cosets) for k in c}
actions = {k: tuple(coset_index[mul(k, t)] for t in representatives) for k in K}
assert {k for k in K if actions[k][0] == 0} == H
for a in K:
    for b in K:
        assert actions[mul(a, b)] == compose(actions[a], actions[b])

B = [v for v in product(range(3), repeat=4) if sum(v) % 3 == 0]
assert len(B) == 27
assert len({tuple(b[j] for b in B) for j in range(4)}) == 4
assert all(permute(b, actions[k]) in B for k in K for b in B)

# Exact induced-character values in Z[zeta_3], represented by a+b*zeta_3.
roots = [(1, 0), (0, 1), (-1, -1)]
chars = {}
for b in B:
    for k in K:
        a0 = a1 = 0
        for j, t in enumerate(representatives):
            if actions[k][j] == j:
                h = mul(mul(inv(t), k), t)
                assert h in H
                trace = traces[h]
                u, v = roots[b[j]]
                a0 += trace * u
                a1 += trace * v
        chars[b, k] = (a0, a1)
norm_sum = sum(a*a - a*b + b*b for a, b in chars.values())
assert chars[(0, 0, 0, 0), one] == (8, 0)
assert norm_sum == len(B)*len(K) == 2592
value_counts = Counter(chars.values())
print(json.dumps(dict(status="PASS", K_order=len(K), H_order=len(H),
                      quaternion_order=len(Q), H_abelianization_order=len(H)//len(derived),
                      K_product_checks=len(K)**2, quaternion_representation_product_checks=len(H)**2,
                      coset_action_product_checks=len(K)**2, B_order=len(B),
                      G_order=len(chars), irreducible_degree=8,
                      exact_character_squared_norm_sum=norm_sum,
                      character_value_distribution=[dict(value=[a,b], count=c)
                          for (a,b), c in sorted(value_counts.items())]), indent=2))
