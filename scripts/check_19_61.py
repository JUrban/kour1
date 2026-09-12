#!/usr/bin/env python3
"""Independent matrix enumeration controls; never calls GAP or its permutations."""
import ast
from collections import Counter
import json
from pathlib import Path


def assigned(path,name):
    line=next(s for s in path.read_text().splitlines() if s.startswith(name+':='))
    return json.loads(line[len(name)+2:-1])


def run():
    reports=[]
    for ring in ['f2','f4','dual','split','z4']:
        data=json.loads(Path(f'results/19.61-{ring}-preparation.json').read_text())
        path=Path(f'results/19.61-{ring}-input.g')
        carpets=assigned(path,'Carpets1961');implications=assigned(path,'Implications1961')
        subsets=data['additive_subgroups'];add=data['add'];mul=data['mul'];m=data['order']
        matrices=[[tuple(a) for a in row] for row in data['matrices']]
        ident=tuple(int(i==j) for i in range(4) for j in range(4))
        for a in range(m):
            assert add[a][0]==a and mul[a][1]==a
            for b in range(m):
                for c in range(m):
                    assert add[add[a][b]][c]==add[a][add[b][c]]
                    assert mul[mul[a][b]][c]==mul[a][mul[b][c]]
                    assert mul[a][add[b][c]]==add[mul[a][b]][mul[a][c]]
        changes={r[0]:r for r in [ast.literal_eval(line) for line in
                 Path(f'results/19.61-{ring}-changes.grows').read_text().splitlines()]}
        selected={i for i,row in enumerate(carpets,1) if ring=='f2' or sum(v!=1 for v in row)<=2}
        # One expansion of each observed group order, including non-field cases.
        by_order={}
        for i,r in sorted(changes.items()):by_order.setdefault(r[3],i)
        selected.update(by_order.values())
        assert len(selected)>0

        def bad_edges(row):
            return [j for j,(r,s,k,req) in enumerate(implications,1)
                    if req[row[r-1]-1][row[s-1]-1] & ~sum(1<<t for t in subsets[row[k-1]-1])]

        def group(row):
            gens=[]
            for r,opt in enumerate(row):
                covered={0};basis=[]
                for t in subsets[opt-1]:
                    if t in covered:continue
                    basis.append(t);todo=list(covered)
                    for a in todo:
                        b=add[a][t]
                        if b not in covered:covered.add(b);todo.append(b)
                    gens.append(matrices[r][t])
                assert covered==set(subsets[opt-1])
            columns=[[[ (k,g[4*k+j]) for k in range(4) if g[4*k+j]] for j in range(4)] for g in gens]
            known={ident};todo=[ident]
            for a in todo:
                for cols in columns:
                    b=[]
                    for i in range(4):
                        for col in cols:
                            v=0
                            for k,x in col:v=add[v][mul[a[4*i+k]][x]]
                            b.append(v)
                    b=tuple(b)
                    if b not in known:
                        known.add(b);todo.append(b)
                        assert len(known)<=50000,'unexpected control group; no capped pass allowed'
            closure=[subsets.index([t for t in range(m) if matrices[r][t] in known])+1 for r in range(8)]
            return known,closure

        states=0;expanded=0;orders=Counter()
        for i in sorted(selected):
            row=carpets[i-1];assert not bad_edges(row)
            known,closure=group(row)
            expected=changes[i][2] if i in changes else row
            assert closure==expected,(ring,i,closure,expected)
            assert not bad_edges(closure)
            if i in changes:
                assert len(known)==changes[i][3];expanded+=1
            states+=len(known);orders[len(known)]+=1
        mutation=None
        if ring=='f2':
            row=[1]*8
            row[data['roots'].index([1,-1])]=2
            row[data['roots'].index([0,2])]=2
            known,closure=group(row)
            assert len(known)==8 and bad_edges(row) and bad_edges(closure)
            mutation=dict(group_order=8,initial_is_carpet=False,closure_is_carpet=False,
                          bad_implications=bad_edges(closure))
        reports.append(dict(ring=ring,cases=len(selected),ids=sorted(selected),
                            expanded_controls=expanded,enumerated_matrix_states=states,
                            group_order_counts=dict(sorted(orders.items())),mutation=mutation))
    return dict(rings=reports,cases=sum(r['cases'] for r in reports),
                expanded_controls=sum(r['expanded_controls'] for r in reports),
                matrix_states=sum(r['enumerated_matrix_states'] for r in reports))


if __name__=='__main__':
    out=run();Path('results/19.61-controls.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS_1961_CONTROLS',json.dumps({k:v for k,v in out.items() if k!='rings'}))
