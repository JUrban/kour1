#!/usr/bin/env python3
"""Reconstruct Fable's 512-element example directly from its bilinear law.

Standard library only. No author GAP presentation or saved group is loaded.
The cocycle identity is checked on all triples in F_2^6; the resulting group
law is then used to check every claimed subgroup and quotient property.
"""
from collections import deque
import json


def cocycle(v, w):
    diagonal = (1, 4, 2)  # u12, u23, u13 in F_2^3
    cross = {(0, 1): 1, (0, 2): 2, (1, 2): 4}
    result = 0
    for i in range(3):
        if ((v >> (2*i)) & 1) & ((w >> (2*i+1)) & 1):
            result ^= diagonal[i]
    for (i, j), basis in cross.items():
        coefficient = (((v >> (2*i)) & 1) & ((w >> (2*j+1)) & 1)) ^ (
            ((v >> (2*i+1)) & 1) & ((w >> (2*j)) & 1))
        if coefficient:
            result ^= basis
    return result


C = [[cocycle(v, w) for w in range(64)] for v in range(64)]
for x in range(64):
    assert C[0][x] == C[x][0] == 0
    for y in range(64):
        for z in range(64):
            assert C[x][y] ^ C[x ^ y][z] == C[y][z] ^ C[x][y ^ z]


def mul(x, y):
    return x ^ y ^ (C[x & 63][y & 63] << 6)


def inv(x):
    return x ^ (C[x & 63][x & 63] << 6)


def subgroup(generators):
    result = {0}
    todo = deque([0])
    while todo:
        x = todo.popleft()
        for g in generators:
            y = mul(x, g)
            if y not in result:
                result.add(y)
                todo.append(y)
    return result


def normal(S):
    return all(mul(mul(inv(g), x), g) in S for g in range(512) for x in S)


e1, f1, e2, f2, e3, f3, u12, u13, u23 = [1 << i for i in range(9)]
Q = subgroup([e1, f1, e2, f2, e3, f3, u12, u13, u23])
assert Q == set(range(512))
assert all(mul(x, inv(x)) == mul(inv(x), x) == 0 for x in Q)
N = [subgroup([e1, f1, u12, u13]), subgroup([e2, f2, u12, u23]),
     subgroup([e3, f3, u13, u23])]
H = subgroup([mul(mul(e1, e2), u23), mul(mul(f1, f2), u23),
              mul(mul(e2, e3), u23), mul(mul(f2, f3), u23),
              mul(u12, u23), mul(u13, u23)])
assert len(H) == 64 and normal(H)
assert [len(S) for S in N] == [16, 16, 16] and all(normal(S) for S in N)
assert set.intersection(*N) == {0}
assert all({mul(h, n) for h in H for n in S} == Q for S in N)
cosets = {frozenset(mul(x, h) for h in H) for x in Q}
representatives = [min(coset) for coset in cosets]
assert len(cosets) == 8
involutions = sum(x not in H and mul(x, x) in H for x in representatives)
nonabelian = any(mul(mul(inv(x), inv(y)), mul(x, y)) not in H
                 for x in representatives for y in representatives)
assert nonabelian and involutions == 5  # characterizes D8 among groups of order 8
print(json.dumps({"cocycle_triples_checked": 64**3, "order_Q": len(Q),
                  "order_H": len(H), "orders_N": [len(S) for S in N],
                  "all_normal": True, "intersection_N": 1,
                  "all_HN_equal_Q": True, "quotient_order": len(cosets),
                  "quotient_nonabelian": nonabelian,
                  "quotient_involutions": involutions, "quotient": "D8",
                  "status": "passed"}, indent=2))
