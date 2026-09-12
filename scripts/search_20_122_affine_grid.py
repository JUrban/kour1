#!/usr/bin/env python3
"""Sufficient minimum-order obstruction in coordinate modules on a 3x3 grid.

Exploratory only. Each support is invariant under the signed coordinate
permutations fixing its center. A shared involution is forced for every
module translation if each of its moved pairs belongs to at least two
of the three supports. This sufficient criterion is verified separately
before any hit can be promoted to a proof.
"""
import itertools
import json
from pathlib import Path


def main():
    points = list(itertools.product(range(3),repeat=2)); pos = {v:i for i,v in enumerate(points)}
    identity = tuple(range(9)); group = set()
    for swap,a,b,u,v in itertools.product(range(2),[1,2],[1,2],range(3),range(3)):
        perm = []
        for x,y in points:
            if swap:x,y=y,x
            perm.append(pos[((a*x+u)%3,(b*y+v)%3)])
        group.add(tuple(perm))
    group = sorted(group); assert len(group) == 72
    stabilizers = [{g for g in group if g[i] == i} for i in range(9)]
    assert all(len(h) == 8 for h in stabilizers)
    supports = []
    for mask in range(8):
        centered = []
        for u,v in points:
            support = set()
            for i,(x,y) in enumerate(points):
                dx,dy = (x-u)%3,(y-v)%3
                orbit = 0 if dx == dy == 0 else (1 if dx == 0 or dy == 0 else 2)
                if mask >> orbit & 1:support.add(i)
            centered.append(frozenset(support))
        supports.append(centered)
    shared = {(b,c):stabilizers[0]&stabilizers[b]&stabilizers[c]
              for b in range(9) for c in range(9)}

    def forced(h,sets):
        if h == identity or any(h[h[i]] != i for i in range(9)):return False
        return all(sum(i in s for s in sets) >= 2 for i in range(9) if h[i] != i)

    hits = []; triples = 0
    for ma,mb,mc in itertools.combinations_with_replacement(range(8),3):
        triples += 1; rows = []
        for b,c in itertools.product(range(9),repeat=2):
            sets = [supports[ma][0],supports[mb][b],supports[mc][c]]
            k = len(set.intersection(*(set(s) for s in sets)))
            h = shared[b,c]; forced_h = [list(g) for g in sorted(h) if forced(g,sets)]
            rows.append(dict(centers=[0,b,c],intersection_dimension=k,quotient_order=len(h),
                             forced_involutions=forced_h,certified_exponent=k+bool(forced_h)))
        lower = min(row['certified_exponent'] for row in rows)
        candidates = [r for r in rows if r['quotient_order'] == 2 and
                      r['intersection_dimension']+1 == lower and r['forced_involutions']]
        if candidates:hits.append(dict(masks=[ma,mb,mc],lower_exponent=lower,
                                       witnesses=candidates,rows=rows))
    summary = dict(status='COMPLETE_SUFFICIENT_COORDINATE_SCREEN',quotient_order=72,
                   module_dimension=9,ambient_order=72*512,support_masks=8,triples=triples,
                   centered_pairs=81,hits=hits,
                   scope='Only coordinate subspaces on the nine-point signed affine grid; a sufficient forced-involution lower bound, not exhaustive minimum orders.')
    Path('results/20.122-affine-grid-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k != 'hits'},sort_keys=True))
    print('HITS',len(hits),[h['masks'] for h in hits])
    print('PASS_20_122_AFFINE_GRID')


if __name__ == '__main__':main()
