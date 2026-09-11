#!/usr/bin/env python3
"""Produce a finite refutation certificate for a fixed-n counterexample to20.100.

The independent GAP verifier uses integer presentation matrices and Smith
normal forms, rather than this weighted-component quotient implementation.
"""
import argparse
from fractions import Fraction
from itertools import combinations, permutations
from math import gcd
from pathlib import Path
import gzip
import hashlib
import json
import re
import resource
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--prime-bound", type=int)
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--resume-certificate", help="Reuse completed nodes from an earlier certificate prefix")
    parser.add_argument("--max-states", type=int, default=2000000)
    parser.add_argument("--seconds", type=int, default=1800)
    args = parser.parse_args()
    n = args.n
    bound = args.prime_bound if args.prime_bound is not None else n+1
    primes = [p for p in range(2, bound+1) if all(p%d for d in range(2, p))]
    pairs = list(combinations(range(n), 2))
    choices = list(permutations(range(1, n+1)))
    started = time.monotonic()
    seen, done = {}, {}
    counts = {"states": 0, "leaves": 0, "edges": 0}
    counterexample = None

    def strip(value):
        value = abs(value)
        if not value:
            return 0
        for p in primes:
            while value % p == 0:
                value //= p
        return value

    def canonical_component(modulus, items):
        if modulus == 1:
            values = sorted((0, label) for _, label in items)
        elif modulus:
            items = [(Fraction(w).numerator * pow(Fraction(w).denominator, -1, modulus) % modulus, label)
                     for w, label in items]
            assert all(gcd(w, modulus) == 1 for w, _ in items)
            candidates = [sorted((w*pow(base, -1, modulus) % modulus, label)
                                 for w, label in items) for base, _ in items]
            values = min(candidates, key=lambda row: (tuple(w for w, _ in row),
                                                      tuple(label for _, label in row)))
        else:
            base = min(w for w, _ in items)
            values = sorted((Fraction(w)/base, label) for w, label in items)
        return (modulus, tuple(w for w, _ in values)), tuple(label for _, label in values)

    def canonical(components):
        parts = sorted(canonical_component(m, items) for m, items in components)
        return tuple(state for state, _ in parts), tuple(label for _, labels in parts for label in labels)

    def valid(state):
        if sum(len(ws) for m, ws in state if m == 1) > 1:
            return False
        return all(len(set(ws)) == len(ws) for _, ws in state)

    def flatten(state):
        return [(c, w) for c, (_, ws) in enumerate(state) for w in ws]

    def quotient(state, i, j, a, b):
        flat = flatten(state)
        c, w = flat[i]
        d, v = flat[j]
        components = [(m, [(u, k) for k, (cc, u) in enumerate(flat) if cc == z])
                      for z, (m, _) in enumerate(state)]
        if c == d:
            m, items = components[c]
            diff = Fraction(a*w-b*v).numerator
            components[c] = (gcd(m, strip(diff)), items)
        else:
            m, items = components[c]
            k, other = components[d]
            modulus = gcd(m, k)
            if modulus == 1:
                merged = [(0, label) for _, label in items+other]
            else:
                ratio = Fraction(a*w, b*v)
                merged = items + [(ratio*u, label) for u, label in other]
            components = [part for z, part in enumerate(components) if z not in (c, d)]
            components.append((modulus, merged))
        return canonical(components)

    def choose_permutation(state):
        flat = flatten(state)
        for perm in choices:
            values = []
            for (c, w), exponent in zip(flat, perm):
                modulus = state[c][0]
                val = w*exponent
                values.append((c, val % modulus if modulus else val))
            if len(set(values)) == n:
                return perm
        return None

    def gap(value):
        if isinstance(value, (list, tuple)):
            return "[" + ",".join(map(gap, value)) + "]"
        return str(value)

    path = Path(args.certificate)
    path.parent.mkdir(parents=True, exist_ok=True)
    resume = Path(args.resume_certificate) if args.resume_certificate else None
    if resume:
        assert resume.resolve() != path.resolve(), "preserve the original prefix in a separate file"
    with gzip.open(path, "wt", encoding="ascii") as output:
        output.write(f"StartProof({n},{bound});\n")
        if resume:
            with gzip.open(resume, "rt", encoding="ascii") as previous:
                assert next(previous) == f"StartProof({n},{bound});\n"
                finished = False
                for line in previous:
                    if line.startswith("FinishProof("):
                        assert line == f"FinishProof({len(done)});\n"
                        finished = True
                        assert previous.read() == ""
                        break
                    match = re.match(r"CheckNode\((\d+),", line)
                    assert match and int(match.group(1)) == len(done)+1
                    start, depth, end = match.end(), 0, None
                    assert line[start] == "["
                    for position in range(start, len(line)):
                        if line[position] == "[":
                            depth += 1
                        elif line[position] == "]":
                            depth -= 1
                            if depth == 0:
                                end = position+1
                                break
                    assert end and line[end] == "," and line.endswith(");\n")
                    raw = re.sub(r"(-?\d+/\d+)", r'"\1"', line[start:end])
                    state = tuple((m, tuple(Fraction(w) for w in ws)) for m, ws in json.loads(raw))
                    assert sum(len(ws) for m, ws in state) == n and state not in done
                    done[state] = len(done)+1
                    if line[end+1:].startswith("[],"):
                        counts["leaves"] += 1
                    else:
                        counts["edges"] += len(pairs)
                    output.write(line)
                counts["states"] = len(done)
            print(json.dumps({"status": "RESUMED_PREFIX", "n": n, "prime_bound": bound,
                              "source": str(resume), "source_had_root_footer": finished,
                              **counts, "seconds": time.monotonic()-started}), flush=True)

        def solve(state):
            nonlocal counterexample
            if state in done:
                return done[state]
            assert state not in seen, "cycle in a purported strict quotient proof"
            seen[state] = True
            counts["states"] += 1
            if counts["states"] > args.max_states or time.monotonic()-started > args.seconds:
                raise TimeoutError("explicit state/time bound reached; certificate incomplete")
            if counts["states"] % 10000 == 0:
                print(json.dumps({**counts, "seconds": round(time.monotonic()-started, 3),
                                  "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), flush=True)
            children = []
            if not valid(state):
                perm = ()
                counts["leaves"] += 1
            else:
                perm = choose_permutation(state)
                if perm is None:
                    counterexample = state
                    raise ValueError("counterexample found")
                for i, j in pairs:
                    child, labels = quotient(state, i, j, perm[i], perm[j])
                    assert child != state
                    child_id = solve(child)
                    children.append((child_id, tuple(label+1 for label in labels)))
                    counts["edges"] += 1
            identifier = len(done)+1
            done[state] = identifier
            del seen[state]
            output.write(f"CheckNode({identifier},{gap(state)},{gap(perm)},{gap(children)});\n")
            return identifier

        try:
            root = solve(tuple((0, (Fraction(1),)) for _ in range(n)))
        except TimeoutError:
            print(json.dumps({"status": "INCOMPLETE_BOUND_REACHED", "n": n,
                              "prime_bound": bound, "completed_nodes": len(done),
                              **counts, "seconds": time.monotonic()-started}), flush=True)
            return
        except ValueError:
            assert counterexample is not None
            print(json.dumps({"status": "COUNTEREXAMPLE", "n": n, "prime_bound": bound,
                              "state": gap(counterexample), **counts}), flush=True)
            return
        output.write(f"FinishProof({root});\n")
    print(json.dumps({"status": "CERTIFICATE_COMPLETE_PENDING_VERIFICATION", "n": n,
                      "prime_bound": bound, **counts, "seconds": time.monotonic()-started,
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "certificate": str(path),
                      "compressed_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
