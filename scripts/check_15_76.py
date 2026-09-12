#!/usr/bin/env python3
"""Exact bounded controls; the general 15.76 theorem is proved separately."""
import itertools as it
import json
import random
from collections import Counter
from pathlib import Path


def invword(w):
    return tuple(-a for a in reversed(w))


def reduceword(w):
    out = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def subst(w, images):
    return reduceword(a for s in w for a in
                      (images[s - 1] if s > 0 else invword(images[-s - 1])))


def comm(u, v):
    return reduceword(invword(u) + invword(v) + u + v)


def clean(d):
    return {k: v for k, v in d.items() if v}


def magnus_ab(w, rank):
    """Literal signed edge chain in the Z^rank covering graph."""
    endpoint = [0] * rank
    edges = Counter()
    for a in w:
        i = abs(a) - 1
        if a > 0:
            edges[tuple(endpoint), i] += 1
            endpoint[i] += 1
        else:
            endpoint[i] -= 1
            edges[tuple(endpoint), i] -= 1
    return tuple(endpoint), clean(edges)


def reduced_words(maxlen):
    level = [()]
    yield ()
    for _ in range(maxlen):
        level = [w + (a,) for w in level for a in (1, -1, 2, -2)
                 if not w or w[-1] != -a]
        yield from level


def metabelian_control():
    counts, survivors, checked = Counter(), [], 0
    usual = magnus_ab((1, 2), 2)
    opposite = magnus_ab((2, 1), 2)
    for w in reduced_words(10):
        if [sum((s > 0) - (s < 0) for s in w if abs(s) == i)
                for i in (1, 2)] != [1, 1]:
            continue
        checked += 1
        counts[len(w)] += 1
        left = subst(w, (w, (3,)))
        right = subst(w, ((1,), subst(w, ((2,), (3,)))))
        if magnus_ab(left, 3) == magnus_ab(right, 3):
            value = magnus_ab(w, 2)
            assert value in (usual, opposite), w
            survivors.append({'word': w, 'operation': 'xy' if value == usual else 'yx'})
    assert checked == 2430
    assert set(x['operation'] for x in survivors) == {'xy', 'yx'}
    return {'normalized_reduced_words': checked, 'by_length': dict(counts),
            'associative_words': len(survivors), 'survivors': survivors}


class Symmetric:
    def __init__(self, n):
        self.elements = list(it.permutations(range(n)))
        lookup = {g: i for i, g in enumerate(self.elements)}
        self.one = lookup[tuple(range(n))]
        self.mul = [[lookup[tuple(g[h[i]] for i in range(n))]
                     for h in self.elements] for g in self.elements]
        self.inv = [next(j for j in range(len(self.elements))
                         if self.mul[i][j] == self.one) for i in range(len(self.elements))]

    def ringmul(self, a, b):
        result = Counter()
        for g, c in a.items():
            for h, d in b.items():
                result[self.mul[g][h]] += c * d
        return clean(result)

    def act(self, a, u):
        result = Counter()
        for g, c in a.items():
            for (h, i), d in u.items():
                result[self.mul[g][h], i] += c * d
        return clean(result)

    def affine_mul(self, left, right):
        a, u = left
        b, v = right
        return self.mul[a][b], add(u, self.act({a: 1}, v))

    def affine_inv(self, value):
        a, u = value
        return self.inv[a], self.act({self.inv[a]: -1}, u)

    def affine_eval(self, w, args):
        value = self.one, {}
        negatives = [self.affine_inv(arg) for arg in args]
        for s in w:
            value = self.affine_mul(value, args[s - 1] if s > 0 else negatives[-s - 1])
        return value

    def fox(self, w, args):
        """Independent scalar-prefix scan giving one ring coefficient per input."""
        p = self.one
        coefficients = [Counter() for _ in args]
        for s in w:
            i = abs(s) - 1
            if s > 0:
                coefficients[i][p] += 1
                p = self.mul[p][args[i]]
            else:
                p = self.mul[p][self.inv[args[i]]]
                coefficients[i][p] -= 1
        return p, [clean(c) for c in coefficients]


def add(*ds):
    out = Counter()
    for d in ds:
        out.update(d)
    return clean(out)


def encode_module(d):
    return [[g, i, c] for (g, i), c in sorted(d.items())]


