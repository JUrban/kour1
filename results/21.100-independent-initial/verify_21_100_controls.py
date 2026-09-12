#!/usr/bin/env python3
"""Exact induced-character verification from permutations and linear maps."""
from collections import Counter, deque
import copy
import json
from pathlib import Path
from verify_20_112_chains import FiniteGroup

ROOT = Path(__file__).resolve().parents[1]


class Cyclotomic:
    def __init__(self, m):
        t = m
        while t > 1 and t % 3 == 0:
            t //= 3
        assert t == 1 and m >= 3
        self.m, self.u, self.d = m, m//3, 2*m//3
        self.zero = (0,)*self.d
        self.roots = []
        for i in range(m):
            row = [0]*self.d
            if i < self.d:
                row[i] = 1
            else:
                row[i-self.u] = row[i-2*self.u] = -1
            self.roots.append(tuple(row))

    def root_sum(self, powers):
        result = [0]*self.d
        for power in powers:
            for i,v in enumerate(self.roots[power % self.m]):
                result[i] += v
        return tuple(result)

    def conjugate(self, a):
        result = [0]*self.d
        for i,v in enumerate(a):
            if v:
                for j,c in enumerate(self.roots[-i % self.m]):
                    result[j] += v*c
        return tuple(result)

    def multiply(self, a, b):
        result = [0]*self.d
        for i,v in enumerate(a):
            if v:
                for j,w in enumerate(b):
                    if w:
                        for k,c in enumerate(self.roots[(i+j) % self.m]):
                            result[k] += v*w*c
        return tuple(result)

    def inner(self, a, b, classes, order):
        result = [0]*self.d
        for x,y,cl in zip(a,b,classes):
            z = self.multiply(x,self.conjugate(y))
            for i,v in enumerate(z):
                result[i] += len(cl)*v
        assert all(v == 0 for v in result[1:]) and result[0] % order == 0
        return result[0]//order


def conjugacy_classes(group, gens):
    remaining = set(group.subgroup(gens))
    classes = []
    index = {}
    while remaining:
        first = min(remaining)
        members = {first}
        queue = deque([first])
        while queue:
            x = queue.popleft()
            for a in gens:
                y = group.conjugate(x,a)
                if y not in members:
                    members.add(y); queue.append(y)
        assert members <= remaining
        for x in members:
            index[x] = len(classes)
        remaining -= members
        classes.append(sorted(members))
    return classes,index


def character_basis(group, gens, packets, ring, stats):
    elements = group.subgroup(gens)
    classes,index = conjugacy_classes(group,gens)
    chars = []
    fingerprints = set()
    for hgens,pairs in packets:
        h = group.subgroup(hgens)
        assert h <= elements and len(pairs) == len(h)
        values = dict(pairs)
        assert len(values) == len(pairs) and set(values) == h and values[group.e] == 0
        assert all(type(v) is int and 0 <= v < ring.m for v in values.values())
        for x in h:
            for a in hgens:
                assert values[group.table[x][a]] == (values[x]+values[a]) % ring.m
                stats['linear_map_edges'] += 1
        remaining = set(elements)
        reps = []
        while remaining:
            r = min(remaining)
            coset = {group.table[x][r] for x in h}
            assert coset <= remaining
            remaining -= coset
            reps.append(r)
        induced = []
        for cl in classes:
            g = cl[0]
            powers = []
            for r in reps:
                x = group.table[group.table[r][g]][group.inv[r]]
                if x in h:
                    powers.append(values[x])
            induced.append(ring.root_sum(powers))
            stats['induced_class_values'] += 1
        degree = len(reps)
        assert induced[index[group.e]] == (degree,)+(0,)*(ring.d-1)
        assert ring.inner(induced,induced,classes,len(elements)) == 1
        fingerprint = tuple(induced)
        assert fingerprint not in fingerprints
        fingerprints.add(fingerprint)
        chars.append((degree,induced))
        stats['certified_irreducibles'] += 1
    assert sum(degree**2 for degree,values in chars) == len(elements), 'incomplete character basis'
    assert len(chars) == len(classes)
    return chars,classes,index


def derived_subgroup(group, gens):
    generators = {group.table[group.inv[x]][group.conjugate(x,a)] for x in gens for a in gens}
    while True:
        subgroup = group.subgroup(sorted(generators))
        more = {group.conjugate(x,a) for x in generators for a in gens}
        if more <= subgroup:
            return subgroup
        generators |= more


