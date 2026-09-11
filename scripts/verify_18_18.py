#!/usr/bin/env python3
"""Literal incidence and permutation-propagation controls for 18.18."""
from collections import deque
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time


def mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p):
    out = [0]*len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def sigma_incidence(n, exceptional=False):
    one = tuple(range(n))
    if exceptional:
        c = [p for p in permutations(range(n)) if mul(p, p) == one and
             all(p[i] != i for i in range(n))]
    else:
        c = []
        for i, j in combinations(range(n), 2):
            p = list(one)
            p[i], p[j] = p[j], p[i]
            c.append(tuple(p))
    m = len(c)
    adj = [[i != j and mul(c[i], c[j]) != mul(c[j], c[i])
            for j in range(m)] for i in range(m)]
    stars, quads = set(), 0
    for q in combinations(range(m), 4):
        if not all(adj[i][j] for i, j in combinations(q, 2)):
            continue
        quads += 1
        stars.add(frozenset(i for i in range(m) if all(i == j or adj[i][j] for j in q)))
    assert len(stars) == n
    assert all(sum(i in s for s in stars) == 2 for i in range(m))
    assert all(len(s & t) == 1 for s, t in combinations(stars, 2))
    for i in range(m):
        image = [c.index(mul(mul(c[i], x), inv(c[i]))) for x in c]
        for s in stars:
            moved = frozenset(image[j] for j in s)
            assert moved in stars and (moved == s) == (i not in s)
    return [n, exceptional, m, len(stars), quads]


def fixtures():
    for n in range(1, 9):
        yield 'C'+str(n), list(range(n)), lambda x, y, n=n: (x+y) % n
    for mods in [(2, 2), (4, 2), (2, 2, 2)]:
        yield 'x'.join('C'+str(n) for n in mods), list(product(*(range(n) for n in mods))), \
            lambda x, y, mods=mods: tuple((a+b) % n for a, b, n in zip(x, y, mods))
    yield 'D8', list(product(range(4), range(2))), \
        lambda x, y: ((x[0]+(-1)**x[1]*y[0]) % 4, (x[1]+y[1]) % 2)
    # Entries (sign, basis), with basis 0=1, 1=i, 2=j, 3=k.
    def quaternion(x, y):
        sx, a = x
        sy, b = y
        if a == 0:
            return sx*sy, b
        if b == 0:
            return sx*sy, a
        if a == b:
            return -sx*sy, 0
        return sx*sy*(1 if (a, b) in [(1, 2), (2, 3), (3, 1)] else -1), 6-a-b
    yield 'Q8', list(product([1, -1], range(4))), quaternion
    yield 'S3', list(permutations(range(3))), mul


def orbit_centralizers(a, b):
    """Exhaust all commuting permutations by propagating one point image.

    The inputs here have pairwise different orbit sizes, so a commuting
    permutation must preserve each orbit. Transitive propagation is unique.
    """
    n = len(a)
    generators = [a, b, inv(a), inv(b)]
    remaining, orbits = set(range(n)), []
    while remaining:
        seen, queue = {min(remaining)}, deque([min(remaining)])
        while queue:
            x = queue.popleft()
            for g in generators:
                if g[x] not in seen:
                    seen.add(g[x])
                    queue.append(g[x])
        remaining -= seen
        orbits.append(sorted(seen))
    assert len(set(map(len, orbits))) == len(orbits)
    factors = []
    for orbit in orbits:
        choices = []
        for target in orbit:
            mapping, queue, consistent = {orbit[0]: target}, deque([orbit[0]]), True
            while queue and consistent:
                x = queue.popleft()
                for g in generators:
                    source, image = g[x], g[mapping[x]]
                    if source in mapping:
                        if mapping[source] != image:
                            consistent = False
                            break
                    else:
                        mapping[source] = image
                        queue.append(source)
            if consistent and len(mapping) == len(orbit) and len(set(mapping.values())) == len(orbit):
                choices.append(mapping)
        factors.append(choices)
    out = set()
    for choices in product(*factors):
        p = list(range(n))
        for mapping in choices:
            for x, y in mapping.items():
                p[x] = y
        p = tuple(p)
        assert mul(p, a) == mul(a, p) and mul(p, b) == mul(b, p)
        out.add(p)
    return out


start = time.monotonic()
incidence = [sigma_incidence(n) for n in range(5, 10)]+[sigma_incidence(6, True)]
centralizer_rows, table_checks = [], 0
for name, elements, operation in fixtures():
    h = len(elements)
    # Find and put the identity first without assuming fixture ordering.
    identity = next(e for e in elements if all(operation(e, x) == operation(x, e) == x for x in elements))
    elements = [identity]+[x for x in elements if x != identity]
    table = [[elements.index(operation(x, y)) for y in elements] for x in elements]
    for x, y, z in product(range(h), repeat=3):
        assert table[table[x][y]][z] == table[x][table[y][z]]
        table_checks += 1
    assert all(any(table[x][y] == table[y][x] == 0 for y in range(h)) for x in range(h))
    a = tuple(g*h+(j+1) % h for g in range(h) for j in range(h))
    b = tuple(table[g][j]*h+j for g in range(h) for j in range(h))
    left = {tuple(table[l][g]*h+j for g in range(h) for j in range(h)) for l in range(h)}
    assert orbit_centralizers(a, b) == left
    for n in [2*h*h+3, 2*h*h+4]:
        ap = a+tuple(range(h*h+1, n))+(h*h,)
        bp = b+(h*h+1, h*h)+tuple(range(h*h+2, n))
        found = orbit_centralizers(ap, bp)
        expected = {p+tuple(range(h*h, n)) for p in left}
        assert found == expected
        centralizer_rows.append([name, h, n, len(found)])
report = dict(status='PASS', incidence=incidence, finite_groups=14,
              table_associativity_checks=table_checks,
              main_centralizers=14, padded_centralizers=len(centralizer_rows),
              centralizer_rows=centralizer_rows, seconds=time.monotonic()-start)
Path('results/18.18-python.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
