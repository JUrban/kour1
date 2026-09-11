#!/usr/bin/env python3
"""Exact rational coordinates for the explicit Z[t]-group in 13.42."""
from fractions import Fraction as Q

L_ONE = (Q(0),)*5
H_ONE = (L_ONE,{})


def lmul(x,y):
    a,b,c,d,e=x
    A,B,C,D,E=y
    s=a*B-b*A
    return (a+A,b+B,c+C+s*Q(1,2),
            d+D+(a*C-c*A)*Q(1,2)+s*(a-A)*Q(1,12),
            e+E+(b*C-c*B)*Q(1,2)+s*(b-B)*Q(1,12))


def linv(x):
    return tuple(-a for a in x)


def vadd(v,w):
    out=dict(v)
    for q,a in w.items():
        out[q]=out.get(q,Q(0))+a
        if not out[q]: del out[q]
    return out


def vscale(v,a):
    return {q:a*b for q,b in v.items() if a*b}


def shift(v,a):
    return {q+a:b for q,b in v.items()}


def hmul(g,h):
    l,v=g
    m,w=h
    return lmul(l,m),vadd(shift(v,m[1]),w)


def hinv(g):
    l,v=g
    return linv(l),vscale(shift(v,-l[1]),-1)


def hpow(g,n):
    assert isinstance(n,int)
    if n<0: return hpow(hinv(g),-n)
    out=H_ONE
    while n:
        if n%2: out=hmul(out,g)
        g=hmul(g,g)
        n//=2
    return out


def conj(g,h):
    return hmul(hmul(hinv(h),g),h)


def comm(g,h):
    return hmul(hinv(g),conj(g,h))


def F(l):
    a,b,c,_,_=l
    return {c/a:a} if not b and a else {}


def f(g):
    return L_ONE,F(g[0])


def exponent(g,p):
    """p is a full tuple of integral polynomial coefficients, low degree first."""
    a=p[0] if p else 0
    b=p[1] if len(p)>1 else 0
    return hmul(hpow(g,a),(L_ONE,vscale(F(g[0]),b)))


def padd(p,q):
    return tuple((p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0)
                 for i in range(max(len(p),len(q))))


def pmul(p,q):
    out=[0]*max(0,len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return tuple(out)
