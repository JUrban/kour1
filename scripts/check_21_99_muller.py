#!/usr/bin/env python3
"""Exact F8 matrices certify a >=2-fixed-point witness at Muller's bad pair."""
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def field_mul(a,b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 8:
            a ^= 11
        b >>= 1
    return result


MUL = [[field_mul(a,b) for b in range(8)] for a in range(8)]
E = tuple(tuple(int(i == j) for j in range(8)) for i in range(8))
COUNTS = dict(matrix_products=0)


def mul(a,b):
    COUNTS['matrix_products'] += 1
    result = [[0]*8 for _ in range(8)]
    for i,k,j in product(range(8),repeat=3):
        result[i][j] ^= MUL[a[i][k]][b[k][j]]
    return tuple(map(tuple,result))


def inv(a):
    rows = [list(x)+list(y) for x,y in zip(a,E)]
    for j in range(8):
        pivot = next(i for i in range(j,8) if rows[i][j])
        rows[j],rows[pivot] = rows[pivot],rows[j]
        scale = next(x for x in range(1,8) if MUL[rows[j][j]][x] == 1)
        rows[j] = [MUL[x][scale] for x in rows[j]]
        for i in range(8):
            if i != j and rows[i][j]:
                c = rows[i][j]
                rows[i] = [x ^ MUL[c][y] for x,y in zip(rows[i],rows[j])]
    assert tuple(tuple(row[:8]) for row in rows) == E
    result = tuple(tuple(row[8:]) for row in rows)
    assert mul(a,result) == mul(result,a) == E
    return result


def power(a,n):
    if n < 0:
        return power(inv(a),-n)
    result = E
    while n:
        if n & 1:
            result = mul(result,a)
        a = mul(a,a); n //= 2
    return result


def chain(*matrices):
    result = E
    for a in matrices:
        result = mul(result,a)
    return result


def conjugate(a,b):
    return chain(inv(b),a,b)


def main():
    for a,b,c in product(range(8),repeat=3):
        assert MUL[MUL[a][b]][c] == MUL[a][MUL[b][c]]
        assert MUL[a][b ^ c] == MUL[a][b] ^ MUL[a][c]
    assert all(any(MUL[a][b] == 1 for b in range(1,8)) for a in range(1,8))
    xr = [list(row) for row in E]
    for i,j in [(1,2),(3,4),(3,5),(3,6),(4,6),(5,6),(7,8)]:
        xr[i-1][j-1] ^= 1
    perm = [[0]*8 for _ in range(8)]
    for i,j in [(1,3),(2,1),(3,7),(4,5),(5,4),(6,2),(7,8),(8,6)]:
        perm[i-1][j-1] = 1
    a = mul(xr,perm)
    roots = [1]
    for _ in range(7):
        roots.append(MUL[roots[-1]][2])
    assert roots[-1] == 1 and len(set(roots[:-1])) == 7
    assert MUL[MUL[2][2]][2] ^ 2 ^ 1 == 0
    exponents = [4,3,3,1,6,4,4,3]
    b = tuple(tuple(roots[exponents[i]] if i == j else 0 for j in range(8)) for i in range(8))
    x = chain(b,power(chain(power(a,2),power(b,2),a),2),power(b,-2),a,power(b,-2))
    t = chain(power(a,-3),b,power(mul(b,a),2),power(b,-2),power(a,2),b)
    y = conjugate(x,t)
    s = mul(a,conjugate(a,b))
    d = chain(x,s,y,s,a,y,power(s,2),t)
    assert conjugate(x,d) == mul(y,x)
    assert conjugate(x,y) == inv(x) and power(x,2) == power(y,2)
    assert power(y,4) == E and power(y,2) != E
    assert s != E and power(s,13) == E and conjugate(s,y) == power(s,8)
    sylow_candidates = [power(s,i) for i in range(13)]
    cyclic = {power(y,j) for j in range(4)}
    h = {mul(u,v) for u in sylow_candidates for v in cyclic}
    assert len(h) == 52 and E in h and x not in h
    assert all(mul(z,s) in h and mul(z,y) in h for z in h)
    assert sum(z not in cyclic for z in h) == 48
    assert all(z in cyclic or power(mul(z,x),13) == E for z in h)
    # y fixes the distinct right cosets H and Hx; x is conjugate to y.
    assert conjugate(y,x) == inv(y)
    r1,r2 = inv(t),mul(x,inv(t))
    assert mul(r1,inv(r2)) not in h
    assert chain(r1,x,inv(r1)) in h and chain(r2,x,inv(r2)) in h
    result = dict(status='PASS_EXPLICIT_TWO_FIXED_COSETS',field_associativity_triples=512,
                  field_distributivity_triples=512,subgroup_order=52,
                  thirteen_power_relations=48,distinct_fixed_cosets=2,
                  matrices={name:matrix for name,matrix in [('a',a),('b',b),('x',x),('t',t),('y',y),('s',s)]},
                  fixed_coset_representatives=[r1,r2],counts=COUNTS,
                  source='Muller2026 Lemma2.1 and Section2.1 matrices; no novelty for these identities.',
                  scope='The specified H-to-Hx pair has a witness fixing at least two cosets. Full group identification, order, maximality and all other coset pairs are not certified here.',
                  new_complete_candidates_added=0)
    (ROOT/'results/21.99-muller-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_2199_MULLER fixed_cosets=2 subgroup_order=52 field_triples=1024',COUNTS)


if __name__ == '__main__':
    main()
