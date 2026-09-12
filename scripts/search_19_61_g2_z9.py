#!/usr/bin/env python3
"""Determine all Z/9 root closures from exact congruence-kernel spaces."""
import collections
import hashlib
import json
from pathlib import Path
import time
from linear_19_61_mod3 import Space


def run():
    started=time.monotonic()
    input_path=Path('results/19.61-g2z9-input.json')
    kernel_path=Path('results/19.61-g2z9-unit-kernels.json')
    data=json.loads(input_path.read_text());kernels=json.loads(kernel_path.read_text())
    cases={tuple(c['unit_row']):c for c in kernels['cases']}
    vectors=[bytes(v) for v in kernels['root_vectors']]
    assert len(cases)==217 and Space(vectors).rank()==12
    changes=[];orders=collections.Counter();ranks=collections.Counter();failures=[];rows=[]
    for index,row in enumerate(data['carpets'],1):
        unit_row=tuple(2 if x==2 else 1 for x in row)
        case=cases[unit_row]
        if case['full']:
            assert row==[2]*12
            closure=list(row);rank=None;order=None
        else:
            space=Space(case['kernel_basis'])
            for r,x in enumerate(row):
                if x==1:
                    for vector in case['root_modules'][r]:space.add(vector)
            closure=[2 if x==2 else int(space.contains(vectors[r])) for r,x in enumerate(row)]
            rank=space.rank();order=case['image_order']*3**rank
            ranks[rank]+=1;orders[order]+=1
        assert all(x<=y for x,y in zip(row,closure))
        bad=[i for i,(r,s,k,req) in enumerate(data['implications'])
             if req[closure[r]][closure[s]]&~data['masks'][closure[k]]]
        record=dict(index=index,unit_case=case['index'],closure=closure,kernel_rank=rank,order=order)
        rows.append(record)
        if closure!=row:changes.append(dict(record,initial=row))
        if bad:failures.append(dict(record,initial=row,failed_implications=bad))
    result=dict(carpets=len(rows),expanded=len(changes),failures=failures,changes=changes,
                rows=rows,proper_order_counts=dict(sorted(orders.items())),
                proper_kernel_rank_counts=dict(sorted(ranks.items())),
                input_sha256=hashlib.sha256(input_path.read_bytes()).hexdigest(),
                kernel_sha256=hashlib.sha256(kernel_path.read_bytes()).hexdigest(),
                elapsed_seconds=time.monotonic()-started)
    path=Path('results/19.61-g2z9-search.json');assert not path.exists()
    path.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_Z9_SEARCH',len(rows),len(changes),len(failures),'seconds',result['elapsed_seconds'],flush=True)


if __name__=='__main__':run()
