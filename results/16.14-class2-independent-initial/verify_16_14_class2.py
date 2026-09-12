#!/usr/bin/env python3
"""Reconstruct class-two square maps using only literal finite tables."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def log2(n):
    assert n > 0 and n & (n-1) == 0
    return n.bit_length()-1


def closure(table, gens):
    found, queue = {0}, [0]
    for x in queue:
        for g in gens:
            y = table[x][g]
            if y not in found:
                found.add(y); queue.append(y)
    return found


def quotient(table, domain, subgroup):
    labels, reps = {}, []
    for x in sorted(domain):
        if x not in labels:
            index = len(reps); reps.append(x)
            coset = {table[x][h] for h in subgroup}
            assert len(coset) == len(subgroup) and not coset.intersection(labels)
            labels.update({y:index for y in coset})
    assert set(labels) == set(domain)
    qt = [[labels[table[x][y]] for y in reps] for x in reps]
    return qt, reps, labels


def coordinates(table, subset):
    result = {0:0}; basis = []
    for g in sorted(subset):
        if g not in result:
            bit = 1 << len(basis); basis.append(g)
            added = {table[x][g]: value ^ bit for x, value in result.items()}
            assert not set(added).intersection(result)
            result.update(added)
    assert set(result) == set(subset)
    for x in subset:
        for y in subset:
            assert result[table[x][y]] == result[x] ^ result[y]
    return result, basis


def polynomial_check(q):
    n = log2(len(q))
    for x in range(1 << n):
        value = 0
        for i in range(n):
            if x >> i & 1:
                value ^= q[1 << i]
                for j in range(i):
                    if x >> j & 1:
                        value ^= q[(1 << i) | (1 << j)] ^ q[1 << i] ^ q[1 << j]
        assert q[x] == value


def check(model):
    table, gens = model['table'], model['generators']
    size = len(table); all_elements = set(range(size))
    assert all(len(row) == size and set(row) == all_elements for row in table)
    assert table[0] == list(range(size)) and all(table[x][0] == x for x in all_elements)
    assert all(g in all_elements for g in gens)
    assert all({table[x][g] for x in all_elements} == all_elements for g in gens)
    assert closure(table, gens) == all_elements
    # Every left translation commutes with each generating right translation.
    # Reachability extends this to every right translation and proves associativity.
    edges = 0
    for i in all_elements:
        for j in all_elements:
            for g in gens:
                assert table[table[i][j]][g] == table[i][table[j][g]]
                edges += 1
    inverse = [table[x].index(0) for x in range(size)]
    assert all(table[inverse[x]][x] == 0 for x in all_elements)
    z = {x for x in all_elements if all(table[x][g] == table[g][x] for g in gens)}
    for x in all_elements:
        for y in all_elements:
            comm = table[table[table[inverse[x]][inverse[y]]][x]][y]
            assert comm in z
    phi = closure(table, {table[x][x] for x in all_elements})
    z2 = {table[x][x] for x in z}; zp = z.intersection(phi)
    assert z2.issubset(zp)
    at, ar, al = quotient(table, all_elements, z)
    st, sr, sl = quotient(table, zp, z2)
    v = {x for x in range(len(at)) if at[x][x] == 0}
    vc, vb = coordinates(at, v)
    sc, sb = coordinates(st, range(len(st)))
    q = [None]*len(v)
    for x in v:
        q[vc[x]] = sc[sl[table[ar[x]][ar[x]]]]
    representative_checks = 0
    for x in all_elements:
        if al[x] in v:
            assert q[vc[al[x]]] == sc[sl[table[x][x]]]
            representative_checks += 1
    polynomial_check(q)
    polarization = [[q[x ^ y] ^ q[x] ^ q[y] for y in range(len(q))] for x in range(len(q))]
    triples = 0
    for x in range(len(q)):
        for y in range(len(q)):
            for w in range(len(q)):
                assert polarization[x ^ y][w] == polarization[x][w] ^ polarization[y][w]
                triples += 1
    involutions = {x for x in all_elements if table[x][x] == 0}
    central = involutions.issubset(z); zeros = q.count(0)
    assert (zeros == 1) == central
    d, r, c = log2(size//len(phi)), log2(len(z)//len(z2)), log2(len(z)//len(zp))
    n, s = log2(len(v)), log2(len(st))
    assert n == log2(len(at)//len({at[x][x] for x in range(len(at))}))
    assert d == n+c and r == c+s
    if central:
        assert n <= 2*s and d+c <= 2*r
    exponent = 1
    for x in all_elements:
        power, order = x, 1
        while power:
            power = table[power][x]; order += 1
            assert order <= size
        exponent = max(exponent, order)
    row = [size,exponent,d,r,c,n,s,int(central),zeros,len(involutions)]
    assert row == model['expected']
    return dict(label=model['label'], row=row, q=q,
                stats=dict(table_entries=size*size, associativity_generator_cases=edges,
                           representative_checks=representative_checks,
                           polarization_triples=triples))


def quadratic_controls():
    rows = []
    for n in range(1,6):
        monomials = [sum(((x >> i) & 1) << x for x in range(1 << n)) for i in range(n)]
        monomials += [sum((((x >> i) & 1) & ((x >> j) & 1)) << x for x in range(1 << n))
                      for i in range(n) for j in range(i)]
        masks = [0]
        for mono in monomials:
            masks += [m ^ mono for m in masks]
        all_bits = (1 << (1 << n))-1; nonzero_bits = all_bits ^ 1
        for s in ([1,2] if n <= 4 else [1]):
            count, unique = 0, 0
            for a in masks:
                for b in (masks if s == 2 else [0]):
                    mask = a | b
                    unique += mask == nonzero_bits; count += 1
                    if n > 2*s:
                        assert ((all_bits ^ mask).bit_count() & 1) == 0
            assert not (n > 2*s and unique)
            rows.append([n,s,count,unique])
    # An anisotropic cubic map F2^3 -> F2 shows why the degree bound matters.
    cubic = [int(x != 0) for x in range(8)]
    try:
        polynomial_check(cubic)
    except AssertionError:
        pass
    else:
        raise AssertionError('accepted cubic as quadratic')
    return rows


def main():
    models = [json.loads((ROOT/f'results/16.14-class2-model-{i}.json').read_text())
              for i in range(1,11)]
    cases = [check(model) for model in models]
    rejected = []
    for name, index, change in [
        ('wrong_product',4,lambda m:m['table'][1].__setitem__(1,1)),
        ('missing_generators',4,lambda m:m.update(generators=[])),
        ('wrong_centre_rank',4,lambda m:m['expected'].__setitem__(3,2)),
        ('false_central_involutions',3,lambda m:m['expected'].__setitem__(7,1)),
        ('wrong_zero_count',3,lambda m:m['expected'].__setitem__(8,1)),
    ]:
        broken = copy.deepcopy(models[index]); change(broken)
        try:
            check(broken)
        except (AssertionError, IndexError, KeyError, ValueError):
            rejected.append(name)
        else:
            raise AssertionError('accepted '+name)
    result = dict(status='PASS',cases=cases,quadratic_controls=quadratic_controls(),
                  rejected_corruptions=rejected,rejected_cubic_control=True,
                  stats={key:sum(c['stats'][key] for c in cases) for key in cases[0]['stats']},
                  scope='Finite controls for the class-two theorem; arbitrary class remains unresolved.')
    (ROOT/'results/16.14-class2-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
    print('PASS_16_14_CLASS2_INDEPENDENT models=10 rejected_corruptions=5')


if __name__ == '__main__':
    main()
