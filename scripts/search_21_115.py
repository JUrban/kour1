#!/usr/bin/env python3
"""Exact bounded feasibility search for Kourovka 21.115.

Input cosets are independently enumerated in GAP. A solver timeout is UNKNOWN,
never a negative result. Any feasible union is checked by integer set arithmetic.
"""
import argparse
import importlib.metadata
import itertools
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "software/coset-python"))
from ortools.sat.python import cp_model


def maximal_cosets(data):
    order = data["group_id"][0]
    identity_bit = 1 << (data["identity"] - 1)
    masks = set()
    for coset in data["cosets"]:
        assert len(coset) == len(set(coset))
        assert all(1 <= x <= order for x in coset)
        mask = sum(1 << (x - 1) for x in coset)
        assert mask and not mask & identity_bit
        masks.add(mask)
    kept = []
    for mask in sorted(masks, key=lambda m: (-m.bit_count(), m)):
        if not any(mask & larger == mask for larger in kept):
            kept.append(mask)
    return kept


def solve(data, n, seconds, workers):
    started = time.monotonic()
    order = data["group_id"][0]
    # Strict failure means uncovered < order / 2**n.
    threshold = (order + (1 << n) - 1) // (1 << n) - 1
    masks = maximal_cosets(data)
    model = cp_model.CpModel()
    selected = [model.new_bool_var(f"c{i}") for i in range(len(masks))]
    model.add(sum(selected) <= n)
    missing = []
    for x in range(order):
        if x + 1 == data["identity"]:
            continue
        z = model.new_bool_var(f"u{x}")
        missing.append(z)
        model.add(z + sum(selected[i] for i, mask in enumerate(masks)
                          if mask >> x & 1) >= 1)
    model.add(sum(missing) <= threshold - 1)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 21115
    status = solver.solve(model)
    result = dict(group_id=data["group_id"], n=n, status=solver.status_name(status),
                  maximum_uncovered_for_failure=threshold,
                  cosets_before=len(data["cosets"]), cosets_after=len(masks),
                  elapsed_seconds=time.monotonic() - started,
                  branches=solver.num_branches, conflicts=solver.num_conflicts)
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        chosen = [mask for i, mask in enumerate(masks) if solver.value(selected[i])]
        union = 0
        for mask in chosen:
            union |= mask
        uncovered = order - union.bit_count()
        assert len(chosen) <= n and 0 < uncovered
        assert uncovered * (1 << n) < order
        assert not union >> (data["identity"] - 1) & 1
        result.update(chosen_cosets=[[x + 1 for x in range(order) if mask >> x & 1]
                                     for mask in chosen], uncovered=uncovered,
                      flag="CANDIDATE_REQUIRES_INDEPENDENT_GROUP_CERTIFICATE")
    return result


def self_test():
    # Test the solver against brute force on unrelated set systems. This checks
    # the strict threshold, implicit missing identity, and dominance reduction.
    count = 0
    for order in range(3, 9):
        universe = list(range(2, order + 1))
        families = [ [[x] for x in universe],
                     [universe],
                     [universe[::2], universe[1::2]],
                     [list(c) for c in itertools.combinations(universe, 2)] ]
        for family in families:
            family = [c for c in family if c]
            data = dict(group_id=[order, 0], identity=1, cosets=family)
            for n in range(1, 4):
                brute = any(0 < order - len(set().union(*cs))
                            and (order - len(set().union(*cs))) * (1 << n) < order
                            for k in range(min(n, len(family)) + 1)
                            for cs in itertools.combinations(map(set, family), k))
                result = solve(data, n, 5, 1)
                assert result["status"] in ("INFEASIBLE", "OPTIMAL", "FEASIBLE")
                assert brute == (result["status"] != "INFEASIBLE"), result
                count += 1
    print(json.dumps(dict(self_test="PASS", cases=count,
                          ortools=importlib.metadata.version("ortools"))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--seconds", type=float, default=10)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--min-n", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=100)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    for path in args.paths:
        data = json.loads(Path(path).read_text())
        for n in range(args.min_n, min(args.max_n, (data["group_id"][0] - 1).bit_length() - 1) + 1):
            result = solve(data, n, args.seconds, args.workers)
            print(json.dumps(result, sort_keys=True), flush=True)
            if "flag" in result:
                return


if __name__ == "__main__":
    main()
