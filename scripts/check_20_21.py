#!/usr/bin/env python3
"""Table-only normal-subgroup and quotient controls for the 20.21 pilot."""
import ast
from collections import Counter
import hashlib
import json
from math import lcm
from pathlib import Path


def generated(table, generators, cap=None):
    generators = set(generators) - {0}
    known, todo = {0}, [0]
    for x in todo:
        for g in generators:
            y = table[x][g]
            if y not in known:
                known.add(y)
                todo.append(y)
                if cap is not None and len(known) > cap:
                    return None
    return frozenset(known)


def orders(table):
    out = []
    for i in range(len(table)):
        x, power = i, 1
        while x:
            x = table[x][i]
            power += 1
            assert power <= len(table)
        out.append(power)
    return out


def validate(table):
    n = len(table)
    assert table[0] == list(range(n))
    assert all(len(row) == n and sorted(row) == list(range(n)) for row in table)
    assert all(table[x][0] == x for x in range(n))
    for a in range(n):
        row_a = table[a]
        for b in range(n):
            row_ab, row_b = table[row_a[b]], table[b]
            assert all(row_ab[c] == row_a[row_b[c]] for c in range(n))
    return [row.index(0) for row in table]


def quotient(table, normal):
    n = len(table)
    owner = [-1] * n
    representatives = []
    for g in range(n):
        if owner[g] >= 0:
            continue
        i = len(representatives)
        representatives.append(g)
        for x in normal:
            owner[table[x][g]] = i
    assert all(i >= 0 for i in owner)
    return [[owner[table[a][b]] for b in representatives] for a in representatives]


def normal_subgroups(table, inverse, cap):
    n = len(table)
    conjugates = [frozenset(table[table[inverse[x]][g]][x] for x in range(n))
                  for g in range(n)]
    one = frozenset({0})
    known, todo = {one}, [one]
    for H in todo:
        for g in range(n):
            if g in H:
                continue
            K = generated(table, H | conjugates[g], cap)
            if K is not None and K not in known:
                known.add(K)
                todo.append(K)
    return known


def is_a4(table):
    if Counter(orders(table)) != {1: 1, 2: 3, 3: 8}:
        return False
    inv = [row.index(0) for row in table]
    threes = sorted({generated(table, [x]) for x, o in enumerate(orders(table)) if o == 3},
                    key=lambda H: sorted(H))
    assert len(threes) == 4
    images = set()
    for g in range(12):
        p = tuple(threes.index(frozenset(table[table[inv[g]][x]][g] for x in H)) for H in threes)
        assert sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0
        images.add(p)
    assert len(images) == 12  # Explicit faithful realization as A4.
    return True


def run():
    source = Path('results/20.21-tables.grows')
    cases = normal_count = cyclic = alternating = pairs = triples = 0
    ids = []
    for line in source.read_text().splitlines():
        identity, table, claimed_c, claimed_a, eligible = ast.literal_eval(
            line.replace('true', 'True').replace('false', 'False'))
        n = len(table)
        assert n == identity[0]
        inverse = validate(table)
        triples += n ** 3
        normals = normal_subgroups(table, inverse, n // 12)
        ns = sorted((H for H in normals if len(H) == n // 12), key=lambda H: sorted(H))
        cc, aa = set(), set()
        for H in ns:
            assert all(table[table[inverse[g]][h]][g] in H for g in range(n) for h in H)
            q = quotient(table, H)
            if max(orders(q)) == 12:
                cc.add(H)
            elif is_a4(q):
                aa.add(H)
        assert cc == {frozenset(H) for H in claimed_c}
        assert aa == {frozenset(H) for H in claimed_a}
        commutators = {table[table[table[inverse[a]][inverse[b]]][a]][b]
                       for a in range(n) for b in range(n)}
        derived = generated(table, commutators)
        assert (lcm(*orders(quotient(table, derived))) % 12 == 0) == eligible
        assert bool(cc) == eligible
        all_orders = orders(table)
        for K in cc:
            for L in aa:
                # The selected controls have explicit nonisomorphism witnesses.
                assert Counter(all_orders[x] for x in K) != Counter(all_orders[x] for x in L)
                pairs += 1
        ids.append(identity)
        cases += 1
        normal_count += len(ns)
        cyclic += len(cc)
        alternating += len(aa)

    # A bare 2-group CAN have isomorphic kernels with C4 and V4 quotients.
    # M16 = C8 semidirect C2, the involution acting by a -> a^5.
    atoms = [(i, j) for j in range(2) for i in range(8)]
    table = [[atoms.index(((i + pow(5, j, 8) * k) % 8, (j + l) % 2))
              for k, l in atoms] for i, j in atoms]
    inverse = validate(table)
    K = generated(table, [atoms.index((2, 0))])
    L = generated(table, [atoms.index((2, 1))])
    assert len(K) == len(L) == 4
    assert max(orders(table)[x] for x in K) == max(orders(table)[x] for x in L) == 4
    assert Counter(orders(quotient(table, K))) == {1: 1, 2: 3}
    assert Counter(orders(quotient(table, L))) == {1: 1, 2: 1, 4: 2}
    assert all(table[table[inverse[g]][h]][g] in H for H in (K, L) for g in range(16) for h in H)
    assert cases == 25 and pairs == 6
    return dict(cases=cases, ids=ids, associativity_triples=triples + 16 ** 3,
                normal_index12_subgroups=normal_count, cyclic_quotient_kernels=cyclic,
                a4_quotient_kernels=alternating, nonisomorphic_kernel_pairs=pairs,
                mutation={'order': 16, 'kernels': 'C4,C4', 'quotients': 'V4,C4'},
                table_sha256=hashlib.sha256(source.read_bytes()).hexdigest())


if __name__ == '__main__':
    result = run()
    Path('results/20.21-controls.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
    print('PASS_2021_CONTROLS', result['cases'])
