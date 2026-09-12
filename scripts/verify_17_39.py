#!/usr/bin/env python3
"""Independent integer normal forms; normalizers are centralizers of involutions."""
import itertools, json
from collections import Counter

def model(p,d):
    vectors=list(itertools.product(range(p),repeat=d));zero=(0,)*d
    identity=(zero,zero,0,0)
    def mul(x,y):
        u,v,z,e=x;a,b,c,f=y;s=1-2*e
        return (tuple((u[i]+a[i])%p for i in range(d)),
                tuple((v[i]+s*b[i])%p for i in range(d)),
                (z+s*c+s*sum(u[i]*b[i] for i in range(d)))%p,(e+f)%2)
    def inv(x):
        u,v,z,e=x;s=1-2*e
        return (tuple(-a%p for a in u),tuple(-s*b%p for b in v),
                s*(-z+sum(u[i]*v[i] for i in range(d)))%p,e)
    group=[(u,v,z,e) for u in vectors for v in vectors for z in range(p) for e in range(2)]
    t=(zero,zero,0,1)
    involutions=[g for g in group if g!=identity and mul(g,g)==identity]
    normalizer=[g for g in group if mul(g,t)==mul(t,g)]
    assert normalizer==[(u,zero,0,e) for u in vectors for e in range(2)]
    assert len(involutions)==p**(d+1) and len(group)==2*p**(2*d+1)
    assert all(mul(g,inv(g))==identity and mul(inv(g),g)==identity for g in group)
    generators=[]
    for i in range(d):
        v=tuple(int(j==i) for j in range(d))
        generators.extend([(v,zero,0,0),(zero,v,0,0)])
    generators.append(t)
    center=[g for g in group if all(mul(g,x)==mul(x,g) for x in generators)]
    assert center==[identity]
    # Every Sylow 2 subgroup has a unique involution h, so its normalizer
    # is C_G(h). Compute its intersection with D by literal commutation.
    pair_sets={frozenset(g for g in normalizer if mul(g,h)==mul(h,g)) for h in involutions}
    states={frozenset(normalizer)};hist=[];mins=[]
    while True:
        hist.append(sorted([size,count] for size,count in Counter(map(len,states)).items()))
        mins.append(min(map(len,states)))
        if 1 in map(len,states):break
        next_states={s&c for s in states for c in pair_sets}
        assert next_states!=states;states=next_states
    assert len(mins)==d+1
    inter=set(normalizer);chain=[len(inter)]
    for i in range(d):
        v=tuple(int(j==i) for j in range(d));g=(zero,v,0,0)
        h=mul(mul(inv(g),t),g)
        inter={x for x in inter if mul(x,h)==mul(h,x)};chain.append(len(inter))
    assert chain[-1]==1
    # Verify the exact graph of U^g for every g using all basis elements.
    graph_checks=0
    for g in group:
        a,b,c,e=g;s=1-2*e
        for i in range(d):
            u=tuple(int(j==i) for j in range(d));x=(u,zero,0,0)
            assert mul(mul(inv(g),x),g)==(u,zero,s*b[i]%p,0)
            graph_checks+=1
    triples=0
    if (p,d)==(3,1):
        for a,b,c in itertools.product(group,repeat=3):
            assert mul(mul(a,b),c)==mul(a,mul(b,c));triples+=1
    row=[p,d,len(group),len(normalizer),len(involutions),len(pair_sets),mins,hist,chain]
    return row,dict(graph_basis_checks=graph_checks,associativity_triples=triples,elements_checked=len(group))

def main():
    totals=Counter()
    for p,d in [(3,1),(3,2),(3,3),(3,4),(5,1),(5,2),(7,1)]:
        row,checks=model(p,d);totals.update(checks)
        print('ROW1739 '+json.dumps(row,separators=(',',':')))
    print('CHECK1739 '+json.dumps(dict(totals),sort_keys=True))
    print('PASS_17_39_WORDS')

if __name__=='__main__':main()
