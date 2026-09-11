#!/usr/bin/env python3
"""Exact controls for the affine family in 17.33.

Infinite membership assertions are established by the written proof. This
checks coordinates, presentation relations, every proper subspace through
holonomy rank five, and an independent finite affine quotient.
"""
from itertools import product
from pathlib import Path
import json
import random

ROOT=Path(__file__).resolve().parents[1]
RNG=random.Random(1733)

def parity(x):
    return x.bit_count() & 1

def span(values):
    result={0}
    for x in values:
        result |= {y ^ x for y in tuple(result)}
    return frozenset(result)

def all_subspaces(n):
    spaces={frozenset([0])}
    for _ in range(n):
        spaces |= {span(tuple(s)+(v,)) for s in tuple(spaces)
                   for v in range(1<<n)}
    return sorted(spaces,key=lambda x:(len(x),sorted(x)))

class Affine:
    def __init__(self,n):
        self.n=n
        self.coords=tuple(product(range(1,1<<n),range(n)))
        self.m=len(self.coords)
        self.zero=(0,(0,)*self.m)
        self.signs={e:tuple((-1)**parity(chi&e) for chi,j in self.coords)
                    for e in range(1<<n)}
    def valid(self,g):
        e,a=g
        return len(a)==self.m and all((a[k]&1)==((e>>j)&1)
                                     for k,(chi,j) in enumerate(self.coords))
    def mul(self,g,h):
        e,a=g;f,b=h
        return e^f,tuple(x+s*y for x,s,y in zip(a,self.signs[e],b))
    def inv(self,g):
        e,a=g
        return e,tuple(-s*x for s,x in zip(self.signs[e],a))
    def lift(self,e):
        return e,tuple((e>>j)&1 for chi,j in self.coords)
    def translate(self,k,value=1):
        a=[0]*self.m;a[k]=2*value
        return 0,tuple(a)
    def sample(self,e=None):
        if e is None:e=RNG.randrange(1<<self.n)
        return e,tuple(2*RNG.randrange(-7,8)+((e>>j)&1) for chi,j in self.coords)
    def image(self,g,psi,k):
        e,a=g;chi,j=self.coords[k]
        ell=sum(a[(psi-1)*self.n+t] for t in range(self.n) if chi&(1<<t))
        return a[k],ell
    def matrix(self,g):
        e,a=g;d=self.m+1
        out=[[0]*d for _ in range(d)]
        for i in range(self.m):out[i][i]=self.signs[e][i];out[i][-1]=a[i]
        out[-1][-1]=1
        return out

def kmul(x,y):
    return x[0]+(-1 if x[1]&1 else 1)*y[0],x[1]+y[1]

