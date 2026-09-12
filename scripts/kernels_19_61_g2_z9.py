#!/usr/bin/env python3
"""Exact Schreier kernels for every proper prime-field root carpet lifted to Z/9."""
import ast
import hashlib
import json
from pathlib import Path
import time
from carpet_horn_19_61 import assigned
from linear_19_61_mod3 import Space
from matrices_19_61_mod9 import Matrices,IDENTITY,roots_mod9


def run():
    native=Matrices();mm=native.multiply;roots,matrices=roots_mod9()
    reduced=[[bytes(x%3 for x in a) for a in row] for row in matrices]
    vectors=[bytes(((a-b)%9)//3 for a,b in zip(row[3],IDENTITY)) for row in matrices]
    assert Space(vectors).rank()==12
    source=Path('results/19.61-g2p3-input.g');carpets=assigned(source,'Carpets1961')
    orders=dict(ast.literal_eval(line) for line in Path('results/19.61-g2p3-orders.grows').read_text().splitlines())
    reports=[];total_states=total_edges=0;started=time.monotonic()
    for index,row in enumerate(carpets,1):
        if row==[2]*12:
            reports.append(dict(index=index,unit_row=row,full=True));continue
        units=[r for r,x in enumerate(row) if x==2]
        known={IDENTITY:(IDENTITY,IDENTITY)};todo=[IDENTITY];space=Space();edges=0
        for bar in todo:
            lift,inverse=known[bar]
            for r in units:
                next_lift=mm(lift,matrices[r][1]);next_bar=bytes(x%3 for x in next_lift);edges+=1
                if next_bar not in known:
                    next_inverse=mm(matrices[r][8],inverse)
                    assert mm(next_lift,next_inverse)==IDENTITY
                    known[next_bar]=(next_lift,next_inverse);todo.append(next_bar)
                    assert len(known)<=20000,'no truncated transversal accepted'
                else:
                    representative,representative_inverse=known[next_bar]
                    if next_lift==representative:continue
                    delta=bytes(((a-b)%9)//3 for a,b in zip(next_lift,representative))
                    inv_bar=bytes(x%3 for x in representative_inverse)
                    vector=mm(inv_bar,delta,3)
                    space.add(vector)
        assert len(known)==orders[index]
        assert all((reduced[r][1] in known)==(row[r]==2) for r in range(12))
        basis=space.basis()
        for vector in basis:
            for r in units:assert space.contains(mm(mm(reduced[r][2],vector,3),reduced[r][1],3))
        assert all(space.contains(vectors[r]) for r in units)
        modules=[]
        for r in range(12):
            module=Space(basis);first=module.add(vectors[r]);pending=[] if first is None else [first]
            for vector in pending:
                for s in units:
                    image=mm(mm(reduced[s][2],vector,3),reduced[s][1],3)
                    added=module.add(image)
                    if added is not None:pending.append(added)
            modules.append([list(v) for v in module.basis()])
        reports.append(dict(index=index,unit_row=row,full=False,image_order=len(known),schreier_edges=edges,
                            kernel_rank=space.rank(),kernel_basis=[list(v) for v in basis],root_modules=modules))
        total_states+=len(known);total_edges+=edges
        print('PROGRESS_1961_Z9_KERNEL',index,len(known),space.rank(),flush=True)
    assert total_states==109693 and len(reports)==217
    result=dict(cases=reports,matrix_states=total_states,schreier_edges=total_edges,root_vectors=[list(v) for v in vectors],
                prime_input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),elapsed_seconds=time.monotonic()-started)
    Path('results/19.61-g2z9-unit-kernels.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_Z9_KERNELS',len(reports),total_states,total_edges,'seconds',result['elapsed_seconds'],flush=True)


if __name__=='__main__':run()
