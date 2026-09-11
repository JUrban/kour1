#!/usr/bin/env python3
"""Exact finite controls using a tensor presentation, not an assumed PBW basis.

Construct I/(U h + I^(c+1)) from all nonempty tensor words of length <=c,
then row-reduce the enveloping relations and left-ideal relations over Q.
This independently tests the filtration/equalizer step of the general proof.
The finite cases cannot establish the arbitrary-dimensional theorem.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import random
import time


def add(a, b, scale=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + scale * v
        if not out[k]:
            del out[k]
    return out


class Span:
    def __init__(self):
        self.rows = {}

    def reduce(self, v):
        v = dict(v)
        # Eliminate every pivot, including those beyond a free coordinate.
        for p in sorted(self.rows):
            if p in v:
                v = add(v, self.rows[p], -v[p])
        return v

    def insert(self, v):
        v = self.reduce(v)
        if not v:
            return False
        p = min(v)
        scale = Q(1, v[p])
        self.rows[p] = {k: scale * a for k, a in v.items()}
        return True


def verify(name, dim, c, brackets, h, group_checks=False):
    start = time.monotonic()
    table = {}
    for (i, j), v in brackets.items():
        table[i, j] = v
        table[j, i] = {k: -a for k, a in v.items()}

    def lie(a, b):
        out = {}
        for i, x in a.items():
            for j, y in b.items():
                out = add(out, table.get((i, j), {}), x * y)
        return out

    basis = [{i: Q(1)} for i in range(dim)]
    for x, y, z in product(basis, repeat=3):
        assert not add(add(lie(x, lie(y, z)), lie(y, lie(z, x))), lie(z, lie(x, y)))
    hs = Span()
    for x in h:
        assert hs.insert(x)
    assert all(not hs.reduce(lie(x, y)) for x in h for y in h)

    words_by_length = [list(product(range(dim), repeat=n)) for n in range(c + 1)]
    words = [w for layer in words_by_length[1:] for w in layer]
    index = {w: i for i, w in enumerate(words)}
    relations = Span()
    relation_count = 0
    # Every u*(x_i*x_j-x_j*x_i-[x_i,x_j])*v surviving tensor truncation.
    for n in range(c):
        for a in range(n + 1):
            for u in words_by_length[a]:
                for v in words_by_length[n - a]:
                    for i in range(dim):
                        for j in range(i + 1, dim):
                            row = {}
                            if n + 2 <= c:
                                row[index[u + (i, j) + v]] = Q(1)
                                row = add(row, {index[u + (j, i) + v]: Q(-1)})
                            for k, z in table.get((i, j), {}).items():
                                row = add(row, {index[u + (k,) + v]: -Q(z)})
                            relations.insert(row)
                            relation_count += 1
    for layer in words_by_length[:c]:
        for u in layer:
            for x in h:
                relations.insert({index[u + (i,)]: Q(a) for i, a in x.items()})
                relation_count += 1

    free = [i for i in range(len(words)) if i not in relations.rows]
    mindex = {w: i for i, w in enumerate(free)}

    def project(v):
        return {mindex[i]: a for i, a in relations.reduce(v).items()}

    def left_raw(i, v):
        return {index[(i,) + words[k]]: a for k, a in v.items() if len(words[k]) < c}

    # The presented denominator really is stable under the left action.
    for i in range(dim):
        for row in relations.rows.values():
            assert not relations.reduce(left_raw(i, row))

    actions = [[project(left_raw(i, {k: Q(1)})) for k in free] for i in range(dim)]

    def act(x, m):
        out = {}
        for i, a in x.items():
            for j, b in m.items():
                out = add(out, actions[i][j], a * b)
        return out

    derivatives = [project({index[(i,)]: Q(1)}) for i in range(dim)]

    def derivative(x):
        out = {}
        for i, a in x.items():
            out = add(out, derivatives[i], a)
        return out

    ds = Span()
    for v in derivatives:
        ds.insert(v)
    assert len(ds.rows) == dim - len(h)
    assert all(not derivative(x) for x in h)

    mbasis = [{i: Q(1)} for i in range(len(free))]
    for x, y in product(basis, repeat=2):
        assert derivative(lie(x, y)) == add(act(x, derivative(y)), act(y, derivative(x)), -1)
        for m in mbasis:
            assert act(lie(x, y), m) == add(act(x, act(y, m)), act(y, act(x, m)), -1)

    def split(v):
        return ({k: a for k, a in v.items() if k < dim},
                {k - dim: a for k, a in v.items() if k >= dim})

    def pair(x, m):
        return add(x, {dim + k: a for k, a in m.items()})

    def bracket(a, b):
        x, m = split(a)
        y, n = split(b)
        return pair(lie(x, y), add(act(x, n), act(y, m), -1))

    pbasis = [{i: Q(1)} for i in range(dim + len(free))]
    lower = list(pbasis)
    lower_dims = [len(lower)]
    for r in range(c):
        new = Span()
        for x in pbasis:
            for y in lower:
                new.insert(bracket(x, y))
        lower = list(new.rows.values())
        lower_dims.append(len(lower))
    assert not lower

    checks = 0
    if group_checks:
        assert c <= 3
        def bch(x, y, comm):
            xy = comm(x, y)
            return add(add(add(x, y), xy, Q(1, 2)),
                       add(comm(x, xy), comm(y, comm(y, x))), Q(1, 12))

        rng = random.Random(1734 + dim + c)
        for _ in range(200):
            x = {i: Q(rng.randrange(-3, 4), rng.randrange(1, 5)) for i in range(dim)}
            y = {i: Q(rng.randrange(-3, 4), rng.randrange(1, 5)) for i in range(dim)}
            x = {i: a for i, a in x.items() if a}
            y = {i: a for i, a in y.items() if a}
            z = bch(x, y, lie)
            assert pair(z, derivative(z)) == bch(pair(x, derivative(x)), pair(y, derivative(y)), bracket)
            assert pair(z, {}) == bch(pair(x, {}), pair(y, {}), bracket)
            checks += 2

    result = {
        "name": name, "lie_dimension": dim, "class_bound": c,
        "subalgebra_dimension": len(h), "tensor_dimension": len(words),
        "relations_processed": relation_count, "relation_rank": len(relations.rows),
        "module_dimension": len(free), "derivative_rank": len(ds.rows),
        "target_lower_central_dimensions": lower_dims,
        "rational_bch_homomorphism_checks": checks,
        "seconds": round(time.monotonic() - start, 3), "status": "PASS"
    }
    print(json.dumps(result), flush=True)
    return result


def main():
    results = []
    results.append(verify("abelian_noncoordinate", 3, 1, {}, [{0: 1, 1: 2}]))
    heis = {(0, 1): {2: 1}}
    for name, h in [
        ("heisenberg_trivial", []), ("heisenberg_all", [{i: 1} for i in range(3)]),
        ("heisenberg_nonideal", [{0: 1}]),
        ("heisenberg_nonhomogeneous", [{0: 1, 2: 2}]),
        ("heisenberg_central", [{2: 1}]),
        ("heisenberg_ideal", [{0: 1}, {2: 1}])
    ]:
        results.append(verify(name, 3, 2, heis, h, True))
    free3 = {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}}
    for name, h in [
        ("free2_class3_nonideal", [{0: 1}]),
        ("free2_class3_nonhomogeneous", [{0: 1, 2: 1}, {3: 1, 4: 2}]),
        ("free2_class3_nonabelian_subalgebra", [{0: 1}, {2: 1}, {3: 1}]),
        ("free2_class3_central", [{3: 1, 4: 2}])
    ]:
        results.append(verify(name, 5, 3, free3, h, True))
    fil4 = {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}}
    results.append(verify("filiform_class4_nonhomogeneous", 5, 4, fil4, [{0: 1, 2: 1}, {4: 1}]))
    # A filtered deformation: [e1,e2]=e4 in addition to the filiform brackets.
    # This Lie algebra is not being treated as homogeneous in the tensor model.
    deformation = dict(fil4)
    deformation[1, 2] = {4: 1}
    results.append(verify("filtered_class4_deformation", 5, 4, deformation, [{1: 1, 3: 2}, {4: 1}]))
    out = {"method": "exact rational tensor-presentation quotient; no assumed PBW basis",
           "cases": results, "status": "PASS", "limitations": "Finite sanity checks, not a proof for all Lie algebras."}
    path = Path(__file__).resolve().parents[1] / "results/17.34-verification.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print("PASS 17.34 tensor quotient, equalizer, module, class, and BCH controls", flush=True)


if __name__ == "__main__":
    main()
