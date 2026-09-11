#!/usr/bin/env python3
"""Compare the actual C++ cyclicity routine with independent Krylov tests."""
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import math
import random
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
RNG=random.Random(1695)

def rank(vectors,n):
    # Row reduction by columns, independent of the C++ leading-bit routine.
    rows=[[v>>i&1 for v in vectors] for i in range(n)]
    r=0
    for j in range(len(vectors)):
        pivot=next((i for i in range(r,n) if rows[i][j]),None)
        if pivot is None: continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        for i in range(r+1,n):
            if rows[i][j]: rows[i]=[x^y for x,y in zip(rows[i],rows[r])]
        r+=1
        if r==n: return r
    return r

def krylov_cyclic(a):
    n=len(a)
    # A cyclic operator has a cyclic vector; search every nonzero vector.
    for v in range(1,1<<n):
        powers=[]
        for _ in range(n):
            powers.append(v)
            v=sum((sum((a[j]>>i&1)*(v>>j&1) for j in range(n))&1)<<i
                  for i in range(n))
        if rank(powers,n)==n: return True
    return False

def main():
    cases=[];counts={}
    for n in range(1,5):
        count=0
        for a in product(range(1<<n),repeat=n):
            if rank(a,n)==n:
                cases.append(a);count+=1
        expected=math.prod((1<<n)-(1<<i) for i in range(n))
        assert count==expected
        counts[n]=count
    # Controls include singular matrices: the cyclicity test does not require
    # invertibility, although the search itself only considers invertible input.
    for n in [5,6]:
        cases.extend(tuple(RNG.randrange(1<<n) for _ in range(n)) for _ in range(1000))
    cases.extend(tuple(1<<i for i in range(n)) for n in range(1,7))
    cases.extend((0,)*n for n in range(1,7))
    harness='''#define main search_main
#include "SOURCE"
#undef main
int main() {
    unsigned n;
    while(std::cin>>n) {
        Matrix a{};
        for(unsigned i=0;i<n;++i)std::cin>>a[i];
        std::cout<<cyclic(a,n)<<'\\n';
    }
    return 0;
}
'''.replace('SOURCE',str(ROOT/'scripts/search_16_95.cpp'))
    with TemporaryDirectory(prefix='verify1695-') as tmp:
        src=Path(tmp)/'check.cpp';binary=Path(tmp)/'check'
        src.write_text(harness)
        subprocess.run(['g++','-O2','-std=c++20',str(src),'-o',str(binary)],check=True)
        data=''.join(str(len(a))+' '+' '.join(map(str,a))+'\n' for a in cases)
        output=subprocess.run([str(binary)],input=data,text=True,capture_output=True,check=True)
        observed=output.stdout.splitlines()
    assert len(observed)==len(cases)
    cyclic_count=0
    for a,value in zip(cases,observed):
        expected=krylov_cyclic(a)
        assert value==str(int(expected)),(a,value,expected)
        cyclic_count+=expected
    log=(ROOT/'results/16.95-f2-through6.log').read_text()
    dimensions=[]
    for line in log.splitlines():
        if not line.startswith('DIMENSION_DONE'):continue
        d={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',line)}
        n=d['n'];expected=math.prod((1<<n)-(1<<i) for i in range(n))//math.factorial(n)
        assert d['bases']==d['expected']==expected and d['hits']==0
        assert d['bases']<=d['tests']<=d['bases']*math.factorial(n)
        assert 1<=d['max_tests']<=math.factorial(n) and line.endswith(' PASS')
        dimensions.append(d)
    assert [d['n'] for d in dimensions]==list(range(1,7))
    total_bases=sum(d['bases'] for d in dimensions)
    total_tests=sum(d['tests'] for d in dimensions)
    assert log.splitlines()[-1]==f'DONE bases={total_bases} tests={total_tests} hits=0 PASS'
    result=dict(problem='16.95',status='PASS',exhaustive_GL_counts=counts,
                independent_cyclicity_controls=len(cases),cyclic_controls=cyclic_count,
                unordered_bases=total_bases,permuted_matrices_tested=total_tests,
                dimensions=dimensions,
                scope='All invertible binary matrices in dimensions1..6, modulo column permutations. Bounded evidence only.')
    (ROOT/'results/16.95-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
