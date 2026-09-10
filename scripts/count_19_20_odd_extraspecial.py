#!/usr/bin/env python3
"""Exact formulas for E_(p,m) x C_p^r, p odd, E of exponent p.

See research/19.20-odd-extraspecial.md for derivations and limitations.
"""
from collections import Counter
from fractions import Fraction
from math import isqrt, prod
import json


def exact_div(a, b):
    q, rem = divmod(a, b)
    assert rem == 0
    return q


def gl(n, p):
    return prod(p**n-p**i for i in range(n))


def sp(m, p):
    return p**(m*m)*prod(p**(2*i)-1 for i in range(1, m+1))


def gaussian(n, d, p):
    if not 0 <= d <= n:
        return 0
    return exact_div(prod(p**n-p**i for i in range(d)), gl(d, p))


def isotropic(m, d, p):
    if not 0 <= d <= m:
        return 0
    return exact_div(prod(p**(2*(m-i))-1 for i in range(d)),
                     prod(p**(d-i)-1 for i in range(d)))


def aut_order(t, s, p):
    if t == 0:
        return gl(s, p)
    return p**(2*t+s+2*t*s)*gl(s, p)*(p-1)*sp(t, p)


def count(p, m, r):
    assert p % 2 and m >= 1 and r >= 0
    assert all(p % d for d in range(2, isqrt(p)+1))
    k = 2*m+r
    ends = p**((r+1)*k)*(sum(isotropic(m, t, p)*
                            prod(p**k-p**i for i in range(t))
                            for t in range(m+1))+(p-1)*sp(m, p))
    types = Counter()
    projection_count = Counter()
    for d in range(2*m+1):
        for t in range(d//2+1):
            z = d-2*t
            if z > m or t > m-z:
                continue
            nw = isotropic(m, z, p)*exact_div(sp(m-z, p), sp(t, p)*sp(m-z-t, p))
            projection_count[d] += nw
            for a in range(r+1):
                base = nw*gaussian(r, a, p)*p**(d*(r-a))
                if t == 0:
                    types[(0, d+a+1)] += base
                    types[(0, d+a)] += base*p**(d+a)
                else:
                    types[(t, d+a-2*t)] += base
    # Independent total for all subspaces of each dimension in the symplectic space.
    assert all(projection_count[d] == gaussian(2*m, d, p) for d in range(2*m+1))
    partials = sum(n*n*aut_order(t, s, p) for (t, s), n in types.items())
    return dict(p=p, m=m, r=r, order=p**(2*m+1+r), ends=ends, partials=partials,
                ratio=str(Fraction(ends, partials)), total_subgroups=sum(types.values()),
                types=[dict(extraspecial_half_rank=t, central_extra_rank=s,
                            subgroup_count=n, aut_order=aut_order(t, s, p))
                       for (t, s), n in sorted(types.items())])


if __name__ == '__main__':
    rows = [count(p, m, r) for p in (3, 5, 7) for m in range(1, 5) for r in range(5)]
    print(json.dumps(dict(status='FORMULAS_EVALUATED',
                         equality_hits=[x for x in rows if x['ends'] == x['partials']],
                         cases=rows), indent=2))
