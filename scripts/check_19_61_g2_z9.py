#!/usr/bin/env python3
"""Independent sparse Python matrix controls for the Z/9 kernel method."""
import collections
import itertools
import json
from pathlib import Path
import random
from matrices_19_61_mod9 import IDENTITY,roots_mod9
from linear_19_61_mod3 import Space


def reference_rank(rows,width):
    a=[list(v) for v in rows];rank=0
    for j in range(width):
        pivot=next((i for i in range(rank,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        c=pow(a[rank][j],-1,3);a[rank]=[c*x%3 for x in a[rank]]
        for i in range(len(a)):
            if i!=rank:
                c=a[i][j];a[i]=[(x-c*y)%3 for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank


def run():
    rng=random.Random(19610903);linear_checks=0
    for dimension in [2,3,16]:
        pools=list(itertools.product(range(3),repeat=dimension)) if dimension<=3 else None
        samples=list(itertools.combinations(pools,2)) if pools else [
            [tuple(rng.randrange(3) for _ in range(dimension)) for _ in range(rng.randrange(17))]
            for __ in range(128)]
        for rows in samples:
            s=Space(rows);rank=reference_rank(rows,dimension);assert s.rank()==rank
            probes=pools if pools else [tuple(rng.randrange(3) for _ in range(dimension)) for __ in range(16)]
            for v in probes:
                assert s.contains(v)==(reference_rank(list(rows)+[v],dimension)==rank);linear_checks+=1
    data=json.loads(Path('results/19.61-g2z9-input.json').read_text())
    prediction=json.loads(Path('results/19.61-g2z9-search.json').read_text())
    roots,matrices=roots_mod9();assert roots==data['roots']
    selected={i for i,row in enumerate(data['carpets'],1) if sum(bool(x) for x in row)<=2}
    by_order={}
    for row in prediction['rows']:
        if row['order'] and row['order']<=20000:by_order.setdefault(row['order'],row['index'])
    selected.update(by_order.values())
    operators={}
    for r in range(12):
        for t in [1,3]:
            a=matrices[r][t];op=[]
            for j in range(14):
                delta=[(k,(a[14*k+j]-int(k==j))%9) for k in range(14)
                       if (a[14*k+j]-int(k==j))%9]
                if delta:op.append((j,delta))
            operators[r,t]=op
    states=0;hist=collections.Counter();kernel_states=0
    for index in sorted(selected):
        row=data['carpets'][index-1];ops=[operators[r,1 if x==2 else 3] for r,x in enumerate(row) if x]
        known={IDENTITY};todo=[IDENTITY]
        for a in todo:
            for op in ops:
                b=bytearray(a)
                for j,delta in op:
                    for i in range(14):b[14*i+j]=(a[14*i+j]+sum(a[14*i+k]*v for k,v in delta))%9
                b=bytes(b)
                if b not in known:
                    known.add(b);todo.append(b);assert len(known)<=20000,'no capped group accepted'
        actual=[]
        for r in range(12):
            parameters=[t for t in range(9) if matrices[r][t] in known]
            actual.append(data['subsets'].index(parameters))
        expected=prediction['rows'][index-1]
        assert actual==expected['closure'] and len(known)==expected['order'],index
        kernel=[bytes(((a-b)%9)//3 for a,b in zip(g,IDENTITY)) for g in known
                if all(a%3==b for a,b in zip(g,IDENTITY))]
        assert len(kernel)==3**expected['kernel_rank']
        assert reference_rank(kernel,196)==expected['kernel_rank']
        assert all(not req[actual[r]][actual[s]]&~data['masks'][actual[k]] for r,s,k,req in data['implications'])
        states+=len(known);hist[len(known)]+=1;kernel_states+=len(kernel)
    result=dict(cases=len(selected),matrix_states=states,kernel_states=kernel_states,
                largest_group=max(hist),group_order_histogram=dict(sorted(hist.items())),
                selected_indices=sorted(selected),linear_membership_controls=linear_checks)
    print('PASS_1961_Z9_MATRIX_CONTROLS',len(selected),states,kernel_states,linear_checks,flush=True)
    return result


if __name__=='__main__':
    result=run();Path('results/19.61-g2z9-controls.json').write_text(json.dumps(result,indent=2)+'\n')
