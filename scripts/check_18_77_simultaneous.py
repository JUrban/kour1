#!/usr/bin/env python3
"""Enumerate forbidden hyperplanes for two-parameter matrix families."""
import random,itertools,json,time
from pathlib import Path
from check_18_77 import alternating,matrix,image_log
ROOT=Path(__file__).resolve().parents[1]
def run():
 rng=random.Random(1877015);rows=[]
 for p,k,n,num in [(2,1,2,4),(3,1,2,4),(3,2,2,4),(5,1,2,4),(5,2,2,4),(5,1,4,4),(5,2,4,4),(7,1,6,4)]:
  q=p**k
  normals=[(1,t) for t in range(p)]+[(0,1)]
  for _ in range(num):
   coeff=[alternating(n,q,rng) for _ in range(2)]
   values=[(x,image_log(matrix(coeff,x,q),p,k)//2) for x in itertools.product(range(q),repeat=2)]
   e=max(v for x,v in values);assert e<p
   maximum={tuple(z%p for z in x) for x,v in values if v==e};t=p-e;checks=0
   for forbidden in itertools.combinations(normals,t):
    assert any(all(sum(a*b for a,b in zip(ell,x))%p for ell in forbidden) for x in maximum)
    checks+=1
   rows.append({'p':p,'k':k,'matrix_size':n,'max_e':e,'simultaneous_elements':t,'parameter_values':q*q,'forbidden_hyperplane_sets':checks,'max_residues':len(maximum)})
 return rows
if __name__=='__main__':
 start=time.monotonic();rows=run();(ROOT/'results/18.77-simultaneous-controls.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS_1877_SIMULTANEOUS',len(rows),'pencils',sum(r['forbidden_hyperplane_sets'] for r in rows),'hyperplane sets',time.monotonic()-start,'seconds')
