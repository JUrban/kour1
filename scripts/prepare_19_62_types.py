#!/usr/bin/env python3
"""Audit ten integral Lie models and prepare every formal square target."""
import ast
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path

TYPES=['a2','a3','a4','b2','b3','b4','c3','c4','d4','f4']


def prepare(label):
    source=Path('results/19.62-'+label+'-integral.grows')
    roots,powers,adj,cartan=ast.literal_eval(source.read_text())
    nr=len(roots);dimension=len(adj);rank=len(cartan)
    assert rank==int(label[1:]) and dimension==nr+rank
    assert all(type(v) is int for a in adj for row in a for v in row)
    brackets={(i,j):[(k,adj[i][k][j]) for k in range(dimension) if adj[i][k][j]]
              for i in range(dimension) for j in range(dimension)}
    for i in range(dimension):
        for j in range(dimension):
            assert all(adj[i][k][j]==-adj[j][k][i] for k in range(dimension))
            for k in range(dimension):
                out=collections.defaultdict(int)
                for a,b,c in [(i,j,k),(j,k,i),(k,i,j)]:
                    for h,v in brackets[a,b]:
                        for z,w in brackets[h,c]:out[z]+=v*w
                assert not any(out.values())
    identity={(i,i,0,0):1 for i in range(dimension)}
    sparse=[[[[(j,v) for j,v in enumerate(row) if v] for row in p] for p in pp] for pp in powers]
    def factor(a,root,dt,du,c):
        out={}
        for power,rows in enumerate(sparse[root]):
            scale=c**power
            for (i,k,t,u),v in a.items():
                for j,w in rows[k]:
                    key=i,j,t+power*dt,u+power*du
                    out[key]=out.get(key,0)+v*w*scale
        return {k:v for k,v in out.items() if v}
    for r in range(nr):
        for i in range(rank):
            assert [adj[nr+i][k][r] for k in range(dimension)]==[roots[r][i]*int(k==r) for k in range(dimension)]
        actual={(i,i):1 for i in range(dimension)}
        for k,power in enumerate(powers[r]):
            expected={(i,j):math.factorial(k)*v for i,row in enumerate(power) for j,v in enumerate(row) if v}
            assert expected==actual
            out=collections.defaultdict(int)
            for (i,h),v in actual.items():
                for j,w in enumerate(adj[r][h]):
                    if w:out[i,j]+=v*w
            actual={key:v for key,v in out.items() if v}
        assert not actual
        # Polynomial root-group law x(t)x(u)=x(t+u).
        lhs=factor(factor(identity,r,1,0,1),r,0,1,1);rhs={}
        for k,power in enumerate(powers[r]):
            for i,row in enumerate(power):
                for j,v in enumerate(row):
                    if v:
                        for a in range(k+1):rhs[i,j,a,k-a]=v*math.comb(k,a)
        assert lhs==rhs
    rules=[];signed=[];identities=0;entries=0
    for r,a in enumerate(roots):
        for s,b in enumerate(roots):
            if a==b or a==[-v for v in b]:continue
            terms=[]
            for i,j in itertools.product(range(1,4),repeat=2):
                v=[i*x+j*y for x,y in zip(a,b)]
                if v in roots:
                    c=1
                    if i==j==1:
                        while [y-c*x for x,y in zip(a,b)] in roots:c+=1
                    assert c in [1,2];terms.append((i+j,i,j,roots.index(v),c))
            terms.sort();assert len(terms)<=2
            lhs=factor(factor(factor(factor(identity,r,1,0,-1),s,0,1,-1),r,1,0,1),s,0,1,1)
            matches=[]
            for signs in itertools.product([-1,1],repeat=len(terms)):
                rhs=identity
                for (_,i,j,k,c),sign in zip(terms,signs):rhs=factor(rhs,k,i,j,c*sign)
                if rhs==lhs:matches.append(signs)
            assert len(matches)==1,(label,r,s)
            for (_,i,j,k,c),sign in zip(terms,matches[0]):
                rules.append([r,s,k,i,j,c]);signed.append([r,s,k,i,j,c*sign])
            identities+=1;entries+=len(lhs)
    incoming=collections.defaultdict(list)
    for r,s,k,i,j,c in rules:incoming[k].append((r,s,i,j,c))
    cases={}
    def include(k,variables,c):
        key=k,tuple(sorted(variables));cases[key]=math.gcd(cases.get(key,0),c)
    for k,a in enumerate(roots):
        opposite=roots.index([-v for v in a])
        for first,last in itertools.product(incoming[k],incoming[opposite]):
            r,s,i,j,c=first;u,v,h,l,d=last
            include(k,[(r,2*i),(s,2*j),(u,h),(v,l)],c*c*d)
        for first,second in itertools.combinations_with_replacement(incoming[k],2):
            for last in incoming[opposite]:
                variables=[item for rule in [first,second,last] for item in [(rule[0],rule[2]),(rule[1],rule[3])]]
                include(k,variables,2*first[4]*second[4]*last[4])
    result=dict(type=label,roots=roots,rules=rules,signed_rules=signed,
                cases=[dict(root=k,variables=v,coefficient=c) for (k,v),c in sorted(cases.items())],
                integral_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                jacobi_triples=dimension**3,polynomial_root_group_laws=nr,
                polynomial_commutator_identities=identities,polynomial_matrix_entries=entries)
    path=Path('results/19.62-'+label+'-monomial-input.json');assert not path.exists()
    path.write_text(json.dumps(result,indent=2)+'\n')
    with path.with_suffix('.txt').open('w') as f:
        f.write(str(nr)+' '+str(len(rules))+'\n')
        for r in rules:f.write(' '.join(map(str,r))+'\n')
        f.write(str(len(cases))+'\n')
        for c in result['cases']:f.write(' '.join(map(str,[c['root'],c['coefficient'],len(c['variables'])]+[v for a in c['variables'] for v in a]))+'\n')
    print('PASS_1962_TYPE_PREPARATION',label,nr,len(rules),len(cases),flush=True)
    return result


if __name__=='__main__':
    for label in TYPES:prepare(label)
    print('PASS_1962_ALL_TYPE_PREPARATIONS',len(TYPES),flush=True)
