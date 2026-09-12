#!/usr/bin/env python3
"""Exact coordinate controls of PF:2026.000002; GAP uses free relators."""
import json
import random


def check(p, n):
    m, s, q = p ** (n + 1), p ** n, 1 + p
    qinv = pow(q, -1, m)
    assert pow(q, s, m) == 1
    powers = [pow(qinv, j, m) for j in range(m)]

    def semimul(x, y):
        return ((x[0] + powers[x[1]] * y[0]) % m, (x[1] + y[1]) % m)

    def project(x):
        return ((x[0] + s * (x[1] // s)) % m, x[1] % s)

    def mul(x, y):
        carry, j = divmod(x[1] + y[1], s)
        return ((x[0] + powers[x[1]] * y[0] + s * carry) % m, j)

    def power(x, k):
        out = (0, 0)
        while k:
            if k & 1:
                out = mul(out, x)
            x = mul(x, x)
            k //= 2
        return out

    a, b = (1, 0), (0, 1)
    assert power(a, m) == power(b, m) == (0, 0)
    assert power(a, s) == power(b, s) == (s, 0)
    assert mul(mul(power(b, m - 1), a), b) == power(a, q)
    assert mul(mul(mul(power(a, m - 1), power(b, m - 1)), a), b) == power(a, p)
    assert {(k * s % m, -k * s % m) for k in range(p)} == {
        (i, j) for j in range(m) for i in [(-s * (j // s)) % m]
        if project((i, j)) == (0, 0)
    }
    for r in range(1, n + 2):
        x = power(a, p ** r)
        assert mul(mul(power(b, m - 1), x), b) == power(a, p ** r * q)

    rng = random.Random(17113 + 100 * p + n)
    if m <= 25:
        elements = [(i, j) for i in range(m) for j in range(m)]
        pairs = ((x, y) for x in elements for y in elements)
        mode = "all semidirect pairs"
    else:
        pairs = (((rng.randrange(m), rng.randrange(m)),
                  (rng.randrange(m), rng.randrange(m))) for _ in range(4000))
        mode = "4000 seeded pairs"
    count = 0
    for x, y in pairs:
        assert project(semimul(x, y)) == mul(project(x), project(y))
        count += 1
    for _ in range(1000):
        x, y, z = [(rng.randrange(m), rng.randrange(s)) for _ in range(3)]
        assert mul(mul(x, y), z) == mul(x, mul(y, z))
    return dict(p=p, n=n, size=m*s, nilpotency_class=n+1,
                abelian_invariants=[p, s], projection_pairs=count, coverage=mode,
                associativity_controls=1000)


if __name__ == "__main__":
    # GAP separately reaches n=6 for p<=7 and n=4 for p=11.
    rows = [check(p, n) for p in [2, 3, 5, 7, 11] for n in range(1, 4)]
    print(json.dumps(rows, indent=2))
    print("PASS_17113_COORDINATES cases=%d projection_pairs=%d associativity=%d" %
          (len(rows), sum(r["projection_pairs"] for r in rows), 1000 * len(rows)))
