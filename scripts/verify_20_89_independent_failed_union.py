#!/usr/bin/env python3
"""Independent exact matrix and affine controls; no GAP or third-party imports."""
from itertools import product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def mul(a,b,n=3,p=3):
    return tuple(sum(a[i*n+k]*b[k*n+j] for k in range(n))%p
                 for i in range(n) for j in range(n))


def ident(n=3):
    return tuple(int(i==j) for i in range(n) for j in range(n))


def inv(a,n=3,p=3):
    rows=[[a[i*n+j] for j in range(n)]+[int(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        k=next(i for i in range(j,n) if rows[i][j])
        rows[j],rows[k]=rows[k],rows[j]
        v=pow(rows[j][j],-1,p)
        rows[j]=[(v*x)%p for x in rows[j]]
        for i in range(n):
            if i!=j:
                v=rows[i][j]
                rows[i]=[(x-v*y)%p for x,y in zip(rows[i],rows[j])]
    return tuple(x for row in rows for x in row[n:])


def filtration():
    els=[]
    for d in product([1,2],repeat=3):
        for a,b,c in product(range(3),repeat=3):
            els.append((d[0],a,b,0,d[1],c,0,0,d[2]))
    group=set(els); assert len(group)==216
    inverses={a:inv(a) for a in els}
    products=0
    for a in els:
        assert mul(a,inverses[a])==ident()
        for b in els:
            assert mul(a,b) in group
            products+=1
    pairs=[(0,2),(0,1),(1,2)]
    u={a for a in els if a[0]==a[4]==a[8]==1}
    chain=[{ident()}]+[{a for a in u if all(a[i*3+j]==0 for i,j in pairs[s:])} for s in range(1,4)]
    assert list(map(len,chain))==[1,3,9,27]
    checks=central=0
    wrong_scalar_witness=None
    # In F_3 an inverse scalar equals itself, so mutate to the wrong pair,
    # rather than pretending that inversion distinguishes the convention.
    for s,(i,j) in enumerate(pairs,1):
        for x in chain[s]:
            for a in els:
                y=mul(mul(inverses[a],x),a)
                assert y in chain[s]
                expected=x[i*3+j]*a[j*3+j]*pow(a[i*3+i],-1,3)%3
                assert y[i*3+j]==expected
                wrong=x[i*3+j]*a[0]*pow(a[4],-1,3)%3
                if wrong!=y[i*3+j]: wrong_scalar_witness=[s,list(x),list(a)]
                checks+=1
            for a in u:
                assert mul(inverses[x],mul(mul(inverses[a],x),a)) in chain[s-1]
                central+=1
    assert wrong_scalar_witness is not None
    # Ascending distance is not a normal filtration: (1,2) is moved
    # into the (1,3) direction by conjugation with 1+e_23.
    x=(1,1,0,0,1,0,0,0,1); a=(1,0,0,0,1,1,0,0,1)
    assert mul(mul(inv(a),x),a)[2]!=0
    return dict(order=216,layer_orders=list(map(len,chain)),products=products,
                conjugation_checks=checks,central_checks=central)


def affine_mul(a,b):
    """(translation vector, scalar sign), with action sign=(-1)^epsilon."""
    v,e=a;w,f=b
    return (tuple((x+(-1 if e else 1)*y)%3 for x,y in zip(v,w)),e^f)


def affine_inv(a):
    v,e=a
    return (tuple(((-1 if e==0 else 1)*x)%3 for x in v),e)


def comm(a,b):
    return affine_mul(affine_mul(affine_mul(affine_inv(a),affine_inv(b)),a),b)


def mixed():
    finite=list(product([(0,),(1,),(2,)],range(2)))
    rows=[]
    for r in range(1,5):
        vectors=list(product(range(3),repeat=r))
        second=list(product(vectors,range(2)))
        gg=list(product(finite,second))
        pp=list(product(finite,[(v,0) for v in vectors]))
        checks=0
        for x in gg:
            for b in pp:
                # Compute both factors: the finite factor need not be trivial.
                y=tuple(comm(comm(xx,bb),bb) for xx,bb in zip(x,b))
                assert y[0] in finite and y[1]==((0,)*r,0)
                checks+=1
        reflector=((0,)*r,1)
        for v in vectors:
            assert comm((v,0),reflector)==(v,0)
        rows.append([r,len(gg),len(pp),checks,len(vectors)])
    # A common sink cannot be reduced to the identity: S_3 has a
    # nontrivial translation fixed by repeated commutation with a reflection.
    translation=((1,),0);reflection=((0,),1)
    assert comm(comm(translation,reflection),reflection)==translation
    return rows


def rational_control():
    from fractions import Fraction as Q
    # In the affine group over Q, inverse conjugation by scalar 2 sends
    # v to v/2. Thus the commutator iterates are (-1/2)^j, all distinct.
    # Use actual generic 2x2 multiplication and inversion over Q here.
    def prod(a,b):
        return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],
                a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
    def inverse(a):
        d=a[0]*a[3]-a[1]*a[2]
        return (a[3]/d,-a[1]/d,-a[2]/d,a[0]/d)
    x=tuple(map(Q,[1,1,0,1]));g=tuple(map(Q,[2,0,0,1]));seen=set()
    for k in range(65):
        assert x[1]==(-Q(1,2))**k and x not in seen
        seen.add(x)
        x=prod(prod(prod(inverse(x),inverse(g)),x),g)
    return len(seen)


def nonnormal_sink():
    gg=set()
    for swap,s,t,x,y in product(range(2),[1,2],[1,2],range(3),range(3)):
        gg.add((0,s,x,t,0,y,0,0,1) if swap else (s,0,x,0,t,y,0,0,1))
    assert len(gg)==72
    inverse={a:inv(a) for a in gg}
    for a in gg:
        for b in gg:assert mul(a,b) in gg
    a=(2,0,0,0,1,0,0,0,1)
    sink=set()
    for x in gg:
        orbit=[]
        while x not in orbit:
            orbit.append(x)
            x=mul(mul(mul(inverse[x],inverse[a]),x),a)
        sink.update(orbit[orbit.index(x):])
    assert sink=={(1,0,x,0,1,0,0,0,1) for x in range(3)}
    for x in sink:
        for y in sink:assert mul(x,y) in sink
    normal_closure={mul(mul(inverse[g],x),g) for x in sink for g in gg}
    assert len(normal_closure)==9 and normal_closure!=sink
    for x in normal_closure:
        for y in normal_closure:assert mul(x,y) in normal_closure
    return dict(group_order=72,sink_size=3,sink_group_order=3,normal_closure_order=9,
                product_checks=5184)


def main():
    summary=dict(status='PASS',filtration=filtration(),mixed_rows=mixed(),
                 rational_distinct_iterates=rational_control(),
                 nonnormal_sink=nonnormal_sink(),
                 rejected_shortcuts=['wrong_diagonal_pair','reversed_filtration',
                                     'trivial_common_sink','admit_infinite_reflection',
                                     'sink_group_is_ambient_normal'])
    text=json.dumps(summary,sort_keys=True)
    print(text)
    print('PASS_20_89_INDEPENDENT')


if __name__=='__main__':main()
