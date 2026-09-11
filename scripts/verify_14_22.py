#!/usr/bin/env python3
"""Exact controls for the proofs in research/14.22-proof.md.

Independent polynomial matrices versus Z^2 * Z normal forms, and a
central normal form for Q *_Z (Z x Z). No finite check proves the
universal assertions about arbitrary systems or torsion-freeness.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import random

RNG = random.Random(1422)


def add(a, b):
    c = a.copy()
    for m, v in b.items():
        c[m] = c.get(m, 0) + v
        if not c[m]:
            del c[m]
    return c


def neg(a):
    return {m: -v for m, v in a.items()}


def mul(a, b):
    c = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            m = (i+k, j+l)
            c[m] = c.get(m, 0) + v*w
    return {m: v for m, v in c.items() if v}


ONE, ZERO = {(0, 0): 1}, {}
Z, T = {(1, 0): 1}, {(0, 1): 1}
ID = (ONE, ZERO, ZERO, ONE)


def mm(a, b):
    return (add(mul(a[0], b[0]), mul(a[1], b[2])),
            add(mul(a[0], b[1]), mul(a[1], b[3])),
            add(mul(a[2], b[0]), mul(a[3], b[2])),
            add(mul(a[2], b[1]), mul(a[3], b[3])))


def upper(p):
    return (ONE, p, ZERO, ONE)


def lower(p):
    return (ONE, ZERO, p, ONE)


MATS = (upper(ONE), upper(neg(ONE)), upper(Z), upper(neg(Z)),
        lower(T), lower(neg(T)))
# A syllable (kind, u, v) has kind 0 for Z^2 and kind 1 for Z.
LETTERS = ((0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
           (1, 1, 0), (1, -1, 0))


def fp_append(word, syllable):
    out = list(word)
    kind, u, v = syllable
    if out and out[-1][0] == kind:
        _, p, q = out.pop()
        u, v = u+p, v+q
    if u or v:
        out.append((kind, u, v))
    return tuple(out)


def evaluate_word(word):
    nf, matrix = (), ID
    for s in word:
        nf = fp_append(nf, LETTERS[s])
        matrix = mm(matrix, MATS[s])
    assert (not nf) == (matrix == ID), (word, nf, matrix)
    assert add(mul(matrix[0], matrix[3]), neg(mul(matrix[1], matrix[2]))) == ONE
    return nf, matrix


def polynomial_controls():
    count = identities = specializations = 0
    frontier = [((), (), ID)]
    for length in range(7):
        following = []
        for word, nf, matrix in frontier:
            count += 1
            identities += not nf
            assert (not nf) == (matrix == ID)
            if length < 6:
                for s in range(6):
                    if word and s == (word[-1] ^ 1):
                        continue
                    following.append((word+(s,), fp_append(nf, LETTERS[s]),
                                      mm(matrix, MATS[s])))
        frontier = following
    for _ in range(500):
        word = [RNG.randrange(6) for _ in range(RNG.randint(10, 45))]
        nf, matrix = evaluate_word(word)
        count += 1
        identities += not nf
        if nf:
            # Specialization z=q leaves a matrix over Q[t].
            # Find an actual separating rational specialization.
            for q in range(-50, 51):
                specialized = []
                for p in matrix:
                    a = {}
                    for (i, j), v in p.items():
                        a[j] = a.get(j, 0) + v*q**i
                    specialized.append({j: v for j, v in a.items() if v})
                if specialized != [{0: 1}, {}, {}, {0: 1}]:
                    specializations += 1
                    break
            else:
                raise AssertionError('No separating specialization in control range')
    # Check the exact leading trace coefficient used in the proof,
    # including upper entries q+n*z, with q possibly zero.
    trace_controls = 500
    for _ in range(trace_controls):
        k = RNG.randint(1, 10)
        matrix, expected = ID, ONE
        for _ in range(k):
            q, n = RNG.randint(-4, 4), RNG.randint(-4, 4)
            if not (q or n):
                n = 1
            p = {(0, 0): q, (1, 0): n}
            p = {m: v for m, v in p.items() if v}
            b = RNG.choice([-3, -2, -1, 1, 2, 3])
            matrix = mm(matrix, mm(upper(p), lower({(0, 1): b})))
            expected = mul(expected, {m: v*b for m, v in p.items()})
        trace = add(matrix[0], matrix[3])
        leading = {(i, 0): v for (i, j), v in trace.items() if j == k}
        assert leading == expected and leading
        assert max(j for i, j in trace) == k
    return dict(words=count, identity_words=identities,
                separating_specializations=specializations,
                leading_trace_controls=trace_controls)


# In K=Q *_Z (Z x <x>), the common Z is central.
# A normal form consists of an integer central part followed by an
# alternating word in Q/Z and <x>. Rational representatives lie in [0,1).
# The carry when adding two Q/Z representatives is added to the centre.
def normalize(central, word):
    out = []
    for kind, value in word:
        if out and out[-1][0] == kind:
            value += out.pop()[1]
        if kind == 'q':
            carry = value.numerator // value.denominator
            central += carry
            value -= carry
        if value:
            out.append((kind, value))
    return central, tuple(out)


E = (0, ())


def kmul(a, b):
    return normalize(a[0]+b[0], a[1]+b[1])


def kinv(a):
    return normalize(-a[0], [(k, -v) for k, v in reversed(a[1])])


def kpow(a, n):
    if n < 0:
        return kpow(kinv(a), -n)
    out = E
    for _ in range(n):
        out = kmul(out, a)
    return out


def comm(a, b):
    return kmul(kmul(kmul(kinv(a), kinv(b)), a), b)


def random_k():
    return normalize(RNG.randint(-5, 5), [
        ('q', F(RNG.randint(-10, 10), RNG.randint(1, 12)))
        if RNG.randrange(2) else ('x', RNG.randint(-4, 4))
        for _ in range(RNG.randint(0, 12))])


def amalgam_controls():
    power_checks = 0
    for _ in range(4000):
        a, b, c = random_k(), random_k(), random_k()
        assert kmul(kmul(a, b), c) == kmul(a, kmul(b, c))
        assert kmul(a, kinv(a)) == kmul(kinv(a), a) == E
        if a != E:
            for n in [2, 3, 5, 7]:
                assert kpow(a, n) != E
                power_checks += 1
    x = normalize(0, [('x', 1)])
    central = normalize(0, [('q', F(1))])
    assert comm(x, central) == E
    witnesses = []
    for m in range(2, 33):
        r = normalize(0, [('q', F(1, m))])
        assert kpow(r, m) == central
        w = comm(x, r)
        assert len(w[1]) == 4
        for n in range(1, 33):
            assert len(kpow(w, n)[1]) == 4*n
        witnesses.append(dict(root_degree=m, commutator_syllables=len(w[1])))
    # Check arbitrary rational coefficient lists fit the chosen cyclic
    # subgroup, whereas the next root escapes it.
    from math import lcm
    for _ in range(1000):
        coefficients = [F(RNG.randint(-30, 30), RNG.randint(1, 50))
                        for _ in range(RNG.randint(0, 20))]
        d = lcm(*(q.denominator for q in coefficients))
        assert all((q*d).denominator == 1 for q in coefficients)
        assert (F(1, 2*d)*d).denominator != 1
    return dict(associativity_and_inverse_controls=4000,
                sampled_nontrivial_power_checks=power_checks,
                coefficient_support_controls=1000, witnesses=witnesses)


def main():
    data = dict(problem='14.22', status='PASS', seed=1422,
                polynomial=polynomial_controls(), amalgam=amalgam_controls(),
                scope='Exact bounded controls; universal claims rest on the written proof.')
    target = Path(__file__).resolve().parents[1] / 'results/14.22-verification.json'
    target.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
