#!/usr/bin/env python3
"""G2 over four-element rings, using exhaustive finite closure enumeration."""
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path
import time
from carpet_horn_19_61 import CarpetClosure

D=14


def prepare(label="f9"):
    assert label=="f9"
    started=time.monotonic();m=9;tag="g2f9"
    source=Path('results/19.61-g2-integral.grows')
    manifest=json.loads(Path('results/19.61-g2-summary.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['sha256'][str(source)]
    roots,powers,adj,cartan=ast.literal_eval(source.read_text())
    assert len(roots)==12 and cartan==[[2,-1],[-3,2]]
    add=lambda a,b:((a%3+b%3)%3)+3*((a//3+b//3)%3)
    mul=lambda a,b:((a%3*b%3+2*(a//3)*(b//3))%3)+3*((a%3*(b//3)+(a//3)*(b%3))%3)
    adds=[[add(a,b) for b in range(m)] for a in range(m)]
    muls=[[mul(a,b) for b in range(m)] for a in range(m)]
    neg=[next(b for b in range(m) if add(a,b)==0) for a in range(m)]
    for a,b,c in itertools.product(range(m),repeat=3):
        assert add(add(a,b),c)==add(a,add(b,c))
        assert mul(mul(a,b),c)==mul(a,mul(b,c))
        assert mul(a,add(b,c))==add(mul(a,b),mul(a,c))
        assert mul(a,b)==mul(b,a) and mul(a,1)==a
    char=3
    integer=lambda v:v%char
    ident=tuple(int(i==j) for i in range(D) for j in range(D))
    columns={}
    def cols(a):
        if a not in columns:columns[a]=[[(k,a[D*k+j]) for k in range(D) if a[D*k+j]] for j in range(D)]
        return columns[a]
    def dot(a,col,offset=0):
        s=0
        for k,v in col:s=adds[s][muls[a[offset+k]][v]]
        return s
    def mm(a,b):return tuple(dot(a,col,D*i) for i in range(D) for col in cols(b))
    def act(v,a):return tuple(dot(v,col) for col in cols(a))
    matrices=[]
    for row in powers:
        row=[tuple(x for rr in a for x in rr) for a in row];out=[]
        for t in range(m):
            a=[0]*(D*D);tk=1
            for power in row:
                for v,x in enumerate(power):a[v]=adds[a[v]][muls[tk][integer(x)]]
                tk=mul(tk,t)
            out.append(tuple(a))
        matrices.append(out)
    for row in matrices:
        assert len(set(row))==m
        for t,u in itertools.product(range(m),repeat=2):assert mm(row[t],row[u])==row[add(t,u)]
    subsets=[tuple(t for t in range(m) if mask>>t&1) for mask in range(1,1<<m,2)]
    subsets=sorted([s for s in subsets if all(add(a,b) in s for a in s for b in s)],key=lambda s:(len(s),s))
    masks=[sum(1<<t for t in s) for s in subsets];implications=[];checks=0
    for ri,r in enumerate(roots):
        for si,s in enumerate(roots):
            if r==s or r==[-x for x in s]:continue
            terms=[]
            for i,j in itertools.product(range(1,4),repeat=2):
                v=[i*r[k]+j*s[k] for k in range(2)]
                if v in roots:terms.append((i+j,i,j,roots.index(v)))
            terms.sort();dest=[t[-1] for t in terms]
            assert len(dest)<=4 and len(set(dest))==len(dest)
            normal={}
            for coeff in itertools.product(range(m),repeat=len(dest)):
                a=ident
                for k,t in zip(dest,coeff):a=mm(a,matrices[k][t])
                assert a not in normal;normal[a]=coeff
            factors={}
            for t,u in itertools.product(range(m),repeat=2):
                a=mm(mm(mm(matrices[ri][neg[t]],matrices[si][neg[u]]),matrices[ri][t]),matrices[si][u])
                assert a in normal,(label,r,s,t,u)
                factors[t,u]=normal[a];checks+=1
            for pos,k in enumerate(dest):
                req=[[sum(1<<v for v in {factors[t,u][pos] for t in a for u in b}) for b in subsets] for a in subsets]
                if any(v!=1 for row in req for v in row):implications.append([ri+1,si+1,k+1,req])
    closure=CarpetClosure(12,adds,subsets,implications);carpets=[]
    for value in closure.closed_sets():
        row=closure.row(value)
        assert all(not req[row[r-1]-1][row[s-1]-1]&~masks[row[k-1]-1] for r,s,k,req in implications)
        carpets.append(row)
        assert len(carpets)<=1000000,'no capped enumeration is accepted'
    carpets.sort();assert len(set(carpets))==len(carpets)
    print('PASS_1961_G2_RING_CARPETS',tag,len(carpets),'seconds',time.monotonic()-started,flush=True)
    # Derive the seven-dimensional invariant module from the frozen F3 orbit.
    old=json.loads(Path('results/19.61-g2p3-preparation.json').read_text())
    echelon={}
    for original in old['chosen_orbit']:
        v=list(original)
        for i,row in sorted(echelon.items()):
            c=v[i]
            if c:v=[(a-c*b)%3 for a,b in zip(v,row)]
        if any(v):
            i=next(i for i,x in enumerate(v) if x);c=pow(v[i],-1,3)
            echelon[i]=[(c*x)%3 for x in v]
    assert len(echelon)==7
    pivots=sorted(echelon)
    for i in reversed(pivots):
        for j in pivots:
            if j>=i:continue
            c=echelon[j][i]
            echelon[j]=[(a-c*b)%3 for a,b in zip(echelon[j],echelon[i])]
    basis=[echelon[i] for i in pivots]
    def coordinates(vector):
        out=[vector[i] for i in pivots];reconstructed=[0]*D
        for c,row in zip(out,basis):
            for j,v in enumerate(row):reconstructed[j]=adds[reconstructed[j]][muls[c][v]]
        assert reconstructed==list(vector)
        return tuple(out)
    restricted=[[tuple(x for row in basis for x in coordinates(act(row,a))) for a in rr] for rr in matrices]
    def cols7(a):return [[(k,a[7*k+j]) for k in range(7) if a[7*k+j]] for j in range(7)]
    columns7={a:cols7(a) for row in restricted for a in row}
    inverse=[0]+[next(b for b in range(1,m) if muls[a][b]==1) for a in range(1,m)]
    def project(vector):
        leading=next(x for x in vector if x);c=inverse[leading]
        return tuple(muls[c][x] for x in vector)
    def act7(v,a):return project(tuple(dot(v,col) for col in columns7[a]))
    generators=[row[t] for row in restricted for t in [1,3]]
    vector=project(coordinates(tuple(int(i==1) for i in range(D))))
    seen={vector};todo=[vector]
    for v in todo:
        for a in generators:
            w=act7(v,a)
            if w not in seen:
                seen.add(w);todo.append(w)
                assert len(seen)<=70000,'projective orbit must be complete'
    orbit=sorted(seen);lookup={v:i+1 for i,v in enumerate(orbit)}
    print('PASS_1961_G2_F9_ORBIT',len(orbit),'seconds',time.monotonic()-started,flush=True)
    perms=[[[lookup[act7(v,a)] for v in orbit] for a in row] for row in restricted]
    assert all(sorted(p)==list(range(1,len(orbit)+1)) for row in perms for p in row)
    expected=9**6*(9**6-1)*(9**2-1)
    j=lambda v:json.dumps(v,separators=(',',':'))
    path=Path(f'results/19.61-{tag}-input.g');assert not path.exists()
    text='RingLabel1961:='+j(tag)+';\nSubsets1961:='+j(subsets)+';\nMasks1961:='+j(masks)+';\n'
    text+='Implications1961:='+j(implications)+';\nCarpets1961:='+j(carpets)+';\n'
    text+='RootPerms1961:=List('+j(perms)+', row->List(row,PermList));\n'
    text+=f'ExpectedOrder1961:={expected};\n';path.write_text(text)
    report=dict(ring=label,order=m,roots=roots,add=adds,mul=muls,matrices=matrices,
                additive_subgroups=subsets,assignments=len(subsets)**12,carpets=len(carpets),
                implications=len(implications),commutator_checks=checks,horn_rules=len(closure.rules),
                orbit_degree=len(orbit),orbit=orbit,invariant_basis=basis,restricted_matrices=restricted,
                faithful_action_status="requires abstract identification/order argument or direct controls",
                expected_ambient_order=expected,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                elapsed_seconds=time.monotonic()-started)
    Path(f'results/19.61-{tag}-preparation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS_1961_G2_RING_PREPARATION',tag,'carpets',len(carpets),'degree',len(orbit),'seconds',report['elapsed_seconds'],flush=True)


if __name__=='__main__':prepare()
