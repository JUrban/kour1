#!/usr/bin/env python3
"""Exact finite-support identities in C[C3*C2], with local function controls."""
from collections import defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path


# A word is a tuple of nonidentity factor syllables: a, a^2, or b.
def mul(x, y):
    out = list(x)
    for factor, exponent in y:
        modulus = 3 if factor == 'a' else 2
        if out and out[-1][0] == factor:
            exponent = (out.pop()[1] + exponent) % modulus
            if exponent:
                out.append((factor, exponent))
        else:
            out.append((factor, exponent))
    return tuple(out)


def inverse(x):
    return tuple((f, (-e) % (3 if f == 'a' else 2)) for f, e in reversed(x))


def convolution(x, y):
    out = defaultdict(Fraction)
    for g, c in x.items():
        for h, d in y.items():
            out[mul(g, h)] += c*d
    return {g: c for g, c in out.items() if c}


one = {(): Fraction(1)}
a, aa, b = (('a', 1),), (('a', 2),), (('b', 1),)
u, v = {a: Fraction(1), aa: Fraction(1)}, {b: Fraction(1)}
uinv = {a: Fraction(1, 2), aa: Fraction(1, 2), (): Fraction(-1, 2)}
adj = convolution(convolution(u, v), u)
green = convolution(convolution(uinv, v), uinv)
assert len(adj) == 4 and set(adj.values()) == {1} and () not in adj
assert set(map(inverse, adj)) == set(adj)
assert convolution(u, uinv) == convolution(uinv, u) == one
assert convolution(adj, green) == convolution(green, adj) == one
assert len(green) == 9
s1, s2 = mul(mul(a, b), a), mul(mul(aa, b), a)
assert s1 in adj and s2 in adj
assert mul(s1, inverse(s2)) == aa
assert mul(mul(aa, s1), aa) == b

# Distinct reduced words (ab)^n give a transparent finite check on the
# infinite-order family used in the proof, not a proof by finite sampling.
ab = mul(a, b)
powers = [()]
for _ in range(100):
    powers.append(mul(powers[-1], ab))
assert len(set(powers)) == 101
assert all(len(w) == 2*n for n, w in enumerate(powers))

# Each output coordinate of both composed operators depends on a finite
# set. Test every basis function on those dependency sets, at all reduced
# words of syllable length at most six. This includes boundary terms;
# no truncated induced adjacency matrix is used.
vertices = {()}
frontier = {()}
for _ in range(6):
    nxt = {mul(x, y) for x in frontier for y in (a, aa, b)} - vertices
    vertices |= nxt
    frontier = nxt
coordinate_checks = 0
for left, right in ((adj, green), (green, adj)):
    for x in vertices:
        actual = defaultdict(Fraction)
        for s, c in left.items():
            for t, d in right.items():
                actual[mul(mul(x, s), t)] += c*d
        for y, c in actual.items():
            assert c == (1 if y == x else 0)
            coordinate_checks += 1

# Removing one neighbour destroys the identity. This detects a mistaken
# weighted or incomplete connection set being accepted by the control.
bad = dict(adj)
bad.pop(s1)
assert convolution(bad, green) != one

def printable(word):
    return '1' if not word else ''.join(f if e == 1 else f+'^'+str(e) for f, e in word)


result = dict(status='PASS', degree=len(adj), inverse_support=len(green),
              tested_vertices=len(vertices), basis_coordinate_checks=coordinate_checks,
              distinct_power_controls=len(powers), omitted_edge_rejected=True,
              adjacency={printable(k): str(v) for k, v in adj.items()},
              inverse={printable(k): str(v) for k, v in green.items()},
              scope='Finite-support identities and controls. The infinite graph and all-functions conclusion rest on the separate proof.')
Path('results/15.89-free-product-python.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
