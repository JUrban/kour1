#!/usr/bin/env python3
"""Independent full orbital-colour automorphism enumeration; standard library only."""
import ast
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path


def compose(p, q):
    return tuple(q[x] for x in p)


def generated(gens, n):
    identity = tuple(range(n))
    known, todo = {identity}, [identity]
    for p in todo:
        for g in gens:
            q = compose(p, g)
            if q not in known:
                known.add(q)
                todo.append(q)
    return frozenset(known)


def point_orbits(group, n):
    unseen, answer = set(range(n)), []
    while unseen:
        i = min(unseen)
        orb = frozenset(g[i] for g in group)
        answer.append(orb)
        unseen -= orb
    return tuple(answer)


def colours(group, n):
    matrix = [[-1] * n for _ in range(n)]
    colour = 0
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                for p in group:
                    a, b = p[i], p[j]
                    assert matrix[a][b] in (-1, colour)
                    matrix[a][b] = colour
                colour += 1
    return tuple(map(tuple, matrix))


def automorphisms(matrix):
    """Enumerate ALL colour-preserving bijections, with no group-theory input."""
    n = len(matrix)
    initial = {i: tuple(j for j in range(n) if matrix[i][i] == matrix[j][j])
               for i in range(n)}
    mapping = [-1] * n
    answer = set()

    def visit(domains):
        if not domains:
            answer.add(tuple(mapping))
            return
        i = min(domains, key=lambda x: len(domains[x]))
        for j in domains[i]:
            remaining = {}
            for k, candidates in domains.items():
                if k == i:
                    continue
                compatible = tuple(l for l in candidates if l != j
                                   and matrix[i][k] == matrix[j][l]
                                   and matrix[k][i] == matrix[l][j])
                if not compatible:
                    break
                remaining[k] = compatible
            else:
                mapping[i] = j
                visit(remaining)
                mapping[i] = -1

    visit(initial)
    return frozenset(answer)


@lru_cache(maxsize=256)
def closure(group, n):
    return automorphisms(colours(group, n))


def quotient(p, orbits):
    locations = {o: i for i, o in enumerate(orbits)}
    return tuple(locations[frozenset(p[x] for x in o)] for o in orbits)


def decode(rows):
    return tuple(tuple(x - 1 for x in row) for row in rows)


def run():
    counts, enlarged, orbit_counts = Counter(), Counter(), Counter()
    maximum_degree, repeated = 0, 0
    sizes = {'C2_C3': (2, 3), 'Q8_C3': (8, 3),
             'S3_C5': (6, 5), 'A4_C5': (12, 5)}
    source = Path('results/20.1-actions.grows')
    for line_number, line in enumerate(source.read_text().splitlines(), 1):
        row = ast.literal_eval(line)
        label, indices, n, order, corder, acorder, bcorder, ps, cs, ag, bg = row
        group, claimed = frozenset(decode(ps)), frozenset(decode(cs))
        assert len(group) == order and len(claimed) == corder
        assert all(sorted(p) == list(range(n)) for p in group | claimed)
        A, B = generated(decode(ag), n), generated(decode(bg), n)
        assert (len(A), len(B)) == sizes[label]
        assert all(compose(a, b) == compose(b, a) for a in A for b in B)
        assert frozenset(compose(a, b) for a in A for b in B) == group
        ao, bo = point_orbits(A, n), point_orbits(B, n)
        assert all(len(a & b) <= 1 for a in ao for b in bo)
        aq = frozenset(quotient(a, bo) for a in A)
        bq = frozenset(quotient(b, ao) for b in B)
        assert len(aq) == len(A) and len(bq) == len(B)
        ac, bc = closure(aq, len(bo)), closure(bq, len(ao))
        actual = closure(group, n)
        assert actual == claimed, (line_number, label, indices)
        assert (len(ac), len(bc)) == (acorder, bcorder)
        assert all(quotient(c, bo) in ac and quotient(c, ao) in bc for c in actual)
        assert len(actual) <= len(ac) * len(bc)
        assert len({(quotient(c, bo), quotient(c, ao)) for c in actual}) == len(actual)
        if ac == aq and bc == bq:
            assert actual == group
        if label in ('C2_C3', 'Q8_C3'):
            assert actual == group
        enlarged[label] += int(actual != group)
        counts[label] += 1
        maximum_degree = max(n, maximum_degree)
        repeated += int(len(set(indices)) < len(indices))
        orbit_counts[len(point_orbits(group, n))] += 1

    # Coprimeness cannot be removed: even flips on three pairs form V4.
    a = (1, 0, 3, 2, 4, 5)
    b = (0, 1, 3, 2, 5, 4)
    V = generated((a, b), 6)
    VC = closure(V, 6)
    assert len(V) == 4 and len(VC) == 8
    va, vb = point_orbits(generated((a,), 6), 6), point_orbits(generated((b,), 6), 6)
    assert any(len(x & y) == 2 for x in va for y in vb)

    # Cross-orbit pair conditions matter: diagonal C3 versus independent C3^2.
    c = (1, 2, 0, 4, 5, 3)
    diagonal = generated((c,), 6)
    matrix = [list(row) for row in colours(diagonal, 6)]
    for i in range(3):
        for j in range(3, 6):
            matrix[i][j], matrix[j][i] = 100, 101
    assert len(closure(diagonal, 6)) == 3 and len(automorphisms(matrix)) == 9
    assert enlarged['S3_C5'] > 0 and enlarged['A4_C5'] > 0
    assert repeated > 0 and orbit_counts[1] > 0 and orbit_counts[3] > 0
    return dict(cases=sum(counts.values()), counts=dict(counts), enlarged=dict(enlarged),
                orbit_counts=dict(sorted(orbit_counts.items())), repeated_actions=repeated,
                maximum_degree=maximum_degree, shared_prime_mutation=[4, 8],
                cross_orbit_mutation=[3, 9],
                action_sha256=hashlib.sha256(source.read_bytes()).hexdigest())


if __name__ == '__main__':
    result = run()
    Path('results/20.1-controls.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
    print('PASS_201_CONTROLS', result['cases'])
