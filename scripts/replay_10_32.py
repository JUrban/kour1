#!/usr/bin/env python3
"""Independently replay GAP witnesses using Python permutations and integers."""
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def partitions(n, largest=None):
    if n == 0:
        yield ()
        return
    if largest is None:
        largest = n
    for first in range(min(n, largest), 0, -1):
        for rest in partitions(n-first, first):
            yield (first,) + rest


def prime(n):
    return n >= 2 and all(n % k for k in range(2, int(n**0.5)+1))


def multiply(a, b):
    """GAP convention: apply a first, then b."""
    return tuple(b[x-1] for x in a)


def power(a, k):
    if k < 0:
        inverse = [0]*len(a)
        for i, x in enumerate(a, 1):
            inverse[x-1] = i
        a, k = tuple(inverse), -k
    ans = tuple(range(1, len(a)+1))
    while k:
        if k & 1:
            ans = multiply(ans, a)
        a = multiply(a, a)
        k //= 2
    return ans


def cycle_type(a):
    assert sorted(a) == list(range(1, len(a)+1))
    remaining = set(range(1, len(a)+1))
    lengths = []
    while remaining:
        x = min(remaining)
        length = 0
        while x in remaining:
            remaining.remove(x)
            length += 1
            x = a[x-1]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def representative(parts):
    a = []
    start = 1
    for length in parts:
        a.extend(range(start+1, start+length))
        a.append(start)
        start += length
    return tuple(a)


def main():
    cert = ROOT/'results/10.32-witnesses.json'
    records = json.loads(cert.read_text())
    expected = {(n, q, p) for n in range(10, 26)
                for q in range(5, n//2+1) if prime(q) and 8*q > 3*n+8
                for p in partitions(n)}
    seen = set()
    counts = Counter()
    for n, q, parts, a, b in records:
        key = (n, q, tuple(sorted(parts, reverse=True)))
        assert key in expected and key not in seen
        seen.add(key)
        a, b = tuple(a), tuple(b)
        odd = (n-len(parts)) % 2
        assert cycle_type(a) == ((2*q,) if odd else (q, q)) + (1,)*(n-2*q)
        assert cycle_type(b) == (q, q) + (1,)*(n-2*q)
        target = representative(parts)
        assert multiply(a, b) == target
        order_a = 2*q if odd else q
        for r in (2*q+1, -2*q-1):
            for s in (2*q+2, -2*q-2):
                x, y = power(a, pow(r, -1, order_a)), power(b, pow(s, -1, q))
                assert multiply(power(x, r), power(y, s)) == target
                conjugate = multiply(multiply(power(y, -s), x), power(y, s))
                assert multiply(power(y, s), power(conjugate, r)) == target
                counts['root_identities'] += 2
        counts['odd' if odd else 'even'] += 1
    assert seen == expected

    # Exact rational margins for the analytic estimate, without logarithmic rounding.
    assert Fraction(101624, 100000) < Fraction(49, 48)
    assert Fraction(11, 24)-Fraction(49, 128) == Fraction(29, 384)
    assert Fraction(29, 384)-Fraction(1, 16) == Fraction(5, 384)
    assert Fraction(5*1126, 384) > Fraction(49, 48)
    assert Fraction(8, 3)+Fraction(5, 96) == Fraction(87, 32) < Fraction(11, 4)
    assert 11**6 < 563*4**6

    status = json.loads((ROOT/'results/10.32-gap-status.json').read_text())
    assert status['status'] == 'PASS' and status['returncode'] == 0
    assert status['clean_log'] and status['complete']
    for name, digest in status['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
    result = dict(status='PASS', witnesses=len(records), degree_prime_pairs=len({x[:2] for x in seen}),
                  counts=dict(counts), exact_rational_margins=6,
                  certificate_sha256=hashlib.sha256(cert.read_bytes()).hexdigest(),
                  scope='Independent finite witness replay; analytic estimates imported.')
    (ROOT/'results/10.32-replay-summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS_1032_REPLAY', json.dumps(result))


if __name__ == '__main__':
    main()
