#!/usr/bin/env python3
"""Exact Z/9 commutator conditions and brute-force enumeration of all 3^12 assignments."""
import hashlib
import itertools
import json
from pathlib import Path
import time
from matrices_19_61_mod9 import Matrices,IDENTITY,roots_mod9


def run():
    started=time.monotonic();native=Matrices();mm=native.multiply;roots,matrices=roots_mod9()
    subsets=[[0],[0,3,6],list(range(9))];masks=[sum(1<<t for t in s) for s in subsets]
    implications=[];checks=0
    for ri,r in enumerate(roots):
        for si,s in enumerate(roots):
            if r==s or r==[-v for v in s]:continue
            terms=[]
            for i,j in itertools.product(range(1,4),repeat=2):
                v=[i*r[k]+j*s[k] for k in range(2)]
                if v in roots:terms.append((i+j,i,j,roots.index(v)))
            terms.sort();dest=[t[-1] for t in terms]
            assert len(dest)<=4 and len(set(dest))==len(dest)
            normal={}
            for coeff in itertools.product(range(9),repeat=len(dest)):
                a=IDENTITY
                for k,t in zip(dest,coeff):a=mm(a,matrices[k][t])
                assert a not in normal;normal[a]=coeff
            factors={}
            for t,u in itertools.product(range(9),repeat=2):
                a=mm(mm(mm(matrices[ri][-t%9],matrices[si][-u%9]),matrices[ri][t]),matrices[si][u])
                assert a in normal;(factors[t,u],checks)=(normal[a],checks+1)
            for pos,k in enumerate(dest):
                req=[[sum(1<<v for v in {factors[t,u][pos] for t in a for u in b}) for b in subsets] for a in subsets]
                if any(v!=1 for row in req for v in row):implications.append([ri,si,k,req])
    carpets=[]
    for row in itertools.product(range(3),repeat=12):
        if all(not req[row[r]][row[s]]&~masks[row[k]] for r,s,k,req in implications):carpets.append(row)
    result=dict(roots=roots,subsets=subsets,masks=masks,implications=implications,carpets=carpets,
                assignments=3**12,commutator_checks=checks,elapsed_seconds=time.monotonic()-started,
                integral_source_sha256=hashlib.sha256(Path('results/19.61-g2-integral.grows').read_bytes()).hexdigest())
    path=Path('results/19.61-g2z9-input.json');assert not path.exists();path.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_Z9_PREPARATION',len(carpets),'of',3**12,'seconds',result['elapsed_seconds'],flush=True)


if __name__=='__main__':run()
