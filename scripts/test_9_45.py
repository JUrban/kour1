#!/usr/bin/env python3
"""Independent finite basis search; exact covolumes, no splitting test."""
import hashlib
import json
import time
from collections import Counter
from itertools import product
from math import gcd, isqrt
from pathlib import Path

from orthogonal_9_45 import normalize, splitting_vectors

ROOT = Path(__file__).resolve().parents[1]


def dot(v, w):
    return sum(x * y for x, y in zip(v, w))


def primal_search(r, m):
    n = len(r)
    # All lattice vectors of length at most 1, from all cosets in [-1,1]^n.
    vectors = set()
    for k in range(m):
        s = [(k * x) % m for x in r]
        choices = [(-m, 0, m) if x == 0 else (x - m, x) for x in s]
        for w in product(*choices):
            q = dot(w, w)
            if 0 < q <= m * m and next(x for x in w if x) > 0:
                vectors.add(w)
    target = m ** (2 * n - 2)
    vs = sorted((dot(w, w), w) for w in vectors if target % dot(w, w) == 0)
    nodes = 0

    def visit(indices, chosen, remaining):
        nonlocal nodes
        nodes += 1
        if len(chosen) == n:
            return chosen if remaining == 1 else None
        if len(indices) < n - len(chosen):
            return None
        for pos, idx in enumerate(indices):
            q, w = vs[idx]
            if remaining % q:
                continue
            nxt = [j for j in indices[pos + 1:] if dot(w, vs[j][1]) == 0]
            result = visit(nxt, chosen + [w], remaining // q)
            if result is not None:
                return result
        return None

    return visit(list(range(len(vs))), [], target), len(vectors), nodes


def projective_residues(n, m):
    units = [u for u in range(m) if gcd(u, m) == 1]
    for r in product(range(m), repeat=n):
        if gcd(m, *r) != 1:
            continue
        if all(r <= tuple((u * x) % m for x in r) for u in units):
            yield r


def prime_power_criterion(r, m):
    p = next((d for d in range(2, isqrt(m) + 1) if m % d == 0), m)
    t, k = m, 0
    while t % p == 0:
        t //= p
        k += 1
    if t != 1:
        return None
    support = [x for x in r if x]
    if len(support) <= 1:
        return True
    if len(support) != 2:
        return False
    s0, s1 = support
    for c in range(1, k + 1):
        d = p ** c
        for u in range(-isqrt(d), isqrt(d) + 1):
            v = isqrt(d - u * u)
            if u * u + v * v != d or gcd(u, v) != 1:
                continue
            for v0 in {v, -v}:
                for a in range(m):
                    if gcd(a, m) == 1 and (s0 + a * v0) % m == 0 \
                            and (s1 - a * u) % m == 0:
                        return True
    return False


def main():
    start = time.monotonic()
    cases, counts = [], Counter()
    ranges = [(1, 24), (2, 40), (3, 12), (4, 6), (5, 3)]
    for n, bound in ranges:
        for m in range(1, bound + 1):
            for r in projective_residues(n, m):
                ws = splitting_vectors(r, m)
                witness, short_count, nodes = primal_search(r, m)
                positive = len(ws) == n
                assert positive == (witness is not None), (r, m, ws, witness)
                assert len(ws) <= n and len(set(ws)) == len(ws)
                assert all(dot(v, w) == 0 for i, v in enumerate(ws) for w in ws[i + 1:])
                pp = prime_power_criterion(r, m) if m > 1 else None
                if pp is not None:
                    assert pp == positive, ("prime power", r, m)
                    counts["prime_power_controls"] += 1
                if positive:
                    assert __import__('math').prod(dot(w, w) for w in ws) == m ** (2*n-2)
                cases.append(dict(r=r, m=m, splitting=ws, independent_basis=witness,
                                  short_vectors=short_count, search_nodes=nodes))
                counts["cases"] += 1
                counts["positive" if positive else "negative"] += 1
                counts["short_vectors"] += short_count
                counts["search_nodes"] += nodes
            print(json.dumps(dict(progress=[n, m], cases=counts['cases'])), flush=True)
    # Named controls for half-coordinate signs and composite interactions.
    named = [((1, 1), 2, True), ((1, 1), 6, True), ((1, 5), 6, True),
             ((1, 1, 1), 2, False), ((1, 5, 2), 6, True),
             ((3, 1, 2), 6, False),
             ((0, 1, 2), 3, False), ((1, 3), 25, False), ((1, 7), 25, True)]
    for r, m, expected in named:
        ws = splitting_vectors(r, m)
        assert (len(ws) == len(r)) == expected, (r, m, ws, expected)
    assert normalize(['-1/2', '7/6', '4/3']) == ((3, 1, 2), 6)
    target = ROOT / 'results/9.45-controls.json'
    target.write_text(json.dumps(dict(ranges=ranges, counts=counts, cases=cases,
        named_controls=[dict(r=r, m=m, expected=e) for r,m,e in named],
        seconds=time.monotonic()-start), indent=2)+'\n')
    print('PASS_945_PYTHON', json.dumps(counts, sort_keys=True),
          hashlib.sha256(target.read_bytes()).hexdigest(), flush=True)


if __name__ == '__main__':
    main()
