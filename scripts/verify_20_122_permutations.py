#!/usr/bin/env python3
"""Independent S4 x C2 reconstruction; no GAP library or catalogue input."""
import copy
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    elements = sorted(tuple(p)+q for p in itertools.permutations(range(1,5))
                      for q in [(5,6),(6,5)])
    pos = {x:i for i,x in enumerate(elements)}
    # Right-action convention: apply x, then y.
    table = [[pos[tuple(y[v-1] for v in x)] for y in elements] for x in elements]
    unit = pos[tuple(range(1,7))]
    assert unit == 0
    n = len(elements)
    inverse = [next(y for y in range(n) if table[x][y] == unit and table[y][x] == unit)
               for x in range(n)]
    assert all(table[table[x][y]][w] == table[x][table[y][w]]
               for x in range(n) for y in range(n) for w in range(n))

    def closure(gens):
        gens = set(gens)
        seen = {unit}; todo = [unit]
        while todo:
            x = todo.pop()
            for y in gens:
                v = table[x][y]
                if v not in seen: seen.add(v); todo.append(v)
        return frozenset(seen)

    def conjugate(h,x):
        return frozenset(table[table[inverse[x]][v]][x] for v in h)

    def comm(x,y):
        return table[table[table[inverse[x]][inverse[y]]][x]][y]

    def upper_central(h):
        current = frozenset([unit]); orders = [1]
        while current != h:
            new = frozenset(x for x in h if all(comm(x,y) in current for y in h))
            if new == current: break
            current = new; orders.append(len(current))
        return current == h, orders

    def normalize(family):
        return sorted(sorted(h) for h in family)

    r = pos[(2,3,4,1,5,6)]; s = pos[(1,4,3,2,5,6)]; z = pos[(1,2,3,4,6,5)]
    rz = table[r][z]
    t = [table[r][r],pos[(2,1,4,3,5,6)],pos[(4,3,2,1,5,6)]]
    a = closure([r,s,z]); b = closure([rz,s]); c = closure([r,z])
    expected_fit = closure(t+[z])
    assert [len(h) for h in [a,b,c]] == [16,8,8]
    nilpotency = [upper_central(h) for h in [a,b,c]]
    assert all(v[0] for v in nilpotency)

    # Every subgroup is reached from 1 by adjoining one element at a time.
    # Thus this enumeration independently determines every normal nilpotent subgroup.
    subgroups = {frozenset([unit])}; todo = list(subgroups)
    while todo:
        h = todo.pop()
        for x in range(n):
            if x in h: continue
            k = closure(set(h)|{x})
            if k not in subgroups: subgroups.add(k); todo.append(k)
    normals = [h for h in subgroups if all(conjugate(h,x) == h for x in range(n))]
    normal_nilpotents = [h for h in normals if upper_central(h)[0]]
    fit = closure(set().union(*normal_nilpotents))
    assert fit == expected_fit and upper_central(fit)[0]
    derived = frozenset(range(n)); derived_orders = [n]
    while len(derived) > 1:
        new = closure(comm(x,y) for x in derived for y in derived)
        assert new != derived
        derived = new; derived_orders.append(len(derived))

    b_conjugates = [conjugate(b,x) for x in range(n)]
    c_conjugates = [conjugate(c,x) for x in range(n)]
    family = {a & bx & cy for bx in b_conjugates for cy in c_conjugates}
    minimal = {h for h in family if not any(k < h for k in family)}
    smallest = {h for h in family if len(h) == min(map(len,family))}
    expected_family = {closure([rz]),closure([table[t[0]][z]])}
    for v in t[1:]: expected_family |= {closure([v]),closure([table[v][z]])}
    assert family == expected_family and minimal == family
    assert sorted(map(len,family)) == [2,2,2,2,2,4]
    lower = closure(set().union(*smallest)); upper = closure(set().union(*minimal))
    assert lower == fit and upper == a and rz not in fit
    normal_closure = closure(table[table[inverse[x]][rz]][x] for x in range(n))
    assert not upper_central(normal_closure)[0]

    data = dict(elements=[list(x) for x in elements],table=table,a=sorted(a),b=sorted(b),
                c=sorted(c),fit=sorted(fit),b_orbit=normalize(set(b_conjugates)),
                c_orbit=normalize(set(c_conjugates)),family=normalize(family),
                minimal=normalize(minimal),smallest=normalize(smallest),
                Min=sorted(upper),min=sorted(lower))
    native = json.loads((ROOT/'results/20.122-native-model.json').read_text())

    def check(candidate):
        assert candidate == data

    check(native)
    corruptions = {}
    changed = copy.deepcopy(native); changed['b'] = changed['c']; corruptions['wrong_B'] = changed
    changed = copy.deepcopy(native); changed['family'].pop(); corruptions['omitted_intersection'] = changed
    changed = copy.deepcopy(native); changed['minimal'].append(sorted(closure([t[0]])))
    corruptions['invented_minimal_member'] = changed
    changed = copy.deepcopy(native); changed['fit'].append(rz); corruptions['false_fitting_member'] = changed
    changed = copy.deepcopy(native); changed['smallest'] = changed['minimal']; corruptions['conflated_minima'] = changed
    rejected = []
    for name,changed in corruptions.items():
        try: check(changed)
        except AssertionError: rejected.append(name)
        else: raise AssertionError(name)
    summary = dict(status='PASS',order=n,all_subgroups=len(subgroups),normal_subgroups=len(normals),
                   normal_nilpotent_subgroups=len(normal_nilpotents),nilpotency_orders=[v[1] for v in nilpotency],
                   derived_orders=derived_orders,multiplication_entries=n*n,associativity_triples=n**3,
                   conjugating_pairs=n*n,b_orbit=len(set(b_conjugates)),c_orbit=len(set(c_conjugates)),
                   intersection_orders=sorted(map(len,family)),Min_order=len(upper),min_order=len(lower),
                   fitting_order=len(fit),outside_element=elements[rz],
                   outside_normal_closure_order=len(normal_closure),rejected_corruptions=rejected)
    (ROOT/'results/20.122-permutations-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
    print('PASS_20_122_PERMUTATIONS rejected_corruptions=5')


if __name__ == '__main__': main()