def matrix_mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def main():
    presentation=local_maps=squares=matrix_checks=group_checks=0
    subspace_counts={}
    for n in range(2,6):
        model=Affine(n)
        lifts=[model.lift(1<<i) for i in range(n)]
        for i,g in enumerate(lifts):
            expected=[0]*model.m
            for k,(chi,j) in enumerate(model.coords):
                if j==i and not (chi&(1<<i)):expected[k]=2
            assert model.mul(g,g)==(0,tuple(expected));presentation+=1
            for k,(chi,j) in enumerate(model.coords):
                t=model.translate(k)
                lhs=model.mul(model.mul(g,t),model.inv(g))
                rhs=model.translate(k,(-1)**((chi>>i)&1))
                assert lhs==rhs;presentation+=1
        for i in range(n):
            for j in range(i+1,n):
                correction=tuple(2*((((chi>>j)&1) if col==i else 0)
                                    -(((chi>>i)&1) if col==j else 0))
                                 for chi,col in model.coords)
                assert model.mul(lifts[i],lifts[j])==model.mul(
                    (0,correction),model.mul(lifts[j],lifts[i]));presentation+=1
        # Verify the translation squares in the commutator subgroup explicitly.
        for k,(chi,j) in enumerate(model.coords):
            i=next(t for t in range(n) if chi&(1<<t));g=lifts[i];a=model.translate(k)
            comm=model.mul(model.mul(model.mul(g,a),model.inv(g)),model.inv(a))
            assert comm==model.translate(k,-2);presentation+=1
        for _ in range(500):
            g,h,k=model.sample(),model.sample(),model.sample()
            assert model.valid(model.mul(g,h))
            assert model.mul(model.mul(g,h),k)==model.mul(g,model.mul(h,k))
            assert model.mul(g,model.inv(g))==model.zero
            group_checks+=1
            assert g==model.zero or model.mul(g,g)!=model.zero;squares+=1
        spaces=all_subspaces(n);subspace_counts[n]=len(spaces)
        for space in spaces:
            if len(space)==1<<n:continue
            psi=next(p for p in range(1,1<<n) if all(not parity(p&e) for e in space))
            # Every holonomy value is covered, with independent integer translates.
            for e in sorted(space):
                g=model.sample(e);h=model.sample(RNG.choice(tuple(space)))
                image_g=[]
                for k,(chi,j) in enumerate(model.coords):
                    x=model.image(g,psi,k);y=model.image(h,psi,k)
                    assert (x[1]&1)==parity(chi&e)
                    assert model.image(model.mul(g,h),psi,k)==kmul(x,y)
                    image_g.append(x);local_maps+=1
                assert tuple(x[0] for x in image_g)==g[1]
                assert any(x!=(0,0) for x in image_g) or g==model.zero
        if n<=3:
            for _ in range(75):
                g,h=model.sample(),model.sample()
                assert matrix_mul(model.matrix(g),model.matrix(h))==model.matrix(model.mul(g,h))
                matrix_checks+=1

    # Entire order-256 quotient Gamma_2 / 2N, in independent residue coordinates.
    model=Affine(2)
    elements=[(e,tuple(((e>>j)&1)+2*z for (chi,j),z in zip(model.coords,bits)))
              for e in range(4) for bits in product(range(2),repeat=model.m)]
    assert len(elements)==256 and len(set(elements))==256
    def mod(g):return g[0],tuple(x%4 for x in g[1])
    def direct_product(g,h):
        e,a=g;f,b=h
        return e^f,tuple((a[k]+(-b[k] if parity(chi&e) else b[k]))%4
                        for k,(chi,j) in enumerate(model.coords))
    index={g:i for i,g in enumerate(elements)}
    table=[]
    for g in elements:
        table.append([])
        for h in elements:
            result=direct_product(g,h)
            assert result==mod(model.mul(g,h)) and result in index
            table[-1].append(index[result])
    centre=[i for i in range(256) if all(table[i][j]==table[j][i] for j in range(256))]
    involutions=[i for i in range(256) if table[i][i]==index[model.zero]]
    assert centre==involutions and len(centre)==64
    # Finite local embeddings into (Z/4 semidirect Z/4)^6, checked on all pairs.
    finite_map_checks=0
    for space in all_subspaces(2):
        if len(space)==4:continue
        psi=next(p for p in range(1,4) if all(not parity(p&e) for e in space))
        subgroup=[g for g in elements if g[0] in space]
        images={g:tuple(tuple(v%4 for v in model.image(g,psi,k))
                        for k in range(model.m)) for g in subgroup}
        assert len(set(images.values()))==len(subgroup)
        for g in subgroup:
            for h in subgroup:
                expect=tuple(tuple(v%4 for v in kmul(x,y)) for x,y in zip(images[g],images[h]))
                assert images[direct_product(g,h)]==expect;finite_map_checks+=1
    result=dict(problem='17.33',status='PASS',holonomy_dimensions=list(range(2,6)),
                presentation_relations=presentation,group_law_controls=group_checks,
                torsion_square_controls=squares,subspaces=subspace_counts,
                local_homomorphism_checks=local_maps,independent_matrix_products=matrix_checks,
                finite_quotient_order=256,finite_quotient_products=65536,
                finite_quotient_centre_order=64,finite_local_map_products=finite_map_checks,
                scope='Exact finite controls; infinite local embeddings and nonmembership are proved structurally.')
    (ROOT/'results/17.33-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
