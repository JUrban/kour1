#!/usr/bin/env python3
"""Exact finite controls for 14.26; the parameter-uniform proof is separate."""
from fractions import Fraction as F
from math import factorial, comb
from itertools import combinations_with_replacement, product
from pathlib import Path
import json,time

def add(a,b,s=1):
 r=a.copy()
 for k,v in b.items():
  r[k]=r.get(k,0)+s*v
  if not r[k]: del r[k]
 return r

def scale(a,s): return {k:v*s for k,v in a.items() if v*s}
def rawmul(a,b,c):
 r={}
 for x,v in a.items():
  for y,w in b.items():
   if len(x)+len(y)<=c:
    z=tuple(sorted(x+y));r[z]=r.get(z,0)+v*w
 return {k:v for k,v in r.items() if v}
def pmul(a,b):
 r={}
 for x,v in a.items():
  for y,w in b.items():
   z=tuple(i+j for i,j in zip(x,y));r[z]=r.get(z,0)+v*w
 return {k:v for k,v in r.items() if v}
def ppow(a,n,k):
 r={(0,)*k:F(1)}
 for _ in range(n):r=pmul(r,a)
 return r

def dual(k,R,I,selected):
 one={(0,)*k:F(1)};q=one;C=1
 for a in range(k):
  for b in range(a+1,k):
   z=[0]*k;z[a]=1;p={tuple(z):F(1)};z=[0]*k;z[b]=1;p[tuple(z)]=F(-1)
   for d in range(1,R+1):
    q=pmul(q,add(pmul(p,p),one,-d*d));C*=-d*d
 avg={tuple(int(i==j) for i in range(k)):F(1,k) for j in range(k)}
 for j in I:
  if j!=selected:q=scale(pmul(q,add(avg,one,-j)),F(1,selected-j))
 return scale(q,F(1,C))

class Algebra:
 def __init__(self,c,R,m):
  self.c,self.R,self.m=c,R,m;self.rows={};self.generators=[]
  quadratics=[]
  for d in range(1,R+1):
   rows=[{} for _ in range(2*m+1)]
   for i in range(m+1):
    for j in range(m+1):
     mon=tuple(sorted((i,j)))
     for v in range(j+1):
      p=rows[i+v];p[mon]=p.get(mon,0)+F(comb(j,v)*d**(j-v),factorial(i)*factorial(j))
   quadratics+=rows
  for k in range(2,c+1):
   for mon in combinations_with_replacement(range(m+1),k-2):
    for q in quadratics:
     p=rawmul(q,{mon:F(1)},c);self.generators.append(p)
     r=self.reduce(p)
     if r:
      pivot=min(r);self.rows[pivot]=scale(r,1/r[pivot])
 def reduce(self,p):
  todo=p.copy();out={}
  while todo:
   pivot=min(todo);v=todo[pivot]
   if pivot in self.rows:todo=add(todo,self.rows[pivot],-v)
   else:out[pivot]=v;del todo[pivot]
  return out
 def mul(self,a,b):return self.reduce(rawmul(a,b,self.c))
 def power(self,a,n):
  r={():F(1)}
  for _ in range(n):r=self.mul(r,a)
  return r
 def f(self,i):return {(j,):F(i**j,factorial(j)) for j in range(self.m+1) if i**j}
 def D(self,p):
  r={}
  for mon,v in p.items():
   for s,j in enumerate(mon):
    if j<self.m:
     z=tuple(sorted(mon[:s]+(j+1,)+mon[s+1:]));r[z]=r.get(z,0)+v
  return r
 def alpha(self,p,s=1):
  # Direct exp(sD) on the free algebra, then quotient.
  r={}
  for mon,v in p.items():
   a={():v}
   for j in mon:
    a=rawmul(a,{(j+h,):F(s**h,factorial(h)) for h in range(self.m-j+1) if s**h},self.c)
   r=add(r,a)
  return self.reduce(r)

def mmul(A,B,mul,addfun,zero,n):
 return {(a,b):sum_polys([mul(A.get((a,h),zero),B.get((h,b),zero)) for h in range(a,b+1)],addfun,zero) for a in range(n) for b in range(a,n)}
def sum_polys(ps,addfun,zero):
 out=zero
 for p in ps:out=addfun(out,p)
 return out

