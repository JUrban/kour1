#!/usr/bin/env python3
"""Exact sanity checks for the elementary proof of Kourovka 10.35.

Finite checks do not certify the universal matrix lemma. Its proof is
in research/10.35-proof.md. No floating-point arithmetic is used.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import datetime
import hashlib
import json
import random


def mul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


def scale(s, a):
    return tuple(tuple(s * x for x in row) for row in a)


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def adj(a):
    return ((a[1][1], -a[0][1]), (-a[1][0], a[0][0]))


def inv(a):
    return scale(F(1) / det(a), adj(a))


def eye(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def power(a, k):
    if k < 0:
        a, k = inv(a), -k
    r = eye(len(a))
    while k:
        if k % 2:
            r = mul(r, a)
        a, k = mul(a, a), k // 2
    return r


# Q(i) represented by a+bi, with exact rational components.
class Gaussian:
    __slots__ = ('re', 'im')

    def __init__(self, re=0, im=0):
        self.re, self.im = F(re), F(im)

    def __add__(self, other):
        if not isinstance(other, Gaussian):
            other = Gaussian(other)
        return Gaussian(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return Gaussian(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, Gaussian):
            other = Gaussian(other)
        return Gaussian(self.re * other.re - self.im * other.im,
                        self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def __pow__(self, k):
        assert isinstance(k, int) and k >= 0
        r, a = Gaussian(1), self
        while k:
            if k % 2:
                r = r * a
            a, k = a * a, k // 2
        return r

    def __rtruediv__(self, other):
        norm = self.re**2 + self.im**2
        return Gaussian(other) * Gaussian(self.re / norm, -self.im / norm)

    def __eq__(self, other):
        if not isinstance(other, Gaussian):
            other = Gaussian(other)
        return self.re == other.re and self.im == other.im

    def __hash__(self):
        # Equal real rationals must have the same hash.
        return hash(self.re) if self.im == 0 else hash((self.re, self.im))


def turn(v, k):
    x, y = v
    return ((x, y), (-y, x), (-x, -y), (y, -x))[k % 4]


def group_mul(g, h):
    x, y, k = g
    u, v = turn(h[:2], k)
    return x + u, y + v, k + h[2]


def group_inv(g):
    x, y = turn((-g[0], -g[1]), -g[2])
    return x, y, -g[2]


def complex_rep(g):
    x, y, k = g
    c = F(2)**k
    u, v = turn((1, 0), k)
    return ((Gaussian(c*u, c*v), Gaussian(c*x, c*y)),
            (Gaussian(), Gaussian(c)))


def rational_rep(g):
    x, y, k = g
    u, v = turn((1, 0), k)
    c = F(2)**k
    return scale(c, ((u, -v, x), (v, u, y), (0, 0, 1)))


def lemma_hypotheses(x, y):
    """Clear inverse denominators, valid for arbitrary rational entries."""
    dx, dy = det(x), det(y)
    assert dx and dy
    b_num = mul(mul(y, x), adj(y))
    if mul(x, b_num) != mul(b_num, x):
        return False
    y2 = mul(y, y)
    return scale(dx, mul(mul(y2, x), adj(y2))) == scale(dy**2, adj(x))


def main():
    rng = random.Random(1035)
    ident = eye(2)
    a = complex_rep((1, 0, 0))
    b = complex_rep((0, 1, 0))
    t = complex_rep((0, 0, 1))
    assert mul(a, b) == mul(b, a)
    assert mul(mul(t, a), inv(t)) == b
    assert mul(mul(t, b), inv(t)) == inv(a)
    assert power(t, 4) == scale(16, ident)
    assert power(a, 2) != ident
    assert lemma_hypotheses(a, t)  # Field hypothesis is necessary.

    elements = list(product(range(-2, 3), range(-2, 3), range(-4, 5)))
    assert len(set(map(complex_rep, elements))) == len(elements)
    assert len(set(map(rational_rep, elements))) == len(elements)
    for g in elements:
        assert group_mul(g, group_inv(g)) == (0, 0, 0)
        assert mul(complex_rep(g), complex_rep(group_inv(g))) == ident
        assert mul(rational_rep(g), rational_rep(group_inv(g))) == eye(3)
        assert mul(mul(power(a, g[0]), power(b, g[1])), power(t, g[2])) == complex_rep(g)
    for _ in range(2500):
        g, h, k = (rng.choice(elements) for _ in range(3))
        assert group_mul(group_mul(g, h), k) == group_mul(g, group_mul(h, k))
        gh = group_mul(g, h)
        assert mul(complex_rep(g), complex_rep(h)) == complex_rep(gh)
        assert mul(rational_rep(g), rational_rep(h)) == rational_rep(gh)

    matrices = [((a, b), (c, d)) for a, b, c, d in
                product(range(-2, 3), repeat=4) if a*d-b*c]
    satisfying = 0
    for x in matrices:
        for y in matrices:
            if lemma_hypotheses(x, y):
                satisfying += 1
                assert mul(x, x) == ident

    rational_pairs = 0
    rational_satisfying = 0
    while rational_pairs < 4000:
        x, y = [tuple(tuple(F(rng.randint(-4, 4), rng.randint(1, 4))
                            for _ in range(2)) for _ in range(2)) for _ in range(2)]
        if not det(x) or not det(y):
            continue
        rational_pairs += 1
        if lemma_hypotheses(x, y):
            rational_satisfying += 1
            assert mul(x, x) == ident

    # Torsion target control: a survives, but a^2 does not.
    x, y = ((-1, 0), (0, 1)), ((0, 1), (1, 0))
    z = mul(mul(y, x), inv(y))
    assert z == ((1, 0), (0, -1))
    assert mul(x, z) == mul(z, x)
    assert mul(mul(y, z), inv(y)) == inv(x)
    assert lemma_hypotheses(x, y)
    assert x != ident and mul(x, x) == ident
    closure = {ident}
    while True:
        expanded = closure | {mul(g, s) for g in closure for s in (x, y)}
        if expanded == closure:
            break
        closure = expanded
    assert len(closure) == 8

    data = {
        'status': 'PASS',
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'arithmetic': 'Python integers and Fraction; Q(i) as rational pairs',
        'seed': 1035,
        'normal_forms_checked': len(elements),
        'normal_form_inverses_and_word_substitutions': len(elements),
        'associativity_and_both_representation_product_checks': 2500,
        'invertible_integer_matrices': len(matrices),
        'integer_matrix_pairs_checked': len(matrices)**2,
        'integer_pairs_satisfying_lemma_hypotheses': satisfying,
        'random_rational_pairs_checked': rational_pairs,
        'random_rational_pairs_satisfying_lemma_hypotheses': rational_satisfying,
        'torsion_target_image_order': len(closure),
        'field_and_dimension_positive_controls': 'PASS',
        'limitation': 'Finite sanity checks only; the universal conclusion is proved in research/10.35-proof.md.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    Path('results/10.35-verification.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
