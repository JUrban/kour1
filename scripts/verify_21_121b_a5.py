#!/usr/bin/env python3
"""All subgroups of A5^2 by table-driven Goursat data, without GAP."""
import collections
import functools
import itertools
import json
import math
from verify_21_121b_soluble import permutation_table
from verify_21_121b_normal_sylow import all_subgroups, subgroup_closure


def inverses(table):
    return [next(y for y in range(len(table)) if table[x][y]==table[y][x]==0)
            for x in range(len(table))]


def element_order(table,x):
    y=x;n=1
    while y:
        y=table[y][x];n+=1
    return n


def sylow2(n):
    return n & -n


def quotient(h,n,table,gens):
    pos={};reps=[]
    for x in sorted(h):
        if x in pos:continue
        c={table[x][y] for y in n}
        for y in c:pos[y]=len(reps)
        reps.append(x)
    qt=tuple(tuple(pos[table[x][y]] for y in reps) for x in reps)
    return qt,pos,tuple(dict.fromkeys(pos[x] for x in gens if pos[x]))


@functools.lru_cache(None)
def isomorphisms(t,u,gens):
    if len(t)!=len(u):return ()
    if len(t)==1:return ((0,),)
    source_orders=[element_order(t,x) for x in range(len(t))]
    target_orders=[element_order(u,x) for x in range(len(u))]
    if sorted(source_orders)!=sorted(target_orders):return ()
    choices=[[x for x in range(len(u)) if target_orders[x]==source_orders[g]] for g in gens]
    result=[]
    for images in itertools.product(*choices):
        mapping={0:0};queue=[0];valid=True
        for x in queue:
            if not valid:break
            for g,a in zip(gens,images):
                y=t[x][g];b=u[mapping[x]][a]
                if y in mapping:
                    if mapping[y]!=b:valid=False;break
                else:mapping[y]=b;queue.append(y)
        if valid and len(mapping)==len(t) and len(set(mapping.values()))==len(u):
            result.append(tuple(mapping[x] for x in range(len(t))))
    return tuple(result)


def main():
    t=permutation_table(5,True);iv=inverses(t);groups=all_subgroups(t)
    def normal(n,h):
        return n<=h and all(t[t[iv[g]][x]][g] in n for g in groups[h] for x in groups[n])
    def abelian(h):
        return all(t[x][y]==t[y][x] for x in groups[h] for y in groups[h])
    def soluble(h):
        while len(h)>1:
            comm={t[t[t[iv[x]][iv[y]]][x]][y] for x in h for y in h}
            nxt=subgroup_closure(tuple(comm),t)
            if nxt==h:return False
            h=nxt
        return True
    assert len(groups)==59
    assert all(abelian(h) for h in groups if len(h)%2)
    assert all(soluble(h) for h in groups if len(h)<60)
    whole=frozenset(range(60))
    assert not soluble(whole)
    normals={h:[n for n in groups if normal(n,h)] for h in groups}
    assert sorted(map(len,normals[whole]))==[1,60]
    oddcore={h:max((n for n in normals[h] if len(n)%2),key=len) for h in groups}
    assert all(abelian(n) for n in oddcore.values())
    records=collections.defaultdict(list)
    for h in groups:
        for n in normals[h]:
            qt,pos,gens=quotient(h,n,t,groups[h])
            records[len(qt)].append((h,n,qt,pos,gens))
    histogram=collections.Counter();seen=set();iso_count=0
    for qorder,pool in sorted(records.items()):
        for left,right in itertools.product(pool,repeat=2):
            a,na,ta,pa,ga=left;b,nb,tb,pb,gb=right
            for phi in isomorphisms(ta,tb,ga):
                iso_count+=1
                # Goursat uniquely determines H from its projections,
                # the two kernels and the quotient matching.
                h=frozenset(60*x+y for x in a for y in b if phi[pa[x]]==pb[y])
                assert h not in seen
                seen.add(h)
                assert len(h)==len(a)*len(b)//qorder
                assert {z//60 for z in h}==set(a) and {z%60 for z in h}==set(b)
                if len(a)==len(b)==60:
                    assert len(h) in (60,3600)
                    r=1 if len(h)==60 else 2;border=bp=1
                elif len(a)==60 or len(b)==60:
                    assert qorder==1
                    r=1;border=min(len(a),len(b));bp=sylow2(border)
                else:
                    r=0;border=len(h);bp=sylow2(border)
                # All normal odd subgroups project into the odd cores.
                # Their intersection with H is itself normal, odd and
                # abelian, hence is exactly the largest admissible subgroup.
                k={z for z in h if z//60 in oddcore[a] and z%60 in oddcore[b]}
                best=len(h)//len(k);power=sylow2(len(h))
                assert power==4**r*bp
                assert best<=60**r*bp**2
                histogram[(len(h),power,best,r,border,bp)]+=1
    single=collections.Counter()
    for h in groups:
        r=int(len(h)==60);border=1 if r else len(h);bp=sylow2(border)
        key=(len(h),sylow2(len(h)),len(h)//len(oddcore[h]),r,border,bp)
        single[key]+=1
    for n,hist in [(1,single),(2,histogram)]:
        print(json.dumps(dict(model='a5_power',factors=n,subgroups=sum(hist.values()),
                              histogram=[[list(k),v] for k,v in sorted(hist.items())]),sort_keys=True))
    print('PASS_21_121B_A5_INDEPENDENT subgroups='+str(len(seen))+
          ' goursat_isomorphisms='+str(iso_count)+
          ' quotient_table_pairs_cached='+str(isomorphisms.cache_info().currsize))


if __name__=='__main__':main()
