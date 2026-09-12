#!/usr/bin/env python3
"""Replay the finite algebra model using coefficient convolution over word cuts.

This imports no arithmetic from its producer. Reachability and closure certify
the generated group; the universal associativity proof is in the report.
"""
import argparse
from copy import deepcopy
from itertools import permutations, product
import json
from pathlib import Path


def check(packet):
    assert packet['p'] == 3
    basis = [()] + [w for k in range(1, 4)
                    for w in permutations(range(3), k)]
    assert packet['basis'] == [list(w) for w in basis]
    index = {w: i for i, w in enumerate(basis)}
    cuts = [[(index[w[:k]], index[w[k:]]) for k in range(len(w)+1)]
            for w in basis]

    def mul(a, b):
        return tuple(sum(a[i]*b[j] for i, j in splits) % 3 for splits in cuts)

    one = (1,) + (0,)*15
    generators = [tuple(int(j == 0 or w == (i,)) for j, w in enumerate(basis))
                  for i in range(3)]
    rows = packet['elements']
    assert len(rows) == 6561 == packet['order']
    assert all(len(row) == 16 and row[0] == 1 and
               all(type(x) is int and 0 <= x < 3 for x in row) for row in rows)
    elements = {tuple(row) for row in rows}
    assert len(elements) == 6561 and one in elements
    assert len(packet['words']) == 6561
    edges, witnesses, noncubes, cyclic_images = 0, 0, 0, 0
    cosets = {}
    for row, word in zip(rows, packet['words']):
        assert type(word) is str and all(c in '012' for c in word)
        g = tuple(row)
        value = one
        for digit in word:
            value = mul(value, generators[int(digit)])
        assert value == g
        witnesses += 1
        for s in generators:
            assert mul(g, s) in elements
            edges += 1
        cube = mul(mul(g, g), g)
        coefficient = g[1]*g[2]*g[3] % 3
        expected = tuple(1 if j == 0 else coefficient if len(w) == 3 else 0
                         for j, w in enumerate(basis))
        assert cube == expected
        noncubes += cube != one
        v = g[1:4]
        cosets[v] = cosets.get(v, 0) + 1
        rotated = tuple(g[index[tuple((i-1) % 3 for i in w)]] for w in basis)
        assert rotated in elements
        cyclic_images += 1
    assert set(cosets) == set(product(range(3), repeat=3))
    assert set(cosets.values()) == {243}
    assert packet['kernel_order'] == cosets[(0, 0, 0)] == 243
    assert packet['hyperplane_order'] == 2187
    assert noncubes == packet['noncubes'] == 1944
    return dict(elements=6561, witnesses=witnesses, generator_edges=edges,
                cubes=6561, cyclic_images=cyclic_images, noncubes=noncubes,
                kernel_order=243, hyperplane_order=2187)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model', nargs='?',
                        default='results/17.118-three-generator-model.json')
    args = parser.parse_args()
    packet = json.loads(Path(args.model).read_text())
    result = check(packet)
    controls = []
    for mode in ['basis', 'coefficient', 'duplicate', 'witness', 'summary']:
        bad = deepcopy(packet)
        if mode == 'basis':
            bad['basis'][1] = [2]
        elif mode == 'coefficient':
            bad['elements'][100][5] = (bad['elements'][100][5]+1) % 3
        elif mode == 'duplicate':
            bad['elements'][100] = list(bad['elements'][101])
        elif mode == 'witness':
            bad['words'][100] += '0'
        else:
            bad['noncubes'] += 1
        try:
            check(bad)
        except AssertionError:
            controls.append(mode)
        else:
            raise AssertionError('accepted corruption: '+mode)
    result['rejected_mutations'] = controls
    print(json.dumps(result, sort_keys=True))
    print('PASS_17118_MODEL elements=6561 generator_edges=19683 mutations=5')


if __name__ == '__main__':
    main()
