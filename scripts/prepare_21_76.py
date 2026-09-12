#!/usr/bin/env python3
"""Exact F9 enumeration and a 40-coset certificate for Notebook 21.76."""
import argparse
import json
from collections import deque
from pathlib import Path


def add(x, y):
    return (x % 3 + y % 3) % 3 + 3 * ((x // 3 + y // 3) % 3)


def mul(x, y):
    a, b, c, d = x % 3, x // 3, y % 3, y // 3
    return (a * c + 2 * b * d) % 3 + 3 * ((a * d + b * c) % 3)


def mm(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (add(mul(a, e), mul(b, g)), add(mul(a, f), mul(b, h)),
            add(mul(c, e), mul(d, g)), add(mul(c, f), mul(d, h)))


I = (1, 0, 0, 1)
U = (1, 1, 0, 1)


def enumerate_group(beta):
    generators = (U, (1, 0, beta, 1))
    words = {I: ''}
    queue = deque([I])
    while queue:
        a = queue.popleft()
        for letter, b in zip('UV', generators):
            c = mm(a, b)
            if c not in words:
                words[c] = words[a] + letter
                queue.append(c)
    return words


def generate():
    pilot = []
    for beta in range(1, 9):
        group = enumerate_group(beta)
        pilot.append(dict(beta=beta, order=len(group),
                          upper=[a for a in range(9) if (1, a, 0, 1) in group],
                          lower=[a for a in range(9) if (1, 0, a, 1) in group]))
    words = enumerate_group(3)
    powers = (I, U, mm(U, U))
    cosets = {min(mm(p, g) for p in powers) for g in words}
    identity_coset = min(powers)
    representatives = [I] + sorted(cosets - {identity_coset})
    lookup = {mm(p, r): (i, e) for i, r in enumerate(representatives)
              for e, p in enumerate(powers)}
    rows = []
    for r in representatives:
        rows.append(dict(matrix=r, word=words[r],
                         U=lookup[mm(r, U)], V=lookup[mm(r, (1, 0, 3, 1))]))
    return dict(encoding='a+3b means a+b*j, j^2=2, a,b in {0,1,2}',
                addition=[[add(a, b) for b in range(9)] for a in range(9)],
                multiplication=[[mul(a, b) for b in range(9)] for a in range(9)],
                generators=[U, (1, 0, 3, 1)],
                elements=[dict(matrix=g, word=words[g]) for g in sorted(words)],
                cosets=rows, pilot=pilot,
                upper=[0, 1, 2], lower=[0, 3, 6], obstruction=[1, 3, 1, 3])


def render(certificate):
    lines = ['# Problem 21.76: explicit finite certificate', '',
             'An entry `a+3b` denotes `a+b*j` in F9, where j^2=2.',
             'Each matrix tuple lists its entries by rows. Let U=(1,1,0,1)',
             'and V=(1,0,3,1). Row i gives r_i and, in the last two columns,',
             '(k,e) such that r_i U=U^e r_k or r_i V=U^e r_k.',
             'All 120 matrices U^e r_i (0<=e<3, 0<=i<40) are distinct.',
             'Thus their union is preserved by right multiplication by U,V.',
             'It contains the identity, so it contains the generated group.',
             'The words in the JSON certificate prove every r_i is generated,',
             'giving equality and order 120.', '',
             '| i | r_i | U transition (k,e) | V transition (k,e) |',
             '|---:|---|---|---|']
    for i, row in enumerate(certificate['cosets']):
        lines.append(f"| {i} | {tuple(row['matrix'])} | {tuple(row['U'])} | {tuple(row['V'])} |")
    lines += ['', 'Every entry can be checked by ordinary 2-by-2 multiplication',
              'with j^2=2 and arithmetic modulo three. The independent checker',
              'instead uses 4-by-4 matrices over F3, checks every product of',
              'the 120 matrices, and checks all listed words and transitions.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results/21.76-certificate.json')
    parser.add_argument('--table', default='research/21.76-finite-table.md')
    args = parser.parse_args()
    certificate = generate()
    Path(args.output).write_text(json.dumps(certificate, indent=2) + '\n')
    Path(args.table).write_text(render(certificate))
    print('PASS_2176_PREPARATION elements=%d cosets=%d' %
          (len(certificate['elements']), len(certificate['cosets'])))


if __name__ == '__main__':
    main()
