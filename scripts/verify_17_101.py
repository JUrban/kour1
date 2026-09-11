#!/usr/bin/env python3
"""Finite exact controls for the tree-module construction in problem17.101.

These verify the finite linear algebra and convention-sensitive examples.
The infinite HNN tree and the final homogeneous union are proved in the text.
"""
from itertools import product
from math import gcd,prod
from pathlib import Path
import json
import random

ROOT=Path(__file__).resolve().parents[1]
RNG=random.Random(17101)

def rank(rows,p):
    if not rows:return 0
    a=[list(row) for row in rows];r=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]%p),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        c=pow(a[r][j]%p,-1,p);a[r]=[x*c%p for x in a[r]]
        for i in range(r+1,len(a)):
            c=a[i][j]%p
            if c:a[i]=[(x-c*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def injective_matrix(d,e,p):
    if e==0:return [[] for _ in range(d)]
    while True:
        a=[[RNG.randrange(p) for _ in range(e)] for _ in range(d)]
        if rank(a,p)==e:return a

def mm(a,b,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]

def mv(a,v,p):
    return tuple(sum(x*y for x,y in zip(row,v))%p for row in a)

def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def main():
    trees=vertex_checks=0
    for p in [2,3,5,7]:
        for _ in range(100):
            n=RNG.randrange(1,17);dims=[RNG.randrange(0,7) for _ in range(n)]
            edges=[]
            for v in range(1,n):
                parent=RNG.randrange(v)
                e=RNG.randrange(min(dims[v],dims[parent])+1)
                edges.append((v,parent,e,injective_matrix(dims[v],e,p),
                              injective_matrix(dims[parent],e,p)))
            size=sum(dims);width=sum(x[2] for x in edges)
            offset=[sum(dims[:i]) for i in range(n)]
            # Each row below is an edge generator's boundary in the vertex sum.
            rels=[]
            for v,w,e,a,b in edges:
                for j in range(e):
                    row=[0]*size
                    for i in range(dims[v]):row[offset[v]+i]=a[i][j]
                    for i in range(dims[w]):row[offset[w]+i]=-b[i][j]%p
                    rels.append(row)
            assert rank(rels,p)==width
            for v,d in enumerate(dims):
                basis=[]
                for j in range(d):
                    row=[0]*size;row[offset[v]+j]=1;basis.append(row)
                assert rank(rels+basis,p)==width+d
                vertex_checks+=1
            trees+=1

    # Non-split cyclic-module edge embeddings, checked without field arithmetic.
    cyclic_cases=coefficient_checks=nonsplit_endpoints=0
    for _ in range(120):
        n=RNG.randrange(2,7)
        orders=[RNG.choice([2,4,6,8,9,12]) for _ in range(n)]
        edges=[]
        for v in range(1,n):
            w=RNG.randrange(v);common=gcd(orders[v],orders[w])
            d=RNG.choice([a for a in range(1,common+1) if common%a==0])
            units=[a for a in range(d) if gcd(a,d)==1]
            if d==1:units=[0]
            a=orders[v]//d*RNG.choice(units);b=orders[w]//d*RNG.choice(units)
            assert len({a*x%orders[v] for x in range(d)})==d
            assert len({b*x%orders[w] for x in range(d)})==d
            nonsplit_endpoints+=int(gcd(d,orders[v]//d)>1)+int(gcd(d,orders[w]//d)>1)
            edges.append((v,w,d,a,b))
        for values in product(*(range(e[2]) for e in edges)):
            boundary=[0]*n
            for x,(v,w,d,a,b) in zip(values,edges):
                boundary[v]=(boundary[v]+a*x)%orders[v]
                boundary[w]=(boundary[w]-b*x)%orders[w]
            assert not any(values) or sum(x!=0 for x in boundary)>=2
            coefficient_checks+=1
        cyclic_cases+=1
    assert nonsplit_endpoints>0

    # A cycle can kill a vertex: do not substitute a finite quotient graph
    # for the actual Bass--Serre tree. Three one-dimensional spaces over F3.
    cycle=[[1,-1,0],[0,1,-1],[-2,0,1]]
    assert rank(cycle,3)==3

    # Necessary enlargement: J2 plus a trivial summand for C_p. The fixed line
    # inside im(g-1) cannot be sent to the extra fixed line by a commuting
    # endomorphism on the original space, but it can after adding one dimension.
    extension_controls=0
    for p in [2,3,5,7]:
        g=ident(3);g[0][1]=1
        e1=(1,0,0);e3=(0,0,1)
        # A(g-I)=(g-I)A and A e1=e3 are inconsistent linear equations.
        equations=[];rhs=[]
        units=[]
        for i in range(3):
            for j in range(3):
                a=[[0]*3 for _ in range(3)];a[i][j]=1;units.append(a)
        for i in range(3):
            for j in range(3):
                equations.append([(mm(a,g,p)[i][j]-mm(g,a,p)[i][j])%p for a in units]);rhs.append(0)
        for i in range(3):
            equations.append([mv(a,e1,p)[i] for a in units]);rhs.append(e3[i])
        assert rank(equations,p)<rank([row+[b] for row,b in zip(equations,rhs)],p)
        # Coordinates e1,e2,e3,e4, with g e2=e2+e1, g e4=e4+e3.
        big=ident(4);big[0][1]=big[2][3]=1
        swap=[[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
        assert mm(big,swap,p)==mm(swap,big,p)
        assert mv(swap,(1,0,0,0),p)==(0,0,1,0)
        assert mm(swap,swap,p)==ident(4)
        power=ident(4)
        for _ in range(p):power=mm(power,big,p)
        assert power==ident(4) and big!=ident(4)
        for v in product(range(p),repeat=3):
            assert mv(big,v+(0,),p)==mv(g,v,p)+(0,)
            extension_controls+=1

    # Tensor-map equivariance on a proper, non-G-invariant submodule of the
    # natural S3 representation. A=(12), B=(23), f is the restriction of (123).
    tensor_controls=0
    a=[[0,1,0],[1,0,0],[0,0,1]]
    b=[[1,0,0],[0,0,1],[0,1,0]]
    f=[[0,0,1],[1,0,0],[0,1,0]]
    for p in [2,3,5,7]:
        assert mm(f,a,p)==mm(b,f,p)
        for x,y in product(range(p),repeat=2):
            u=(x,y,0)
            assert mv(f,mv(a,u,p),p)==mv(b,mv(f,u,p),p)
            tensor_controls+=1
    result=dict(problem='17.101',status='PASS',field_tree_cases=trees,
                vertex_injectivity_checks=vertex_checks,cyclic_module_trees=cyclic_cases,
                cyclic_module_coefficient_checks=coefficient_checks,
                nonsplit_cyclic_module_endpoints=nonsplit_endpoints,
                cycle_collapse_control=True,necessary_enlargement_controls=extension_controls,
                tensor_equivariance_controls=tensor_controls,
                scope='Finite controls of tree injections and extension conventions; no computational claim about the infinite homogeneous union.')
    (ROOT/'results/17.101-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
