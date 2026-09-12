#!/usr/bin/env python3
"""Independent integer-field and exhaustive affine-subgroup controls."""
import collections
import json
import math


class Field:
    def __init__(self, p, modulus):
        self.p = p
        self.modulus = modulus
        self.d = len(modulus)-1
        self.q = p**self.d
        self.digits = [tuple((i//p**j) % p for j in range(self.d)) for i in range(self.q)]
        self.add = [[sum(((a+b) % p)*p**j for j, (a,b) in
                         enumerate(zip(self.digits[x],self.digits[y])))
                     for y in range(self.q)] for x in range(self.q)]
        self.mul = [[self.multiply(x,y) for y in range(self.q)] for x in range(self.q)]
        self.neg = [next(y for y in range(self.q) if self.add[x][y] == 0) for x in range(self.q)]
        self.inv = [None]+[next(y for y in range(1,self.q) if self.mul[x][y] == 1)
                          for x in range(1,self.q)]

    def multiply(self,x,y):
        p,d=self.p,self.d
        v=[0]*(2*d-1)
        for i,a in enumerate(self.digits[x]):
            for j,b in enumerate(self.digits[y]):
                v[i+j]=(v[i+j]+a*b)%p
        for i in range(len(v)-1,d-1,-1):
            t=v[i]
            for j,b in enumerate(self.modulus):
                v[i-d+j]=(v[i-d+j]-t*b)%p
        return sum(v[i]*p**i for i in range(d))

    def check(self):
        q=self.q
        for a in range(q):
            assert self.add[a][0] == a and self.mul[a][1] == a
            for b in range(q):
                assert self.add[a][b] == self.add[b][a]
                assert self.mul[a][b] == self.mul[b][a]
                for c in range(q):
                    assert self.add[self.add[a][b]][c] == self.add[a][self.add[b][c]]
                    assert self.mul[self.mul[a][b]][c] == self.mul[a][self.mul[b][c]]
                    assert self.mul[a][self.add[b][c]] == self.add[self.mul[a][b]][self.mul[a][c]]
        return q**3


def subgroup_closure(generators, table):
    known={0}
    queue=[0]
    for x in queue:
        for g in generators:
            y=table[x][g]
            if y not in known:
                known.add(y)
                queue.append(y)
    return frozenset(known)


def all_subgroups(table):
    trivial=frozenset([0])
    generators={trivial:()}
    queue=[trivial]
    for h in queue:
        covered=set(h)
        for g in range(len(table)):
            if g in covered:
                continue
            # Elements h*g in this coset give the same generated extension.
            covered.update(table[x][g] for x in h)
            gens=generators[h]+(g,)
            k=subgroup_closure(gens,table)
            if k not in generators:
                generators[k]=gens
                queue.append(k)
    return generators


def check_affine(p,modulus):
    field=Field(p,modulus)
    triples=field.check()
    q=field.q
    elements=[(a,b) for a in range(1,q) for b in range(q)]
    positions={x:i for i,x in enumerate(elements)}
    table=[[positions[(field.mul[a][c],field.add[b][field.mul[a][d]])]
            for c,d in elements] for a,b in elements]
    inverse=[positions[(field.inv[a],field.neg[field.mul[field.inv[a]][b]])]
             for a,b in elements]
    for x in range(len(table)):
        assert table[x][inverse[x]] == table[inverse[x]][x] == 0
    groups=all_subgroups(table)
    histogram=collections.Counter()
    normals_checked=0
    for k,kgens in groups.items():
        u=sum(elements[x][0] == 1 for x in k)
        assert len(k)%u == 0 and math.gcd(len(k)//u,p) == 1
        best=len(k)
        for n,ngens in groups.items():
            if not n <= k or math.gcd(len(n),p) != 1:
                continue
            if any(table[x][y] != table[y][x] for x in ngens for y in ngens):
                continue
            if any(table[table[inverse[g]][x]][g] not in n for g in kgens for x in ngens):
                continue
            normals_checked+=1
            best=min(best,len(k)//len(n))
        assert best == (1 if u == 1 else len(k))
        assert best <= (1 if u == 1 else u*(u-1))
        histogram[(len(k),u,best)]+=1
    rows=[[*key,value] for key,value in sorted(histogram.items())]
    return dict(model=f"affine_{q}",order=len(table),p=p,subgroups=len(groups),
                histogram=rows,field_triples=triples,normal_abelian_candidates=normals_checked)


def main():
    models=[(2,[0,1]),(3,[0,1]),(2,[1,1,1]),(5,[0,1]),(7,[0,1]),
            (2,[1,1,0,1]),(3,[1,0,1]),(2,[1,1,0,0,1])]
    rows=[]
    for model in models:
        row=check_affine(*model)
        rows.append(row)
        print(json.dumps(row,sort_keys=True),flush=True)
    print("PASS_21_121B_INDEPENDENT models="+str(len(rows))+
          " subgroups="+str(sum(r['subgroups'] for r in rows))+
          " field_triples="+str(sum(r['field_triples'] for r in rows)))


if __name__ == '__main__':
    main()
