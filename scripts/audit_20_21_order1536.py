#!/usr/bin/env python3
"""Audit catalogue reduction, all shards, native controls, and every kernel pair."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re
import check_20_21_order1536 as kernel_controls
import control_table_associativity_20_21 as native_controls


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while block:=f.read(2**20):h.update(block)
    return h.hexdigest()


def run():
    packet=json.loads(Path('results/20.21-order1536-packet.json').read_text())
    for path,digest in packet['sha256'].items():assert sha(path)==digest,path
    # The previously audited lower-bound packet is unchanged; preserve its full bindings.
    previous=json.loads(Path('results/20.21-order768-packet.json').read_text())
    for path,digest in previous['sha256'].items():assert sha(path)==digest,path
    launch=json.loads(Path('results/20.21-order1536-launch-manifest.json').read_text())
    for path,digest in launch['sha256'].items():assert sha(path)==digest,path
    library=gzip.decompress(Path('gap-4.16.1/pkg/smallgrp/small8/smlgp8.g.gz').read_bytes())
    assert library==Path('results/20.21-smallgrp-layer8-source.txt').read_bytes()
    boundary=Path('results/20.21-order1536-boundary-controls.log').read_text()
    assert boundary.count('BOUNDARY_2021 ')==8 and 'PASS_2021_INTERVAL_BOUNDARIES 8' in boundary
    assert not re.search(r'Error|Syntax warning|Traceback',boundary)
    search=json.loads(Path('results/20.21-order1536-interval-summary.json').read_text())
    assert search['status']=='COMPLETE_NO_CANDIDATE'
    assert (search['total_groups'],search['interval_first'],search['interval_last'],search['interval_count'])==(408641062,408526598,408544625,18028)
    assert search['totals']==dict(tested=18028,eligible=5006,both=5006,hits=0)
    allrows=[]
    for job in search['jobs']:
        i=job['index'];assert job['returncode']==0
        for path,digest in job['sha256'].items():assert sha(path)==digest,path
        output=Path(job['log']).read_text();assert not re.search(r'Error|Syntax warning|Traceback|CANDIDATE_',output)
        matches=re.findall(r'PASS_2021_SHARD\s*(\[[^\]]+\])',output)
        assert len(matches)==output.count('PASS_2021_SHARD')==1
        counts=ast.literal_eval(matches[0]);assert counts==search['shard_counts'][i]
        assert counts[:4]==[1536,i,4,4507] and counts[-1]==0
        rows=[json.loads(line) for line in Path(job['rows']).read_text().splitlines()]
        assert len(rows)==counts[5]
        assert all(r[0]==1536 and 408526598<=r[1]<=408544625 and (r[1]-408526598)%4==i for r in rows)
        allrows+=rows
    assert len(allrows)==len({r[1] for r in allrows})==5006
    assert sum(len(r[2])+len(r[3]) for r in allrows)==30414
    assert sum(len(r[2])*len(r[3]) for r in allrows)==26760
    native=native_controls.run()
    assert native==json.loads(Path('results/20.21-associativity-controls.json').read_text())
    assert kernel_controls.run()==json.loads(Path('results/20.21-order1536-kernel-controls.json').read_text())
    obs=json.loads(Path('results/20.21-order1536-final-process-observations.json').read_text())
    assert all(p['exit_code']==0 and p['tool_chunk'] for p in obs['processes'])
    print('PASS_2021_ORDER1536_PACKET',len(packet['sha256']),'catalogue=408641062 searched=18028 pairs=26760 lower_bound=3072')


if __name__=='__main__':run()
