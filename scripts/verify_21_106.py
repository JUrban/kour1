#!/usr/bin/env python3
"""Exact sanity checks for the Heisenberg counterexample to 21.106.

This is NOT a finite verification of the infinite theorem. It independently
checks group arithmetic and evaluates the stated first-order formula in small
finite quotients, without replacing that formula by a determinant condition.
The infinite proof is in research/21.106-proof.md.
"""
from itertools import product
from math import gcd
import json


def mul(x, y, modulus=None):
    a, b, c = x
    d, e, f = y
    out = (a + d, b + e, c + f + a * e)
    return tuple(v % modulus for v in out) if modulus else out


def inv(x, modulus=None):
    a, b, c = x
    out = (-a, -b, a * b - c)
    return tuple(v % modulus for v in out) if modulus else out


def comm(x, y, modulus=None):
    return mul(mul(mul(inv(x, modulus), inv(y, modulus), modulus), x, modulus), y, modulus)


def arithmetic_checks():
    identity = (0, 0, 0)
    points = list(product(range(-2, 3), repeat=3))
    pairs = 0
    for x in points:
        assert mul(x, inv(x)) == identity == mul(inv(x), x)
        for y in points:
            assert comm(x, y) == (0, 0, x[0] * y[1] - y[0] * x[1])
            for n in (2, 3, 4, 5):
                reduce = lambda t: tuple(a % n for a in t)
                assert reduce(mul(x, y)) == mul(reduce(x), reduce(y), n)
            pairs += 1
    return {"integral_elements": len(points), "integral_pairs": pairs,
            "reduction_moduli": [2, 3, 4, 5]}


def evaluate_formula(n):
    """Evaluate Cent, P, Q, and phi by finite group operations and sets."""
    identity = (0, 0, 0)
    elements = list(product(range(n), repeat=3))
    whole = set(elements)
    centralizers = {u: {t for t in elements if comm(u, t, n) == identity}
                    for u in elements}
    center = {u for u in elements if centralizers[u] == whole}
    p_values = {u for u in elements
                if center <= {comm(u, t, n) for t in elements}}
    phi_values = set()
    witnesses = 0
    for u in sorted(p_values):
        for v in sorted(p_values):
            # This is the actual set product in Q, not a determinant shortcut.
            product_set = {mul(h, k, n) for h in centralizers[u]
                           for k in centralizers[v]}
            q_value = product_set == whole
            determinant_unit = gcd(u[0] * v[1] - v[0] * u[1], n) == 1
            assert q_value == determinant_unit
            if q_value:
                phi_values.add(comm(u, v, n))
                witnesses += 1
    expected = {(0, 0, a) for a in range(n) if gcd(a, n) == 1}
    assert phi_values == expected
    return {"modulus": n, "group_order": len(elements),
            "center_size": len(center), "P_values": len(p_values),
            "witness_pairs": witnesses, "phi_values": sorted(phi_values)}


if __name__ == "__main__":
    print(json.dumps({"arithmetic": arithmetic_checks()}, sort_keys=True), flush=True)
    for modulus in (2, 3, 4, 5):
        print(json.dumps(evaluate_formula(modulus), sort_keys=True), flush=True)
    print("PASS: bounded arithmetic and finite-quotient formula checks; see written proof for infinite claim.")
