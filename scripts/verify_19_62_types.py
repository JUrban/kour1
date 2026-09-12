#!/usr/bin/env python3
"""Independent coverage and integer-derivation verification for all ten types."""
import collections
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from prepare_19_62_types import TYPES
from verify_19_62_monomial_certificates import verify_case


def targets(data):
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
        assert c in [1,2];incoming[k].append((r,s,i,j,c))
    required={}
    def include(k,variables,c):
        key=k,tuple(sorted(variables));required[key]=math.gcd(required.get(key,0),c)
    for k,p in enumerate(roots):
        opposite=roots.index([-v for v in p])
        for a,b in itertools.product(incoming[k],incoming[opposite]):
            include(k,[(a[0],2*a[2]),(a[1],2*a[3]),(b[0],b[2]),(b[1],b[3])],a[4]**2*b[4])
        for a,b,c in itertools.product(incoming[k],incoming[k],incoming[opposite]):
            include(k,[item for v in [a,b,c] for item in [(v[0],v[2]),(v[1],v[3])]],2*a[4]*b[4]*c[4])
    actual={(c['root'],tuple(map(tuple,c['variables']))):c['coefficient'] for c in data['cases']}
    assert actual==required and len(actual)==len(data['cases'])


def run():
    reports=[]
    for label in TYPES:
        source=Path('results/19.62-'+label+'-monomial-input.json');data=json.loads(source.read_text())
        targets(data);certificate=Path('results/19.62-'+label+'-monomial-certificates.jsonl')
        seen=set();nodes=0;largest=0;first=None
        with certificate.open() as f:
            for line in f:
                index,rows=json.loads(line);assert index not in seen;seen.add(index)
                n=verify_case(data,index,rows);nodes+=n;largest=max(largest,n)
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
            else:raise AssertionError('corrupted derivation accepted')
        result=dict(type=label,cases=len(seen),derivation_nodes=nodes,largest_certificate=largest,
                    mutations_rejected=rejected,input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest())
        reports.append(result);print('PASS_1962_TYPE_CERTIFICATE',label,len(seen),nodes,largest,rejected,flush=True)
    assert sum(r['cases'] for r in reports)==68344
    return dict(types=reports,cases=sum(r['cases'] for r in reports),derivation_nodes=sum(r['derivation_nodes'] for r in reports))


if __name__=='__main__':
    result=run();Path('results/19.62-types-verification.json').write_text(json.dumps(result,indent=2)+'\n')
