#!/usr/bin/env python3
"""Direct matrix controls for sparse carpets and small enlargement types."""
import ast
import json
from pathlib import Path
from carpet_horn_19_61 import assigned

D=14


def run():
    reports=[];ident=tuple(int(i==j) for i in range(D) for j in range(D))
    for label in ['g2f4','g2dual','g2split','g2z4']:
        data=json.loads(Path(f'results/19.61-{label}-preparation.json').read_text())
        path=Path(f'results/19.61-{label}-input.g')
        rows=assigned(path,'Carpets1961');subsets=assigned(path,'Subsets1961')
        masks=assigned(path,'Masks1961');implications=assigned(path,'Implications1961')
        matrices=[[tuple(a) for a in row] for row in data['matrices']]
        adds=data['add'];muls=data['mul'];m=len(adds)
        neg=[next(b for b in range(m) if adds[a][b]==0) for a in range(m)]
        # Check the explicit spanning witness by Gaussian elimination over the ring.
        witness=data['spanning_witness'];assert len(witness)==D
        orbit=set(map(tuple,data['orbit']));assert all(tuple(v) in orbit for v in witness)
        work=[list(v) for v in witness]
        units={a:next(b for b in range(m) if muls[a][b]==1) for a in range(m) if 1 in muls[a]}
        for i in range(D):
            j=next(j for j in range(i,D) if work[j][i] in units)
            work[i],work[j]=work[j],work[i]
            inv=units[work[i][i]];work[i]=[muls[inv][v] for v in work[i]]
            for j in range(D):
                if j==i:continue
                c=neg[work[j][i]];work[j]=[adds[v][muls[c][w]] for v,w in zip(work[j],work[i])]
        assert tuple(x for row in work for x in row)==ident
        changes={r[0]:r for r in (ast.literal_eval(line) for line in Path(f'results/19.61-{label}-changes.grows').read_text().splitlines())}
        selected={i for i,row in enumerate(rows,1) if sum(v!=1 for v in row)<=2}
        by_order={}
        for i,entry in changes.items():
            if entry[3]<=20000:by_order.setdefault(entry[3],i)
        selected.update(by_order.values())
        operators={}
        for r,row in enumerate(matrices):
            for t,a in enumerate(row):
                op=[]
                for j in range(D):
                    delta=[(k,adds[a[D*k+j]][neg[int(k==j)]]) for k in range(D)
                           if adds[a[D*k+j]][neg[int(k==j)]]]
                    if delta:op.append((j,delta))
                operators[r,t]=op
        def carpet(row):return all(not req[row[r-1]-1][row[s-1]-1]&~masks[row[k-1]-1] for r,s,k,req in implications)
        states=0;expanded=0;hist={};max_order=0
        for index in sorted(selected):
            row=rows[index-1];assert carpet(row)
            ops=[operators[r,t] for r,v in enumerate(row) for t in subsets[v-1] if t]
            known={ident};todo=[ident]
            for a in todo:
                for op in ops:
                    b=list(a)
                    for j,delta in op:
                        for i in range(D):
                            value=a[D*i+j]
                            for k,v in delta:value=adds[value][muls[a[D*i+k]][v]]
                            b[D*i+j]=value
                    b=tuple(b)
                    if b not in known:
                        known.add(b);todo.append(b)
                        assert len(known)<=20000,('uncertified cap',label,index)
            actual=[]
            for r in range(12):
                parameters=[t for t in range(m) if matrices[r][t] in known]
                actual.append(subsets.index(parameters)+1)
            expected=changes[index][2] if index in changes else row
            assert actual==expected and carpet(actual),(label,index,actual,expected)
            if index in changes:
                assert len(known)==changes[index][3];expanded+=1
            states+=len(known);max_order=max(max_order,len(known));hist[len(known)]=hist.get(len(known),0)+1
        report=dict(label=label,cases=len(selected),expanded=expanded,matrix_states=states,
                    largest_group=max_order,small_enlargement_orders=sorted(by_order),group_order_histogram=hist,
                    selected_indices=sorted(selected),spanning_witness_verified=True)
        reports.append(report);print('PASS_1961_G2_RING_CONTROLS',label,len(selected),states,flush=True)
    return dict(rings=reports,cases=sum(r['cases'] for r in reports),expanded=sum(r['expanded'] for r in reports),
                matrix_states=sum(r['matrix_states'] for r in reports))


if __name__=='__main__':
    result=run();Path('results/19.61-g2-rings-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_G2_RINGS_CONTROLS',result['cases'],result['expanded'],result['matrix_states'])
