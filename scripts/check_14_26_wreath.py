#!/usr/bin/env python3
"""Independent Heisenberg wreath finite table and its polynomial local model."""
from check_14_26_polynomial import Algebra, F, add, mmul, scale
from pathlib import Path
import json,time

ONE=(0,0,0)
def hmul(x,y):
 a,b,c=x;A,B,C=y
 return (a+A,b+B,c+C+a*B)
def wmul(x,y):
 f,n=x;g,m=y;out=dict(f)
 for i,v in g:
  j=i+n;v=hmul(out.get(j,ONE),v)
  if v==ONE:out.pop(j,None)
  else:out[j]=v
 return (tuple(sorted(out.items())),n+m)

def run():
 start=time.monotonic();identity=((),0)
 generators=[((((0,(1,0,0)),)),0),((((0,(-1,0,0)),)),0),((((0,(0,1,0)),)),0),((((0,(0,-1,0)),)),0),((),1),((),-1)]
 S={identity};front={identity}
 for _ in range(2):
  front={wmul(x,y) for x in front for y in generators};S|=front
 S=sorted(S);lookup={x:i for i,x in enumerate(S)}
 table=[(a,b,lookup[z]) for a,x in enumerate(S) for b,y in enumerate(S) if (z:=wmul(x,y)) in lookup]
 I={i for f,n in S for i,g in f}
 for a,b,z in table:
  I.update(i+S[a][1] for i,g in S[b][0])
 I=sorted(I);R=max(1,max(I)-min(I));c=2;m=2*R+len(I)-1;A=Algebra(c,R,m)
 one={(a,b):({():F(1)} if a==b else {}) for a in range(3) for b in range(a,3)}
 mul=lambda x,y:mmul(x,y,A.mul,add,{},3)
 def rho(g,i):
  a,b,z=g;r={p:v.copy() for p,v in one.items()};r[0,1]=scale(A.f(i),a);r[1,2]=scale(A.f(i),b);r[0,2]=scale(A.power(A.f(i),2),z)
  return r
 def psi(x):
  f,n=x;r=one
  for i,g in f:r=mul(r,rho(g,i))
  return r,n
 images=[psi(x) for x in S]
 def key(x):
  mat,n=x
  return n,tuple((p,tuple(sorted(v.items()))) for p,v in sorted(mat.items()))
 assert len({key(x) for x in images})==len(S)
 for a,b,z in table:
  x,n=images[a];y,j=images[b]
  out=mul(x,{p:A.alpha(v,n) for p,v in y.items()}),n+j
  assert out==images[z],(a,b,z)
 # The ball contains a noncommuting pair and both orderings of its product.
 x,y=generators[0],generators[2]
 assert wmul(x,y)!=wmul(y,x)
 assert wmul(x,y) in lookup and wmul(y,x) in lookup
 assert images[lookup[wmul(x,y)]]!=images[lookup[wmul(y,x)]]
 return {'status':'PASS','base':'integral Heisenberg group, independently implemented triples','radius':2,'generators_including_inverses':6,'elements':len(S),'multiplication_relations':len(table),'separated_pairs':len(S)*(len(S)-1)//2,'positions':I,'R':R,'c':c,'m':m,'relation_rank':len(A.rows),'elapsed_seconds':time.monotonic()-start}
if __name__=='__main__':
 out=run();Path('results/14.26-wreath-controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));print('PASS_14_26_WREATH')
