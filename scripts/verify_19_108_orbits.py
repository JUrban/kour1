#!/usr/bin/env python3
"""Independent integer replay and finite-Fourier controls for 19.108.

Uses only Python's standard library, without GAP or a matrix package.
The conjugacy-class coverage still relies on GAP's subgroup enumerator.
"""
import ast
from collections import deque
from itertools import product
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def multiply(a, b, q):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) % q
                 for i in range(2) for j in range(2))


def generated(matrices, q):
    identity = (1, 0, 0, 1)
    seen = {identity}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for y in matrices:
            z = multiply(x, y, q)
            if z not in seen:
                seen.add(z)
                queue.append(z)
    return seen


def act(v, m, q):
    return ((v[0]*m[0]+v[1]*m[2]) % q,
            (v[0]*m[1]+v[1]*m[3]) % q)


def fourier_nonzero(orbit, x, q, p):
    counts = [0]*q
    for v in orbit:
        counts[sum(a*b for a, b in zip(v, x)) % q] += 1
    # Phi_(p^e)(X) = 1 + X^(q/p) + ... + X^((p-1)q/p).
    step = q//p
    return any(len({counts[r+k*step] for k in range(p)}) != 1
               for r in range(step))


def periodic(orbit, q, bound):
    if not orbit:
        return True
    for v in orbit:
        for i in range(len(v)):
            w = list(v)
            w[i] = (w[i]+bound) % q
            if tuple(w) not in orbit:
                return False
    return True


def main():
    controls = 0
    for q, p in [(3, 3), (4, 2), (8, 2), (9, 3)]:
        points = [(i,) for i in range(q)]
        bounds = [p**i for i in range(q.bit_length()) if q % p**i == 0]
        for mask in range(1 << q):
            orbit = {v for i, v in enumerate(points) if mask & (1 << i)}
            for bound in bounds:
                vanishes = all(not fourier_nonzero(orbit, x, q, p)
                               for x in points if (bound*x[0]) % q)
                assert periodic(orbit, q, bound) == vanishes
                controls += 1
    # D16 = C8 semidirect C2, with inversion and a faithful linear character.
    # The induced degree-2 character is nonzero on its order-8 generator.
    assert fourier_nonzero({(1,), (7,)}, (1,), 8, 2)
    assert not periodic({(1,), (7,)}, 8, 4)
    print(f"PASS exhaustive Fourier controls={controls} positive_D16_control=1")

    text = (ROOT/'results/19.108-c27square.log').read_text()
    assert 'Error' not in text and 'Syntax' not in text
    rows = re.findall(r'^DATA class=(\d+) matrices=(.*)$', text, re.M)
    done = re.search(r'^DONE subgroup_classes=(\d+) regular_orbits=(\d+) '
                     r'periodicity_checks=(\d+) hits=(\d+) ms=(\d+)$', text, re.M)
    assert done, 'Missing completion marker'
    classes, expected_orbits, expected_checks, hits, _ = map(int, done.groups())
    assert len(rows) == classes and hits == 0
    assert [int(i) for i, _ in rows] == list(range(1, classes+1))
    sgens = [(1,1,0,1), (1,0,3,1), (4,0,0,1), (1,0,0,4)]
    sylow = generated(sgens, 27)
    assert len(sylow) == 19683
    expected_sylow = {(a,b,c,d) for a in range(1,27,3)
                      for b in range(27) for c in range(0,27,3)
                      for d in range(1,27,3)}
    assert sylow == expected_sylow
    points = set(product(range(27), repeat=2))
    primitive = [x for x in points if x[0] % 3 or x[1] % 3]
    seen_subgroups = set()
    regular = 0
    exact_sums = 0
    for identifier, literal in rows:
        matrices = [tuple(x for row in m for x in row) for m in ast.literal_eval(literal)]
        h = generated(matrices, 27)
        assert len(h) == 81 and h <= sylow
        key = frozenset(h)
        assert key not in seen_subgroups
        seen_subgroups.add(key)
        unseen = set(points)
        local_orbits = []
        while unseen:
            v = min(unseen)
            orbit = {act(v, m, 27) for m in h}
            assert orbit <= unseen
            unseen -= orbit
            if len(orbit) == 81:
                regular += 1
                local_orbits.append(orbit)
                assert periodic(orbit, 27, 9)
        # Full exact Fourier check on one regular orbit from every class that
        # has one; the translation check above covers every regular orbit.
        if local_orbits:
            for x in primitive:
                assert not fourier_nonzero(local_orbits[0], x, 27, 3)
                exact_sums += 1
        if int(identifier) % 100 == 0:
            print(f"REPLAY classes={identifier} regular_orbits={regular}", flush=True)
    assert regular == expected_orbits == expected_checks
    print(f"PASS sylow_elements=19683 distinct_subgroups={classes} "
          f"regular_orbits={regular} exact_cyclotomic_sums={exact_sums} hits=0")


if __name__ == '__main__':
    main()
