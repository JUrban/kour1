#!/usr/bin/env python3
"""Compare omitted-pair carpets to frozen exact finite group closures."""
import ast
import hashlib
import json
from pathlib import Path
from carpet_horn_19_61 import assigned
from check_19_61_square_completion_finite import LABELS


def run():
    reports = []; hashes = {}
    for label in LABELS:
        source = Path('results/19.61-'+label+'-input.g')
        prep = Path('results/19.61-'+label+'-preparation.json')
        for path in [source, prep]:
            hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        rows = [tuple(row) for row in assigned(source, 'Carpets1961')]
        subsets = assigned(source, 'Subsets1961'); masks = assigned(source, 'Masks1961')
        rules = assigned(source, 'Implications1961')
        data = json.loads(prep.read_text()); roots = data['roots']
        lookup = {row: i for i, row in enumerate(rows, 1)}
        pairs = [(i, roots.index([-v for v in root])) for i, root in enumerate(roots)]
        pairs = [(i, j) for i, j in pairs if i < j]
        join = {mask: min((i for i, v in enumerate(masks, 1) if not mask & ~v),
                          key=lambda i: len(subsets[i-1]))
                for mask in range(1, 1 << (max(max(s) for s in subsets)+1), 2)}
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
        controls = changed_elsewhere = 0; distinct = set()
        for row in rows:
            b = derived(row)
            for p, opposite in pairs:
                f = list(row); f[p] = b[p]; f[opposite] = b[opposite]; f = tuple(f)
                assert f in lookup
                index = lookup[f]; closure = changes.get(index, f)
                assert closure[p] == b[p] and closure[opposite] == b[opposite]
                controls += 1; changed_elsewhere += closure != f; distinct.add(index)
        report = dict(label=label, original_carpets=len(rows), opposite_pairs=len(pairs),
                      controls=controls, distinct_omitted_carpets=len(distinct),
                      closure_enlarged_elsewhere=changed_elsewhere)
        reports.append(report)
        print('PASS_1546_OMITTED_PAIRS', label, len(rows), controls, len(distinct), changed_elsewhere, flush=True)
    return dict(rings=reports, controls=sum(v['controls'] for v in reports), sha256=hashes)


if __name__ == '__main__':
    Path('results/15.46-omitted-pairs-controls.json').write_text(json.dumps(run(), indent=2)+'\n')
