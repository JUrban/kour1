#!/usr/bin/env python3
"""Check the certificate using only ordinary matrices over the prime field."""
import argparse
import copy
import json
from pathlib import Path


def mm(x, y):
    n = len(x)
    return tuple(tuple(sum(x[i][k] * y[k][j] for k in range(n)) % 3
                       for j in range(n)) for i in range(n))


def identity(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def scalar(x):
    assert type(x) is int and 0 <= x < 9
    a, b = x % 3, x // 3
    return ((a, 2 * b % 3), (b, a))


def block(m):
    assert len(m) == 4
    parts = [scalar(x) for x in m]
    return tuple(tuple(parts[2 * (i // 2) + j // 2][i % 2][j % 2]
                       for j in range(4)) for i in range(4))


def verify(c):
    for a in range(9):
        for b in range(9):
            s = tuple(tuple((scalar(a)[i][j] + scalar(b)[i][j]) % 3
                            for j in range(2)) for i in range(2))
            assert scalar(c['addition'][a][b]) == s
            assert scalar(c['multiplication'][a][b]) == mm(scalar(a), scalar(b))
    assert mm(scalar(3), scalar(3)) == scalar(2)
    assert len({scalar(x) for x in range(9)}) == 9
    for x in range(1, 9):
        assert sum(mm(scalar(x), scalar(y)) == identity(2) for y in range(9)) == 1

    assert c['generators'] == [[1, 1, 0, 1], [1, 0, 3, 1]]
    U, V = map(block, c['generators'])
    I = identity(4)
    assert mm(mm(U, U), U) == I and U != I
    assert mm(mm(V, V), V) == I and V != I
    elements = [block(row['matrix']) for row in c['elements']]
    S = set(elements)
    assert len(elements) == len(S) == 120 and I in S and U in S and V in S
    for row, g in zip(c['elements'], elements):
        w = I
        assert set(row['word']) <= set('UV')
        for letter in row['word']:
            w = mm(w, dict(U=U, V=V)[letter])
        assert w == g
        assert all(mm(g, h) in S for h in S)
        assert sum(mm(g, h) == I and mm(h, g) == I for h in S) == 1
    assert c['upper'] == [a for a in range(9) if block([1, a, 0, 1]) in S] == [0, 1, 2]
    assert c['lower'] == [a for a in range(9) if block([1, 0, a, 1]) in S] == [0, 3, 6]
    assert c['obstruction'] == [1, 3, 1, 3]
    assert mm(mm(scalar(1), scalar(3)), scalar(1)) == scalar(3)
    assert 3 not in c['upper']

    rows = c['cosets']
    assert len(rows) == 40 and block(rows[0]['matrix']) == I
    representatives = [block(row['matrix']) for row in rows]
    powers = [I, U, mm(U, U)]
    generated = [mm(p, r) for r in representatives for p in powers]
    assert len(set(generated)) == 120 and set(generated) == S
    for row, r in zip(rows, representatives):
        word = I
        for letter in row['word']:
            assert letter in 'UV'
            word = mm(word, dict(U=U, V=V)[letter])
        assert word == r
        for name, g in [('U', U), ('V', V)]:
            k, e = row[name]
            assert type(k) is int and type(e) is int and 0 <= k < 40 and 0 <= e < 3
            assert mm(r, g) == mm(powers[e], representatives[k])
    expected_orders = [24, 24, 120, 720, 720, 120, 720, 720]
    for beta, row in enumerate(c['pilot'], 1):
        assert row['beta'] == beta and row['order'] == expected_orders[beta - 1]
    assert len(c['pilot']) == 8
    return dict(elements=120, products=14400, inverses=120, words=160,
                cosets=40, transitions=80, field_operations=162,
                upper=c['upper'], lower=c['lower'])


def run():
    c = json.loads(Path('results/21.76-certificate.json').read_text())
    result = verify(c)
    mutations = []
    d = copy.deepcopy(c); d['elements'].pop(); mutations.append(d)
    d = copy.deepcopy(c); d['multiplication'][3][3] = 1; mutations.append(d)
    d = copy.deepcopy(c); d['elements'][0]['word'] += 'U'; mutations.append(d)
    d = copy.deepcopy(c); d['cosets'][0]['V'][1] = (d['cosets'][0]['V'][1] + 1) % 3; mutations.append(d)
    d = copy.deepcopy(c); d['upper'].append(3); mutations.append(d)
    d = copy.deepcopy(c); d['lower'] = [0, 1, 2]; mutations.append(d)
    d = copy.deepcopy(c); d['obstruction'][3] = 1; mutations.append(d)
    for d in mutations:
        try:
            verify(d)
        except AssertionError:
            pass
        else:
            raise AssertionError('accepted a corrupted certificate')
    result['mutations_rejected'] = len(mutations)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results/21.76-controls.json')
    args = parser.parse_args()
    result = run()
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print('PASS_2176_CONTROLS', json.dumps(result, sort_keys=True))
