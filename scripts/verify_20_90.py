#!/usr/bin/env python3
"""Independent exact controls for the characteristic-two construction in 20.90."""
from collections import Counter, deque
from itertools import product
import hashlib
import json


def fmul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def pmul(a, b):
    """Untruncated F4[t] multiplication, packed in base four."""
    out = 0
    i = 0
    while b:
        c = b & 3
        aa, row, j = a, 0, 0
        while aa:
            row ^= fmul(aa & 3, c) << (2*j)
            aa >>= 2
            j += 1
        out ^= row << (2*i)
        b >>= 2
        i += 1
    return out


def mmul(a, b, mul=pmul):
    return (mul(a[0], b[0]) ^ mul(a[1], b[2]),
            mul(a[0], b[1]) ^ mul(a[1], b[3]),
            mul(a[2], b[0]) ^ mul(a[3], b[2]),
            mul(a[2], b[1]) ^ mul(a[3], b[3]))


ID = (1, 0, 0, 1)
X = (1, 1, 0, 1)
Y0 = (0, 1, 1, 2)


def generated(gens, mul):
    seen = {ID}
    todo = deque([ID])
    while todo:
        a = todo.popleft()
        for b in gens:
            c = mmul(a, b, mul)
            if c not in seen:
                seen.add(c)
                todo.append(c)
    return seen


def order(a, mul):
    b, n = a, 1
    while b != ID:
        b = mmul(b, a, mul)
        n += 1
        assert n <= 100000
    return n


all_matrices = list(product(range(4), repeat=4))
sl = {a for a in all_matrices if fmul(a[0], a[3]) ^ fmul(a[1], a[2]) == 1}
gen = generated([X, Y0], fmul)
assert len(sl) == 60 and gen == sl
assert [order(a, fmul) for a in [X, Y0, mmul(X, Y0, fmul)]] == [2, 5, 5]

# Independently prove simplicity using normal closures, with no subgroup library.
def inverse(a):
    return (a[3], a[1], a[2], a[0])

yi = inverse(Y0)
diagonal = mmul(mmul(mmul(yi, X, fmul), yi, fmul), yi, fmul)
assert diagonal == (2, 0, 0, 3)
assert mmul(mmul(Y0, X, fmul), yi, fmul) == (1, 0, 1, 1)
for a in range(4):
    upper, lower = (1, a, 0, 1), (1, 0, a, 1)
    duc = mmul(mmul(mmul(diagonal, upper, fmul), inverse(diagonal), fmul), inverse(upper), fmul)
    dlc = mmul(mmul(mmul(diagonal, lower, fmul), inverse(diagonal), fmul), inverse(lower), fmul)
    assert duc == (1, fmul(2, a), 0, 1)
    assert dlc == (1, 0, fmul(3, a), 1)

normal_closures = 0
for a in sorted(sl - {ID}):
    conjugates = [mmul(mmul(inverse(b), a, fmul), b, fmul) for b in sl]
    assert generated(conjugates, fmul) == sl
    normal_closures += 1
assert mmul(X, Y0, fmul) != mmul(Y0, X, fmul)

# The nonscalar matrix centralizer lemma in all of M2(F4).
algebra_count = 0
group_centralizers = Counter()
for a in all_matrices:
    scalar = a[1] == a[2] == 0 and a[0] == a[3]
    if scalar:
        continue
    centralizer = {b for b in all_matrices if mmul(a, b, fmul) == mmul(b, a, fmul)}
    span = {(u ^ fmul(v, a[0]), fmul(v, a[1]),
             fmul(v, a[2]), u ^ fmul(v, a[3])) for u, v in product(range(4), repeat=2)}
    assert centralizer == span and len(span) == 16
    assert all(mmul(b, c, fmul) == mmul(c, b, fmul) for b in span for c in span)
    algebra_count += 1
    if a in sl:
        group_centralizers[len(centralizer & sl)] += 1
assert algebra_count == 252 and group_centralizers == {3: 20, 4: 15, 5: 24}
assert [a for a in sl if a[1] == a[2] == 0 and a[0] == a[3]] == [ID]

# Direct polynomial matrix powers versus a separately maintained recurrence.
Y = (0, 1, 1, 6)  # omega + t = 2 + 4.
power = ID
prev, cur = 0, 1
for n in range(1, 257):
    power = mmul(power, Y)
    nxt = pmul(6, cur) ^ prev
    assert power == (prev, cur, cur, nxt)
    assert (nxt.bit_length() - 1) // 2 == n
    assert nxt >> (2*n) == 1
    assert power != ID
    prev, cur = cur, nxt

# A meaningful negative control: a congruence quotient need not be CN.
# Enumerate the actual two-generator image modulo t^2.
def truncated_mul(a, b):
    return pmul(a, b) & 15

image2 = generated([X, Y], truncated_mul)
scalar = (5, 0, 0, 5)  # (1+t) I, determinant 1 modulo t^2.
assert scalar in image2 and scalar != ID
assert all(mmul(scalar, a, truncated_mul) == mmul(a, scalar, truncated_mul) for a in image2)
assert {tuple(v & 3 for v in a) for a in image2} == sl
# Therefore this centralizer surjects onto the nonsoluble simple group SL2(F4).

result = {
    "finite_group_order": len(sl),
    "generator_and_product_orders": [2, 5, 5],
    "nontrivial_normal_closures_checked": normal_closures,
    "nonscalar_algebra_centralizers_checked": algebra_count,
    "nonidentity_SL2_centralizer_sizes": dict(sorted(group_centralizers.items())),
    "polynomial_power_controls": 256,
    "mod_t_squared_image_order": len(image2),
    "mod_t_squared_has_nontrivial_scalar_center": True,
    "finite_matrix_set_sha256": hashlib.sha256(json.dumps(sorted(sl)).encode()).hexdigest(),
    "status": "PASS",
}
print(json.dumps(result, indent=2, sort_keys=True))
