#!/usr/bin/env python3
"""Finite-field basis checks of the parameterized holomorph construction."""
from itertools import product


def order(a, p):
    v = a % p
    n = 1
    while v != 1:
        v = v*a % p
        n += 1
    return n


total = 0
for p, q, r, d in [(11,5,2,2), (29,7,3,3), (53,13,2,6), (103,17,3,8)]:
    assert order(r, q) == 2*d
    z = next(z for z in range(2, p) if order(z, p) == p-1)
    lam = pow(z, (p-1)//q, p)
    assert order(lam, p) == q
    s = [pow(r, i, q) for i in range(d)]
    assert [u for u in range(1,q) if {u*x % q for x in s} == set(s)] == [1]

    def theta(v):
        x, k = v
        return (x[1:]+(pow(lam,-k % q,p)*x[0] % p,), r*k % q)

    def theta_inv(v):
        x, k = v
        oldk = pow(r,-1,q)*k % q
        return ((pow(lam,oldk,p)*x[-1] % p,)+x[:-1], oldk)

    def hol(v, par):
        x, k = v
        abc, j = par
        return (tuple((a*x[i]+b+c*pow(lam,s[i]*k % q,p)) % p
                      for i,(a,b,c) in enumerate(abc)), (k+j) % q)

    def conjugate_par(par):
        abc, j = par
        a,b,c = abc[0]
        v = pow(lam,-j % q,p)
        return (abc[1:]+[(v*a % p,v*c % p,v*b % p)], r*j % q)

    identity_abc = [(1,0,0)]*d
    generators = [(identity_abc,1)]
    for i in range(d):
        for triple in [(z,0,0),(1,1,0),(1,0,1)]:
            abc = list(identity_abc)
            abc[i] = triple
            generators.append((abc,0))
    basis = [tuple(0 for _ in range(d))]
    basis += [tuple(int(i==j) for i in range(d)) for j in range(d)]
    count = 0
    for x,k in product(basis,range(q)):
        v = (x,k)
        assert theta_inv(theta(v)) == v
        for par in generators:
            assert theta(hol(theta_inv(v),par)) == hol(v,conjugate_par(par))
            count += 1
        w = v
        for _ in range(d):
            w = theta(w)
        assert w == (tuple(pow(lam,-s[i]*k % q,p)*x[i] % p for i in range(d)), -k % q)
        for _ in range(d):
            w = theta(w)
        assert w == v
    total += count
    print(f'FAMILY p={p} q={q} r={r} d={d} coset_order={2*d} basis_checks={count} PASS')
print(f'DONE families=4 basis_checks={total} PASS')
