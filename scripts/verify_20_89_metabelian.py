#!/usr/bin/env python3
"""Independent normal forms and orbit walks; no GAP data imported."""
import collections
import itertools
import json


def dihedral(n):
    xs=list(itertools.product(range(n),range(2)))
    return xs,lambda x,y:((x[0]+(-1)**x[1]*y[0])%n,(x[1]+y[1])%2)


def affine4():
    def mul4(x,y):
        z=0
        while y:
            if y&1:z^=x
            y>>=1;x<<=1
            if x&4:x^=7
        return z
    return list(itertools.product(range(4),range(3))),lambda x,y:(x[0]^mul4([1,2,3][x[1]],y[0]),(x[1]+y[1])%3)


def heisenberg():
    return list(itertools.product(range(3),repeat=3)),lambda x,y:((x[0]+y[0])%3,(x[1]+y[1])%3,(x[2]+y[2]+x[0]*y[1])%3)


def wreath():
    def product(x,y):
        v=y[:2] if x[2]==0 else y[:2][::-1]
        return ((x[0]+v[0])%3,(x[1]+v[1])%3,(x[2]+y[2])%2)
    return list(itertools.product(range(3),range(3),range(2))),product


def analyze(label,data,metabelian=True):
    xs,mul=data;n=len(xs);idx={x:i for i,x in enumerate(xs)}
    tab=[[idx[mul(x,y)] for y in xs] for x in xs]
    identity=next(e for e in range(n) if all(tab[e][x]==tab[x][e]==x for x in range(n)))
    inv=[next(y for y in range(n) if tab[x][y]==tab[y][x]==identity) for x in range(n)]
    for a,b,c in itertools.product(range(n),repeat=3):
        assert tab[tab[a][b]][c]==tab[a][tab[b][c]]
    comm=lambda x,a:tab[tab[tab[inv[x]][inv[a]]][x]][a]
    def generated(seed):
        s={identity};q=[identity];letters=set(seed)|{inv[x] for x in seed}
        for x in q:
            for a in letters:
                z=tab[x][a]
                if z not in s:s.add(z);q.append(z)
        return s
    derived=generated({comm(x,y) for x in range(n) for y in range(n)})
    assert all(comm(x,y)==identity for x in derived for y in derived)==metabelian
    sinks=[]
    for a in range(n):
        sink=set()
        for x in range(n):
            path=[];positions={}
            while x not in positions:
                positions[x]=len(path);path.append(x);x=comm(x,a)
            sink.update(path[positions[x]:])
        sinks.append(sink)
    if metabelian:
        for a in range(n):
            assert generated(sinks[a])==sinks[a]
            assert sinks[inv[a]]==sinks[a]
            assert all(tab[tab[inv[g]][x]][g] in sinks[a] for g in range(n) for x in sinks[a])
        for a,b in itertools.product(range(n),repeat=2):
            assert sinks[tab[a][b]]<={tab[x][y] for x in sinks[a] for y in sinks[b]}
    else:
        bad=[a for a in range(n) if generated(sinks[a])!=sinks[a]]
        assert bad
    hist=sorted(collections.Counter(map(len,sinks)).items())
    return [label,n,len(derived),hist,n*n,n**3],sinks


rows=[]
for n in [3,4,5,6,15]:rows.append(analyze('D'+str(2*n),dihedral(n))[0])
for label,data in [('A4',affine4()),('H27',heisenberg()),('W18',wreath())]:rows.append(analyze(label,data)[0])
perms=list(itertools.permutations(range(4)))
s4=lambda x,y:tuple(y[x[i]] for i in range(4))
control,sinks=analyze('S4',(perms,s4),False)

family=[]
for r in range(9):
    for m in [1,3,5,15]:
        n=2**r*m
        # A separate integer periodic-point test, with no group table.
        periodic=[];maximum_tail=0
        for x in range(n):
            seen={};path=[];y=x
            while y not in seen:
                seen[y]=len(path);path.append(y);y=(-2*y)%n
            if seen[y]==0:periodic.append(x)
            maximum_tail=max(maximum_tail,seen[y])
        assert periodic==list(range(0,n,2**r))
        assert maximum_tail==r
        family.append([r,m,n,len(periodic),maximum_tail])

assert family[[r[:2] for r in family].index([0,3])][3]==3 # sink need not be trivial
assert [next(z[3] for z in family if z[:2]==[0,m]) for m in [1,3,5,15]]==[1,3,5,15]
# An actual counterexample to the claimed uniform time for Prüfer 2-torsion.
assert all(((-2)**r)%(2**(r+1))!=0 for r in range(20))
print(json.dumps(dict(rows=rows,nonmetabelian_control=control,dihedral_family=family,
    rejected_mutations=['all finite-group sinks are subgroups','all almost Engel sinks are trivial',
                        'bounded entry time for Prüfer 2-torsion','finite dihedral tests give a uniform sink']),sort_keys=True))
print('PASS_20_89_METABELIAN_WORDS')
