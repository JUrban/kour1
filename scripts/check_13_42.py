#!/usr/bin/env python3
"""Symbolic all-coordinate BCH check and exact controls on the A-group axioms."""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import json
import random

from model_13_42 import (L_ONE,H_ONE,lmul,linv,vadd,vscale,shift,hmul,hinv,
                         hpow,conj,comm,F,f,exponent,padd,pmul)

ROOT=Path(__file__).resolve().parents[1]


class Poly:
    """Sparse commutative polynomials over Q, for ten generic coordinates."""
    def __init__(self,value=0):
        if isinstance(value,Poly):self.d=value.d
        elif isinstance(value,dict):self.d={m:Q(c) for m,c in value.items() if c}
        else:self.d={():Q(value)} if value else {}

    def __add__(self,other):
        out=dict(self.d)
        for m,c in Poly(other).d.items():out[m]=out.get(m,Q(0))+c
        return Poly(out)
    __radd__=__add__

    def __neg__(self):return Poly({m:-c for m,c in self.d.items()})
    def __sub__(self,other):return self+-Poly(other)
    def __rsub__(self,other):return Poly(other)+-self

    def __mul__(self,other):
        out={}
        for m,c in self.d.items():
            for n,d in Poly(other).d.items():
                key=tuple(sorted(m+n))
                out[key]=out.get(key,Q(0))+c*d
        return Poly(out)
    __rmul__=__mul__

    def __bool__(self):return bool(self.d)
    def __eq__(self,other):return self.d==Poly(other).d


def aa(a,b):
    out=dict(a)
    for w,c in b.items():out[w]=out.get(w,Poly())+c
    return {w:c for w,c in out.items() if c}


def am(a,b):
    out={}
    for w,c in a.items():
        for v,d in b.items():
            if len(w+v)<=3:out[w+v]=out.get(w+v,Poly())+c*d
    return {w:c for w,c in out.items() if c}


def asc(a,r):return {w:r*c for w,c in a.items() if r*c}


def lie(coords):
    a,b,c,d,e=map(Poly,coords)
    return {w:v for w,v in {'x':a,'y':b,'xy':c,'yx':-c,
            'xxy':d,'xyx':-2*d,'yxx':d,
            'yxy':2*e,'yyx':-e,'xyy':-e}.items() if v}


def aexp(a):
    a2=am(a,a)
    return aa({'':Poly(1)},aa(a,aa(asc(a2,Q(1,2)),asc(am(a2,a),Q(1,6)))))


def symbolic_check():
    z=[Poly({(i,):1}) for i in range(10)]
    lhs=am(aexp(lie(z[:5])),aexp(lie(z[5:])))
    rhs=aexp(lie(lmul(z[:5],z[5:])))
    words=['']+[''.join(t) for n in (1,2,3) for t in product('xy',repeat=n)]
    for w in words:assert lhs.get(w,Poly())==rhs.get(w,Poly()),w
    # Generic reverse-product subtraction verifies the commuting criterion.
    xy=lmul(z[:5],z[5:]);yx=lmul(z[5:],z[:5])
    a,b,c,_,_=z[:5];A,B,C,_,_=z[5:]
    assert [u-v for u,v in zip(xy,yx)]==[Poly(),Poly(),a*B-b*A,a*C-c*A,b*C-c*B]
    inverse=[-u for u in z[:5]]
    assert lmul(z[:5],inverse)==(Poly(),)*5
    conjugate=lmul(lmul(tuple(-u for u in z[5:]),z[:5]),z[5:])
    assert conjugate[:3]==(a,b,c+a*B-b*A)
    return {'generic_coordinates':10,'truncated_words':len(words),
            'nonzero_product_coefficients':sum(len(c.d) for c in lhs.values()),
            'product_difference_zero':True,'commuting_criterion':True,
            'inverse':True,'conjugacy_coordinates':True}


