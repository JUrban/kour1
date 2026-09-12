#!/usr/bin/env python3
"""Permutation and integer multiplication-table checks for the soluble lemma."""
import itertools
import json
import math
from verify_21_121b_normal_sylow import all_subgroups, subgroup_closure


def permutation_table(n,even=False):
    elts=list(itertools.permutations(range(n)))
    if even:
        elts=[x for x in elts if sum(x[i]>x[j] for i in range(n) for j in range(i+1,n))%2==0]
    pos={x:i for i,x in enumerate(elts)}
    return [[pos[tuple(a[b[i]] for i in range(n))] for b in elts] for a in elts]


def sl23_table():
    # Quaternion basis 1,i,j,k, with sign bit 4; i*j=k, j*k=i, k*i=j.
    def quat(a,b):
        sign=(a//4+b//4)%2
        x,y=a%4,b%4
        if x==0: z=y
        elif y==0: z=x
        elif x==y: z=0; sign^=1
        elif (x,y) in [(1,2),(2,3),(3,1)]: z=6-x-y
        else: z=6-x-y; sign^=1
        return z+4*sign
    def alpha(x,n):
        return x if x%4==0 else 4*(x//4)+1+(x%4-1+n)%3
    elts=list(itertools.product(range(8),range(3)))
    pos={x:i for i,x in enumerate(elts)}
    return [[pos[(quat(q,alpha(r,a)),(a+b)%3)] for r,b in elts] for q,a in elts]


def heisenberg_times_c2():
    elts=list(itertools.product(range(3),range(3),range(3),range(2)))
    pos={x:i for i,x in enumerate(elts)}
    return [[pos[((u+a)%3,(v+b)%3,(z+c+u*b)%3,(e+f)%2)]
             for a,b,c,f in elts] for u,v,z,e in elts]


def check(name,p,table,negative=False):
    order=len(table)
    inverse=[next(y for y in range(order) if table[x][y]==table[y][x]==0) for x in range(order)]
    triples=0
    for x,y,z in itertools.product(range(order),repeat=3):
        assert table[table[x][y]][z] == table[x][table[y][z]]
        triples+=1
    groups=all_subgroups(table)
    whole=frozenset(range(order))
    derived=whole
    while len(derived)>1:
        commutators={table[table[table[inverse[x]][inverse[y]]][x]][y]
                     for x in derived for y in derived}
        nxt=subgroup_closure(tuple(commutators),table)
        if nxt==derived: break
        derived=nxt
    assert (len(derived)==1) != negative
    def abelian(h):
        return all(table[x][y]==table[y][x] for x in groups[h] for y in groups[h])
    def normal(h,k):
        return h<=k and all(table[table[inverse[g]][x]][g] in h for g in groups[k] for x in groups[h])
    def centralizer(k,h):
        return frozenset(x for x in k if all(table[x][y]==table[y][x] for y in groups[h]))
    allnormal=[h for h in groups if normal(h,whole)]
    J=1
    for k in groups:
        if math.gcd(len(k),p)==1:
            best=min(len(k)//len(a) for a in groups if normal(a,k) and abelian(a))
            J=max(J,best)
    sylow=1
    while order%(sylow*p)==0: sylow*=p
    bound=J**3*sylow**2
    if negative:
        best=min(order//len(a) for a in allnormal if abelian(a) and math.gcd(len(a),p)==1)
        assert J==1 and best>bound
        row=dict(model=name,p=p,J=J,order=order,sylow_order=sylow,minimum_index=best,quadratic_bound=bound)
    else:
        n=max((h for h in allnormal if math.gcd(len(h),p)==1),key=len)
        assert all(h<=n for h in allnormal if math.gcd(len(h),p)==1)
        subn=[h for h in groups if h<=n]
        measure={h:len(h)*len(centralizer(n,h)) for h in subn}
        maximal=[h for h in subn if measure[h]==max(measure.values())]
        b=frozenset.intersection(*maximal)
        assert b in groups and abelian(b) and normal(b,whole)
        assert len(n)//len(b)<=J**2 and order//len(b)<=bound
        # A table-driven quotient, including its normal subgroups and Fitting core.
        cosets=[]; quotient_index={}
        for g in range(order):
            if g in quotient_index: continue
            c=frozenset(table[x][g] for x in n)
            for x in c: quotient_index[x]=len(cosets)
            cosets.append(c)
        reps=[min(c) for c in cosets]
        qt=[[quotient_index[table[x][y]] for y in reps] for x in reps]
        qgroups=all_subgroups(qt)
        qinv=[next(y for y in range(len(qt)) if qt[x][y]==qt[y][x]==0) for x in range(len(qt))]
        qnormal=[h for h in qgroups if all(qt[qt[qinv[g]][x]][g] in h for g in range(len(qt)) for x in h)]
        def p_power(n):
            while n%p==0: n//=p
            return n==1
        pcore=max((h for h in qnormal if p_power(len(h))),key=len)
        if len(qt)>1:
            assert len(pcore)>1
            assert all(x in pcore for x in range(len(qt)) if all(qt[x][y]==qt[y][x] for y in pcore))
        # All maximal subgroups of this p-core, using only subgroup containment.
        proper=[h for h in qgroups if h<pcore]
        maximal_p=[h for h in proper if not any(h<k<pcore for k in proper)]
        phi=frozenset.intersection(*maximal_p) if maximal_p else pcore
        frattini_index=len(pcore)//len(phi)
        if len(qt)>1:
            assert len(qt)<=J*sylow*(frattini_index-1)
        row=dict(model=name,p=p,J=J,order=order,sylow_order=sylow,
                 p_prime_core_order=len(n),cd_order=len(b),quotient_order=len(qt),
                 fitting_order=len(pcore),frattini_index=frattini_index,
                 constructed_index=order//len(b),quadratic_bound=bound)
    row['associativity_triples']=triples
    row['subgroups']=len(groups)
    return row


def main():
    models=[('s3',p,permutation_table(3),False) for p in (2,3)]
    models += [('s4',p,permutation_table(4),False) for p in (2,3)]
    models += [('sl2_3',p,sl23_table(),False) for p in (2,3)]
    models += [('heisenberg3_times_c2',2,heisenberg_times_c2(),False),
               ('a5_negative_control',2,permutation_table(5,True),True)]
    rows=[check(*m) for m in models]
    for row in rows: print(json.dumps(row,sort_keys=True))
    print('PASS_21_121B_SOLUBLE_INDEPENDENT models='+str(len(rows))+
          ' associativity_triples='+str(sum(r['associativity_triples'] for r in rows)))


if __name__=='__main__':
    main()
