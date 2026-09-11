#!/usr/bin/env python3
"""Enumerate a normal closure by coordinate permutations; certify reachability."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'software/coset-python'))
import numpy as np


def enumerate_derived(data, cap=4096):
    n, m = data['n'], data['pair_orbits']
    assert 1 <= n <= 256 and cap >= 1
    table = (np.asarray(data['table'], dtype=np.int64) - 1).astype(np.uint8)
    inverse = (np.asarray(data['inverse'], dtype=np.int64) - 1).astype(np.uint8)
    reps = (np.asarray(data['representatives'], dtype=np.int64) - 1).astype(np.uint8)
    x, y = reps[:, 0], reps[:, 1]
    comm = table[table[table[inverse[x], inverse[y]], x], y]
    values = np.arange(n, dtype=np.int64)[None, :]
    moves = np.stack([
        table[values, comm[:, None]],
        table[table[inverse[x, None], values], x[:, None]],
        table[table[inverse[y, None], values], y[:, None]],
    ])
    assert moves.shape == (3, m, n)
    assert all(sorted(row.tolist()) == list(range(n))
               for perm in moves for row in perm)
    root = bytes([data['identity']-1])*m
    nodes, seen, parents = [root], {root: 0}, [[-1, -1]]
    coordinates = np.arange(m)
    cursor = 0
    complete = True
    while cursor < len(nodes):
        vector = np.frombuffer(nodes[cursor], dtype=np.uint8)
        for move in range(3):
            child = moves[move, coordinates, vector].tobytes()
            if child not in seen:
                seen[child] = len(nodes)
                nodes.append(child)
                parents.append([cursor, move])
                if len(nodes) > cap:
                    complete = False
                    break
        if not complete:
            break
        cursor += 1
    return {'status': 'COMPLETE' if complete else 'CAP_EXCEEDED',
            'cap': cap, 'node_count': len(nodes),
            'vectors_hex': [v.hex() for v in nodes], 'parents': parents,
            'moves': ['right_multiply_commutator', 'conjugate_x', 'conjugate_y']}


def verify_certificate(data, certificate):
    """Scalar replay, independently of the NumPy transition implementation."""
    table, inverse = data['table'], data['inverse']
    m, n = data['pair_orbits'], data['n']
    identity = data['identity']-1
    vectors = [bytes.fromhex(v) for v in certificate['vectors_hex']]
    assert len(vectors) == certificate['node_count']
    assert len(set(vectors)) == len(vectors)
    assert all(len(v) == m and all(a < n for a in v) for v in vectors)
    assert vectors[0] == bytes([identity])*m
    parents = certificate['parents']
    assert len(parents) == len(vectors) and parents[0] == [-1, -1]
    assert certificate['moves'] == [
        'right_multiply_commutator', 'conjugate_x', 'conjugate_y']

    def mul(a, b):
        return table[a][b]-1

    def inv(a):
        return inverse[a]-1

    xy = [(a-1, b-1) for a, b in data['representatives']]

    def transition(vector, move):
        out = []
        for d, (x, y) in zip(vector, xy):
            if move == 0:
                c = mul(mul(mul(inv(x), inv(y)), x), y)
                out.append(mul(d, c))
            elif move == 1:
                out.append(mul(mul(inv(x), d), x))
            elif move == 2:
                out.append(mul(mul(inv(y), d), y))
            else:
                raise AssertionError('invalid move')
        return bytes(out)

    for i in range(1, len(vectors)):
        parent, move = parents[i]
        assert 0 <= parent < i and 0 <= move < 3
        assert transition(vectors[parent], move) == vectors[i]
    edge_checks = 0
    if certificate['status'] == 'COMPLETE':
        assert len(vectors) <= certificate['cap']
        nodes = set(vectors)
        for v in vectors:
            for move in range(3):
                assert transition(v, move) in nodes
                edge_checks += 1
    else:
        assert certificate['status'] == 'CAP_EXCEEDED'
        assert len(vectors) == certificate['cap']+1
    return {'status': 'PASS_VECTOR_CERTIFICATE', 'nodes': len(vectors),
            'reachability_checks': len(vectors)-1, 'closure_edge_checks': edge_checks,
            'complete': certificate['status'] == 'COMPLETE'}


def normalized_export(data, certificate):
    assert certificate['status'] == 'COMPLETE'
    table = data['table']
    values = []
    for vector in certificate['vectors_hex']:
        row = []
        for d, (x, y) in zip(bytes.fromhex(vector), data['representatives']):
            xy = table[x-1][y-1]
            row.append(table[xy-1][d])
        values.append(row)
    out = dict(data)
    out.update(status='EXPORTED', word_functions=values,
               normalized_count=len(values), cap=certificate['cap'],
               function_group_order=data['exponent']**2*len(values),
               function_group_order_source='axis-restriction proof and certified derived order')
    return out
