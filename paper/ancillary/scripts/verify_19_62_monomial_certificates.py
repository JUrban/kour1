#!/usr/bin/env python3
"""Check explicit integer derivations without running the monomial search."""
import collections
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path


def expected_targets(data):
    roots=data['roots'];rules=data['rules'];incoming=collections.defaultdict(list)
    expected_rules=set()
    for r,a in enumerate(roots):
        for s,b in enumerate(roots):
            if a==b or a==[-v for v in b]:continue
            for i,j in itertools.product(range(1,4),repeat=2):
                p=[i*x+j*y for x,y in zip(a,b)]
                if p in roots:expected_rules.add((r,s,roots.index(p),i,j))
    assert {tuple(r[:5]) for r in rules}==expected_rules and len(rules)==len(expected_rules)
    for r,s,k,i,j,c in rules:
        assert c in [1,2,3];incoming[k].append((r,s,i,j,c))
    required={}
    def include(k,variables,c):
        key=k,tuple(sorted(variables));required[key]=math.gcd(required.get(key,0),c)
    for k,p in enumerate(roots):
        opposite=roots.index([-v for v in p])
        for a,b in itertools.product(incoming[k],incoming[opposite]):
            include(k,[(a[0],2*a[2]),(a[1],2*a[3]),(b[0],b[2]),(b[1],b[3])],a[4]**2*b[4])
        # Ordered pairs independently cover the off-diagonal square terms.
        for a,b,c in itertools.product(incoming[k],incoming[k],incoming[opposite]):
            variables=[item for v in [a,b,c] for item in [(v[0],v[2]),(v[1],v[3])]]
            include(k,variables,2*a[4]*b[4]*c[4])
    actual={(c['root'],tuple(map(tuple,c['variables']))):c['coefficient'] for c in data['cases']}
    assert actual==required and len(actual)==len(data['cases'])==2712
    return required


def verify_case(data,index,nodes):
    assert 1<=index<=len(data['cases']);case=data['cases'][index-1]
    variables=case['variables'];radices=[v[1]+1 for v in variables];root_count=len(data['roots'])
    count=math.prod(radices);done={};derived={}
    for node in nodes:
        assert len(node)==6;key,a,b,var,left,right=node
        assert key not in done and 0<=a<64 and 0<=b<64
        code,root=divmod(key,root_count);assert 0<code<count
        exponents=[];remaining=code
        for radix in radices:remaining,digit=divmod(remaining,radix);exponents.append(digit)
        assert remaining==0 and sum(exponents)>0
        coefficient=2**a*3**b
        if var>=0:
            assert 0<=var<len(variables) and coefficient==1 and left==right==[]
            assert exponents==[int(d==var) for d in range(len(variables))]
            assert root==variables[var][0];derived[key]=False
        else:
            assert var==-1;coefficients=[]
            for edge in [left,right]:
                assert len(edge)==3;rule_index,lkey,rkey=edge
                assert 0<=rule_index<len(data['rules']) and lkey in done and rkey in done
                r,s,k,i,j,c=data['rules'][rule_index]
                lr,le,lc=done[lkey];rr,re,rc=done[rkey]
                assert (lr,rr,root)==(r,s,k)
                assert [i*x+j*y for x,y in zip(le,re)]==exponents
                coefficients.append(c*lc**i*rc**j)
            assert math.gcd(*coefficients)==coefficient
            derived[key]=True
        done[key]=(root,exponents,coefficient)
    target=(count-1)*root_count+case['root']
    assert target in done and derived[target]
    r,e,c=done[target]
    assert r==case['root'] and e==[v[1] for v in variables] and case['coefficient']%c==0
    return len(nodes)


def run():
    source=Path('results/19.62-g2-monomial-input.json');data=json.loads(source.read_text())
    expected_targets(data)
    certificate=Path('results/19.62-g2-monomial-certificates.jsonl')
    seen=set();nodes=0;largest=0;first=None
    for line in certificate.read_text().splitlines():
        index,rows=json.loads(line);assert index not in seen;seen.add(index)
        size=verify_case(data,index,rows);nodes+=size;largest=max(largest,size)
        if first is None:first=index,rows
    assert seen==set(range(1,len(data['cases'])+1))
    index,rows=first;mutants=[]
    bad=copy.deepcopy(rows);bad[-1][1]+=1;mutants.append(bad)
    bad=copy.deepcopy(rows);bad[-1][4][1]=bad[-1][0];mutants.append(bad)
    bad=copy.deepcopy(rows);bad[-1][4][0]=(bad[-1][4][0]+1)%len(data['rules']);mutants.append(bad)
    bad=copy.deepcopy(rows);bad.pop();mutants.append(bad)
    rejected=0
    for bad in mutants:
        try:verify_case(data,index,bad)
        except (AssertionError,KeyError):rejected+=1
        else:raise AssertionError('a corrupt derivation was accepted')
    result=dict(cases=len(seen),derivation_nodes=nodes,largest_certificate=largest,mutations_rejected=rejected,
                input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest())
    print('PASS_1962_G2_MONOMIAL_CERTIFICATES',len(seen),nodes,largest,rejected,flush=True)
    return result


if __name__=='__main__':
    result=run();Path('results/19.62-g2-monomial-verification.json').write_text(json.dumps(result,indent=2)+'\n')
