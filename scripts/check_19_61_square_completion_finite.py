#!/usr/bin/env python3
"""Compare iterative square completion to frozen independently found closures."""
import ast
import hashlib
import json
from pathlib import Path
from carpet_horn_19_61 import assigned

LABELS = ['f2', 'f4', 'dual', 'split', 'z4', 'g2p2', 'g2p3',
          'g2f4', 'g2dual', 'g2split', 'g2z4', 'g2f9']


def run():
    reports = []; hashes = {}
    for label in LABELS:
        source = Path('results/19.61-'+label+'-input.g')
        prep = Path('results/19.61-'+label+'-preparation.json')
        for p in [source, prep]:
            hashes[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
        rows = assigned(source, 'Carpets1961'); subsets = assigned(source, 'Subsets1961')
        masks = assigned(source, 'Masks1961'); rules = assigned(source, 'Implications1961')
        data = json.loads(prep.read_text()); roots = data['roots']
        if label in ['g2p2', 'g2p3']:
            p = data['prime']; add = [[(a+b) % p for b in range(p)] for a in range(p)]
            mul = [[a*b % p for b in range(p)] for a in range(p)]
        else:
            add, mul = data['add'], data['mul']
        n = len(add); opposite = [roots.index([-v for v in r]) for r in roots]
        lookup = set(map(tuple, rows)); join = {}
        for mask in range(1, 1 << n, 2):
            values = {i for i in range(n) if mask >> i & 1}
            while True:
                updated = values | {add[a][b] for a in values for b in values}
                if updated == values:
                    break
                values = updated
            join[mask] = subsets.index(sorted(values))+1
        square_step = {}
        for i, left in enumerate(subsets, 1):
            for j, right in enumerate(subsets, 1):
                mask = masks[i-1]
                for x in left:
                    for y in right:
                        mask |= 1 << mul[mul[x][x]][y]
                square_step[i, j] = join[mask]
        def derived(row):
            needed = [1]*len(roots)
            for r, s, k, required in rules:
                needed[k-1] |= required[row[r-1]-1][row[s-1]-1]
            return tuple(join[v] for v in needed)
        changes = {}
        paths = [Path('results/19.61-g2f9-shard'+str(i)+'-changes.grows') for i in range(4)] if label == 'g2f9' else [Path('results/19.61-'+label+'-changes.grows')]
        for path in paths:
            hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
            for line in path.read_text().splitlines():
                row = ast.literal_eval(line); assert row[0] not in changes
                changes[row[0]] = tuple(row[2])
        enlarged = steps = largest = strict_upper = 0
        completed = set()
        for index, original in enumerate(rows, 1):
            initial = tuple(original); base = derived(initial); current = initial; rounds = 0
            while True:
                following = tuple(square_step[current[r], current[opposite[r]]] for r in range(len(roots)))
                if following == current:
                    break
                assert following in lookup and derived(following) == base
                assert all(not masks[current[r]-1] & ~masks[following[r]-1] for r in range(len(roots)))
                current = following; rounds += 1
                assert rounds <= n*len(roots)
            closure = changes.get(index, initial)
            assert all(not masks[closure[r]-1] & ~masks[current[r]-1] for r in range(len(roots)))
            assert derived(closure) == base
            enlarged += current != initial; strict_upper += current != closure
            completed.add(current); steps += rounds; largest = max(largest, rounds)
        report = dict(label=label, carpets=len(rows), completion_enlarged=enlarged,
                      closure_enlarged=len(changes), completion_strictly_larger_than_closure=strict_upper,
                      distinct_completions=len(completed), total_rounds=steps, maximum_rounds=largest)
        reports.append(report)
        print('PASS_1961_FINITE_SQUARE_COMPLETION', label, len(rows), enlarged, strict_upper, largest, flush=True)
    return dict(rings=reports, carpets=sum(v['carpets'] for v in reports), sha256=hashes)


if __name__ == '__main__':
    Path('results/19.61-square-completion-finite.json').write_text(json.dumps(run(), indent=2)+'\n')
