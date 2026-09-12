#!/usr/bin/env python3
"""Enumerate finite carpets as closed sets of root-parameter atoms."""
import json
from pathlib import Path
import time


def assigned(path,name):
    line=next(s for s in path.read_text().splitlines() if s.startswith(name+':='))
    return json.loads(line[len(name)+2:-1])


class CarpetClosure:
    def __init__(self,roots,add,subsets,implications):
        self.roots=roots;self.m=len(add);self.subsets=subsets
        self.n=roots*(self.m-1)
        bit=lambda r,t:0 if t==0 else 1<<(r*(self.m-1)+t-1)
        rules={}
        def rule(premise,conclusion):
            conclusion &= ~premise
            if conclusion:rules[premise]=rules.get(premise,0)|conclusion
        for r in range(roots):
            for a in range(1,self.m):
                for b in range(1,self.m):rule(bit(r,a)|bit(r,b),bit(r,add[a][b]))
        cyclic=[None]+[min((i for i,s in enumerate(subsets) if t in s),key=lambda i:len(subsets[i]))
                       for t in range(1,self.m)]
        for r,s,k,req in implications:
            r-=1;s-=1;k-=1
            for a in range(1,self.m):
                for b in range(1,self.m):
                    mask=req[cyclic[a]][cyclic[b]]
                    out=sum(bit(k,t) for t in range(1,self.m) if mask>>t&1)
                    rule(bit(r,a)|bit(s,b),out)
        self.rules=sorted(rules.items());self.trigger=[[] for _ in range(self.n)]
        for premise,out in self.rules:
            assert premise.bit_count() in [1,2]
            pending=premise
            while pending:
                low=pending&-pending;pending-=low
                self.trigger[low.bit_length()-1].append((premise^low,out))
        self.mask_to_subset={sum(1<<(t-1) for t in s if t):i+1 for i,s in enumerate(subsets)}

    def close(self,value):
        pending=value
        while pending:
            low=pending&-pending;pending-=low
            for other,out in self.trigger[low.bit_length()-1]:
                if value&other==other:
                    new=out&~value;value|=new;pending|=new
        return value

    def closed_sets(self):
        value=self.close(0)
        yield value
        while True:
            for i in range(self.n-1,-1,-1):
                bit=1<<i
                if value&bit:continue
                prefix=bit-1
                candidate=self.close((value&prefix)|bit)
                if candidate&prefix==value&prefix:
                    value=candidate;yield value;break
            else:return

    def row(self,value):
        mask=(1<<(self.m-1))-1
        return tuple(self.mask_to_subset[(value>>(r*(self.m-1)))&mask] for r in range(self.roots))


def controls():
    reports=[]
    for label in ['f2','f4','dual','split','z4','g2p2','g2p3']:
        started=time.monotonic();path=Path(f'results/19.61-{label}-input.g')
        data=json.loads(Path(f'results/19.61-{label}-preparation.json').read_text())
        if label.startswith('g2'):
            p=data['prime'];add=[[(a+b)%p for b in range(p)] for a in range(p)]
        else:add=data['add']
        c=CarpetClosure(len(data['roots']),add,assigned(path,'Subsets1961'),assigned(path,'Implications1961'))
        expected=set(map(tuple,assigned(path,'Carpets1961')))
        seen=set()
        for value in c.closed_sets():
            assert c.close(value)==value
            assert all(value&a!=a or value&b==b for a,b in c.rules)
            row=c.row(value);assert row in expected and row not in seen;seen.add(row)
        assert seen==expected
        report=dict(label=label,carpets=len(seen),atoms=c.n,rules=len(c.rules),elapsed_seconds=time.monotonic()-started)
        reports.append(report);print('PASS_1961_HORN_CONTROL',json.dumps(report),flush=True)
    return dict(carpets=sum(r['carpets'] for r in reports),rings=reports)


if __name__=='__main__':
    result=controls();Path('results/19.61-horn-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_1961_HORN_ALL',result['carpets'])
