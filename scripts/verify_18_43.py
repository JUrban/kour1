#!/usr/bin/env python3
"""Independent small enumeration checks and exact trace-polynomial certificates."""
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path
import subprocess

P = 2**31 - 1
DIAGONALS = [(3, 5, 7), (11, 13, 17)]
BS = [((2, 3, 5), (7, 11, 13), (17, 19, 23)),
      ((29, 31, 37), (41, 43, 47), (53, 59, 61))]


def multiply(a, b, modulus=None):
    d = len(a)
    out = [[sum(a[i][k] * b[k][j] for k in range(d)) for j in range(d)]
           for i in range(d)]
    return [[x % modulus for x in row] for row in out] if modulus else out


def trace_word(word, a, b, modulus=None):
    d = len(a)
    m = [[int(i == j) for j in range(d)] for i in range(d)]
    for letter in word:
        m = multiply(m, a if letter == 'a' else b, modulus)
    out = sum(m[i][i] for i in range(d))
    return out % modulus if modulus else out


def fingerprint(word, dimension):
    vals = []
    for ds, b in zip(DIAGONALS, BS):
        a = [[ds[i] if i == j else 0 for j in range(dimension)]
             for i in range(dimension)]
        b = [row[:dimension] for row in b[:dimension]]
        vals.append(trace_word(word, a, b, P))
    return (vals[0] << 31) | vals[1]


def canonical(word):
    return min(word[i:] + word[:i] for i in range(len(word)))


def trace_polynomial(word, dimension=3):
    """Counter of monomials for diagonal A and generic B, over the integers.

    Exponent keys list the D diagonal-A variables followed by D^2 directed
    B-entry variables in row-major order. No numerical specialization occurs.
    """
    if 'b' not in word:
        out = Counter()
        for i in range(dimension):
            exps = [0] * (dimension + dimension**2)
            exps[i] = len(word)
            out[tuple(exps)] += 1
        return out
    last_b = word.index('b')
    rotated = word[last_b + 1:] + word[:last_b + 1]
    runs = [len(s) for s in rotated.split('b')[:-1]]
    m = len(runs)
    out = Counter()
    for colors in product(range(dimension), repeat=m):
        exps = [0] * (dimension + dimension**2)
        for i, run in enumerate(runs):
            source = colors[i]
            target = colors[(i + 1) % m]
            exps[source] += run
            exps[dimension + source * dimension + target] += 1
        out[tuple(exps)] += 1
    return out


def controls():
    total = 0
    for d in (2, 3):
        for n in range(1, 13):
            text = subprocess.check_output(['bin/search_18_43', str(n), str(d), 'dump'], text=True)
            rows = [line.split()[1:] for line in text.splitlines() if line.startswith('FINGERPRINT ')]
            cpp = {w: int(key) for w, key in rows}
            brute = {canonical(''.join(bits)) for bits in product('ab', repeat=n)}
            assert len(rows) == len(cpp) == len(brute)
            assert set(cpp) == brute
            for w, key in cpp.items():
                assert key == fingerprint(w, d), (d, n, w)
            total += len(cpp)
    # A known GL2 trace identity and its GL3 distinction.
    u, v = 'aababb', 'aabbab'
    assert canonical(u) != canonical(v)
    assert trace_polynomial(u, 2) == trace_polynomial(v, 2)
    assert trace_polynomial(u, 3) != trace_polynomial(v, 3)
    assert fingerprint(u, 3) != fingerprint(v, 3)
    dets = []
    for b in BS:
        det = sum((-1 if perm in ((0, 2, 1), (1, 0, 2), (2, 1, 0)) else 1)
                  * b[0][perm[0]] * b[1][perm[1]] * b[2][perm[2]]
                  for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)))
        assert det % P
        dets.append(det)
    print(json.dumps({'result': 'PASS', 'necklace_evaluations': total,
                      'dimensions': [2, 3], 'lengths': [1, 12],
                      'B_determinants': dets,
                      'known_GL2_identity': [u, v], 'same_pair_GL3_identity': False}))


def certify(u, v, dimension, output):
    assert u and v and set(u + v) <= {'a', 'b'}
    assert canonical(u) != canonical(v), 'Words are conjugate by cyclic rotation.'
    # This swap leaves the identity question unchanged and reduces expansion size.
    if u.count('b') > u.count('a'):
        trans = str.maketrans('ab', 'ba')
        u, v = u.translate(trans), v.translate(trans)
    left, right = trace_polynomial(u, dimension), trace_polynomial(v, dimension)
    result = {'u': u, 'v': v, 'dimension': dimension,
              'left_monomials': len(left), 'right_monomials': len(right),
              'polynomial_identity': left == right,
              'nonconjugate': canonical(u) != canonical(v)}
    if output:
        data = dict(result)
        data['left_terms'] = [[list(k), v] for k, v in sorted(left.items())]
        data['right_terms'] = [[list(k), v] for k, v in sorted(right.items())]
        Path(output).write_text(json.dumps(data, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('words', nargs='*')
    parser.add_argument('--dimension', type=int, choices=(2, 3), default=3)
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.words:
        if len(args.words) != 2:
            parser.error('Supply exactly two words, or no words for controls.')
        certify(*args.words, args.dimension, args.output)
    else:
        controls()
