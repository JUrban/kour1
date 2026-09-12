#!/usr/bin/env python3
"""Derive carpets from all frozen finite inputs and compare their closures."""
import ast
import hashlib
import json
from pathlib import Path
from carpet_horn_19_61 import assigned


def run():
    reports=[];hashes={}
    for label in ['f2','f4','dual','split','z4','g2p2','g2p3','g2f4','g2dual','g2split','g2z4','g2f9']:
        path=Path('results/19.61-'+label+'-input.g')
        hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        rows=assigned(path,'Carpets1961');subsets=assigned(path,'Subsets1961')
        masks=assigned(path,'Masks1961');implications=assigned(path,'Implications1961')
        preparation=Path('results/19.61-'+label+'-preparation.json')
        hashes[str(preparation)]=hashlib.sha256(preparation.read_bytes()).hexdigest()
        data=json.loads(preparation.read_text());roots=data['roots']
        if label in ['g2p2','g2p3']:
            p=data['prime'];add=[[(a+b)%p for b in range(p)] for a in range(p)];mul=[[a*b%p for b in range(p)] for a in range(p)]
        else:add=data['add'];mul=data['mul']
        opposite=[roots.index([-v for v in r]) for r in roots]
        lookup={tuple(row):i for i,row in enumerate(rows,1)}
        changes={}
        paths=[Path('results/19.61-g2f9-shard'+str(i)+'-changes.grows') for i in range(4)] if label=='g2f9' else [Path('results/19.61-'+label+'-changes.grows')]
        for p in paths:
            hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
            for line in p.read_text().splitlines():
                r=ast.literal_eval(line);assert r[0] not in changes;changes[r[0]]=r
        join={v:min((i for i,m in enumerate(masks,1) if not v&~m),key=lambda i:len(subsets[i-1]))
              for v in range(1,1<<max(max(s) for s in subsets)+1,2)}
        for v,index in join.items():
            terms={t for t in range(len(add)) if v>>t&1}
            while True:
                more=terms|{add[a][b] for a in terms for b in terms}
                if more==terms:break
                terms=more
            assert sorted(terms)==subsets[index-1]
        hits=[];derived=set();square_failures=[]
        for index,row in enumerate(rows,1):
            required=[1]*len(row)
            for r,s,k,req in implications:required[k-1]|=req[row[r-1]-1][row[s-1]-1]
            result=tuple(join[v] for v in required);assert result in lookup
            target=lookup[result]
            if target not in derived:
                bad=[r for r in range(len(roots)) if any(mul[mul[t][t]][u] not in subsets[result[r]-1]
                     for t in subsets[result[r]-1] for u in subsets[result[opposite[r]]-1])]
                if bad:square_failures.append(dict(derived_index=target,roots=bad))
            derived.add(target)
            if target in changes:hits.append(dict(initial_index=index,initial=row,derived_index=target,derived=result,closure=changes[target][2]))
        report=dict(label=label,carpets=len(rows),distinct_derived=len(derived),hits=hits,square_failures=square_failures)
        reports.append(report);print('PASS_1962_DERIVED_SCREEN',label,len(rows),len(derived),len(hits),flush=True)
    return dict(rings=reports,input_sha256=hashes)


if __name__=='__main__':
    result=run();Path('results/19.62-derived-screen.json').write_text(json.dumps(result,indent=2)+'\n')