def verify_case(row):
    group = FiniteGroup(row)
    ring = Cyclotomic(row['root_order'])
    stats = Counter(group.stats)
    auto = row['automorphism']
    assert sorted(auto) == list(range(group.n)) and any(auto[i] != i for i in range(group.n))
    assert all(auto[auto[i]] == i for i in range(group.n))
    for x in range(group.n):
        for a in group.gens:
            assert auto[group.table[x][a]] == group.table[auto[x]][auto[a]], 'not an automorphism'
            stats['automorphism_edges'] += 1
    fixed = frozenset(x for x in range(group.n) if auto[x] == x)
    cgens = row['fixed_generators']
    assert group.subgroup(cgens) == fixed
    cab = len(fixed)//len(derived_subgroup(group,cgens))
    assert [len(fixed),cab] == row['expected_fixed'][:2]
    chars,classes,index = character_basis(group,group.gens,row['group_characters'],ring,stats)
    cchars,cclasses,cindex = character_basis(group,cgens,row['fixed_characters'],ring,stats)
    assert max(d for d,v in cchars) == row['expected_fixed'][2]
    assert sum(d == 1 for d,v in cchars) == cab
    summary = []
    never_count = 0
    for degree,values in chars:
        if not all(values[i] == values[index[auto[cl[0]]]] for i,cl in enumerate(classes)):
            continue
        restriction = [values[index[cl[0]]] for cl in cclasses]
        mult = [ring.inner(restriction,v,cclasses,len(fixed)) for d,v in cchars]
        assert all(x >= 0 for x in mult)
        assert sum(x*d for x,(d,v) in zip(mult,cchars)) == degree
        odd = [i for i,x in enumerate(mult) if x % 2]
        assert len(odd) == 1
        correspondent_degree = cchars[odd[0]][0]
        zero_witness = next((cl[0] for cl,v in zip(cclasses,restriction) if v == ring.zero),None)
        never = zero_witness is None
        assert never == (correspondent_degree == 1), 'pointwise counterexample'
        never_count += never
        summary.append(dict(degree=degree,correspondent_degree=correspondent_degree,
                            nonvanishing=never,zero_witness=zero_witness))
        stats['invariant_characters'] += 1
        stats['restriction_multiplicities'] += len(cchars)
        stats['nonlinear_correspondents'] += correspondent_degree > 1
    assert len(summary) == len(cchars) and never_count == cab
    stats['groups'] += 1
    return dict(catalogue_id=row['catalogue_id'],fixed_order=len(fixed),fixed_abelianization=cab,
                characters=summary),stats


def main():
    data = json.loads((ROOT/'results/21.100-independent-certificate.json').read_text())
    expected = {(243,51),(243,56),(729,138),(729,245),(729,258),(729,268),(729,402)}
    assert {tuple(r['catalogue_id']) for r in data['groups']} == expected
    assert len(data['groups']) == 7
    summaries = []
    total = Counter()
    for row in data['groups']:
        summary,stats = verify_case(row)
        summaries.append(summary); total.update(stats)
        print('VERIFIED',row['catalogue_id'],dict(sorted(stats.items())),flush=True)
    rejected = []
    for name in ['cayley','automorphism','linear_map','missing_character','inducing_subgroup']:
        bad = copy.deepcopy(data['groups'][0])
        if name == 'cayley':
            bad['cayley'][bad['identity']][0] = bad['identity']
        elif name == 'automorphism':
            bad['automorphism'][0],bad['automorphism'][1] = bad['automorphism'][1],bad['automorphism'][0]
        elif name == 'linear_map':
            pairs = bad['group_characters'][0][1]
            pair = next(x for x in pairs if x[0] == bad['identity'])
            pair[1] = 1
        elif name == 'missing_character':
            bad['group_characters'].pop()
        else:
            bad['group_characters'][0][0] = []
        try:
            verify_case(bad)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('accepted corruption '+name)
    result = dict(status='PASS_INDEPENDENT_CHARACTERS',counts=dict(sorted(total.items())),
                  groups=summaries,rejected_mutations=rejected,new_complete_candidates_added=0)
    (ROOT/'results/21.100-independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_21100_INDEPENDENT models=7 irreducibles=%d invariant=%d nonlinear=%d mutations=5' %
          (total['certified_irreducibles'],total['invariant_characters'],total['nonlinear_correspondents']))


if __name__ == '__main__':
    main()
