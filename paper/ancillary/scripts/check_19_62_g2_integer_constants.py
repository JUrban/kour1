#!/usr/bin/env python3
"""Verify every G2 commutator identity as a polynomial matrix over Z[t,u]."""
import ast
import hashlib
import itertools
import json
from pathlib import Path


def run():
    source=Path('results/19.61-g2-integral.grows');roots,powers,adj,cartan=ast.literal_eval(source.read_text())
    data=json.loads(Path('results/19.62-g2-monomial-input.json').read_text());assert data['roots']==roots
    rules={(r,s,k,i,j):c for r,s,k,i,j,c in data['rules']}
    sparse=[[[[(j,v) for j,v in enumerate(row) if v] for row in p] for p in pp] for pp in powers]
    identity={(i,i,0,0):1 for i in range(14)}
    def factor(a,root,dt,du,c):
        out={}
        for power,rows in enumerate(sparse[root]):
            scale=c**power
            for (i,k,t,u),v in a.items():
                for j,w in rows[k]:
                    key=i,j,t+power*dt,u+power*du
                    out[key]=out.get(key,0)+v*w*scale
        return {k:v for k,v in out.items() if v}
    signed=[];identities=0;coefficient_entries=0;max_degree=0
    for r,a in enumerate(roots):
        for s,b in enumerate(roots):
            if a==b or a==[-v for v in b]:continue
            terms=sorted((i+j,i,j,k,c) for (rr,ss,k,i,j),c in rules.items() if (rr,ss)==(r,s))
            lhs=factor(factor(factor(factor(identity,r,1,0,-1),s,0,1,-1),r,1,0,1),s,0,1,1)
            matches=[]
            for signs in itertools.product([-1,1],repeat=len(terms)):
                rhs=identity
                for (_,i,j,k,c),sign in zip(terms,signs):rhs=factor(rhs,k,i,j,c*sign)
                if rhs==lhs:matches.append(signs)
            assert len(matches)==1,(r,s,len(matches))
            for (_,i,j,k,c),sign in zip(terms,matches[0]):signed.append([r,s,k,i,j,c*sign])
            identities+=1;coefficient_entries+=len(lhs)
            max_degree=max(max_degree,max(t+u for i,j,t,u in lhs))
    assert identities==120 and len(signed)==156
    result=dict(identities=identities,nonzero_polynomial_matrix_entries=coefficient_entries,
                largest_total_degree=max_degree,signed_rules=signed,
                integral_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    print('PASS_1962_G2_INTEGER_CONSTANTS',identities,len(signed),coefficient_entries,max_degree,flush=True)
    return result


if __name__=='__main__':
    result=run();Path('results/19.62-g2-integer-constants.json').write_text(json.dumps(result,indent=2)+'\n')
