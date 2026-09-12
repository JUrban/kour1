#!/usr/bin/env python3
"""Verify permutation models and maximal N^3-subnormal chains, without GAP."""
from array import array
from collections import Counter, deque
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FiniteGroup:
    def __init__(self, row):
        self.n = n = row['catalogue_id'][0]
        self.e = e = row['identity']
        edges = row['cayley']
        perms = list(map(tuple, row['permutations']))
        assert len(edges) == n and 0 <= e < n and perms
        degree = len(perms[0])
        assert all(sorted(p) == list(range(degree)) for p in perms)
        assert all(len(r) == len(perms) and all(type(x) is int and 0 <= x < n for x in r)
                   for r in edges)
        model = {e: tuple(range(degree))}
        queue = deque([e])
        self.gens = list(edges[e])
        self.order = [e]
        parent = {}
        while queue:
            a = queue.popleft()
            for j, generator in enumerate(perms):
                b = edges[a][j]
                product = tuple(generator[k] for k in model[a])
                if b in model:
                    assert model[b] == product, 'permutation edge mismatch'
                else:
                    model[b] = product
                    parent[b] = (a, j)
                    self.order.append(b)
                    queue.append(b)
        assert len(model) == n and len(set(model.values())) == n
        self.table = []
        for a in range(n):
            products = array('H', [0])*n
            products[e] = a
            for b in self.order[1:]:
                u, j = parent[b]
                products[b] = edges[products[u]][j]
            self.table.append(products)
        self.inv = [next(b for b in range(n) if self.table[a][b] == e) for a in range(n)]
        assert all(self.table[self.inv[a]][a] == e for a in range(n))
        self.full = frozenset(range(n))
        self.cache = {}
        self.stats = Counter(permutation_edges=n*len(perms), table_entries=n*n)

    def subgroup(self, generators):
        key = tuple(sorted(generators))
        assert all(type(x) is int and 0 <= x < self.n for x in key)
        if key not in self.cache:
            found = {self.e}
            queue = deque([self.e])
            while queue:
                a = queue.popleft()
                for b in key:
                    c = self.table[a][b]
                    if c not in found:
                        found.add(c)
                        queue.append(c)
            self.cache[key] = frozenset(found)
        return self.cache[key]

    def conjugate(self, x, a):
        return self.table[self.table[self.inv[a]][x]][a]

    def normal(self, subgroup_gens, upper_gens):
        subgroup = self.subgroup(subgroup_gens)
        upper = self.subgroup(upper_gens)
        return subgroup <= upper and all(self.conjugate(x, a) in subgroup
                                         for x in subgroup_gens for a in upper_gens)

    def core(self, lower, upper_gens):
        current = lower
        while True:
            new = current.intersection(*(frozenset(self.conjugate(x, a) for x in current)
                                         for a in upper_gens))
            if new == current:
                return current
            current = new

    def maximal(self, lower_gens, upper_gens):
        lower, upper = self.subgroup(lower_gens), self.subgroup(upper_gens)
        assert lower < upper
        remaining = set(upper-lower)
        while remaining:
            x = min(remaining)
            assert self.subgroup(lower_gens+[x]) == upper, 'nonmaximal edge'
            remaining.difference_update(self.table[x][y] for y in lower)
            self.stats['maximal_cosets'] += 1

    def nilpotent_factor(self, lower_gens, upper_gens):
        assert self.normal(lower_gens, upper_gens)
        center, upper = self.subgroup(lower_gens), self.subgroup(upper_gens)
        while center != upper:
            next_center = frozenset(x for x in upper if all(
                self.table[self.inv[x]][self.conjugate(x, a)] in center
                for a in upper_gens))
            assert center < next_center, 'nonnilpotent factor'
            center = next_center
            self.stats['central_steps'] += 1
        self.stats['nilpotent_factors'] += 1

    def sylow_chain(self, row):
        p = row['prime']
        assert p > 1 and all(p % d for d in range(2, int(p**0.5)+1))
        power, remainder = 1, self.n
        while remainder % p == 0:
            remainder //= p
            power *= p
        sylow = self.subgroup(row['sylow'])
        assert len(sylow) == power
        normalizer = frozenset(a for a in range(self.n) if all(
            self.conjugate(x, a) in sylow for x in row['sylow']))
        target = self.subgroup(row['normalizer'])
        assert target == normalizer, 'incorrect Sylow normalizer'
        current = self.full
        for edge in row['chain']:
            upper, lower = self.subgroup(edge['upper']), self.subgroup(edge['lower'])
            assert current == upper and target <= lower
            self.maximal(edge['lower'], edge['upper'])
            core = self.core(lower, edge['upper'])
            assert core == self.subgroup(edge['core']), 'incorrect core'
            tower = edge['tower']
            assert 2 <= len(tower) <= 4
            assert self.subgroup(tower[0]) == core and self.subgroup(tower[-1]) == upper
            for gens in tower:
                assert self.normal(gens, edge['upper'])
            for a, b in zip(tower, tower[1:]):
                assert self.subgroup(a) < self.subgroup(b)
                self.nilpotent_factor(a, b)
            current = lower
            self.stats['chain_edges'] += 1
        assert current == target, 'incomplete chain'
        self.stats['sylow_chains'] += 1


