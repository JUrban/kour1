#!/usr/bin/env python3
"""Exact independent coset-inclusion controls in quasicyclic groups."""
from fractions import Fraction
from itertools import product
from random import Random
import json


def digit_map(x, p):
    x %= 1
    result, place = 0, 1
    while x:
        x *= p
        digit = x.numerator // x.denominator
        result += digit * place
        x -= digit
        place *= p
    return result


def endpoints(coset, p):
    a, n = coset
    if n is None:
        return (0, float('inf'))
    size = p**n
    left = digit_map(a, p) // size * size
    return left, left+size-1


def actual_inclusion(c, e, p):
    a, n = c
    b, m = e
    if m is None:
        return True
    return n is not None and n <= m and ((a-b)*p**m).denominator == 1


rng = Random(11116)
enumerated_cosets = 0
pair_checks = 0
for p, maximum in [(2, 8), (3, 5), (5, 4), (7, 3)]:
    size = p**maximum
    xs = [Fraction(k, size) for k in range(size)]
    assert sorted(digit_map(x, p) for x in xs) == list(range(size))
    for n in range(maximum+1):
        step = p**(maximum-n)
        for k in range(step):
            actual = sorted(digit_map(xs[k+j*step], p) for j in range(p**n))
            left, right = endpoints((xs[k], n), p)
            assert actual == list(range(left, right+1))
            enumerated_cosets += 1
    for _ in range(10000):
        c, e = [(Fraction(rng.randrange(p**12), p**12),
                 rng.choice(list(range(14))+[None])) for _ in range(2)]
        l, r = endpoints(c, p)
        ll, rr = endpoints(e, p)
        assert actual_inclusion(c, e, p) == (l >= ll and r <= rr)
        pair_checks += 1

# The ordinary numerical interval hull would give a false containment.
assert Fraction(0) < Fraction(1, 4) < Fraction(1, 2)
assert not actual_inclusion((Fraction(1, 4), 0), (Fraction(0), 1), 2)
assert [digit_map(Fraction(k, 8), 2) for k in [1, 5]] == [4, 5]
# Repeating a prime permits a diagonal subgroup which is not a box.
diagonal = {(0, 0), (1, 1)}
assert diagonal != set(product({x for x, _ in diagonal}, {y for _, y in diagonal}))
print(json.dumps({'status': 'PASS', 'finite_cosets': enumerated_cosets,
                  'exact_quasicyclic_pair_checks': pair_checks,
                  'primes': [2, 3, 5, 7], 'includes_full_group': True,
                  'digit_reversal_negative_control': 'PASS',
                  'repeated_prime_negative_control': 'PASS'}, indent=2))
