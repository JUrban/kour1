#!/usr/bin/env python3
"""Exact C2 root matrices, commutator factors, and all small-ring carpets."""
import argparse
import itertools
import json
from pathlib import Path
import time

ROOTS = [(2,0),(-2,0),(0,2),(0,-2),(1,1),(1,-1),(-1,1),(-1,-1)]


def prepare(label):
    started = time.monotonic()
    m = 2 if label == 'f2' else 4
    if label == 'z4':
        add = lambda a,b:(a+b)%4
        mul = lambda a,b:a*b%4
    else:
        add = lambda a,b:a^b
        reduction = {'f2':0,'f4':3,'dual':0,'split':2}[label]
        mul = lambda a,b:((a&1)*(b&1)) ^ ((((a&1)*(b>>1)) ^ ((a>>1)*(b&1)))<<1) ^ (reduction if (a>>1)*(b>>1) else 0)
    neg = [next(b for b in range(m) if add(a,b)==0) for a in range(m)]
    for a,b,c in itertools.product(range(m),repeat=3):
        assert add(add(a,b),c)==add(a,add(b,c))
        assert mul(mul(a,b),c)==mul(a,mul(b,c))
        assert mul(a,add(b,c))==add(mul(a,b),mul(a,c))
        assert mul(a,b)==mul(b,a) and mul(a,1)==a
    ident = tuple(int(i==j) for i in range(4) for j in range(4))

    def mm(a,b):
        out = []
        for i in range(4):
            for j in range(4):
                s = 0
                for k in range(4):s=add(s,mul(a[4*i+k],b[4*k+j]))
                out.append(s)
        return tuple(out)

    def transpose(a):return tuple(a[4*j+i] for i in range(4) for j in range(4))

    def root(r,t):
        a=list(ident)
        if abs(r[0])==2 or abs(r[1])==2:
            i=0 if r[0] else 1
            x,y=(i,i+2) if r[i]>0 else (i+2,i)
            a[4*x+y]=t
        else:
            positions={(1,-1):[(0,1,t),(3,2,neg[t])],
                       (-1,1):[(1,0,t),(2,3,neg[t])],
                       (1,1):[(0,3,t),(1,2,t)],
                       (-1,-1):[(2,1,t),(3,0,t)]}[r]
            for x,y,v in positions:a[4*x+y]=v
        return tuple(a)

    matrices=[[root(r,t) for t in range(m)] for r in ROOTS]
    form=[0]*16
    for i in range(2):form[4*i+i+2]=1;form[4*(i+2)+i]=neg[1]
    form=tuple(form)
    for row in matrices:
        assert len(set(row))==m
        for t,u in itertools.product(range(m),repeat=2):
            assert mm(row[t],row[u])==row[add(t,u)]
            assert mm(mm(transpose(row[t]),form),row[t])==form
    subsets=[tuple(x for x in range(m) if mask>>x&1) for mask in range(1,1<<m,2)]
    subsets=sorted([s for s in subsets if all(add(a,b) in s for a in s for b in s)],key=lambda s:(len(s),s))
    masks=[sum(1<<x for x in s) for s in subsets]
    implications=[];commutator_checks=0
    for ri,r in enumerate(ROOTS):
        for si,s in enumerate(ROOTS):
            if r==s or r==tuple(-v for v in s):continue
            terms=[]
            for i,j in itertools.product(range(1,4),repeat=2):
                v=tuple(i*r[k]+j*s[k] for k in range(2))
                if v in ROOTS:terms.append((i+j,i,j,ROOTS.index(v)))
            terms.sort();dest=[t[-1] for t in terms]
            assert len(dest)<=2 and len(set(dest))==len(dest)
            normal_forms={}
            for coeff in itertools.product(range(m),repeat=len(dest)):
                a=ident
                for k,v in zip(dest,coeff):a=mm(a,matrices[k][v])
                assert a not in normal_forms
                normal_forms[a]=coeff
            factors={}
            for t,u in itertools.product(range(m),repeat=2):
                comm=mm(mm(mm(matrices[ri][neg[t]],matrices[si][neg[u]]),matrices[ri][t]),matrices[si][u])
                assert comm in normal_forms,(label,r,s,t,u)
                factors[t,u]=normal_forms[comm];commutator_checks+=1
            for pos,k in enumerate(dest):
                required=[[sum(1<<v for v in {factors[t,u][pos] for t in a for u in b})
                           for b in subsets] for a in subsets]
                if any(v!=1 for row in required for v in row):
                    implications.append([ri,si,k,required])
    carpets=[]
    for row in itertools.product(range(len(subsets)),repeat=8):
        if all(not req[row[r]][row[s]] & ~masks[row[k]] for r,s,k,req in implications):
            carpets.append(row)
    vectors=list(itertools.product(range(m),repeat=4))
    lookup={v:i+1 for i,v in enumerate(vectors)}
    perms=[]
    for row in matrices:
        pr=[]
        for mat in row:
            images=[]
            for v in vectors:
                w=[]
                for j in range(4):
                    x=0
                    for i in range(4):x=add(x,mul(v[i],mat[4*i+j]))
                    w.append(x)
                images.append(lookup[tuple(w)])
            assert sorted(images)==list(range(1,len(vectors)+1))
            pr.append(images)
        perms.append(pr)
    path=Path(f'results/19.61-{label}-input.g')
    assert not path.exists(),'preserve previous generated data'
    j=lambda v:json.dumps(v,separators=(',',':'))
    # GAP arrays use indices shifted by one; parameters remain the integers0..m-1.
    gap_imp=[[r+1,s+1,k+1,req] for r,s,k,req in implications]
    text='RingLabel1961:='+j(label)+';\n'
    text+='Subsets1961:='+j(subsets)+';\nMasks1961:='+j(masks)+';\n'
    text+='Implications1961:='+j(gap_imp)+';\n'
    text+='Carpets1961:='+j([[v+1 for v in row] for row in carpets])+';\n'
    text+='RootPerms1961:=List('+j(perms)+', row->List(row,PermList));\n'
    path.write_text(text)
    report=dict(ring=label,order=m,roots=ROOTS,add=[[add(a,b) for b in range(m)] for a in range(m)],
                mul=[[mul(a,b) for b in range(m)] for a in range(m)],matrices=matrices,
                additive_subgroups=subsets,assignments=len(subsets)**8,carpets=len(carpets),
                implications=len(implications),commutator_checks=commutator_checks,
                permutation_degree=len(vectors),elapsed_seconds=time.monotonic()-started)
    Path(f'results/19.61-{label}-preparation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS_1961_PREPARATION',label,'carpets',len(carpets),'seconds',report['elapsed_seconds'],flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('rings',nargs='+',choices=['f2','f4','dual','split','z4'])
    for name in parser.parse_args().rings:prepare(name)
