#!/usr/bin/env python3
"""Finite checks of the N5 formation-family calculation.

Membership in these formations depends only on group order. The
universe 1,...,210 has a cyclic-group witness for each order and
separates all five classes. This verifies the finite lattice witness,
not the infinite non-algebraicity assertion in part (a).
"""
from itertools import combinations, product
import json


def powerset(xs):
    xs = list(xs)
    return [tuple(c) for n in range(len(xs)+1) for c in combinations(xs,n)]


def prime_factors(n):
    result = set()
    p = 2
    while p*p <= n:
        if n % p == 0:
            result.add(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        result.add(n)
    return result


universe = frozenset(range(1,211))
signatures = [frozenset(n for n in universe if prime_factors(n) <= primes)
              for primes in (set(),{2},{2,3},{5})] + [universe]
assert len(set(signatures)) == 5
O,A,B,C,U = range(5)


def meet(indexes):
    r = universe
    for i in indexes:
        r = r & signatures[i]
    return signatures.index(r)


def join(indexes):
    upper = [j for j in range(5)
             if all(signatures[i] <= signatures[j] for i in indexes)]
    return meet(upper)


comparisons = {(i,j) for i,j in product(range(5),repeat=2)
               if signatures[i] <= signatures[j]}
expected = {(i,i) for i in range(5)} | {(O,j) for j in range(5)} \
           | {(i,U) for i in range(5)} | {(A,B)}
assert comparisons == expected
for indexes in powerset(range(5)):
    lo,hi = meet(indexes),join(indexes)
    assert all((lo,i) in comparisons and (i,hi) in comparisons for i in indexes)
    assert all((j,lo) in comparisons for j in range(5)
               if all((j,i) in comparisons for i in indexes))
    assert all((hi,j) in comparisons for j in range(5)
               if all((i,j) in comparisons for i in indexes))

failures = []
modular_cases = 0
for x,y,z in product(range(5), repeat=3):
    if (x,z) not in comparisons:
        continue
    modular_cases += 1
    lhs = join((x,meet((y,z))))
    rhs = meet((join((x,y)),z))
    if lhs != rhs:
        failures.append([x,y,z,lhs,rhs])
assert failures == [[A,C,B,A,B]]
assert 3 in signatures[B] and 3 not in signatures[A]

# A full power-set lattice is a positive control for the same modular test.
boolean = [frozenset(s) for s in powerset(range(4))]
positive_cases = 0
for x,y,z in product(boolean,repeat=3):
    if x <= z:
        assert x | (y & z) == (x | y) & z
        positive_cases += 1

print(json.dumps(dict(status='PASS',order_universe=[1,210],
    formation_signature_sizes=list(map(len,signatures)),
    all_subfamilies_checked=32,modular_cases=modular_cases,
    modular_failures=failures,labels=['O','A','B','C','U'],
    boolean_positive_cases=positive_cases,
    infinite_non_algebraicity_tested=False),indent=2))
