#!/usr/bin/env python3
"""Exact, deterministic arithmetic controls for the PSL_6(5^a) family."""
import hashlib
import json
from math import gcd, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def valuation(n, p):
    assert n > 0 and p > 1
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def polynomial(q, modulus):
    # Horner evaluation, independent of the geometric quotient below.
    s = 1
    for _ in range(4):
        s = (s*q + 1) % modulus
    return (s*q - 1) % modulus


def run():
    a, root = 1, 5
    lifts = []
    for k in range(3, 513):
        m = 1 << k
        q = pow(5, a, 2*m)
        assert 0 < a < (1 << (k-2)) and a % 2 == 1
        assert q % m == root and polynomial(q, m) == 0
        shift = 1 << (k-2)
        assert pow(5, shift, 2*m) == 1+m
        q_other = pow(5, a+shift, 2*m)
        assert (q_other-q) % (2*m) == m
        residues = [polynomial(t, 2*m) for t in (q, q_other)]
        assert sorted(residues) == [0, m]
        b = a if residues[0] == m else a+shift
        assert polynomial(pow(5, b, 2*m), 2*m) == m
        lifts.append({'k':k, 'a':a, 'exact_exponent':b, 'root':root})
        a = a if residues[0] == 0 else a+shift
        # Lift in q directly using a sum of powers, rather than in a.
        direct = (sum(root**i for i in range(1, 6))-1) % (2*m)
        assert direct in (0, m)
        root = root if direct == 0 else root+m
        assert pow(5, a, 2*m) == root

    exact = []
    for a in (1,3,5,9,17,49,113,625):
        q = 5**a
        degree = (q**6-1)//(q-1)-2
        # Count ordered independent columns of GL, then divide by
        # determinant image and scalar centre; different order formula.
        gl_order = prod(q**6-q**i for i in range(6))
        divisor = (q-1)*gcd(6,q-1)
        assert gl_order % divisor == 0
        group_order = gl_order//divisor
        assert valuation(group_order,2) == 13
        assert gcd(6,q-1) == 2 and q % 8 == 5
        assert degree == sum(q**i for i in range(1,6))-1
        assert 2*(q**5-1) > degree > 0
        exact.append({'a':a, 'q_bits':q.bit_length(),
                      'degree_v2':valuation(degree,2),
                      'group_order_v2':valuation(group_order,2),
                      'degree_bits':degree.bit_length(),
                      'degree_hex_sha256':hashlib.sha256(hex(degree).encode()).hexdigest(),
                      'order_hex_sha256':hashlib.sha256(hex(group_order).encode()).hexdigest()})
    assert exact[-1]['degree_v2'] == 16

    # Exhaustive independent small residues test uniqueness and every
    # exact valuation, without using the recurrence to generate a.
    exhaustive = []
    for k in range(3,17):
        m = 1 << k
        roots = [x for x in range(5,m,8)
                 if (sum(pow(x,i,m) for i in range(1,6))-1) % m == 0]
        assert roots == [lifts[k-3]['root']]
        exponents = [b for b in range(1,1 << (k-1),2)
                     if (sum(pow(pow(5,b,2*m),i,2*m) for i in range(1,6))-1) % (2*m) == m]
        assert exponents == [lifts[k-3]['exact_exponent']]
        exhaustive.append({'k':k,'root':roots[0],'exact_exponent':exponents[0],
                           'root_candidates':m//8,'exponent_candidates':1 << (k-2)})
    return {'status':'PASS', 'lifts':lifts, 'exact_integer_cases':exact,
            'exhaustive':exhaustive}


if __name__ == '__main__':
    data = run()
    (ROOT/'results/12.40-arithmetic.json').write_text(json.dumps(data,indent=2)+'\n')
    print('PASS_1240_ARITHMETIC 510 lifts; 8 exact integer orders and degrees; '
          '14 exhaustive residue and exponent controls')
