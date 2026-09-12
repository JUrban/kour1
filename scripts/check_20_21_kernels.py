#!/usr/bin/env python3
"""Table-only nonisomorphism witnesses for every retained order768 kernel pair."""
import ast
from collections import Counter,defaultdict
import gzip
import hashlib
import importlib.util
import json
from math import lcm
from pathlib import Path


def run():
    spec=importlib.util.spec_from_file_location('table2021','scripts/check_20_21.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    expected={}
    for path in sorted(Path('results').glob('20.21-order768-fast-shard*.grows')):
        for line in path.read_text().splitlines():
            n,i,cs,aa=ast.literal_eval(line);key=(n,i)
            assert key not in expected
            expected[key]=[Counter(map(tuple,cs)),Counter(map(tuple,aa))]
    assert len(expected)==606
    source=Path('results/20.21-order768-kernel-tables.grows.gz')
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    observed=defaultdict(lambda:[[],[]]);cache={};tables=0;triples=0
    with gzip.open(source,'rt') as stream:
        for line in stream:
            identity,kind,claimed,table=ast.literal_eval(line)
            identity=tuple(identity);assert identity in expected and kind in (0,1)
            assert len(table)==64 and claimed[0]==64
            key=bytes(v for row in table for v in row)
            assert all(len(row)==64 for row in table)
            if key not in cache:
                inv=module.validate(table);triples+=64**3
                orders=module.orders(table)
                comm={table[table[table[inv[a]][inv[b]]][a]][b] for a in range(64) for b in range(64)}
                derived=module.generated(table,comm)
                abelian=module.quotient(table,derived)
                assert all(abelian[a][b]==abelian[b][a] for a in range(len(abelian)) for b in range(len(abelian)))
                invariant=(tuple(sorted(Counter(orders).items())),lcm(*module.orders(abelian)))
                cache[key]=invariant
            observed[identity][kind].append((tuple(claimed),cache[key]))
            tables+=1
    assert set(observed)==set(expected) and tables==2878
    spectrum=abelian_exponent=0
    for identity,(cs,aa) in observed.items():
        assert Counter(p[0] for p in cs)==expected[identity][0]
        assert Counter(p[0] for p in aa)==expected[identity][1]
        for _,a in cs:
            for _,b in aa:
                if a[0]!=b[0]:spectrum+=1
                else:
                    assert a[1]!=b[1],(identity,a,b)
                    abelian_exponent+=1
    assert spectrum+abelian_exponent==2368
    return dict(groups=606,kernel_tables=tables,distinct_tables=len(cache),
                associativity_triples=triples,pairs=2368,
                element_order_spectrum_witnesses=spectrum,
                abelianization_exponent_witnesses=abelian_exponent,
                compressed_source_sha256=source_hash)


if __name__=='__main__':
    result=run();Path('results/20.21-order768-kernel-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_2021_KERNEL_CONTROLS',json.dumps(result,sort_keys=True))
