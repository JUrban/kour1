#!/usr/bin/env python3
"""Exact quaternion, group-algebra, and module controls for 21.60."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


# E=Q[w]/(w^2+w+1), written as pairs.
def emul(x, y):
    a,b=x; c,d=y
    return (a*c-b*d, a*d+b*c-b*d)


def econj(x):
    a,b=x
    return (a-b,-b)


def eadd(x,y):
    return tuple(a+b for a,b in zip(x,y))


def eneg(x):
    return tuple(-a for a in x)


def qmul(x,y):
    u,v=x[:2],x[2:]; s,t=y[:2],y[2:]
    return eadd(emul(u,s),eneg(emul(v,econj(t))))+eadd(emul(u,t),emul(v,econj(s)))


def qconj(x):
    return econj(x[:2])+eneg(x[2:])


def qpower(x,n):
    result=(1,0,0,0)
    for _ in range(n):
        result=qmul(result,x)
    return result


one=(1,0,0,0); w=(0,1,0,0); j=(0,0,1,0)
basis=[one,w,j,qmul(w,j)]
assert qpower(w,3)==one and qpower(j,2)==(-1,0,0,0) and qpower(j,4)==one
assert qmul(j,w)==qmul(qpower(w,2),j)
for x,y,z in product(basis,repeat=3):
    assert qmul(qmul(x,y),z)==qmul(x,qmul(y,z))
norm_checks=0
for x in product(range(-4,5),repeat=4):
    a,b,c,d=x; norm=a*a-a*b+b*b+c*c-c*d+d*d
    assert qmul(x,qconj(x))==(norm,0,0,0)
    assert (norm>0)==any(x)
    if norm:
        assert qmul(x,tuple(F(t,norm) for t in qconj(x)))==one
    norm_checks+=1

# G=C3:C4, including all products and a faithful quaternion realization.
group=list(product(range(3),range(4)))
index={g:i for i,g in enumerate(group)}
def gmul(g,h):
    a,b=g; c,d=h
    return ((a+(-1)**b*c)%3,(b+d)%4)


quat=[qmul(qpower(w,a),qpower(j,b)) for a,b in group]
assert len(set(quat))==12
for s,t in product(range(12),repeat=2):
    assert qmul(quat[s],quat[t])==quat[index[gmul(group[s],group[t])]]


def mmul(x,y):
    a,b,c,d=x; e,f,g,h=y
    return ((a*e+b*g)%2,(a*f+b*h)%2,(c*e+d*g)%2,(c*f+d*h)%2)


I=(1,0,0,1); A=(0,1,1,1); B=(1,1,0,1)
mbasis=[I,A,B,mmul(A,B)]
def madd(*matrices):
    return tuple(sum(t)%2 for t in zip(*matrices)) if matrices else (0,0,0,0)


def reduction(x):
    return madd(*(m for a,m in zip(x,mbasis) if int(a)%2))


residues=list(product(range(2),repeat=4))
assert len({reduction(x) for x in residues})==16
for x,y in product(residues,repeat=2):
    assert reduction(qmul(x,y))==mmul(reduction(x),reduction(y))
lift=(0,1,0,1)
assert tuple(a+b+c for a,b,c in zip(qmul(lift,lift),lift,(2,0,0,0)))==(0,0,0,0)
assert reduction(lift)==(0,0,0,1)

# F2G as twelve-bit vectors, with independent convolution multiplication.
table=[[index[gmul(g,h)] for h in group] for g in group]
def amul(x,y):
    result=0
    for s in range(12):
        if x>>s&1:
            for t in range(12):
                if y>>t&1:
                    result ^= 1<<table[s][t]
    return result


def bits_basis(vectors):
    rows={}
    for row in vectors:
        while row:
            p=row.bit_length()-1
            if p in rows:
                row ^= rows[p]
            else:
                rows[p]=row
                break
    return list(rows.values())


def matrix_bits(m):
    return sum(x<<i for i,x in enumerate(m))


images=[matrix_bits(reduction(q)) for q in quat]
def semisimple_image(x):
    value=x.bit_count()%2
    for i in range(12):
        if x>>i&1:
            value ^= images[i]<<1
    return value


all_elements=range(1<<12)
kernel=[x for x in all_elements if semisimple_image(x)==0]
radical=bits_basis(kernel)
assert len(kernel)==128 and len(radical)==7
radical_dimensions=[]
current=radical
for k in range(1,5):
    radical_dimensions.append(len(current))
    current=bits_basis(amul(x,y) for x in current for y in radical)
assert radical_dimensions==[7,2,1,0]
assert len({semisimple_image(x) for x in all_elements})==32

idempotents=[x for x in all_elements if amul(x,x)==x]
assert len(idempotents)==52
matrix_idempotents={semisimple_image(x)>>1 for x in idempotents}
assert len(matrix_idempotents)==8

aid=1<<index[(1,0)]; bid=1<<index[(0,1)]; unity=1<<index[(0,0)]
aa=amul(aid,aid); zz=amul(bid,bid)
e=unity^aid^aa; complement=unity^e
f=amul(complement,aid^amul(aid,bid)^unity^zz)
assert amul(e,e)==e and amul(f,f)==f and amul(e,f)==amul(f,e)==0
assert semisimple_image(e)==1 and semisimple_image(f)==matrix_bits((0,0,0,1))<<1
modules=[]
for name,idem,factors in [('trivial_cover',e,[4,0]),('two_dimensional_cover',f,[0,2])]:
    left=bits_basis(amul(1<<i,idem) for i in range(12))
    corner=bits_basis(amul(amul(idem,1<<i),idem) for i in range(12))
    corner_radical=bits_basis(amul(amul(idem,r),idem) for r in radical)
    assert len(left)==4 and len(corner)-len(corner_radical)==1
    modules.append({'module':name,'dimension':len(left),'corner_dimension':len(corner),
                    'corner_radical_dimension':len(corner_radical),
                    'composition_factors_1_and_2':factors})
assert len(bits_basis(amul(e,1<<i) for i in range(12)))==4
assert amul(e,f)==0

result={'status':'PASS','group_order':12,'quaternion_basis_associativity_checks':64,
        'positive_norm_and_inverse_controls':norm_checks,'faithful_group_product_checks':144,
        'quaternion_reduction_product_checks':256,'group_algebra_elements':4096,
        'group_algebra_idempotents':len(idempotents),'matrix_quotient_idempotents':8,
        'semisimple_quotient_dimension':5,'radical_power_dimensions':radical_dimensions,
        'projective_indecomposable_controls':modules,
        'explicit_nonliftable_idempotent_coefficients':
            [group[i] for i in range(12) if f>>i&1],
        'note':'No finite test establishes division over Q; the positive norm formula in the proof does.'}
Path('results/21.60-python-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
