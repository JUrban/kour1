#!/usr/bin/env python3
"""Independent deletion enumeration and actual factorization controls."""
from collections import Counter
from itertools import product
import json
from pathlib import Path
import random
import time

from palindromic_length import (free_reduce, involution_reduce, encode,
                               pairing_table, palindromic_factorization)


def brute_deletions(word):
    n = len(word)
    best = n
    for bits in range(1 << n):
        removed = n-bits.bit_count()
        if removed >= best:
            continue
        kept = [word[i] for i in range(n) if bits & (1 << i)]
        if not involution_reduce(kept):
            best = removed
    return best


def frid_at_most_two(word):
    # Independent direct enumeration of the reduced-word form A P Q A^-1,
    # from Frid2025 Theorem1. P and Q are literal palindromes.
    n = len(word)
    for a in range(n//2+1):
        if a and word[-a:] != [-x for x in word[:a][::-1]]:
            continue
        middle = word[a:n-a]
        for cut in range(len(middle)+1):
            left, right = middle[:cut], middle[cut:]
            if left == left[::-1] and right == right[::-1]:
                return True
    return False


def reduced_words(rank, maximum):
    yield []
    frontier = [[]]
    letters = list(range(1, rank+1))+list(range(-rank, 0))
    for _ in range(maximum):
        frontier = [w+[a] for w in frontier for a in letters if not w or w[-1] != -a]
        yield from frontier


start = time.monotonic()
brute_checks = 0
for n in range(9):
    for w in product(range(3), repeat=n):
        cost, _ = pairing_table(w)
        assert cost[0][n] == brute_deletions(w)
        brute_checks += 1
print('PASS_DELETION_ENUMERATION words='+str(brute_checks), flush=True)

cases, distribution = [], Counter()
max_factor_length = 0
for rank, maximum in [(2, 8), (3, 6)]:
    for w in reduced_words(rank, maximum):
        result = palindromic_factorization(w)
        factors = result['palindromes']
        assert result['length'] == len(factors)
        assert all(p and p == p[::-1] and free_reduce(p) == p for p in factors)
        assert free_reduce([x for p in factors for x in p]) == w
        assert (result['length'] <= 2) == frid_at_most_two(w)
        parity_bound = sum(c % 2 for c in Counter(map(abs, w)).values())
        assert parity_bound <= result['length'] <= len(w)
        a, b = result['reflection_lengths']
        assert a % 2 == 0 and b % 2 == 1 and abs(a-b) == 1
        max_factor_length = max([max_factor_length]+list(map(len, factors)))
        distribution[(rank, result['length'])] += 1
        cases.append([w, factors, result['length']])
exhaustive_cases = len(cases)
print('PASS_FREE_WORDS cases='+str(exhaustive_cases), flush=True)

special_cases = 0
for n in range(1, 21):
    # Independent mod-2 abelianization lower bound proves the first value.
    w = list(range(1, n+1))
    result = palindromic_factorization(w)
    assert result['length'] == n
    cases.append([w, result['palindromes'], n])
    # Saarela's bounded-length family, also Example1 in Frid2025.
    w = list(range(1, n+1))+[n+1, n+2]+list(range(n, 0, -1))
    result = palindromic_factorization(w)
    assert result['length'] == 3
    cases.append([w, result['palindromes'], 3])
    special_cases += 2
rng = random.Random(1609)
for _ in range(100):
    w = free_reduce([rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(40)])
    result = palindromic_factorization(w)
    assert len(result['palindromes']) == result['length']
    assert all(p and p == p[::-1] for p in result['palindromes'])
    assert free_reduce([x for p in result['palindromes'] for x in p]) == w
    cases.append([w, result['palindromes'], result['length']])

# GAP reads literal integer lists and checks in an actual free group.
path = Path('results/16.9-witnesses.g')
with path.open('w') as stream:
    stream.write('PalindromicCases:=[\n')
    stream.write(',\n'.join(json.dumps(row) for row in cases))
    stream.write('\n];\n')
report = dict(status='PASS', brute_deletion_words=brute_checks,
              exhaustive_free_words=exhaustive_cases, frid_two_factor_checks=exhaustive_cases,
              special_cases=special_cases, random_long_cases=100, gap_witness_cases=len(cases),
              maximum_exhaustive_factor_length=max_factor_length,
              distributions={str(k): v for k, v in sorted(distribution.items())},
              seconds=time.monotonic()-start)
Path('results/16.9-python-summary.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
