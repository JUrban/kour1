#!/usr/bin/env python3
"""Independent finite-field and multiplicity controls for Problem 4.55.

The infinite descent and decomposition assertions are proved in the paper.
This program imports only exported 3x3 matrices, not GAP arithmetic.
"""
from collections import deque
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    # F25 = F5[z]/(z^2-z+2), matching GAP's printed Conway polynomial.
    add = [[((x % 5 + y % 5) % 5) + 5*((x//5+y//5) % 5)
            for y in range(25)] for x in range(25)]
    mul = [[((x % 5 * (y % 5) + 3*(x//5)*(y//5)) % 5)
            + 5*((x % 5*(y//5)+(x//5)*(y % 5)+(x//5)*(y//5)) % 5)
            for y in range(25)] for x in range(25)]
    neg = [(-x % 5) + 5*(-(x//5) % 5) for x in range(25)]
    inv = [0] + [next(y for y in range(1,25) if mul[x][y] == 1)
                 for x in range(1,25)]
    assert mul[5][5] == add[5][3]
    for a,b,c in product(range(25),repeat=3):
        assert mul[mul[a][b]][c] == mul[a][mul[b][c]]
        assert mul[a][add[b][c]] == add[mul[a][b]][mul[a][c]]

    def mm(a,b):
        return tuple(add[add[mul[a[3*i]][b[j]]][mul[a[3*i+1]][b[3+j]]]]
                     [mul[a[3*i+2]][b[6+j]]] for i in range(3) for j in range(3))

    source = ROOT/'results/4.55-three-dimensional-matrices.json'
    raw = json.loads(source.read_text())
    generators = [tuple(a+5*b for row in m for a,b in row) for m in raw]
    identity = (1,0,0,0,1,0,0,0,1)
    seen = {identity}
    queue = deque([identity])
    while queue:
        a = queue.popleft()
        for b in generators:
            c = mm(a,b)
            if c not in seen:
                seen.add(c)
                queue.append(c)
    assert len(seen) == 7560
    centre = [a for a in seen if all(mm(a,b) == mm(b,a) for b in generators)]
    assert len(centre) == 3
    assert all(a[0] == a[4] == a[8] and all(a[i] == 0 for i in [1,2,3,5,6,7])
               for a in centre)

    # The F25-span of this group is M3(F25), an absolute irreducibility
    # certificate checked without the MeatAxe.
    basis = {}
    for row in sorted(seen):
        row = list(row)
        for pivot,b in sorted(basis.items()):
            c = row[pivot]
            row = [add[x][neg[mul[c][y]]] for x,y in zip(row,b)]
        if any(row):
            pivot = next(i for i,x in enumerate(row) if x)
            scale = inv[row[pivot]]
            basis[pivot] = [mul[scale][x] for x in row]
        if len(basis) == 9:
            break
    assert len(basis) == 9

    rays = [(1,1,0,0),(1,0,1,0),(0,1,0,1),(0,0,1,1)]
    addv = lambda a,b: tuple(x+y for x,y in zip(a,b))
    assert addv(rays[0],rays[3]) == addv(rays[1],rays[2]) == (1,1,1,1)
    valid,atoms = 0,[]
    for v in product(range(13),repeat=4):
        a,b,c,d = v
        # These are the five coefficients in the displayed block.
        ordinary = (b,d,a+c,a+d,b+c)
        assert (ordinary[3] == ordinary[4]) == (a+d == b+c)
        if a+d != b+c or not any(v):
            continue
        valid += 1
        x = min(a,b)
        coefficients = (x,a-x,b-x,d-(b-x))
        assert min(coefficients) >= 0
        assert tuple(sum(coefficients[j]*rays[j][i] for j in range(4))
                     for i in range(4)) == v
        if sum(coefficients) == 1:
            atoms.append(v)
        for i,r in enumerate(rays):
            if all(v[j] == 0 for j in range(4) if r[j] == 0):
                assert all(v[j] == sum(v)//2 for j in range(4) if r[j])
    assert set(atoms) == set(rays)
    degrees = (6,21,21,24,24)
    rank_checks = []
    for a,b,c,d in rays:
        coeffs = (b,d,a+c,a+d,b+c)
        assert all(168*m % deg == 0 for m,deg in zip(coeffs,degrees))
        rank_checks.append(2*sum(m*deg for m,deg in zip(coeffs,degrees)))
    assert rank_checks == [150,180,150,180]
    assert 168*(rank_checks[0]+rank_checks[3]) == 55440
    result = {'status':'PASS','field_order':25,'field_triples':25**3,
              'matrix_group_order':len(seen),'matrix_centre_order':len(centre),
              'matrix_algebra_dimension':len(basis),
              'multiplicity_vectors_examined':13**4,'nonzero_valid_vectors':valid,
              'atoms':rays,'generic_ray_degrees':rank_checks,'common_rank':55440,
              'matrix_input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
              'proof_scope':'finite controls; rational descent and refinements are proved in research/4.55-proof.md'}
    (ROOT/'results/4.55-python-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
