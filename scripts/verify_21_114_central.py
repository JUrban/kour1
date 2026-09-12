#!/usr/bin/env python3
"""Independently check finite central extensions and all quotient subgroups."""
from collections import Counter, deque
import copy
import json
from pathlib import Path

from verify_20_112_chains import FiniteGroup

ROOT = Path(__file__).resolve().parents[1]


def comm(f, a, b):
    t = f.table
    return t[t[t[f.inv[a]][f.inv[b]]][a]][b]


def derived(f, subgroup):
    generators = sorted({comm(f, a, b) for a in subgroup for b in subgroup})
    f.stats['commutator_pairs'] += len(subgroup)**2
    return f.subgroup(generators)


def subgroups(f):
    trivial = frozenset([f.e])
    found = {trivial: []}
    queue = deque([trivial])
    while queue:
        subgroup = queue.popleft()
        basis = found[subgroup]
        remaining = set(f.full-subgroup)
        while remaining:
            x = min(remaining)
            new_basis = basis+[x]
            new = f.subgroup(new_basis)
            if new not in found:
                found[new] = new_basis
                queue.append(new)
            remaining.difference_update(f.table[s][x] for s in subgroup)
    return found


def verify(pdata, qdata, mapping):
    p, q = FiniteGroup(pdata), FiniteGroup(qdata)
    assert p.n == mapping['source_order'] == 512 and q.n == 128
    z = frozenset(mapping['central_kernel'])
    assert len(z) == mapping['kernel_order'] == 4
    zgen = next((x for x in sorted(z) if p.subgroup([x]) == z), None)
    assert zgen is not None, 'kernel must be cyclic of order four'
    assert all(p.table[a][b] == p.table[b][a] for a in z for b in p.full), 'noncentral kernel'
    phi = mapping['quotient_map']
    assert len(phi) == p.n and set(phi) == set(q.full)
    assert phi[p.e] == q.e
    assert frozenset(x for x in p.full if phi[x] == q.e) == z, 'wrong kernel'
    for a in p.full:
        for b in p.full:
            assert phi[p.table[a][b]] == q.table[phi[a]][phi[b]], 'not a homomorphism'
    pd = derived(p, p.full)
    pdd = derived(p, pd)
    pddd = derived(p, pdd)
    assert len(pdd) == 2 and pddd == frozenset([p.e]), 'wrong derived length'
    assert pdd <= z
    qd = derived(q, q.full)
    assert derived(q, qd) == frozenset([q.e])
    bound = q.n//len(qd)
    assert bound == 16
    all_subgroups = subgroups(q)
    distribution = Counter()
    lift_distribution = Counter()
    worst_lift = None
    for subgroup in all_subgroups:
        d = derived(q, subgroup)
        a = len(subgroup)//len(d)
        assert a <= bound, 'quotient is not weakly ab-maximal'
        distribution[(len(subgroup), a)] += 1
        lift = frozenset(x for x in p.full if phi[x] in subgroup)
        lift_d = derived(p, lift)
        lift_a = len(lift)//len(lift_d)
        lift_distribution[(len(lift), lift_a)] += 1
        if worst_lift is None or lift_a > worst_lift[0]:
            worst_lift = [lift_a, sorted(lift), sorted(lift_d)]
    witness = next((a, b) for a in sorted(pd) for b in sorted(pd) if comm(p, a, b) != p.e)
    stats = p.stats+q.stats
    stats['homomorphism_products'] += p.n*p.n
    stats['quotient_subgroups'] += len(all_subgroups)
    return {
        'source_id': mapping['source_id'], 'source_order': p.n, 'quotient_order': q.n,
        'kernel_order': len(z), 'kernel_generator': zgen,
        'derived_orders': [p.n, len(pd), len(pdd), len(pddd)],
        'second_derived_witness': [*witness, comm(p, *witness)],
        'quotient_abelianization': bound,
        'quotient_subgroups': len(all_subgroups),
        'subgroup_distribution': [[*key, value] for key, value in sorted(distribution.items())],
        'source_abelianization': p.n//len(pd),
        'source_maximum_subgroup_abelianization': worst_lift[0],
        'source_maximizing_subgroup': worst_lift[1],
        'source_maximizing_subgroup_derived': worst_lift[2],
        'lift_distribution': [[*key, value] for key, value in sorted(lift_distribution.items())],
        'constructed_order': p.n*len(z)**2,
        'constructed_abelianization': bound*len(z)**2,
        'stats': dict(stats),
    }


def main():
    results = []
    loaded = []
    native = []
    for ident in [854, 860]:
        base = ROOT/f'results/21.114-central-{ident}'
        p, q, mapping = [json.loads(Path(str(base)+suffix).read_text())
                         for suffix in ['-p.json', '-q.json', '-map.json']]
        result = verify(p, q, mapping)
        results.append(result)
        loaded.append((p, q, mapping))
        native.append([ident, [[x+1 for x in perm] for perm in p['permutations']],
                       result['kernel_generator']+1])
    controls = []
    for kind in ['permutation', 'edge', 'kernel', 'map', 'order']:
        p, q, mapping = copy.deepcopy(loaded[0])
        if kind == 'permutation':
            p['permutations'][0][0] = p['permutations'][0][1]
        elif kind == 'edge':
            p['cayley'][0][0] = (p['cayley'][0][0]+1)%p['catalogue_id'][0]
        elif kind == 'kernel':
            mapping['central_kernel'] = mapping['central_kernel'][:-1]
        elif kind == 'map':
            mapping['quotient_map'][0] = (mapping['quotient_map'][0]+1)%q['catalogue_id'][0]
        else:
            mapping['source_order'] += 1
        try:
            verify(p, q, mapping)
        except (AssertionError, StopIteration):
            controls.append(kind)
        else:
            raise AssertionError('accepted corruption '+kind)
    total = Counter()
    for result in results:
        total.update(result['stats'])
    output = {'status': 'PASS', 'cases': results, 'stats': dict(total),
              'rejected_corruptions': controls,
              'scope': 'Exact permutation models, full quotient subgroup enumeration, central maps and derived series. The resulting central-product inequality is proved in the companion mathematical note.'}
    (ROOT/'results/21.114-independent-summary.json').write_text(json.dumps(output, indent=2)+'\n')
    (ROOT/'results/21.114-native-input.g').write_text('NativeInputs114 := '+json.dumps(native)+';;\n')
    print('PASS_21114_INDEPENDENT', json.dumps(dict(total), sort_keys=True))


if __name__ == '__main__':
    main()
