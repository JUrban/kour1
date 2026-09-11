#!/usr/bin/env python3
"""Exhaustive finite linear controls for the 16.20 central construction.

The group order is huge; no enumeration of its elements is claimed.
The written normal-subgroup and homomorphism classification is essential.
"""
from itertools import product
from math import prod
from pathlib import Path
import json
import re

VECTORS = (1, 2, 4, 3, 5, 6, 7)
PRIMES = (7, 11, 13, 17, 19, 23, 29)


def span(values):
    s = {0}
    for x in values:
        s |= {y ^ x for y in tuple(s)}
    return frozenset(s)


def syndrome(mask):
    s = 0
    for i, v in enumerate(VECTORS):
        if mask & (1 << i):
            s ^= v
    return s


SUBSPACES = sorted({span(vs) for vs in product(range(8), repeat=3)},
                   key=lambda s: (len(s), sorted(s)))
CODE = [m for m in range(128) if syndrome(m) == 0]


def inclusion(a, b):
    return a[0] & b[0] == a[0] and a[1] <= b[1]


def meet(a, b):
    return a[0] & b[0], a[1] & b[1]


def join(a, b):
    return a[0] | b[0], span(a[1] | b[1])


def main():
    assert len(SUBSPACES) == 16 and len(CODE) == 16
    assert all((1 << i) not in CODE for i in range(7))
    simple_orders = [p*(p*p-1)//2 for p in PRIMES]
    assert all(b % a for i, a in enumerate(simple_orders)
               for j, b in enumerate(simple_orders) if i != j)
    normal_labels = [(mask, k) for k in SUBSPACES for mask in range(128)
                     if all(v in k for i, v in enumerate(VECTORS)
                            if mask & (1 << i))]
    assert len(normal_labels) == 199
    h = frozenset([0, 1])
    interval = [n for n in normal_labels if h <= n[1]]
    assert len(interval) == 154
    allowed_total = 0
    for mask, k in normal_labels:
        allowed = [a for a in range(128) if not (a & mask)
                   and all(syndrome(a & c) in k for c in CODE)]
        assert allowed
        for a in allowed:
            # These are exactly the possible supports of nontrivial
            # factor maps, modulo choices of factor automorphisms.
            # Every map must kill K and all factors already in N.
            assert all(syndrome(a & word) in k
                       for word in range(128) if syndrome(word) in k)
            allowed_total += 1
    # Endomorphism supports of A itself: zero or every factor.
    endos = [a for a in range(128)
             if all(syndrome(a & c) == 0 for c in CODE)]
    assert endos == [0, 127]
    centre_dominions = []
    for k in SUBSPACES:
        if not h <= k:
            continue
        allowed = [a for a in range(128)
                   if all(syndrome(a & c) in k for c in CODE)]
        images = []
        for a in allowed:
            # Choose the first preimage in F_2^7 of each vector.
            images.append([syndrome(a & next(w for w in range(128)
                                            if syndrome(w) == v))
                           for v in range(8)])
        dominion = set(range(8))
        for f in images:
            for g in images:
                if all((f[v] ^ g[v]) in k for v in h):
                    dominion &= {v for v in range(8) if (f[v] ^ g[v]) in k}
        assert frozenset(dominion) == k
        centre_dominions.append(sorted(k))
    assert len(centre_dominions) == 5
    interval_set = set(interval)
    for a in interval:
        for b in interval:
            assert meet(a, b) in interval_set and join(a, b) in interval_set
    modular_checks = 0
    for a in interval:
        for c in interval:
            if inclusion(a, c):
                for b in interval:
                    assert join(a, meet(b, c)) == meet(join(a, b), c)
                    modular_checks += 1
    k1, k2, k3 = (0, span([1, 2])), (0, span([1, 4])), (0, span([1, 6]))
    left = meet(k1, join(k2, k3))
    right = join(meet(k1, k2), meet(k1, k3))
    assert left != right and left == k1 and right == (0, h)
    root = Path(__file__).resolve().parents[1]
    gap_log = (root/'results/16.20-factor-verification.log').read_text()
    assert 'Error' not in gap_log and 'Syntax' not in gap_log
    rows = re.findall(r'p=(\d+) order=(\d+) centre=2 quotient=(\d+) '
                      r'normals=\[ 1, 2, (\d+) \] PASS', gap_log)
    assert len(rows) == 7
    for row, p, s in zip(rows, PRIMES, simple_orders):
        assert tuple(map(int, row)) == (p, 2*s, s, 2*s)
    assert gap_log.endswith('DONE ALL CHECKS PASS\n')
    data = dict(problem='16.20', status='PASS', primes=PRIMES,
                simple_orders=simple_orders,
                group_order=prod(2*s for s in simple_orders)//16,
                binary_code=CODE, code_dimension=4, centre_order=8,
                normal_subgroups_by_proved_classification=len(normal_labels),
                normal_interval_above_H=len(interval),
                factor_supports_tested=allowed_total,
                endomorphism_supports=endos,
                restricted_centre_dominions=centre_dominions,
                modular_identities_checked=modular_checks,
                nondistributive_witness=[sorted(k1[1]), sorted(k2[1]), sorted(k3[1])],
                scope='Small GAP factors and exhaustive binary controls; full group proof is structural.')
    (root/'results/16.20-verification.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
