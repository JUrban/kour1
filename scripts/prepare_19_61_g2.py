#!/usr/bin/env python3
"""Validate integral G2 root operators and prepare both bad-prime carpet inputs."""
import ast
import hashlib
import itertools
import json
from math import factorial
from pathlib import Path
import time

D=14


def main():
    source=Path('results/19.61-g2-integral.grows')
    roots,powers,adj,cartan=ast.literal_eval(source.read_text())
    assert len(roots)==12 and len(adj)==14 and cartan==[[2,-1],[-3,2]]
    ident=tuple(int(i==j) for i in range(D) for j in range(D))
    flatten=lambda a:tuple(x for row in a for x in row)
    adj=list(map(flatten,adj));powers=[[flatten(a) for a in row] for row in powers]
    columns={}

    def cols(a):
        if a not in columns:columns[a]=[[(k,a[D*k+j]) for k in range(D) if a[D*k+j]] for j in range(D)]
        return columns[a]

    def mm(a,b,p=0):
        out=tuple(sum(a[D*i+k]*x for k,x in col) for i in range(D) for col in cols(b))
        return tuple(x%p for x in out) if p else out

    brackets={(i,j):[(k,adj[i][D*k+j]) for k in range(D) if adj[i][D*k+j]]
              for i in range(D) for j in range(D)}
    for i in range(D):
        for j in range(D):
            assert all(adj[i][D*k+j]==-adj[j][D*k+i] for k in range(D))
            for k in range(D):
                value=[0]*D
                for a,b,c in [(i,j,k),(j,k,i),(k,i,j)]:
                    for h,v in brackets[a,b]:
                        for z,w in brackets[h,c]:value[z]+=v*w
                assert not any(value)
    for r in range(12):
        for i in range(2):
            assert [adj[12+i][D*k+r] for k in range(D)]==[roots[r][i]*int(k==r) for k in range(D)]
        a=ident
        for k,power in enumerate(powers[r]):
            assert tuple(factorial(k)*v for v in power)==a
            a=mm(a,adj[r])
        assert not any(a)
    for prime in [2,3]:
        started=time.monotonic();label=f'g2p{prime}';columns.clear()
        matrices=[[tuple(sum(pow(t,k)*row[k][v] for k in range(len(row)))%prime for v in range(D*D))
                   for t in range(prime)] for row in powers]
        for row in matrices:
            assert len(set(row))==prime
            for t,u in itertools.product(range(prime),repeat=2):assert mm(row[t],row[u],prime)==row[(t+u)%prime]
        subsets=[[0],list(range(prime))];masks=[1,(1<<prime)-1];implications=[];checks=0
        for ri,r in enumerate(roots):
            for si,s in enumerate(roots):
                if r==s or r==[-x for x in s]:continue
                terms=[]
                for i,j in itertools.product(range(1,4),repeat=2):
                    v=[i*r[k]+j*s[k] for k in range(2)]
                    if v in roots:terms.append((i+j,i,j,roots.index(v)))
                terms.sort();dest=[t[-1] for t in terms]
                assert len(dest)<=4 and len(set(dest))==len(dest)
                normal={}
                for coeff in itertools.product(range(prime),repeat=len(dest)):
                    a=ident
                    for k,v in zip(dest,coeff):a=mm(a,matrices[k][v],prime)
                    assert a not in normal;normal[a]=coeff
                factors={}
                for t,u in itertools.product(range(prime),repeat=2):
                    a=mm(mm(mm(matrices[ri][-t%prime],matrices[si][-u%prime],prime),matrices[ri][t],prime),matrices[si][u],prime)
                    assert a in normal,(prime,r,s,t,u)
                    factors[t,u]=normal[a];checks+=1
                for pos,k in enumerate(dest):
                    req=[[sum(1<<v for v in {factors[t,u][pos] for t in a for u in b}) for b in subsets] for a in subsets]
                    if any(v!=1 for row in req for v in row):implications.append([ri+1,si+1,k+1,req])
        carpets=[]
        for row in itertools.product(range(2),repeat=12):
            if all(not req[row[r-1]][row[s-1]] & ~masks[row[k-1]] for r,s,k,req in implications):
                carpets.append([v+1 for v in row])
        gens=[row[1] for row in matrices]

        def act(v,a):return tuple(sum(v[k]*x for k,x in col)%prime for col in cols(a))

        orbits=[];orbit_reports=[]
        for start in [0,1]:
            vector=tuple(int(i==start) for i in range(D));seen={vector};todo=[vector];capped=False
            for v in todo:
                for a in gens:
                    w=act(v,a)
                    if w not in seen:
                        seen.add(w);todo.append(w)
                        if len(seen)>10000:capped=True;break
                if capped:break
            orbit_reports.append(dict(start_basis_vector=start,size=len(seen),complete=not capped))
            if not capped:orbits.append(sorted(seen))
        assert orbits
        orbit=min(orbits,key=len);lookup={v:i+1 for i,v in enumerate(orbit)}
        perms=[[[lookup[act(v,a)] for v in orbit] for a in row] for row in matrices]
        assert all(sorted(p)==list(range(1,len(orbit)+1)) for row in perms for p in row)
        path=Path(f'results/19.61-{label}-input.g');assert not path.exists()
        j=lambda v:json.dumps(v,separators=(',',':'))
        text='RingLabel1961:='+j(label)+';\nSubsets1961:='+j(subsets)+';\nMasks1961:='+j(masks)+';\n'
        text+='Implications1961:='+j(implications)+';\nCarpets1961:='+j(carpets)+';\n'
        text+='RootPerms1961:=List('+j(perms)+', row->List(row,PermList));\n'
        text+=f'ExpectedOrder1961:={prime**6*(prime**6-1)*(prime**2-1)};\n'
        path.write_text(text)
        report=dict(prime=prime,roots=roots,matrices=matrices,orbits=orbit_reports,chosen_orbit=orbit,
                    carpets=len(carpets),assignments=4096,implications=len(implications),commutator_checks=checks,
                    jacobi_basis_triples=14**3,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    elapsed_seconds=time.monotonic()-started)
        Path(f'results/19.61-{label}-preparation.json').write_text(json.dumps(report,indent=2)+'\n')
        print('PASS_1961_G2_PREPARATION',label,'carpets',len(carpets),'degree',len(orbit),'seconds',report['elapsed_seconds'],flush=True)


if __name__=='__main__':main()
