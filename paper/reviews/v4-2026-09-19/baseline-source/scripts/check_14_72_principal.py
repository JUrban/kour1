#!/usr/bin/env python3
"""Exact supplemental ideal checks for the post-review 14.72 restriction.

Requires SymPy. This checks polynomial/ideal statements, not a formal proof
of smoothness, invariant-ring completeness, or the Notebook interpretation.
The manuscript proves those geometric assertions separately.
"""
import json
from pathlib import Path
from sympy import I, symbols, groebner, expand
PAPER=Path(__file__).resolve().parents[1]
x,y,u,v,t=symbols('x y u v t')
f=y-(1+I)*x
relations=[y*y-x**3+x,y*u-x*v,(x*x-1)*u-y*v,t*(x*x+1)-1]
G=groebner(relations+[f],x,y,u,v,t,extension=I)
assert all(G.reduce(q)[1]==0 for q in [x,y,u])
H=groebner(relations+[x,y,u],x,y,u,v,t,extension=I)
assert H.reduce(f)[1]==0
assert list(H)==[x,y,u,t-1],list(H)
base=groebner(relations,x,y,u,v,t,extension=I)
assert base.reduce(f*(y+(1+I)*x)-x*(x-I)**2)[1]==0
# Unit inverse and invariance of the localization parameter.
assert base.reduce((x-I)*(x+I)*t-1)[1]==0
sigma={x:-x,y:I*y,u:I*u,v:v,t:t}
assert all(base.reduce(q.subs(sigma,simultaneous=True))[1]==0 for q in relations)
assert expand((x*x+1).subs(sigma,simultaneous=True)-(x*x+1))==0
# The retained quotient point is on its hypersurface, outside the deleted locus,
# and has zero gradient (a hypersurface in three-space).
a,d=symbols('a d');q=v*v-(a-1)*d;point={a:1,v:0,d:0}
assert q.subs(point)==0 and (a+1).subs(point)!=0
assert all(q.diff(z).subs(point)==0 for z in [a,v,d])
result={'status':'PASS','coefficient_field':'Q(i)','fixed_ideal_groebner_basis':[str(g) for g in H],
 'checks':['ideal (f) equals (x,y,u) in the localized coordinate ring','fixed quotient is Q(i)[v]','factorization and unit inverse','surface relations and localization preserved by sigma','quotient point (1,0,0) survives and has zero gradient'],
 'scope':'Supplemental exact algebra; the geometric proof and invariant-ring completeness remain in the manuscript.'}
print(json.dumps(result,indent=2))
(PAPER/'reviews/revision-2026-09-17/principal-divisor-check.json').write_text(json.dumps(result,indent=2)+'\n')