def run():
    symbolic=symbolic_check()
    rng=random.Random(1342)
    def qrand():return Q(rng.randint(-3,3),rng.randint(1,3))
    def lrand():return tuple(qrand() for _ in range(5))
    def vrand():
        out={}
        for _ in range(3):out=vadd(out,{qrand():qrand()})
        return out
    def hrand():return lrand(),vrand()
    polys=[(),(0,),(1,),(-1,),(0,1),(0,0,1),
           (2,-1,3),(-2,3,-1,2),(1,0,5),(-1,-2,0,1)]
    points=[]
    for _ in range(60):points.append(hrand())
    # Exercise the nonzero and zero branches, inverses, and nonintegral exponents.
    for a,c in product((-2,-1,1,2),(Q(-3,2),Q(0),Q(2,3))):
        points.append(((Q(a),Q(0),c,Q(1,3),Q(-1,2)),vrand()))
    points += [H_ONE,((Q(0),Q(0),Q(1),Q(0),Q(0)),{}),
               ((Q(0),Q(0),Q(0),Q(1),Q(0)),{})]
    checks={'inverse':0,'associativity':0,'f_power_compatibility':0,
            'conjugation':0,'addition':0,'multiplication':0,
            'commuting_products':0,'commuting_pairs':0}
    for g in points:
        assert hmul(g,hinv(g))==hmul(hinv(g),g)==H_ONE
        assert exponent(g,(1,))==g and exponent(g,())==H_ONE
        assert comm(g,f(g))==H_ONE and f(f(g))==H_ONE
        checks['inverse']+=1
        for n,m in product(range(-2,3),repeat=2):
            assert f(hmul(hpow(g,n),hpow(f(g),m)))==hpow(f(g),n)
            checks['f_power_compatibility']+=1
        for p,q in product(polys,repeat=2):
            assert exponent(g,padd(p,q))==hmul(exponent(g,p),exponent(g,q))
            assert exponent(exponent(g,p),q)==exponent(g,pmul(p,q))
            checks['addition']+=1;checks['multiplication']+=1
        h,k=hrand(),hrand()
        assert hmul(hmul(g,h),k)==hmul(g,hmul(h,k))
        assert f(conj(g,h))==conj(f(g),h)
        checks['associativity']+=1
        for p in polys:
            assert exponent(conj(g,h),p)==conj(exponent(g,p),h)
            checks['conjugation']+=1

    commuting=[]
    for g in points:
        for n in (-2,0,2):commuting.append((g,hpow(g,n)))
        commuting.append((g,f(g)))
        # Central L coordinates commute with every H element.
        commuting.append((g,((Q(0),Q(0),Q(0),qrand(),qrand()),{})))
    # Same projective triple with different central coordinates: not only powers.
    for _ in range(100):
        l=lrand();scalar=qrand()
        m=tuple(scalar*x for x in l[:3])+(qrand(),qrand())
        commuting.append(((l,{}),(m,{})))
    # Arbitrary normal-module elements commute, including differing supports.
    for _ in range(50):commuting.append(((L_ONE,vrand()),(L_ONE,vrand())))
    for g,h in commuting:
        assert comm(g,h)==H_ONE
        assert f(hmul(g,h))==hmul(f(g),f(h))
        checks['commuting_pairs']+=1
        for p in polys:
            assert exponent(hmul(g,h),p)==hmul(exponent(g,p),exponent(h,p))
            checks['commuting_products']+=1
    x=((Q(1),Q(0),Q(0),Q(0),Q(0)),{})
    y=((Q(0),Q(1),Q(0),Q(0),Q(0)),{})
    u=exponent(x,(0,1))
    assert u==(L_ONE,{Q(0):Q(1)})
    witnesses=[]
    for n in range(1,65):
        u=comm(u,y)
        expected={Q(i):Q((-1)**(n-i)*comb(n,i)) for i in range(n+1)}
        assert u==(L_ONE,expected) and u!=H_ONE
        witnesses.append({'length':n+1,'support':n+1,'top_coefficient':1,
                          'constant_coefficient':(-1)**n})
    # The original subgroup is nilpotent; its nonzero triple commutators
    # distinguish the class-three starting point from the class-two boundary.
    triple=comm(comm(x,y),x)
    assert triple!=H_ONE and comm(triple,x)==comm(triple,y)==H_ONE
    return {'status':'PASS','symbolic':symbolic,'points':len(points),
            'polynomials':len(polys),'checks':checks,'witnesses':witnesses,
            'source_class_three':True}


if __name__=='__main__':
    data=run()
    (ROOT/'results/13.42-controls.json').write_text(json.dumps(data,indent=2)+'\n')
    print('PASS_1342_CONTROLS',json.dumps({k:v for k,v in data.items() if k!='witnesses'},sort_keys=True))
