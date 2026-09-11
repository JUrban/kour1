#!/usr/bin/env python3
"""Independent literal-permutation replay of the smaller 16.46 targets."""
from itertools import permutations
import json
from pathlib import Path
import time


def mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    out = [0]*len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def evaluate(word, images):
    out = tuple(range(len(images[0])))
    for a in word:
        out = mul(out, images[a-1] if a > 0 else inverse(images[-a-1]))
    return out


# Literal expanded relators, transcribed independently from page 101.
RELATORS = [(1,)*3, (2,)*3, (3,)*2, (4,)*2, (5,)*2, (6,)*2,
            (1, 3)*3, (1, 4)*3, (1, 5)*3, (1, 6)*3,
            (2, 3)*3, (2, 4)*3, (2, 5)*3, (2, 6)*3,
            (1, 2, -1, 3)*2, (1, 2, -1, 4)*2,
            (-1, 2, 1, 5)*2, (-1, 2, 1, 6)*2,
            (2, 1, -2, 3)*2, (-2, 1, 2, 4)*2,
            (2, 1, -2, 5)*2, (-2, 1, 2, 6)*2]


start = time.monotonic()
rows, literal_checks = [], 0
for n in [5, 6, 7]:
    one = tuple(range(n))
    all_perms = list(permutations(range(n)))
    threes = [p for p in all_perms if p != one and mul(mul(p, p), p) == one]
    twos = [p for p in all_perms if p != one and mul(p, p) == one and
            sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2 == 0]
    # Cycle types 3 and 3^2 exhaust order-three conjugacy classes for n<=7.
    # Neither splits in A_n: the 3 type has repeated fixed points; the
    # 3^2 type has repeated length-three cycles.
    representatives = []
    for k in range(1, n//3+1):
        p = list(one)
        for i in range(k):
            a = 3*i
            p[a:a+3] = [a+1, a+2, a]
        representatives.append(tuple(p))
    pairs, triples, slots, witnesses = 0, 0, 0, 0
    for a in representatives:
        for b in threes:
            pairs += 1
            counts = [0]*4
            for x in twos:
                images = [a, b, x, x, x, x]
                if evaluate(RELATORS[6], images) != one or evaluate(RELATORS[10], images) != one:
                    continue
                triples += 1
                values = [evaluate(r, images) == one for r in RELATORS]
                literal_checks += len(RELATORS)
                assert all(values[:14])
                for j in range(4):
                    counts[j] += values[14+j] and values[18+j]
            slots += sum(counts)
            witnesses += all(counts)
    order = len(all_perms)//2
    row = ['A'+str(n), order, len(representatives), len(threes), len(twos),
           pairs, triples, slots, witnesses, 0]
    assert witnesses == 0
    rows.append(row)

report = dict(status='PASS', rows=rows, literal_relator_checks=literal_checks,
              seconds=time.monotonic()-start)
Path('results/16.46-python.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
