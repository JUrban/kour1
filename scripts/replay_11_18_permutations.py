#!/usr/bin/env python3
"""Independent right-action permutation replay of the 2007 paper's examples."""
import json
from pathlib import Path


def mul(a, b):
    return tuple(b[i - 1] for i in a)


def inv(a):
    b = [0] * len(a)
    for i, j in enumerate(a, 1):
        b[j - 1] = i
    return tuple(b)


def perm(*cycles):
    a = list(range(1, 8))
    for cycle in cycles:
        for i, j in zip(cycle, cycle[1:] + cycle[:1]):
            a[i - 1] = j
    return tuple(a)


def comm(a, b):
    return mul(mul(mul(inv(a), inv(b)), a), b)


def orbit(a, b):
    seen, z, k = {}, a, 0
    while z not in seen:
        seen[z] = k
        z, k = comm(z, b), k + 1
        assert k <= 5040
    return {"transient": seen[z], "period": k - seen[z],
            "returns_to_start": seen[z] == 0}


def main():
    pairs = [(perm((1, 7, 2, 4, 5, 3, 6)), perm((1, 4, 3, 7, 6, 2, 5))),
             (perm((1, 2), (3, 4, 5, 6)), perm((2, 3), (4, 7, 5, 6))),
             (perm((1, 2, 3), (4, 5), (6, 7)), perm((1, 6, 5), (2, 7), (3, 4)))]
    result = []
    for i, (a, b) in enumerate(pairs, 1):
        for j, (x, y) in enumerate(((a, b), (inv(a), inv(b)), (inv(a), b), (a, inv(b)))):
            result.append({"pair": i, "variant": j,
                           "first": orbit(x, y), "second": orbit(y, x)})
    expected = json.loads(Path("results/11.18-permutation-conventions.json").read_text())
    assert result == expected
    for i, period in enumerate((49, 16, 18)):
        r = result[4 * i + 1]
        assert r["first"] == r["second"] == {
            "transient": 0, "period": period, "returns_to_start": True}
    print("PASS: 12 convention variants, 24 complete commutator orbits; translated periods 49,16,18")


if __name__ == "__main__":
    main()