def run(c,R,I):
 started=time.monotonic();m=2*R*(c-1)+len(I)-1;A=Algebra(c,R,m)
 counts={'ideal_generators':len(A.generators),'relation_rank':len(A.rows),'dual_relation_checks':0,'dual_separation_checks':0,'D_stability_checks':0,'shift_checks':0,'matrix_homomorphism_checks':0,'matrix_commutation_checks':0,'local_wreath_products':0}
 for r in A.generators:
  assert not A.reduce(A.D(r));counts['D_stability_checks']+=1
 for k in range(1,c+1):
  for i in I:
   Q=dual(k,R,I,i)
   assert all(max(mon,default=0)<=m for mon in Q)
   def ell(p):
    return sum(v*Q.get(mon,0)*__import__('functools').reduce(lambda a,j:a*factorial(j),mon,1) for mon,v in p.items())
   for r in A.generators:
    if r and len(next(iter(r)))==k:
     assert ell(r)==0;counts['dual_relation_checks']+=1
   for j in I:
    # Evaluate before quotient, independently of row reduction.
    p={():F(1)}
    for _ in range(k):p=rawmul(p,A.f(j),c)
    assert ell(p)==int(i==j);counts['dual_separation_checks']+=1
    assert A.power(A.f(j),k)
 for i in range(-R-1,R+2):
  for j in range(-R-1,R+2):
   if 0<abs(i-j)<=R:assert not A.mul(A.f(i),A.f(j))
  for s in [-2,-1,0,1,2]:
   assert A.alpha(A.f(i),s)==A.f(i+s);counts['shift_checks']+=1
 # Alpha descends and is invertible on a spanning set.
 for k in range(c+1):
  for mon in combinations_with_replacement(range(m+1),k):
   p={mon:F(1)}
   assert A.alpha(A.alpha(p),-1)==A.reduce(p)
   q=p
   for _ in range(c*m+1):q=A.D(q)
   assert not q
 n=c+1
 rats=[{(a,b):(F(1) if a==b else F((a+2)*(b+3)+seed,seed+1)) for a in range(n) for b in range(a,n)} for seed in range(3)]
 rmm=lambda g,h:mmul(g,h,lambda x,y:x*y,lambda x,y:x+y,F(0),n)
 amm=lambda g,h:mmul(g,h,A.mul,add,{},n)
 def rho(g,i):return {(a,b):scale(A.power(A.f(i),b-a),v) for (a,b),v in g.items()}
 for g,h in product(rats,repeat=2):
  for i in I:
   assert amm(rho(g,i),rho(h,i))==rho(rmm(g,h),i);counts['matrix_homomorphism_checks']+=1
  for i,j in product(I,repeat=2):
   if i!=j:
    assert amm(rho(g,i),rho(h,j))==amm(rho(h,j),rho(g,i));counts['matrix_commutation_checks']+=1
 for g in rats:
  for i in I:
   assert {p:A.alpha(v) for p,v in rho(g,i).items()}==rho(g,i+1)
 # Wreath multiplication with shift 1: a at min(I), b at min(I),
 # hence b shifts into the next slot. The coordinates remain in I.
 if len(I)>1 and min(I)+1 in I:
  i=min(I)
  for g,h in product(rats,repeat=2):
   left=amm(rho(g,i),{p:A.alpha(v) for p,v in rho(h,i).items()})
   right=amm(rho(g,i),rho(h,i+1))
   assert left==right;counts['local_wreath_products']+=1
 return {'c':c,'R':R,'I':I,'m':m,'ambient_dimension':sum(comb(m+k,k) for k in range(c+1)),'quotient_dimension':sum(comb(m+k,k) for k in range(c+1))-len(A.rows),'counts':counts,'elapsed_seconds':time.monotonic()-started}

if __name__=='__main__':
 start=time.monotonic();out=[]
 for args in [(1,2,[-1,0,1]),(2,1,[0,1]),(2,2,[-1,0,1]),(3,1,[0,1])]:
  r=run(*args);out.append(r);print(json.dumps(r),flush=True)
 result={'status':'PASS','arithmetic':'exact fractions, no modular or numerical tests','scope':'Finite controls only; all-parameter proof is separate.','cases':out,'elapsed_seconds':time.monotonic()-start}
 Path('results/14.26-polynomial-controls.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS_14_26_POLYNOMIAL',flush=True)
