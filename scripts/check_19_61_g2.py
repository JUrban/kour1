#!/usr/bin/env python3
"""Enumerate every proper G2 prime-field carpet subgroup as actual matrices."""
import ast
import json
from pathlib import Path

D=14


def assigned(path,name):
    line=next(s for s in path.read_text().splitlines() if s.startswith(name+':='))
    return json.loads(line[len(name)+2:-1])


def rank(rows,p):
    basis={}
    for row in rows:
        a=list(row)
        for i,b in sorted(basis.items()):
            c=a[i]
            if c:a=[(v-c*w)%p for v,w in zip(a,b)]
        if any(a):
            i=next(i for i,v in enumerate(a) if v);c=pow(a[i],-1,p)
            basis[i]=[(c*v)%p for v in a]
    return len(basis)


def run():
    reports=[]
    ident=tuple(int(i==j) for i in range(D) for j in range(D))
    for p in [2,3]:
        label=f'g2p{p}';data=json.loads(Path(f'results/19.61-{label}-preparation.json').read_text())
        source=Path(f'results/19.61-{label}-input.g');rows=assigned(source,'Carpets1961')
        implications=assigned(source,'Implications1961')
        matrices=[[tuple(a) for a in row] for row in data['matrices']]
        expected=dict(ast.literal_eval(line) for line in Path(f'results/19.61-{label}-orders.grows').read_text().splitlines())
        assert len(expected)==len(rows)==data['carpets']
        masks=[1,(1<<p)-1];states=0;full=0;cases=0
        # Matrix multiplication uses deviations from the identity. No permutation data.
        operators=[]
        for row in matrices:
            a=row[1];op=[]
            for j in range(D):
                delta=[(k,(a[D*k+j]-int(k==j))%p) for k in range(D)
                       if (a[D*k+j]-int(k==j))%p]
                if delta:op.append((j,delta))
            operators.append(op)
        for index,row in enumerate(rows,1):
            assert all(not req[row[r-1]-1][row[s-1]-1] & ~masks[row[k-1]-1]
                       for r,s,k,req in implications)
            if p==3 and row==[2]*12:
                # Full parameter sets have full closure by definition, without
                # enumerating all4,245,696 ambient matrices.
                assert expected[index]==4245696;full+=1;continue
            ops=[operators[r] for r,v in enumerate(row) if v==2]
            known={ident};todo=[ident]
            for a in todo:
                for op in ops:
                    b=list(a)
                    for j,delta in op:
                        for i in range(D):
                            base=D*i+j
                            b[base]=(a[base]+sum(a[D*i+k]*v for k,v in delta))%p
                    b=tuple(b)
                    if b not in known:
                        known.add(b);todo.append(b)
                        assert len(known)<=20000,'no capped result is accepted'
            assert len(known)==expected[index],(label,index,len(known),expected[index])
            for r in range(12):
                actual=[t for t in range(p) if matrices[r][t] in known]
                assert actual==([0] if row[r]==1 else list(range(p))),(label,index,r)
            states+=len(known);cases+=1
        reports.append(dict(label=label,enumerated_cases=cases,full_parameter_cases=full,
                            matrix_states=states,orbit_span_rank=rank(data['chosen_orbit'],p)))
    return dict(rings=reports,enumerated_cases=sum(r['enumerated_cases'] for r in reports),
                full_parameter_cases=sum(r['full_parameter_cases'] for r in reports),
                matrix_states=sum(r['matrix_states'] for r in reports))


if __name__=='__main__':
    result=run();Path('results/19.61-g2-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_G2_CONTROLS',json.dumps(result,sort_keys=True))
