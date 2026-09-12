#!/usr/bin/env python3
"""Frozen order768 search coverage plus full table-only kernel replay."""
import ast
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def run():
    packet=json.loads(Path('results/20.21-order768-packet.json').read_text())
    for p,h in packet['sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
    load('pilot2021','scripts/audit_20_21.py').run()
    summary=json.loads(Path('results/20.21-order768-fast-summary.json').read_text())
    assert summary['status']=='COMPLETE_NO_CANDIDATE'
    assert summary['totals']==dict(tested=1090235,eligible=11562,both=606,hits=0)
    assert len(summary['jobs'])==summary['shards']==8
    seen=set();totals=[0]*4
    for job in summary['jobs']:
        assert job['returncode']==0
        for p,h in job['sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
        text=Path(job['log']).read_text()
        assert not re.search(r'Error|Syntax warning|Traceback|CANDIDATE_',text)
        m=re.findall(r'PASS_2021_SHARD\s*(\[[^\]]+\])',text)
        assert len(m)==text.count('PASS_2021_SHARD')==1
        values=ast.literal_eval(m[0]);i=job['index']
        assert values[:3]==[768,i,8]
        assert values[3]==(1090234-i)//8+1
        assert values==summary['shard_counts'][i]
        rows=[ast.literal_eval(s) for s in Path(job['rows']).read_text().splitlines()]
        assert len(rows)==values[5]
        for n,j,cs,aa in rows:
            assert n==768 and (j-1)%8==i and 1<=j<=1090235
            assert j not in seen;seen.add(j)
            assert cs and aa and set(map(tuple,cs)).isdisjoint(map(tuple,aa))
        totals=[a+b for a,b in zip(totals,values[3:])]
    assert totals==[1090235,11562,606,0] and len(seen)==606
    compression=json.loads(Path('results/20.21-order768-kernel-compression.json').read_text())
    source=Path('results/20.21-order768-kernel-tables.grows.gz')
    data=source.read_bytes();raw=gzip.decompress(data)
    assert len(data)==compression['compressed_bytes']
    assert len(raw)==compression['uncompressed_bytes']
    assert hashlib.sha256(data).hexdigest()==compression['compressed_sha256']
    assert hashlib.sha256(raw).hexdigest()==compression['uncompressed_sha256']
    checker=load('kernels2021','scripts/check_20_21_kernels.py')
    assert checker.run()==json.loads(Path('results/20.21-order768-kernel-controls.json').read_text())
    print('PASS_2021_ORDER768_PACKET',len(packet['sha256']),'groups=1090235 pairs=2368 lower_bound=1536')


if __name__=='__main__':run()
