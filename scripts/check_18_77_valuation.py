#!/usr/bin/env python3
"""A nontrivial divided-Pfaffian family over Z/25, with exact image controls."""
import json,itertools
from pathlib import Path
from check_18_77 import matrix,image_log,image_size
ROOT=Path(__file__).resolve().parents[1]
def pf(a):return a[0][1]*a[2][3]-a[0][2]*a[1][3]+a[0][3]*a[1][2]
def run():
 p=5;k=2;q=25
 a=[[0,1,0,0],[-1,0,0,0],[0,0,0,5],[0,0,-5,0]]
 b=[[0,1,1,0],[-1,0,0,0],[-1,0,0,0],[0,0,0,0]]
 # Homogeneous polynomial Pf(x A+y B)=5x^2+5xy.
 coeff=[pf(a),pf([[a[i][j]+b[i][j] for j in range(4)] for i in range(4)])-pf(a)-pf(b),pf(b)]
 assert coeff==[5,5,0] and any(x%5 for row in a+b for x in row)
 vals=[]
 for x,y in itertools.product(range(q),repeat=2):
  lift=[[x*a[i][j]+y*b[i][j] for j in range(4)] for i in range(4)]
  assert pf(lift)==5*x*x+5*x*y
  e=image_log(matrix([a,b],[x,y],q),p,k)//2;assert e<=3
  if x*(x+y)%5:assert e==3
  vals.append(e)
 for par in [(1,0),(0,1),(1,1),(1,4)]:
  m=matrix([a,b],par,q);assert image_size(m,q)==p**image_log(m,p,k)
 return {'p':p,'k':k,'parameters':q*q,'pfaffian_coefficients':coeff,'max_e':max(vals),'maximum_parameters':vals.count(3),'independent_images':4,'nondivisible_matrix_entries':True}
if __name__=='__main__':
 out=run();(ROOT/'results/18.77-valuation-controls.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS_1877_VALUATION',json.dumps(out))
