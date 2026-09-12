#!/usr/bin/env python3
"""Direct matrix controls for sparse carpets and small enlargement types."""
import ast
import json
from pathlib import Path
from carpet_horn_19_61 import assigned
from check_19_61_g2 import rank

D=14


def run():
    reports=[];ident=tuple(int(i==j) for i in range(D) for j in range(D))
    for label in ['g2f9']:
        data=json.loads(Path(f'results/19.61-{label}-preparation.json').read_text())
        path=Path(f'results/19.61-{label}-input.g')
        rows=assigned(path,'Carpets1961');subsets=assigned(path,'Subsets1961')
        masks=assigned(path,'Masks1961');implications=assigned(path,'Implications1961')
        matrices=[[tuple(a) for a in row] for row in data['matrices']]
        adds=data['add'];muls=data['mul'];m=len(adds)
        neg=[next(b for b in range(m) if adds[a][b]==0) for a in range(m)]
        # Independently reconstruct every root action on the seven-dimensional module.
        basis=data['invariant_basis'];assert len(basis)==7 and rank(basis,3)==7
        restricted=data['restricted_matrices']
        for r,row in enumerate(matrices):
            for t,mat in enumerate(row):
                small=restricted[r][t]
                for i,v in enumerate(basis):
                    image=[0]*D;rebuilt=[0]*D
                    for j in range(D):
                        for k in range(D):image[j]=adds[image[j]][muls[v[k]][mat[D*k+j]]]
                        for k in range(7):rebuilt[j]=adds[rebuilt[j]][muls[small[7*i+k]][basis[k][j]]]
                    assert image==rebuilt
        search=json.loads(Path('results/19.61-g2f9-sharded-summary.json').read_text())
        assert search['status']=='COMPLETE_NO_FAILURE'
        changes={}
        for job in search['jobs']:
            assert job['returncode']==0
            for line in Path(job['changes']).read_text().splitlines():
                row=ast.literal_eval(line);assert row[0] not in changes;changes[row[0]]=row
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
                    selected_indices=sorted(selected),invariant_module_actions_verified=True)
        reports.append(report);print('PASS_1961_G2_F9_MATRIX_CONTROL',label,len(selected),states,flush=True)
    return dict(rings=reports,cases=sum(r['cases'] for r in reports),expanded=sum(r['expanded'] for r in reports),
                matrix_states=sum(r['matrix_states'] for r in reports))


if __name__=='__main__':
    result=run();Path('results/19.61-g2f9-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_G2_F9_CONTROLS',result['cases'],result['expanded'],result['matrix_states'])
