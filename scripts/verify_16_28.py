#!/usr/bin/env python3
"""Independent finite matrix and tagged-word controls for Kourovka 16.28.

These checks do not prove Zariski density or nonclosedness. The universal
argument is in research/16.28-proof.md, over algebraically closed fields.
"""

from itertools import product
from pathlib import Path
import datetime
import hashlib
import json


def mul(a, b, p):
    return ((a[0]*b[0]+a[1]*b[2]) % p,
            (a[0]*b[1]+a[1]*b[3]) % p,
            (a[2]*b[0]+a[3]*b[2]) % p,
            (a[2]*b[1]+a[3]*b[3]) % p)


def det(a, p):
    return (a[0]*a[3]-a[1]*a[2]) % p


def trace(a, p):
    return (a[0]+a[3]) % p


def inverse(a, p):
    assert det(a, p) == 1
    return a[3], -a[1] % p, -a[2] % p, a[0]


def main():
    ident = (1, 0, 0, 1)
    fields = []
    for p in [5, 7, 11, 13]:
        group = [a for a in product(range(p), repeat=4) if det(a, p) == 1]
        y = {a for a in group if trace(a, p) == 1}
        y2 = {mul(a, b, p) for a in y for b in y}
        assert len(group) == p*(p*p-1)
        minus_i = (p-1, 0, 0, p-1)
        assert minus_i not in y2
        assert {inverse(a, p) for a in y} == y
        parameters = 0
        for s in range(1, p-1):
            u = s*pow(1+s, -1, p) % p
            w = (u*(1-u)-1) % p
            a = u, 1, w, (1-u) % p
            d = s, 0, 0, pow(s, -1, p)
            b = mul(inverse(a, p), d, p)
            assert a in y and b in y
            assert mul(a, b, p) == d
            parameters += 1
        fields.append({'prime': p, 'group_order': len(group),
                       'trace_one_set_size': len(y),
                       'all_square_products_checked': len(y)**2,
                       'finite_square_size': len(y2),
                       'diagonal_factorizations': parameters,
                       'minus_identity_absent': True})

    # A finite matrix base with an unbounded integer tag models the
    # central scalar coordinate t^j. Multiply words directly and compare
    # every tag fiber with the corresponding number of Y factors.
    p = 5
    group = [a for a in product(range(p), repeat=4) if det(a, p) == 1]
    y = {a for a in group if trace(a, p) == 1}
    y_powers = [{ident}]
    x = {(a, 0) for a in y} | {(ident, 1)}
    x_power = {(ident, 0)}
    tagged_rows = []
    for n in range(1, 13):
        y_powers.append({mul(a, b, p) for a in y_powers[-1] for b in y})
        x_power = {(mul(a, b, p), j+k) for a, j in x_power for b, k in x}
        expected = {(a, n-k) for k in range(n+1) for a in y_powers[k]}
        assert x_power == expected
        if n >= 2:
            fiber = {a for a, j in x_power if j == n-2}
            assert fiber == y_powers[2]
            assert (p-1, 0, 0, p-1) not in fiber
        tagged_rows.append({'power': n, 'tagged_product_size': len(x_power)})

    result = {
        'status': 'PASS',
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'finite_fields': fields,
        'tagged_product_controls': tagged_rows,
        'limitation': 'Finite arithmetic and exact word checks only; no inference of Zariski density from a finite field.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    Path('results/16.28-independent-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
