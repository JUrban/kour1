#!/usr/bin/env python3
"""Exact integral controls for the conformal-diagonal detection argument."""
import itertools
import json
from pathlib import Path


def roots(n):
    result=[]
    for i in range(n):
        r=[0]*n;r[i]=2;result.append((r,{(i,n+i):1}))
        r=[0]*n;r[i]=-2;result.append((r,{(n+i,i):1}))
    for i,j in itertools.combinations(range(n),2):
        r=[0]*n;r[i]=1;r[j]=-1;result.append((r,{(i,j):1,(n+j,n+i):-1}))
        r=[0]*n;r[i]=-1;r[j]=1;result.append((r,{(j,i):1,(n+i,n+j):-1}))
        r=[0]*n;r[i]=r[j]=1;result.append((r,{(i,n+j):1,(j,n+i):1}))
        r=[0]*n;r[i]=r[j]=-1;result.append((r,{(n+j,i):1,(n+i,j):1}))
    return result


def run():
    reports=[]
    for n in range(1,9):
        d=2*n;rr=roots(n);assert len(rr)==2*n*n
        detectors=set()
        for r,a in rr:
            found=None
            for half in itertools.product([0,1],repeat=n):
                diag=list(half)+[1-v for v in half]
                weights={(diag[i]-diag[j]) for i,j in a}
                if len(weights)==1 and abs(next(iter(weights)))==1:found=half;break
            assert found is not None;detectors.add(found)
        checks=0
        for half in detectors:
            diag=list(half)+[1-v for v in half]
            for r,a in rr:
                weights={diag[i]-diag[j] for i,j in a};assert len(weights)==1
                square={};sandwich={}
                for (i,k),v in a.items():
                    for (h,j),w in a.items():
                        if h==k:
                            square[i,j]=square.get((i,j),0)+v*w
                            sandwich[i,j]=sandwich.get((i,j),0)+v*diag[k]*w
                assert not any(square.values()) and not any(sandwich.values());checks+=1
        # Commutator equations for a generic matrix, eliminated only with unit pivots.
        generators=[a for r,a in rr if sum(abs(v) for v in r)==2 and len(a)==1]
        for i in range(n-1):generators.append({(i,i+1):1,(n+i+1,n+i):-1})
        basis={};equations=0
        for a in generators:
            for i in range(d):
                for j in range(d):
                    equation={}
                    for (h,k),v in a.items():
                        if k==j:equation[d*i+h]=equation.get(d*i+h,0)+v
                        if h==i:equation[d*k+j]=equation.get(d*k+j,0)-v
                    equation={k:v for k,v in equation.items() if v};equations+=1
                    assert sum(v for k,v in equation.items() if k//d==k%d)==0
                    for pivot,row in sorted(basis.items()):
                        c=equation.get(pivot,0)
                        if c:
                            for k,v in row.items():equation[k]=equation.get(k,0)-c*v
                            equation={k:v for k,v in equation.items() if v}
                    if equation:
                        pivot=min(equation);c=equation[pivot];assert abs(c)==1
                        basis[pivot]={k:c*v for k,v in equation.items()}
        assert len(basis)==d*d-1
        reports.append(dict(rank=n,roots=len(rr),detectors=len(detectors),integer_action_checks=checks,
                            centralizer_equations=equations,unit_pivots=len(basis)))
    print('PASS_1962_SYMPLECTIC_CONTROLS',len(reports),sum(r['integer_action_checks'] for r in reports),flush=True)
    return dict(ranks=reports)


if __name__=='__main__':
    result=run();Path('results/19.62-symplectic-controls.json').write_text(json.dumps(result,indent=2)+'\n')
