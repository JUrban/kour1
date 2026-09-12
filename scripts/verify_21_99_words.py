#!/usr/bin/env python3
"""Prove positive permutation-action statements by evaluating generator words."""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMALL_COUNTS = {2:1,3:2,4:5,5:5,6:16,7:7,8:50,9:34,10:45,11:8,12:301}


def inverse(p):
    q = [0]*len(p)
    for i,j in enumerate(p):
        q[j] = i
    return tuple(q)


def verify_row(row):
    assert len(row) == 7
    n,identifier,generators,code,witnesses,trials,raw_nodes = row
    assert type(n) is int and 2 <= n <= 47 and type(identifier) is int and identifier > 0
    identity = tuple(range(n))
    assert generators and all(sorted(g) == list(identity) for g in generators)
    assert all(all(type(i) is int for i in g) for g in generators)
    values = [identity]+list(map(tuple,generators))
    inverses = {0:identity}
    def value(a):
        assert type(a) is int and abs(a) < len(values), 'invalid word reference'
        if a >= 0:
            return values[a]
        if -a not in inverses:
            inverses[-a] = inverse(values[-a])
        return inverses[-a]
    for pair in code:
        assert len(pair) == 2
        a,b = map(value,pair)
        values.append(tuple(b[i] for i in a))
    assert len(witnesses) == n and witnesses[0] == 0, 'missing point witness'
    fixed_counts = Counter()
    for beta in range(1,n):
        w = value(witnesses[beta])
        assert w[0] == beta, 'wrong target point'
        fixed = sum(i == j for i,j in enumerate(w))
        assert fixed != 1, 'witness fixes exactly one point'
        fixed_counts[fixed] += 1
    assert type(trials) is int and trials >= 0
    assert type(raw_nodes) is int and raw_nodes >= len(values)-1
    return Counter(groups=1,witnesses=n-1,circuit_nodes=len(code),
                   point_multiplications=n*len(code),input_generators=len(generators)),fixed_counts


def mutations(sample):
    rejected = []
    for name in ['generator','forward_reference','target','fixed_count','missing_witness']:
        bad = copy.deepcopy(sample)
        if name == 'generator':
            bad[2][0][0] = bad[2][0][1]
        elif name == 'forward_reference':
            bad[3][0][0] = len(bad[2])+1
        elif name == 'target':
            bad[4][1] = 0
        elif name == 'fixed_count':
            bad = [3,1,[[1,0,2],[2,1,0]],[],[0,1,2],0,2]
        else:
            bad[4].pop()
        try:
            verify_row(bad)
        except AssertionError as exc:
            if name == 'fixed_count':
                assert str(exc) == 'witness fixes exactly one point'
            rejected.append(name)
        else:
            raise AssertionError('accepted corruption '+name)
    return rejected


def verify_files(paths,expected):
    counts = Counter(); fixed = Counter(); seen = set(); degrees = Counter()
    sample = None
    max_trials = 0
    for path in paths:
        for line in path.read_text().splitlines():
            row = json.loads(line)
            key = tuple(row[:2])
            assert key not in seen
            seen.add(key)
            current,histogram = verify_row(row)
            counts.update(current); fixed.update(histogram); degrees[row[0]] += 1
            max_trials = max(max_trials,row[5])
            if sample is None and row[0] >= 3 and row[3]:
                sample = row
        print('VERIFIED_FILE',path.name,'cumulative_groups',len(seen),flush=True)
    assert seen == expected, (len(seen),len(expected),len(expected-seen),len(seen-expected))
    assert sample is not None
    return dict(status='PASS_GENERATOR_WORD_CERTIFICATES',counts=dict(sorted(counts.items())),
                degrees=sorted(degrees.items()),fixed_counts=sorted(fixed.items()),
                max_random_steps=max_trials,rejected_mutations=mutations(sample),
                new_complete_candidates_added=0,
                scope='Every supplied action proved directly from generator permutations; catalogue completeness imported.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scope',choices=['pilot','extension'])
    args = parser.parse_args()
    if args.scope == 'pilot':
        paths = [ROOT/'results/21.99-words-pilot-certificate.jsonl']
        expected = {(n,i) for n,count in SMALL_COUNTS.items() for i in range(1,count+1)}
        expected |= {(24,i) for i in range(24990,25001)}
    else:
        paths = [ROOT/f'results/21.99-words-shard{s}-certificate.jsonl' for s in range(8)]
        census = json.loads((ROOT/'results/21.99-words-census.json').read_text())
        expected = {(n,i) for n,count in census for i in range(1,count+1)}
    result = verify_files(paths,expected)
    (ROOT/f'results/21.99-words-{args.scope}-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_2199_WORD_INDEPENDENT',args.scope,json.dumps(result['counts'],sort_keys=True),'mutations=5')


if __name__ == '__main__':
    main()
