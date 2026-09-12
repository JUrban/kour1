#!/usr/bin/env python3
"""Exact prime-power alternating pencils; image enumeration is independent."""
import itertools,json,random,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def vp(a,p,k):
 if a==0:return k
 v=0
 while a%p==0:a//=p;v+=1
 return min(v,k)
def image_log(a,p,k):
 q=p**k;n=len(a);b=[r[:] for r in a];power=0;pos=0
 # Ordinary row/column Smith elimination, not alternating congruence.
 while pos<n:
  choices=[(vp(b[i][j],p,k),i,j) for i in range(pos,n) for j in range(pos,n) if b[i][j]%q]
  if not choices:break
  v,i,j=min(choices);b[pos],b[i]=b[i],b[pos]
  for row in b:row[pos],row[j]=row[j],row[pos]
  scale=pow(b[pos][pos]//p**v,-1,q)
  b[pos]=[(x*scale)%q for x in b[pos]]
  for i in range(pos+1,n):
   assert b[i][pos]%p**v==0
   t=b[i][pos]//p**v
   b[i]=[(x-t*y)%q for x,y in zip(b[i],b[pos])]
  for j in range(pos+1,n):
   assert b[pos][j]%p**v==0
   t=b[pos][j]//p**v
   for i in range(n):b[i][j]=(b[i][j]-t*b[i][pos])%q
  power+=k-v;pos+=1
 return power

def image_size(a,q):
 n=len(a);seen={(0,)*n}
 for col in zip(*a):
  if col==(0,)*n:continue
  multiples=[tuple(t*x%q for x in col) for t in range(q)]
  seen={tuple((x+y)%q for x,y in zip(v,w)) for v in seen for w in multiples}
 return len(seen)
def rank(a,p):
 if not a:return 0
 b=[list(r) for r in a];r=0
 for j in range(len(b[0])):
  i=next((i for i in range(r,len(b)) if b[i][j]%p),None)
  if i is None:continue
  b[r],b[i]=b[i],b[r];u=pow(b[r][j]%p,-1,p);b[r]=[x*u%p for x in b[r]]
  for i in range(r+1,len(b)):
   u=b[i][j];b[i]=[(x-u*y)%p for x,y in zip(b[i],b[r])]
  r+=1
  if r==len(b):break
 return r

def matrix(coeffs,par,q):
 n=len(coeffs[0]);return [[sum(t*a[i][j] for t,a in zip(par,coeffs))%q for j in range(n)] for i in range(n)]
def alternating(n,q,rng):
 a=[[0]*n for _ in range(n)]
 for i in range(n):
  for j in range(i+1,n):a[i][j]=rng.randrange(q);a[j][i]=-a[i][j]%q
 return a

def pencil(coeffs,p,k,independent=False):
 q=p**k;m=len(coeffs);values=[];compared=0
 for par in itertools.product(range(q),repeat=m):
  a=matrix(coeffs,par,q);v=image_log(a,p,k);assert v%2==0
  if independent:assert image_size(a,q)==p**v;compared+=1
  values.append((par,v//2))
 e=max(v for par,v in values);maxpars=[par for par,v in values if v==e]
 span=rank(maxpars,p)
 if e<p:assert span==m
 return {'p':p,'k':k,'matrix_size':len(coeffs[0]),'parameters':len(values),'max_e':e,'maximum_parameters':len(maxpars),'span_mod_p':span,'independent_images':compared}

def run():
 rng=random.Random(1812077);rows=[]
 for p,k,n,num,ind in [(2,1,4,12,True),(2,2,4,4,True),(3,1,4,12,True),(3,2,4,3,True),(5,1,6,12,False),(5,2,4,8,False),(7,1,8,12,False)]:
  for _ in range(num):rows.append(pencil([alternating(n,p**k,rng) for j in range(2)],p,k,ind))
 sharp=[]
 for p in [2,3,5,7]:
  a=[[[0]*(2*p) for i in range(2*p)] for _ in range(2)]
  for t in range(p):
   a[0][2*t][2*t+1]=-t%p;a[0][2*t+1][2*t]=t%p
   a[1][2*t][2*t+1]=1;a[1][2*t+1][2*t]=-1%p
  r=pencil(a,p,1,p<=3);assert r['max_e']==p and r['span_mod_p']==1 and r['maximum_parameters']==p-1
  sharp.append(r)
 # UT_5(F_5): all 5^6 derived-character parameters, beyond class two.
 p=5;n=5;roots=list(itertools.combinations(range(n),2));derived=[e for e in roots if e[1]-e[0]>=2]
 coeff=[]
 for root in derived:
  a=[[0]*len(roots) for _ in roots]
  for i,(u,v) in enumerate(roots):
   for j,(w,z) in enumerate(roots):
    a[i][j]=(int(v==w and (u,z)==root)-int(z==u and (w,v)==root))%p
  coeff.append(a)
 ut=pencil(coeff,p,1);assert ut['max_e']==4 and ut['span_mod_p']==6
 return {'random_pencils':rows,'sharp_threshold':sharp,'ut5_f5':ut,'scope':'Exact alternating matrices; no claim of general-group character parametrization'}
if __name__=='__main__':
 start=time.monotonic();out=run();(ROOT/'results/18.77-controls.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PASS_1877_CONTROLS',len(out['random_pencils']),'random pencils',sum(r['parameters'] for r in out['random_pencils'])+sum(r['parameters'] for r in out['sharp_threshold'])+out['ut5_f5']['parameters'],'parameter values',time.monotonic()-start,'seconds')
