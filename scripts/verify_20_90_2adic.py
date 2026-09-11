#!/usr/bin/env python3
"""Exact mod-4 controls for the separate 2-adic proof of 20.90."""
from collections import deque
from itertools import product
import json

# Encode a+b*omega by a+4*b, with omega^2=-omega-1 over Z/4.
def add(x, y):
    return ((x % 4 + y % 4) % 4) + 4*((x // 4 + y // 4) % 4)


def neg(x):
    return (-x % 4) + 4*((-(x // 4)) % 4)


def mul(x, y):
    a, b = x % 4, x // 4
    c, d = y % 4, y // 4
    return ((a*c-b*d) % 4) + 4*((a*d+b*c-b*d) % 4)


def reduce(x):
    return (x % 2) + 2*((x // 4) % 2)


def matrix_mul(a, b):
    return (add(mul(a[0], b[0]), mul(a[1], b[2])),
            add(mul(a[0], b[1]), mul(a[1], b[3])),
            add(mul(a[2], b[0]), mul(a[3], b[2])),
            add(mul(a[2], b[1]), mul(a[3], b[3])))


identity = (1, 0, 0, 1)
sl = set()
trace_zero = []
for a in product(range(16), repeat=4):
    determinant = add(mul(a[0], a[3]), neg(mul(a[1], a[2])))
    if determinant != 1:
        continue
    sl.add(a)
    if add(a[0], a[3]) == 0:
        assert tuple(map(reduce, a)) != identity
        trace_zero.append(a)
assert len(sl) == 3840 and trace_zero

generators = [(1, 1, 0, 1), (1, 4, 0, 1), (1, 0, 1, 1), (1, 0, 4, 1)]
seen = {identity}
todo = deque([identity])
while todo:
    a = todo.popleft()
    for b in generators:
        c = matrix_mul(a, b)
        if c not in seen:
            seen.add(c)
            todo.append(c)
assert seen == sl
reductions = {tuple(map(reduce, a)) for a in sl}
assert len(reductions) == 60
kernel = {a for a in sl if tuple(map(reduce, a)) == identity}
assert len(kernel) == 64
minus_identity = (3, 0, 0, 3)
assert minus_identity in sl and minus_identity != identity
assert all(matrix_mul(a, minus_identity) == matrix_mul(minus_identity, a) for a in sl)

print(json.dumps({
    "ring_elements": 16,
    "all_matrices_checked": 16**4,
    "SL2_mod_4_order": len(sl),
    "four_elementary_generators_cover_SL2": seen == sl,
    "trace_zero_matrices_with_nonidentity_reduction": len(trace_zero),
    "mod_2_image_order": len(reductions),
    "mod_2_kernel_order": len(kernel),
    "minus_identity_is_nontrivial_central": True,
    "status": "PASS",
}, indent=2, sort_keys=True))
