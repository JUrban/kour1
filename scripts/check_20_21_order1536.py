#!/usr/bin/env python3
"""Table-only witnesses for every retained pair, with audited native associativity."""
from collections import Counter,defaultdict
import gzip
import hashlib
import json
from math import lcm
from pathlib import Path
import check_20_21 as table_tools
from control_table_associativity_20_21 import load


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block:=stream.read(2**20):h.update(block)
    return h.hexdigest()


def run():
    native=load();control=json.loads(Path('results/20.21-associativity-controls.json').read_text())
    assert sha('results/20.21-table-associativity.so')==control['library_sha256']
    assert sha('scripts/table_associativity_20_21.c')==control['source_sha256']
    search=json.loads(Path('results/20.21-order1536-interval-summary.json').read_text())
    export=json.loads(Path('results/20.21-order1536-export-summary.json').read_text())
    assert search['status']=='COMPLETE_NO_CANDIDATE' and export['status']=='COMPLETE'
    expected={}
    for job in search['jobs']:
        assert job['returncode']==0
        for p,h in job['sha256'].items():assert sha(p)==h
        for line in Path(job['rows']).read_text().splitlines():
            n,i,cs,aa=json.loads(line);key=(n,i);assert key not in expected
            expected[key]=[Counter(map(tuple,cs)),Counter(map(tuple,aa))]
    assert len(expected)==5006
    observed=defaultdict(lambda:[[],[]]);cache={};tables=0;triples=0
    hashes={}
    for job in export['jobs']:
        assert job['returncode']==0
        for p,h in job['sha256'].items():assert sha(p)==h
        hashes[job['compressed']]=sha(job['compressed']);raw_digest=hashlib.sha256();raw_size=0
        with gzip.open(job['compressed'],'rb') as stream:
            for line in stream:
                raw_digest.update(line);raw_size+=len(line)
                identity,kind,claimed,table=json.loads(line)
                identity=tuple(identity);assert identity in expected and kind in (0,1)
                assert len(table)==128 and claimed[0]==128 and all(len(row)==128 for row in table)
                assert all(type(x) is int and 0<=x<128 for row in table for x in row)
                key=bytes(v for row in table for v in row)
                if key not in cache:
                    assert table[0]==list(range(128))
                    assert all(table[x][0]==x for x in range(128))
                    assert all(sorted(row)==list(range(128)) for row in table)
                    assert native(key,128)==0;triples+=128**3
                    inverse=[row.index(0) for row in table]
                    assert all(table[inverse[x]][x]==0 for x in range(128))
                    orders=table_tools.orders(table)
                    comm={table[table[table[inverse[a]][inverse[b]]][a]][b] for a in range(128) for b in range(128)}
                    derived=table_tools.generated(table,comm)
                    abelian=table_tools.quotient(table,derived)
                    assert all(abelian[a][b]==abelian[b][a] for a in range(len(abelian)) for b in range(len(abelian)))
                    ab_orders=table_tools.orders(abelian)
                    cache[key]=(tuple(sorted(Counter(orders).items())),lcm(*ab_orders),tuple(sorted(Counter(ab_orders).items())))
                observed[identity][kind].append((tuple(claimed),cache[key]));tables+=1
                if tables%1000==0:print('PROGRESS_2021_1536_KERNEL_CONTROLS',tables,len(cache),flush=True)
        assert raw_digest.hexdigest()==job['raw_sha256'] and raw_size==job['raw_bytes']
    assert set(observed)==set(expected) and tables==30414
    witnesses=[0,0,0]
    for identity,(cs,aa) in observed.items():
        assert Counter(p[0] for p in cs)==expected[identity][0]
        assert Counter(p[0] for p in aa)==expected[identity][1]
        for _,a in cs:
            for _,b in aa:
                differences=[j for j in range(3) if a[j]!=b[j]]
                assert differences,('no independent separator',identity,a,b)
                witnesses[differences[0]]+=1
    assert sum(witnesses)==26760
    return dict(groups=len(expected),kernel_tables=tables,distinct_tables=len(cache),associativity_triples=triples,
                pairs=sum(witnesses),element_order_spectrum_witnesses=witnesses[0],
                abelianization_exponent_witnesses=witnesses[1],abelianization_order_spectrum_witnesses=witnesses[2],
                compressed_source_sha256=hashes,native_library_sha256=control['library_sha256'])


if __name__=='__main__':
    result=run();Path('results/20.21-order1536-kernel-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_2021_ORDER1536_KERNEL_CONTROLS',json.dumps(result,sort_keys=True))
