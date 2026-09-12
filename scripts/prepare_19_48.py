#!/usr/bin/env python3
"""Retain every prefix of a nine-factor counterexample word."""
import argparse
import json
from pathlib import Path
from prepare_21_76 import I, U, mm


def generate():
    V = (1, 0, 4, 1)
    generators = dict(U=U, u=mm(U, U), V=V, v=mm(V, V))
    word = 'VUVuVUvuv'
    prefixes = [I]
    for letter in word:
        prefixes.append(mm(prefixes[-1], generators[letter]))
    assert prefixes[-1] == (1, 5, 0, 1)
    return dict(encoding='a+3b means a+b*j over F3, j^2=2',
                generators=generators, word=word, prefixes=prefixes,
                witness_parameter=5, original_upper_constants=[0, 1, 2],
                beta=4, scope='An exact word, with no group enumeration needed.')


def render(c):
    lines = ['# Problem 19.48: explicit matrix word', '',
             'Encode a+bj as a+3b, with j^2=2 and a,b in {0,1,2}.',
             'U=(1,1,0,1), V=(1,0,4,1); lowercase letters denote inverses.',
             'Read the word VUVuVUvuv from left to right. Each tuple gives',
             'the four entries of the prefix matrix by rows.', '',
             '| Prefix | Matrix |', '|---|---|']
    for i, row in enumerate(c['prefixes']):
        lines.append(f"| {c['word'][:i] or 'identity'} | {tuple(row)} |")
    lines += ['', 'The final matrix is I+(2+j)E12. Its parameter is outside F3.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results/19.48-word.json')
    parser.add_argument('--table', default='research/19.48-word-table.md')
    args = parser.parse_args()
    c = generate()
    Path(args.output).write_text(json.dumps(c, indent=2)+'\n')
    Path(args.table).write_text(render(c))
    print('PASS_1948_PREPARATION factors=9 upper_parameter=2+j')
