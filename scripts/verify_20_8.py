#!/usr/bin/env python3
"""Exact word reductions and all vertex quotients for the 20.8 example."""
from collections import deque


def inverse(w):
    return tuple(-a for a in reversed(w))


def reduced(w):
    result = []
    for a in w:
        if result and result[-1] == -a:
            result.pop()
        else:
            result.append(a)
    return tuple(result)


def substitute(w, images):
    return reduced(a for x in w for a in
                   (images[x] if x > 0 else inverse(images[-x])))


def fold(n, edges, partition=None):
    parent = list(range(n))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    if partition:
        first = {}
        for i, k in enumerate(partition):
            if k in first:
                parent[root(i)] = root(first[k])
            else:
                first[k] = i
    directed = edges + [(v, -a, u) for u, a, v in edges]
    while True:
        transitions = {}
        changed = False
        for u, a, v in directed:
            key, end = (root(u), a), root(v)
            if key in transitions and root(transitions[key]) != end:
                parent[end] = root(transitions[key])
                changed = True
                break
            transitions[key] = end
        if not changed:
            break
    transitions = {(root(u), a): root(v) for u, a, v in directed}
    base = root(0)
    vertices = set(u for u, _ in transitions) | {base}
    # Remove nonbased hanging trees, preserving a possible based stem.
    while True:
        leaf = next((v for v in vertices if v != base and
                     sum(u == v for u, _ in transitions) <= 1), None)
        if leaf is None:
            break
        transitions = {(u,a):v for (u,a),v in transitions.items()
                       if u != leaf and v != leaf}
        vertices.remove(leaf)
    rename = {base: 0}
    queue = deque([base])
    result = []
    while queue:
        u = queue.popleft()
        for a, v in sorted((a,v) for (w,a),v in transitions.items() if w == u):
            if v not in rename:
                rename[v] = len(rename)
                queue.append(v)
            result.append((rename[u],a,rename[v]))
    assert len(rename) == len(vertices)
    assert len(result) % 2 == 0
    return tuple(sorted(result)), len(vertices), len(result)//2


def from_words(words):
    n, edges = 1, []
    for word in words:
        u = 0
        for i, a in enumerate(reduced(word)):
            if i == len(reduced(word))-1:
                v = 0
            else:
                v, n = n, n+1
            edges.append((u,a,v))
            u = v
    return fold(n, edges)


def partitions(n):
    def extend(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
        else:
            for k in range(max(prefix, default=-1)+2):
                yield from extend(prefix+[k])
    yield from extend([])


def main():
    # Domain generators t,x,y = 1,2,3; target generators a,b = 1,2.
    u = (-1,2)*2
    v = (-1,-1,2,2)*2
    g, h = {1:(1,),2:u,3:v}, {1:(2,),2:u,3:v}
    words = [(2,), (1,2,-1), (3,), (1,1,3,-1,-1)]
    assert all(substitute(w,g) == substitute(w,h) for w in words)
    assert g[1] != h[1]
    for label, generators, rank in [
        ('g_image',list(g.values()),3), ('h_image',list(h.values()),3),
        ('K_domain',words,4), ('K_image',[substitute(w,g) for w in words],4)]:
        _, vertices, edges = from_words(generators)
        assert edges-vertices+1 == rank
        print(f'PASS {label} vertices={vertices} edges={edges} rank={rank}')

    edges = [(0,1,1),(1,1,2),(0,2,0),(1,2,1),(0,3,0),(2,3,2)]
    assert from_words(words) == fold(3, edges)
    ranks = []
    distinct = set()
    for partition in partitions(3):
        graph, vertices, n_edges = fold(3, edges, partition)
        rank = n_edges-vertices+1
        ranks.append(rank)
        distinct.add(graph)
        if rank < 4:
            assert vertices == 1 and n_edges == 3
            assert graph == tuple((0,a,0) for a in [-3,-2,-1,1,2,3])
        print(f'QUOTIENT partition={partition} vertices={vertices} edges={n_edges} rank={rank}')
    assert sorted(ranks) == [3,3,3,4,4] and len(distinct) == 3
    print('PASS partitions=5 distinct_folded_quotients=3 fixed_generators=4')


if __name__ == '__main__':
    main()
