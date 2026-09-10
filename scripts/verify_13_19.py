#!/usr/bin/env python3
"""Independent complete matrix certificate; no GAP or algebra packages."""
import itertools
import json
from collections import deque


def matrix_multiply(a, b):
    return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3)) % 2
                 for i in range(3) for j in range(3))


def d(a, b, c):
    return (1, a, c, 0, 1, b, 0, 0, 1)


matrices = [d(*bits) for bits in itertools.product(range(2), repeat=3)]
lookup = {m: i for i, m in enumerate(matrices)}
table = [[lookup[matrix_multiply(a, b)] for b in matrices] for a in matrices]
one, s, t = (lookup[m] for m in (d(0, 0, 0), d(1, 0, 0), d(0, 1, 0)))
inverses = [next(j for j in range(8) if table[i][j] == one and table[j][i] == one)
            for i in range(8)]
z = table[table[inverses[s]][inverses[t]]][table[s][t]]


def mul(a, b):
    return tuple(table[x][y] for x, y in zip(a, b))


def inv(a):
    return tuple(inverses[x] for x in a)


identity = (one,)*4
generators = [(s, s, one, one), (one, one, s, s),
              (t, one, t, one), (one, t, one, t)]
images = [s, s, t, t]
# Enumerate Q by multiplication in actual 3 by 3 matrix factors. Independently
# propagate the proposed generator images and detect any path inconsistency.
phi = {identity: one}
queue = deque([identity])
while queue:
    a = queue.popleft()
    for g, image in zip(generators, images):
        ag, expected = mul(a, g), table[phi[a]][image]
        if ag in phi:
            assert phi[ag] == expected
        else:
            phi[ag] = expected
            queue.append(ag)
Q = set(phi)
assert len(Q) == 256 and set(phi.values()) == set(range(8))

# Construct H separately from its diagonal and central generators.
hgens = [(s,)*4, (t,)*4, (z, z, one, one),
         (z, one, z, one), (z, one, one, z)]
H, queue = {identity}, deque([identity])
while queue:
    a = queue.popleft()
    for g in hgens:
        ag = mul(a, g)
        if ag not in H:
            H.add(ag)
            queue.append(ag)
assert len(H) == 32 and H <= Q
assert H == {a for a in Q if phi[a] == one}

for i in range(4):
    assert {a[i] for a in Q} == set(range(8))
    assert {a[i] for a in H} == set(range(8))
for a in Q:
    for b in Q:
        ab = mul(a, b)
        assert ab in Q
        assert phi[ab] == table[phi[a]][phi[b]]
    for h in H:
        assert mul(mul(inv(a), h), a) in H
for a in H:
    for b in H:
        assert mul(a, b) in H

cosets = {frozenset(mul(a, h) for h in H) for a in Q}
assert len(cosets) == 8 and set.union(*(set(c) for c in cosets)) == Q
assert all(len({phi[a] for a in c}) == 1 for c in cosets)
assert len({phi[next(iter(c))] for c in cosets}) == 8
assert table[s][s] == table[t][t] == one
assert table[table[s][t]][table[s][t]] == z != one
commutators = {table[table[inverses[a]][inverses[b]]][table[a][b]]
               for a in range(8) for b in range(8)}
assert commutators == {one, z}
assert all(table[c][c] == one for c in commutators)

print(json.dumps({
    "status": "PASS", "base_order": 8, "ambient_factors": 4,
    "Q_order": len(Q), "H_order": len(H), "quotient_order": len(cosets),
    "all_product_and_homomorphism_pairs": len(Q)**2,
    "all_normality_pairs": len(Q)*len(H),
    "all_H_product_pairs": len(H)**2,
    "surjective_projections": 8,
    "explicit_irregularity_witness": "s^2=t^2=1, (st)^2=z!=1, (D')^2=1"
}, indent=2))
