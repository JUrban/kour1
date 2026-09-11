#!/usr/bin/env python3
"""Exact finite-support controls for the 18.76 construction.

No division-ring series are truncated or simulated. All calculations here
are in Z[F2 x F2] or F_p[F2 x F2], embedded in the ring used by the proof.
The separate GAP check verifies the elimination obstruction in matrix models.
"""
from collections import Counter
from itertools import product
import json
import random


def word(*parts):
    out = []
    for part in parts:
        for x in part:
            if out and out[-1] == -x:
                out.pop()
            else:
                out.append(x)
    return tuple(out)


def winv(w):
    return tuple(-x for x in reversed(w))


def gmul(g, h):
    return (word(g[0], h[0]), word(g[1], h[1]))


def check(p):
    rng = random.Random(187600 + p)
    count = Counter()
    identity = ((), ())

    def clean(r):
        return {g: (a % p if p else a) for g, a in r.items()
                if (a % p if p else a)}

    def plus(*rs):
        out = Counter()
        for r in rs:
            for g, a in r.items():
                out[g] += a
        return clean(out)

    def neg(r):
        return clean({g: -a for g, a in r.items()})

    def mul(r, s):
        out = Counter()
        for g, a in r.items():
            for h, b in s.items():
                out[gmul(g, h)] += a*b
        return clean(out)

    def mono(x=(), h=()):
        return {(x, h): 1}

    one = mono()

    def deriv(w, factor):
        # Prefix rule, valid even on unreduced words.
        out = {}
        prefix = ()
        for letter in w:
            if letter == 2:
                term = mono(prefix) if factor == 0 else mono(h=prefix)
                out = plus(out, term)
            elif letter == -2:
                pref = word(prefix, (-2,))
                term = mono(pref) if factor == 0 else mono(h=pref)
                out = plus(out, neg(term))
            prefix = word(prefix, (letter,))
        return out

    short = sorted({word(t) for n in range(4)
                    for t in product((1, -1, 2, -2), repeat=n)})
    assert len(short) == 53
    for factor in (0, 1):
        for x, y in product(short, repeat=2):
            acted = mono(x) if factor == 0 else mono(h=x)
            assert deriv(word(x, y), factor) == plus(
                deriv(x, factor), mul(acted, deriv(y, factor)))
            count['derivation_pairs'] += 1
        for n in range(7):
            for raw in product((1, -1, 2, -2), repeat=n):
                assert deriv(raw, factor) == deriv(word(raw), factor)
                count['reduction_checks'] += 1

    def randword():
        return word(rng.choices((1, -1, 2, -2), k=rng.randrange(7)))

    def randring():
        out = Counter()
        for _ in range(rng.randrange(5)):
            out[(randword(), randword())] += rng.randrange(-3, 4)
        return clean(out)

    def nmul(n, m):
        r, x = n
        s, y = m
        return (plus(r, mul(mono(x), s)), word(x, y))

    def gamma_letter(letter, n):
        r, x = n
        if letter > 0:
            offset = deriv(x, 0) if letter == 2 else {}
            return (plus(mul(mono(h=(letter,)), r), offset), x)
        offset = deriv(x, 0) if letter == -2 else {}
        return (mul(mono(h=(letter,)), plus(r, neg(offset))), x)

    def gamma(h, n):
        # Compose the actual generator automorphisms, independently of eta.
        for letter in reversed(h):
            n = gamma_letter(letter, n)
        return n

    def emul(e, f):
        r, x, h = e
        s, y, k = f
        return (plus(r, mul(mono(x, h), s),
                     mul(mul(mono(x), deriv(h, 1)), deriv(y, 0))),
                word(x, y), word(h, k))

    def einv(e):
        r, x, h = e
        correction = mul(deriv(h, 1), deriv(x, 0))
        return (mul(mono(winv(x), winv(h)), plus(neg(r), correction)),
                winv(x), winv(h))

    unit = ({}, (), ())
    for _ in range(600):
        r, s, t = randring(), randring(), randring()
        x, y, z = randword(), randword(), randword()
        h, k, ell = randword(), randword(), randword()
        n, m = (r, x), (s, y)
        for letter in (1, -1, 2, -2):
            assert gamma_letter(-letter, gamma_letter(letter, n)) == n
            assert gamma_letter(letter, nmul(n, m)) == nmul(
                gamma_letter(letter, n), gamma_letter(letter, m))
            count['generator_automorphism_checks'] += 1
        assert gamma(h, n) == (
            plus(mul(mono(h=h), r), mul(deriv(h, 1), deriv(x, 0))), x)
        assert gamma(word(h, k), n) == gamma(h, gamma(k, n))
        count['action_formula_checks'] += 1
        e, f, g = (r, x, h), (s, y, k), (t, z, ell)
        rs, xy = nmul(n, gamma(h, m))
        assert emul(e, f) == (rs, xy, word(h, k))
        assert emul(emul(e, f), g) == emul(e, emul(f, g))
        assert emul(e, einv(e)) == unit == emul(einv(e), e)
        assert emul(unit, e) == e == emul(e, unit)
        assert emul(emul(e, (t, (), ())), einv(e)) == (
            mul(mono(x, h), t), (), ())
        count['extension_checks'] += 1

    a, b, c, d = ({}, (1,), ()), ({}, (2,), ()), \
        ({}, (), (1,)), ({}, (), (2,))
    for e, f in ((a, c), (a, d), (b, c)):
        assert emul(e, f) == emul(f, e)
    assert emul(d, b) == emul((one, (), ()), emul(b, d))
    assert emul(d, b) != emul(b, d)
    assert gmul(((1,), ()), ((2,), ())) != gmul(((2,), ()), ((1,), ()))
    for factor in (0, 1):
        assert deriv((1, 2, -1, -2), factor)
    count['lift_and_nonabelian_controls'] = 8
    return dict(characteristic=p, status='PASS', **count)


if __name__ == '__main__':
    results = [check(p) for p in (0, 2, 3, 5, 7)]
    report = dict(status='PASS', ring='finite-support group algebra',
                  division_ring_simulated=False, cases=results)
    print(json.dumps(report, indent=2))
