#!/usr/bin/env python3
"""Reconstruct selected subgroup lattices directly from multiplication tables."""
import json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def members(mask):
    while mask:
        b=mask&-mask;yield b.bit_length()-1;mask-=b

def check(data):
    table=data['table'];n=data['order'];e=data['identity'];one=1<<e
    assert len(table)==n and all(sorted(r)==list(range(n)) for r in table)
    assert table[e]==list(range(n)) and all(table[x][e]==x for x in range(n))
    inv=[next(y for y in range(n) if table[x][y]==e) for x in range(n)]
    for x in range(n):
        assert table[inv[x]][x]==e
        for y in range(n):
            for z in range(n):assert table[table[x][y]][z]==table[x][table[y][z]]
    prime=next(p for p in range(2,n+1) if n%p==0)
    rem=n
    while rem%prime==0:rem//=prime
    assert rem==1

    def closure(gens):
        seen=one;q=[e]
        for x in q:
            for a in gens:
                y=table[x][a]
                if not seen>>y&1:seen|=1<<y;q.append(y)
        return seen

    # Every subgroup has a predecessor obtained by deleting one generator.
    # For each predecessor, examine every right coset representative: elements
    # in one right coset give the same generated overgroup.
    subgens={one:()};pending=deque([one]);extensions=0
    while pending:
        h=pending.popleft();hlist=list(members(h));covered=h
        for x in range(n):
            if covered>>x&1:continue
            for y in hlist:covered|=1<<table[y][x]
            gens=subgens[h]+(x,);k=closure(gens);extensions+=1
            if k not in subgens:subgens[k]=gens;pending.append(k)
        assert covered==(1<<n)-1
    bysize={}
    for h in subgens:bysize.setdefault(h.bit_count(),[]).append(h)
    phi={};ranks={}
    for h in subgens:
        intersection=h
        for k in bysize.get(h.bit_count()//prime,[]):
            if k&h==k:intersection&=k
        phi[h]=intersection
        q=h.bit_count()//intersection.bit_count();r=0
        while q>1:assert q%prime==0;q//=prime;r+=1
        ranks[h]=r
    rank=max(ranks.values())
    def normal(h):
        return all(h>>table[table[inv[x]][y]][x]&1
                   for x in range(n) for y in members(h))
    s=next(h for h in subgens if ranks[h]==rank and normal(phi[h]))
    family=[];current=s
    for h in bysize[s.bit_count()//prime]:
        if h&s==h and current&h!=current:
            family.append(h);current&=h
    assert current==phi[s] and len(family)==rank
    for i in range(rank):
        omitted=(1<<n)-1
        for j,h in enumerate(family):
            if i!=j:omitted&=h
        assert omitted!=current and omitted&current==current
    pilot=json.loads((ROOT/'results/16.45-pilot.json').read_text())
    row=next(r for r in pilot['rows'] if (r['order'],r['id'])==(n,data['id']))
    assert row['rank']==rank and row['subgroups']==len(subgens)
    return {'order':n,'id':data['id'],'rank':rank,'subgroups':len(subgens),
            'extensions':extensions,'associativity_triples':n**3,
            'subgroup_rank_frequencies':sorted(Counter(ranks.values()).items()),
            'witness_subgroup':list(members(s)),
            'normal_intersection':list(members(current)),
            'base_stabilizers':[list(members(h)) for h in family]}

def run():return [check(d) for d in json.loads((ROOT/'results/16.45-control-inputs.json').read_text())]

if __name__=='__main__':
    rows=run()
    (ROOT/'results/16.45-controls.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('PASS_1645_CONTROLS',len(rows),'groups',sum(r['subgroups'] for r in rows),'subgroups',sum(r['associativity_triples'] for r in rows),'associativity triples')
