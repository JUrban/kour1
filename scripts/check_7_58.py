#!/usr/bin/env python3
"""Independent graph-path and finite nonabelian controls for the criterion."""
import itertools
import json
from collections import deque
from pathlib import Path


def red(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def inv(word):
    return tuple(-x for x in reversed(word))


def subst(word, images):
    return red(x for a in word for x in
               (images[a] if a > 0 else inv(images[-a])))


def graph_control(name, table, generators):
    n, rank = len(table), len(generators)
    unit = next(q for q in range(n) if table[q] == list(range(n)))
    edges = [(q, table[q][g]) for q in range(n) for g in generators]
    neighbours = [[] for _ in range(n)]
    for index, (u, v) in enumerate(edges, 1):
        neighbours[u].append((v, index))
        neighbours[v].append((u, -index))
    paths = {unit: ()}
    queue = deque([unit])
    tree = set()
    while queue:
        u = queue.popleft()
        for v, e in neighbours[u]:
            if v not in paths:
                paths[v] = paths[u] + (e,)
                tree.add(abs(e))
                queue.append(v)
    assert len(paths) == n
    rho = {e: red(paths[u] + (e,) + inv(paths[v]))
           for e, (u, v) in enumerate(edges, 1)}
    assert all(rho[e] == () for e in tree)
    assert all(subst(w, rho) == w for w in rho.values())
    beta = {e: (e,) if e in tree else red(inv(paths[u]) + (e,) + paths[v])
            for e, (u, v) in enumerate(edges, 1)}
    alpha = {e: (e,) if e in tree else rho[e] for e in rho}
    assert all(subst(alpha[e], beta) == (e,) for e in rho)
    assert all(subst(beta[e], alpha) == (e,) for e in rho)

    # Direct membership for the variety of all groups is determined by
    # whether the reduced edge word is a continuous path from the root.
    # This implementation uses endpoints, not the retraction criterion.
    def path_endpoint(word):
        q = unit
        for e in word:
            u, v = edges[abs(e)-1]
            if e < 0:
                u, v = v, u
            if q != u:
                return None
            q = v
        return q

    alphabet = tuple(range(1, len(edges)+1)) + tuple(range(-len(edges), 0))
    words = [()]
    frontier = [()]
    for _ in range(3):
        frontier = [w+(e,) for w in frontier for e in alphabet
                    if not w or w[-1] != -e]
        words.extend(frontier)
    passed = accepted = 0
    for word in words:
        projected = subst(word, rho)
        endpoint = path_endpoint(word)
        for q in range(n):
            criterion = projected == red(word + inv(paths[q]))
            assert criterion == (endpoint == q), (name, word, q)
            accepted += criterion
            passed += 1
    return {'name': name, 'quotient_order': n, 'free_rank': rank,
            'edge_count': len(edges), 'word_length_bound': 3,
            'reduced_edge_words': len(words), 'membership_checks': passed,
            'accepted_pairs': accepted, 'basis_inverse_checks': 2*len(edges)}


def matrix_control():
    # B=UT(3,3), the relatively free class-two exponent-three group on
    # the two edges of the directed Cayley cycle for Q=C2 and rank F=1.
    p = 3
    def mul(a, b):
        return ((a[0]+b[0]) % p, (a[1]+b[1]) % p,
                (a[2]+b[2]+a[0]*b[1]) % p)
    def swap(a):
        return (a[1], a[0], (a[0]*a[1]-a[2]) % p)
    zero, x, y = (0,0,0), (1,0,0), (0,1,0)
    elems = list(itertools.product(range(p), repeat=3))
    for a, b, c in itertools.product(elems, repeat=3):
        assert mul(mul(a,b),c) == mul(a,mul(b,c))
    assert mul(x,y) != mul(y,x)
    for a, b in itertools.product(elems, repeat=2):
        assert swap(mul(a,b)) == mul(swap(a),swap(b))
    assert all(swap(swap(a)) == a for a in elems)
    assert all(mul(mul(a,a),a) == zero for a in elems)
    assert swap(x) == y and swap(y) == x
    d = mul(x,y)
    powers_d = [zero, d, mul(d,d)]
    # rho(x)=1, rho(y)=xy; the commutator maps to 1.
    rho = lambda a: powers_d[a[1]]
    assert all(rho(rho(a)) == rho(a) for a in elems)
    for a, b in itertools.product(elems, repeat=2):
        assert rho(mul(a,b)) == mul(rho(a),rho(b))
    def wmul(a, b):
        return (mul(a[0],swap(b[0]) if a[1] else b[0]), (a[1]+b[1]) % 2)
    ambient = list(itertools.product(elems, range(2)))
    generator = (x,1)
    identity = (zero,0)
    subgroup = {identity}
    cur = wmul(identity,generator)
    while cur != identity:
        assert cur not in subgroup
        subgroup.add(cur)
        cur = wmul(cur,generator)
    assert len(subgroup) == 6
    accepted = {a for a in ambient
                if mul(rho(a[0]), x if a[1] else zero) == a[0]}
    assert accepted == subgroup
    return {'base': 'UT(3,3)', 'base_order': 27, 'ambient_order': 54,
            'image_order': 6, 'membership_checks': 54,
            'base_associativity_triples': 27**3,
            'action_and_retraction_products': 2*27**2}


def run_controls():
    cyclic = lambda n: [[(i+j) % n for j in range(n)] for i in range(n)]
    permutations = list(itertools.permutations(range(3)))
    compose = lambda a,b: tuple(a[b[i]] for i in range(3))
    s3 = [[permutations.index(compose(a,b)) for b in permutations]
          for a in permutations]
    cases = [('trivial_two_loops', cyclic(1), [0,0]),
             ('C2_loop', cyclic(2), [1,0]),
             ('C2_parallel', cyclic(2), [1,1]),
             ('C3_cycle', cyclic(3), [1]),
             ('S3', s3, [permutations.index((1,0,2)),
                         permutations.index((1,2,0))])]
    return {'status': 'PASS_758_CONTROLS',
              'scope': 'Bounded free-edge words and complete nonabelian finite model; not a novelty certificate.',
              'graph_cases': [graph_control(*case) for case in cases],
              'matrix_case': matrix_control()}


def main():
    output = run_controls()
    path = Path(__file__).resolve().parents[1] / 'results/7.58-controls.json'
    path.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
