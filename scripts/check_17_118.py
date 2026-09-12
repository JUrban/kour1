#!/usr/bin/env python3
"""Independent squarefree-word algebra controls for the partial 17.118 proof."""
from collections import deque
from itertools import permutations, product
import json
import math
from pathlib import Path
import random


class Algebra:
    def __init__(self, p):
        self.p = p
        self.words = [()] + [w for k in range(1, p+1)
                             for w in permutations(range(p), k)]
        self.index = {w: i for i, w in enumerate(self.words)}
        self.masks = [sum(1 << x for x in w) for w in self.words]
        self.table = [[-1 if self.masks[i] & self.masks[j]
                       else self.index[x+y]
                       for j, y in enumerate(self.words)]
                      for i, x in enumerate(self.words)]
        self.one = {0: 1}

    def mul(self, a, b):
        out = {}
        for i, x in a.items():
            row = self.table[i]
            for j, y in b.items():
                k = row[j]
                if k >= 0:
                    out[k] = (out.get(k, 0) + x*y) % self.p
        return {k: v for k, v in out.items() if v}

    def power(self, a, n):
        out = self.one
        for _ in range(n):
            out = self.mul(out, a)
        return out

    def pack(self, a):
        return tuple(a.get(i, 0) for i in range(len(self.words)))

    def unpack(self, a):
        return {i: v for i, v in enumerate(a) if v}

    def linear(self, a):
        return tuple(a.get(self.index[(i,)], 0) for i in range(self.p))

    def predicted_power(self, a):
        coefficient = math.prod(self.linear(a)) % self.p
        return {0: 1, **({i: coefficient for i, w in enumerate(self.words)
                         if len(w) == self.p} if coefficient else {})}


def check_algebra(p):
    a = Algebra(p)
    rng = random.Random(17118 + p)
    power_cases, jordan_cases = 0, 0
    higher = [i for i, w in enumerate(a.words) if len(w) >= 2]
    for v in product(range(p), repeat=p):
        u = {0: 1, **{a.index[(i,)]: x for i, x in enumerate(v) if x}}
        # Higher terms must have no effect on the p-th power.
        for i in rng.sample(higher, min(9, len(higher))):
            x = rng.randrange(p)
            if x:
                u[i] = x
        assert a.power(u, p) == a.predicted_power(u)
        power_cases += 1
        if any(v):
            w = v
            while True:
                delta = tuple((w[(i-1) % p] - w[i]) % p for i in range(p))
                if not any(delta):
                    break
                w = delta
                jordan_cases += 1
                assert jordan_cases <= p**p * p
            assert len(set(w)) == 1 and w[0] != 0
            # A translate witnessing that this v does not preserve p-th powers.
            j = next(i for i, x in enumerate(v) if x)
            b = [0 if i == j else next(t for t in range(p) if (t+v[i]) % p)
                 for i in range(p)]
            assert math.prod(b) % p == 0
            assert math.prod((x+y) % p for x, y in zip(v, b)) % p != 0
    # Independent associativity on sparse arbitrary algebra elements.
    for _ in range(600):
        us = [{i: rng.randrange(1, p) for i in rng.sample(range(len(a.words)),
                                                       min(10, len(a.words)))}
              for _ in range(3)]
        assert a.mul(a.mul(us[0], us[1]), us[2]) == a.mul(us[0], a.mul(us[1], us[2]))
    return dict(p=p, algebra_dimension=len(a.words)-1,
                linear_vectors=power_cases, jordan_nonzero_vectors=p**p-1,
                jordan_difference_steps=jordan_cases, associativity_triples=600,
                characteristic_exponent_p_index=p**p)


def check_generated_three():
    a = Algebra(3)
    generators = [{0: 1, a.index[(i,)]: 1} for i in range(3)]
    identity = a.pack(a.one)
    words = {identity: ""}
    queue = deque([identity])
    while queue:
        g = queue.popleft()
        for i, s in enumerate(generators):
            h = a.pack(a.mul(a.unpack(g), s))
            if h not in words:
                words[h] = words[g] + str(i)
                queue.append(h)
    assert len(words) == 6561
    rows = sorted(words)
    bad = 0
    cosets = {}
    cycle = [a.index[tuple((x+1) % 3 for x in w)] for w in a.words]
    for g in rows:
        u = a.unpack(g)
        assert a.power(u, 3) == a.predicted_power(u)
        bad += a.power(u, 3) != a.one
        v = a.linear(u)
        cosets[v] = cosets.get(v, 0) + 1
        rotated = {cycle[i]: x for i, x in u.items()}
        assert a.pack(rotated) in words
    assert bad == 1944 and len(cosets) == 27 and set(cosets.values()) == {243}
    # Exact finite model, with a word witness for every element.
    packet = dict(p=3, basis=[list(w) for w in a.words],
                  elements=[list(g) for g in rows], words=[words[g] for g in rows],
                  order=len(rows), noncubes=bad, kernel_order=243,
                  hyperplane_order=2187)
    return packet


def main():
    records = [check_algebra(p) for p in [2, 3, 5]]
    packet = check_generated_three()
    Path("results/17.118-algebra-controls.json").write_text(json.dumps(records, indent=2) + "\n")
    Path("results/17.118-three-generator-model.json").write_text(json.dumps(packet, separators=(",", ":")) + "\n")
    print(json.dumps(records))
    print("PASS_17118_ALGEBRA primes=3 power_vectors=3156 "
          "generated_group=6561 noncubes=1944")


if __name__ == "__main__":
    main()