def verify_group(row):
    group = FiniteGroup(row)
    assert group.normal(row['frattini'], group.gens)
    # The exact Frattini identification and catalogue label are not assumed
    # in verifying w*N^3 membership of the original group.
    primes = [s['prime'] for s in row['sylows']]
    assert len(primes) == len(set(primes))
    assert all(type(p) is int and p > 1 for p in primes)
    remainder = group.n
    for p in primes:
        while remainder % p == 0:
            remainder //= p
    assert remainder == 1
    for sylow in row['sylows']:
        group.sylow_chain(sylow)
    return group


def main():
    data = json.loads((ROOT/'results/20.112-chain-certificate.json').read_text())
    expected = {(1296, i) for i in list(range(2889,2893))+list(range(3081,3087))}
    expected |= {(1944,3453),(1944,3454),(432,734),(648,703),(648,704)}
    assert {tuple(r['catalogue_id']) for r in data['groups']} == expected
    assert len(data['groups']) == len(expected)
    stats = Counter()
    controls = None
    for row in data['groups']:
        group = verify_group(row)
        stats.update(group.stats)
        if controls is None:
            controls = (row, group)
        print('VERIFIED_GROUP', row['catalogue_id'], dict(sorted(group.stats.items())), flush=True)

    row, group = controls
    mutations = []
    changed = copy.deepcopy(row)
    changed['cayley'][group.e][0] = group.e
    mutations.append(('cayley', lambda: FiniteGroup(changed)))
    # Execute separately so lambda bindings cannot hide a mutation.
    rejected = []
    for name, operation in mutations:
        try:
            operation()
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('accepted corruption: '+name)
    for name in ['normalizer','core','tower','missing_edge']:
        bad = copy.deepcopy(row['sylows'][0])
        if name == 'normalizer':
            bad['normalizer'] = []
        elif name == 'core':
            edge = next(e for e in bad['chain'] if len(group.subgroup(e['core'])) > 1)
            edge['core'] = []
        elif name == 'tower':
            edge = next(e for e in bad['chain'] if len(e['tower']) > 2)
            edge['tower'] = [edge['tower'][0], edge['tower'][-1]]
        else:
            bad['chain'].pop()
        try:
            group.sylow_chain(bad)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('accepted corruption: '+name)
    result = dict(status='PASS_DIRECT_CERTIFICATES', groups=len(data['groups']),
                  original_retained_cases=12, distinct_quotient_models=3,
                  controls=dict(sorted(stats.items())), rejected_mutations=rejected,
                  imported=['GAP SmallGroups catalogue labels and completeness',
                            'exact Frattini identification and quotient-model identification'],
                  new_complete_candidates_added=0)
    (ROOT/'results/20.112-chain-controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS_20112_DIRECT groups=%d sylow_chains=%d chain_edges=%d mutations=%d' %
          (len(data['groups']),stats['sylow_chains'],stats['chain_edges'],len(rejected)))


if __name__ == '__main__':
    main()
