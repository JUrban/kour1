#!/usr/bin/env python3
"""Independent dictionary-polynomial and actual-neighbor controls."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import re


def conv(a, b):
    c = Counter()
    for i, x in a.items():
        for j, y in b.items():
            c[i+j] += x*y
    return dict(c)


def small_exhaustion():
    answer = []
    for r in range(1, 6):
        count = matches = 0
        for bits in product([0, 1], repeat=r-1):
            p = {-r: 1, r: 1}
            for j, b in enumerate(bits, 1):
                if b:
                    p[j] = p[-j] = 1
            pp = conv(p, p)
            for bitsq in product([0, 1], repeat=2*r-1):
                q = {0: 1, 2*r: 1}
                q.update({j: 1 for j, b in enumerate(bitsq, 1) if b})
                qq = conv(q, {-j: v for j, v in q.items()})
                count += 1
                lam = F(pp.get(r, 0)-qq.get(r, 0), 2)
                exponents = set(pp) | set(qq) | set(p)
                if any(pp.get(j, 0)-qq.get(j, 0)-2*lam*p.get(j, 0)
                       for j in exponents if j != 0):
                    continue
                matches += 1
                assert pp.get(0, 0)-qq.get(0, 0)+lam**2 == 0
                epsilon = q.get(r, 0)
                expected = {j+r: v for j, v in p.items()}
                if epsilon:
                    expected[r] = 1
                assert q == expected and lam == -epsilon
        assert matches == 2**r
        answer.append(dict(radius=r, pairs=count, constant_determinants=matches))
    return answer


def multiply(g, h):
    n, e = g
    m, f = h
    return n+(-1 if e else 1)*m, (e+f) % 2


def neighbor_controls():
    rng = random.Random(1589)
    count = 0
    for _ in range(500):
        rotations = set()
        for j in range(1, 8):
            if rng.randrange(2):
                rotations.update([j, -j])
        reflections = {j for j in range(-5, 6) if rng.randrange(2)}
        generators = [(j, 0) for j in rotations]+[(j, 1) for j in reflections]
        z = rng.choice([F(2), F(-2), F(3, 2), F(-1, 3)])
        u, v = rng.randint(-5, 5), rng.randint(-5, 5)
        p = sum(z**j for j in rotations)
        q = sum(z**j for j in reflections)
        qr = sum(z**(-j) for j in reflections)
        def value(g):
            n, e = g
            return (u if e == 0 else v)*z**n
        for n in range(-3, 4):
            for e in range(2):
                actual = sum(value(multiply((n, e), s)) for s in generators)
                predicted = (p*u+q*v if e == 0 else qr*u+p*v)*z**n
                assert actual == predicted
                count += 1
    return count


def main():
    root = Path(__file__).resolve().parents[1]
    records = small_exhaustion()
    text = (root/'results/15.89-dihedral-search.log').read_text()
    rows = re.findall(r'^R=(\d+) q_count=(\d+) constant_determinants=(\d+) '
                      r'nonzero_determinants=(\d+) elapsed_ms=(\d+)$', text, re.M)
    assert len(rows) == 11
    for r, q, c, h, ms in rows:
        r, q, c, h = map(int, [r, q, c, h])
        assert q == 2**(2*r-1) and c == 2**r and h == 0
        if r <= 5:
            assert records[r-1]['constant_determinants'] == c
    assert text.endswith('DONE total_q=2796202 constant_determinants=4094 nonzero_determinants=0\n')
    result = dict(problem='15.89', status='PASS',
                  independent_exhaustion=records,
                  exact_neighbor_actions=neighbor_controls(),
                  cpp_log_ranges_validated=11,
                  scope='Dihedral Cayley subclass only; general claim rests on the written proof.')
    (root/'results/15.89-dihedral-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
