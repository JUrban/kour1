#!/usr/bin/env python3
"""Enumerate the complete supplied families of triple intersections."""
import argparse
import json
from pathlib import Path


def bitset(values):
    assert len(values) == len(set(values)) and all(type(x) is int and x >= 0 for x in values)
    return sum(1 << x for x in values)


def screen(path):
    data = json.loads(path.read_text())
    order = data['order']; count = data['catalogue_count']
    assert [g['id'] for g in data['groups']] == list(range(1,count+1))
    stats = dict(catalogue_groups=count,nilpotent_ambient=0,exported_groups=0,
                 active_classes=0,total_families=0,pair_trivial_shortcuts=0,
                 explicit_families=0,distinct_intersections=0,minimum_order_members=0,
                 inclusion_minimal_members=0)
    hits = []; group_rows = []
    for group in data['groups']:
        if group['nilpotent']:
            stats['nilpotent_ambient'] += 1
            continue
        stats['exported_groups'] += 1
        fit = bitset(group['fit']); assert fit & 1 and fit < 1 << order
        classes = []
        for rep, orbit in group['classes']:
            rep = bitset(rep); orbit = [bitset(h) for h in orbit]
            assert rep in orbit and len(set(orbit)) == len(orbit)
            assert all(h & 1 and h < 1 << order and h.bit_count() == rep.bit_count() for h in orbit)
            assert rep & ~fit
            classes.append((rep,orbit))
        k = len(classes); stats['active_classes'] += k
        checked = shortcuts = 0
        for ai,(a,_) in enumerate(classes):
            pair_sets = [set(a & b for b in orbit) for _,orbit in classes]
            for bi in range(k):
                for ci in range(bi,k):
                    stats['total_families'] += 1; checked += 1
                    if 1 in pair_sets[bi] or 1 in pair_sets[ci]:
                        stats['pair_trivial_shortcuts'] += 1; shortcuts += 1
                        continue
                    family = sorted({b & c for b in pair_sets[bi] for c in pair_sets[ci]},
                                    key=lambda h:(h.bit_count(),h))
                    assert family
                    minimum_size = family[0].bit_count()
                    smallest = [h for h in family if h.bit_count() == minimum_size]
                    minimal = []
                    for h in family:
                        if not any(m & h == m for m in minimal):minimal.append(h)
                    stats['explicit_families'] += 1
                    stats['distinct_intersections'] += len(family)
                    stats['minimum_order_members'] += len(smallest)
                    stats['inclusion_minimal_members'] += len(minimal)
                    bad_smallest = [h for h in smallest if h & ~fit]
                    bad_minimal = [h for h in minimal if h & ~fit]
                    if bad_minimal:
                        hits.append(dict(order=order,id=group['id'],soluble=group['soluble'],
                                         classes=[ai,bi,ci],minimum_size=minimum_size,
                                         outside_minimum_order=bad_smallest,
                                         outside_inclusion_minimal=bad_minimal,
                                         family=family))
        assert checked == k*k*(k+1)//2
        group_rows.append([group['id'],k,checked,shortcuts])
    assert stats['nilpotent_ambient']+stats['exported_groups'] == count
    return dict(status='COMPLETE_SUPPLIED_FAMILIES',order=order,stats=stats,
                group_rows=group_rows,hits=hits,
                scope='GAP catalogue and subgroup-class completeness imported; exported finite models require separate reconstruction.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input',type=Path)
    parser.add_argument('output',type=Path);args=parser.parse_args()
    result=screen(args.input);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'group_rows'},sort_keys=True))
    print(f'PASS_20_122_SCREEN order={result["order"]} hits={len(result["hits"])}')
