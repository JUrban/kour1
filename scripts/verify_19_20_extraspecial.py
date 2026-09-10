#!/usr/bin/env python3
"""Independent exact counts for E_32^+ x C_2, using binary coordinates.

No GAP, SmallGrp identifiers, or subgroup/automorphism library is used.
All subgroups are enumerated; nonabelian types and automorphism orders are
computed by exhaustive isometries of their quadratic quotient spaces.
"""
import itertools
import json
from collections import deque


def cocycle(a, b):
    return ((a & 1) * ((b >> 1) & 1)) ^ (((a >> 2) & 1) * ((b >> 3) & 1))


def q(v):
    return cocycle(v, v)


def polar(a, b):
    return cocycle(a, b) ^ cocycle(b, a)


def mul(a, b):
    return a ^ b ^ (cocycle(a, b) << 4)


def lift(v):
    """F_2^5 = G/<z>; the fifth bit is the extra central involution."""
    return (v & 15) | ((v & 16) << 1)


def subspaces(d):
    zero = frozenset([0])
    seen, queue = {zero}, deque([zero])
    while queue:
        U = queue.popleft()
        for v in range(1, 1 << d):
            if v not in U:
                W = U | frozenset(u ^ v for u in U)
                if W not in seen:
                    seen.add(W)
                    queue.append(W)
    return sorted(seen, key=lambda U: (len(U), sorted(U)))


def basis(U):
    result, span = [], {0}
    for v in sorted(U):
        if v not in span:
            result.append(v)
            span |= {u ^ v for u in span}
    assert span == set(U)
    return result


def isometries(U, W, first_only=False):
    """Count all linear bijections preserving q, by basis images."""
    if len(U) != len(W):
        return 0
    b = basis(U)
    options = [[w for w in W if w and q(w) == q(v)] for v in b]
    total = 0

    def rec(images, span):
        nonlocal total
        k = len(images)
        if k == len(b):
            total += 1
            return first_only
        for w in options[k]:
            if w not in span and all(polar(w, images[j]) == polar(b[k], b[j])
                                     for j in range(k)):
                if rec(images+[w], span | {u ^ w for u in span}):
                    return True
        return False

    rec([], {0})
    return total


def gl(d):
    out = 1
    for i in range(d):
        out *= (1 << d) - (1 << i)
    return out


spaces5 = subspaces(5)
assert len(spaces5) == 374
subgroups = set()
for U in spaces5:
    # All subgroups containing the derived subgroup <z>.
    subgroups.add(frozenset(lift(v) ^ z for v in U for z in [0, 16]))
    # A subgroup avoiding z must be elementary abelian. Its quotient
    # image U is totally singular, and it is one of the 2^dim(U) complements.
    if all(q(v) == 0 for v in U):
        b = basis(U)
        for choices in itertools.product([0, 16], repeat=len(b)):
            H = {0}
            for v, z in zip(b, choices):
                g = lift(v) ^ z
                H |= {mul(h, g) for h in H}
            assert len(H) == len(U) and 16 not in H
            subgroups.add(frozenset(H))

types = []
closure_pairs = 0
for H in sorted(subgroups, key=lambda H: (len(H), sorted(H))):
    for a in H:
        for b in H:
            assert mul(a, b) in H
            closure_pairs += 1
    involutions = sum(mul(a, a) == 0 for a in H)
    center = [a for a in H if all(mul(a, b) == mul(b, a) for b in H)]
    signature = (len(H), len(center), involutions)
    abelian = len(center) == len(H)
    U = frozenset((a & 15) | ((a & 32) >> 1) for a in H)
    chosen = None
    for row in types:
        if tuple(row['signature']) == signature:
            if abelian or isometries(U, row['_U'], first_only=True):
                chosen = row
                break
    if chosen is None:
        if abelian:
            if involutions == len(H):
                rank = len(H).bit_length()-1
                aut = gl(rank)
                desc = f'C2^{rank}'
            else:
                # Every square in G is 1 or z, so at most one C4 factor.
                rank = len(H).bit_length()-3
                assert involutions == len(H)//2
                aut = (1 << (2*rank+1))*gl(rank)
                desc = f'C4 x C2^{rank}'
        else:
            assert 16 in H
            iso_count = isometries(U, U)
            # The derived subgroup is characteristic of order 2; every
            # quadratic isometry lifts in 2^dim(U) independent ways.
            aut = len(U)*iso_count
            desc = 'nonabelian quadratic type'
        chosen = {'signature': signature, 'description': desc,
                  'subgroups': 0, 'aut_order': aut, '_U': U}
        types.append(chosen)
    chosen['subgroups'] += 1

partials = sum(row['subgroups']**2*row['aut_order'] for row in types)

# Independent endomorphism count from a presentation with generators
# x1,y1,x2,y2,c, all involutions, [xi,yi]=z, all other commutators trivial.
# The image of z is either 1 or z.
singular = [v for v in range(16) if q(v) == 0]
commuting_tuples = sum(
    all(polar(v[i], v[j]) == 0 for i in range(5) for j in range(i))
    for v in itertools.product(singular, repeat=5))
orthogonal_order = isometries(frozenset(range(16)), frozenset(range(16)))
assert commuting_tuples == 5860 and orthogonal_order == 72
# If z maps to 1, all five images commute and are involutions; each vector
# image has four independent choices of the two central coordinates.
kill_derived = commuting_tuples * 4**5
# If z maps to z, the first four vector images form an isometry; their
# central coordinates have 4^4 choices, and c has four central images.
preserve_derived = orthogonal_order * 4**4 * 4
ends = kill_derived + preserve_derived
assert ends == 6074368 and partials == 3277312 and ends > partials

for row in types:
    del row['_U']
print(json.dumps({
    'status': 'PASS', 'group': 'extraspecial plus group of order 32 times C2',
    'order': 64, 'quotient_subspaces_enumerated': len(spaces5),
    'all_subgroups': len(subgroups), 'subgroup_types': len(types),
    'subgroup_closure_pairs': closure_pairs,
    'endomorphisms_killing_derived': kill_derived,
    'endomorphisms_preserving_derived': preserve_derived,
    'endomorphisms': ends, 'partial_isomorphisms': partials,
    'types': types
}, indent=2))