def finite_control(n, rng):
    group = Symmetric(n)
    size = len(group.elements)
    x, y = (1,), (2,)
    derived = comm(x, y)
    for _ in range(n - 2):
        derived = comm(derived, invword(x) + derived + x)
    w = reduceword(x + y + derived)
    assert magnus_ab(w, 2) == magnus_ab((1, 2), 2)
    assert magnus_ab(subst(w, (w, (3,))), 3) == magnus_ab(
        subst(w, ((1,), subst(w, ((2,), (3,))))), 3)
    # The perturbation is in F^(n-1); S_n has derived length n-1 for n=3,4.
    # Check this scalar identity exhaustively, independent of that fact.
    for a, b in it.product(range(size), repeat=2):
        p, _ = group.fox(w, (a, b))
        assert p == group.mul[a][b]

    boundary_checks = coefficient_checks = 0
    for _ in range(400):
        word = tuple(rng.choice((1, -1, 2, -2)) for _ in range(rng.randrange(1, 60)))
        a, b = (rng.randrange(size) for _ in range(2))
        u = clean(Counter({(rng.randrange(size), i): rng.randrange(-3, 4) for i in range(3)}))
        v = clean(Counter({(rng.randrange(size), i): rng.randrange(-3, 4) for i in range(3)}))
        p, (f, g) = group.fox(word, (a, b))
        direct = group.affine_eval(word, ((a, u), (b, v)))
        assert direct == (p, add(group.act(f, u), group.act(g, v)))
        coefficient_checks += 1
        boundary = add(group.ringmul(f, add({a: 1}, {group.one: -1})),
                       group.ringmul(g, add({b: 1}, {group.one: -1})))
        assert boundary == add({p: 1}, {group.one: -1})
        boundary_checks += 1

    witness = None
    association_checks = 0
    # All triples for xy and yx; the perturbation needs only a witness.
    for scalars in it.product(range(size), repeat=3):
        args = [(a, {(group.one, i): 1}) for i, a in enumerate(scalars)]
        a, b, c = args
        for operation in ((1, 2), (2, 1)):
            op = lambda u, v: group.affine_eval(operation, (u, v))
            assert op(op(a, b), c) == op(a, op(b, c))
            association_checks += 1
        if witness is None:
            op = lambda u, v: group.affine_eval(w, (u, v))
            left, right = op(op(a, b), c), op(a, op(b, c))
            if left != right:
                witness = {'scalar_indices': scalars,
                           'scalar_permutations': [group.elements[s] for s in scalars],
                           'left': [left[0], encode_module(left[1])],
                           'right': [right[0], encode_module(right[1])]}
    assert witness is not None
    return {'scalar_group': 'S' + str(n), 'word': w,
            'scalar_identity_pairs': size ** 2,
            'boundary_checks': boundary_checks, 'coefficient_checks': coefficient_checks,
            'usual_opposite_associativity_checks': association_checks,
            'nonassociative_perturbation_witness': witness}


def laurent_control():
    solutions = []
    for k, l in it.product(range(-8, 9), repeat=2):
        d = Counter()
        for monomial, c in [((1, k), 1), ((0, k), -1),
                            ((l, 1), 1), ((l, 0), -1),
                            ((1, 1), -1), ((0, 0), 1)]:
            d[monomial] += c
        if not clean(d):
            solutions.append((k, l))
    assert solutions == [(0, 1), (1, 0)]
    return {'pairs_checked': 17 ** 2, 'solutions': solutions}


def reversal_control(rng):
    # Reversal rho is an antihomomorphism fixing a basis; eta inverts its letters.
    for _ in range(1000):
        rank_in, rank_out = rng.randrange(1, 5), rng.randrange(1, 5)
        alphabet_in = tuple(range(1, rank_in + 1)) + tuple(range(-rank_in, 0))
        alphabet_out = tuple(range(1, rank_out + 1)) + tuple(range(-rank_out, 0))
        w = reduceword(rng.choice(alphabet_in) for _ in range(rng.randrange(30)))
        images = [reduceword(rng.choice(alphabet_out) for _ in range(rng.randrange(20)))
                  for _ in range(rank_in)]
        left = tuple(reversed(subst(tuple(reversed(w)), images)))
        right = tuple(-a for a in subst(tuple(-a for a in w), images))
        assert left == right
    return {'free_group_homomorphism_controls': 1000}


def run():
    rng = random.Random(1576)
    return {'status': 'PASS', 'seed': 1576,
            'scope': 'Exact bounded corroboration, not a proof of the general theorem.',
            'metabelian': metabelian_control(),
            'finite_noncommutative': [finite_control(n, rng) for n in (3, 4)],
            'laurent': laurent_control(), 'reversal': reversal_control(rng)}


if __name__ == '__main__':
    data = run()
    Path('results/15.76-controls.json').write_text(json.dumps(data, indent=2) + '\n')
    print('PASS_1576_EXACT_CONTROLS', data['metabelian']['normalized_reduced_words'],
          data['metabelian']['associative_words'])
