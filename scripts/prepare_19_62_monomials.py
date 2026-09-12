#!/usr/bin/env python3
"""Extract rank-two commutator monomials and formal opposite-root targets."""
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path
from matrices_19_61_mod9 import Matrices,IDENTITY,roots_mod9


def run():
    mm=Matrices().multiply;roots,matrices=roots_mod9();rules=[]
    for r,a in enumerate(roots):
        for s,b in enumerate(roots):
            if a==b or a==[-v for v in b]:continue
            terms=[]
            for i,j in itertools.product(range(1,4),repeat=2):
                v=[i*a[k]+j*b[k] for k in range(2)]
                if v in roots:terms.append((i+j,i,j,roots.index(v)))
            terms.sort();normal={}
            for coeff in itertools.product(range(9),repeat=len(terms)):
                mat=IDENTITY
                for term,t in zip(terms,coeff):mat=mm(mat,matrices[term[-1]][t])
                assert mat not in normal;normal[mat]=coeff
            comm=mm(mm(mm(matrices[r][8],matrices[s][8]),matrices[r][1]),matrices[s][1])
            coeff=normal[comm]
            for t,u in itertools.product(range(9),repeat=2):
                comm=mm(mm(mm(matrices[r][-t%9],matrices[s][-u%9]),matrices[r][t]),matrices[s][u])
                assert normal[comm]==tuple(c*pow(t,term[1])*pow(u,term[2])%9 for c,term in zip(coeff,terms))
            for c,(_,i,j,k) in zip(coeff,terms):
                c=min(c,9-c);assert c in [1,2,3];rules.append([r,s,k,i,j,c])
    incoming=collections.defaultdict(list)
    for r,s,k,i,j,c in rules:incoming[k].append((r,s,i,j,c))
    cases={}
    for k,a in enumerate(roots):
        opposite=roots.index([-v for v in a])
        for first in incoming[k]:
            for last in incoming[opposite]:
                r,s,i,j,c=first;u,v,h,l,d=last
                variables=tuple(sorted([(r,2*i),(s,2*j),(u,h),(v,l)]))
                key=(k,variables);cases[key]=math.gcd(cases.get(key,0),c*c*d)
        for first,second in itertools.combinations_with_replacement(incoming[k],2):
            for last in incoming[opposite]:
                variables=tuple(sorted(
                    item for rule in [first,second,last] for item in [(rule[0],rule[2]),(rule[1],rule[3])]))
                key=(k,variables);coefficient=2*first[4]*second[4]*last[4]
                cases[key]=math.gcd(cases.get(key,0),coefficient)
    result=dict(roots=roots,rules=rules,cases=[dict(root=k,variables=v,coefficient=c) for (k,v),c in sorted(cases.items())],
                integral_source_sha256=hashlib.sha256(Path('results/19.61-g2-integral.grows').read_bytes()).hexdigest(),
                status='formal targets only; no inclusion proof')
    Path('results/19.62-g2-monomial-input.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1962_MONOMIAL_PREPARATION',len(rules),len(cases),flush=True)


if __name__=='__main__':run()
