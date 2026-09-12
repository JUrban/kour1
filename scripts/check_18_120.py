#!/usr/bin/env python3
"""Independent table reconstruction of all factorization tests in four groups."""
import json,time
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
def members(h):
 while h:
  b=h&-h;yield b.bit_length()-1;h-=b

def check(data):
 t=data['table'];n=len(t);e=data['identity'];one=1<<e;full=(1<<n)-1
 assert n==data['order'] and all(sorted(row)==list(range(n)) for row in t)
 assert t[e]==list(range(n)) and all(t[x][e]==x for x in range(n))
 inv=[next(y for y in range(n) if t[x][y]==e) for x in range(n)]
 for x in range(n):
  assert t[inv[x]][x]==e
  for y in range(n):
   for z in range(n):assert t[t[x][y]][z]==t[x][t[y][z]]
 def closure(gens):
  gens=tuple(set(gens));seen=one;q=[e]
  for x in q:
   for a in gens:
    y=t[x][a]
    if not seen>>y&1:seen|=1<<y;q.append(y)
  return seen
 subgens={one:()};pending=deque([one])
 while pending:
  h=pending.popleft();hs=list(members(h));covered=h
  for x in range(n):
   if covered>>x&1:continue
   for y in hs:covered|=1<<t[y][x]
   gens=subgens[h]+(x,);k=closure(gens)
   if k not in subgens:subgens[k]=gens;pending.append(k)
  assert covered==full
 def comm(x,y):return t[t[t[inv[x]][inv[y]]][x]][y]
 ab={h:all(t[x][y]==t[y][x] for x in gs for y in gs) for h,gs in subgens.items()}
 # Compute the full lower central series independently from the table.
 gamma=full;cl=0;lower=[]
 while gamma!=one:
  lower.append(gamma.bit_count());gamma=closure(comm(x,y) for x in members(gamma) for y in range(n));cl+=1
  assert cl<=n
 def conjugate(h,g):return sum(1<<t[t[inv[g]][x]][g] for x in members(h))
 unseen=set(subgens);reps=[]
 while unseen:
  h=min(unseen);orbit={conjugate(h,g) for g in range(n)}
  assert orbit<=set(subgens);unseen-=orbit;reps.append((h,len(orbit)))
 aa=[h for h in subgens if ab[h]];tested=0;actual=0;witness_sizes=[]
 for b,orbit_size in reps:
  bg=subgens[b];cg={comm(x,y) for x in bg for y in bg}
  if cg=={e}:continue
  if not all(comm(c,g)==e for c in cg for g in bg):continue
  derived=closure(cg)
  for a in aa:
   if a.bit_count()*b.bit_count()!=n or a&b!=one:continue
   k=closure((*subgens[a],*members(derived)));intersection=k&b
   assert intersection in subgens and ab[intersection]
   assert a.bit_count()*intersection.bit_count()==k.bit_count()
   tested+=1;actual+=orbit_size;witness_sizes.append(intersection.bit_count())
 row=next(r for r in json.loads((ROOT/'results/18.120-pilot.json').read_text())['rows'] if (r['order'],r['id'])==(n,data['id']))
 assert row['class']==cl and row['subgroup_classes']==len(reps) and row['disjoint_factorizations']==tested
 return {'order':n,'id':data['id'],'class':cl,'lower_central_orders':lower,'subgroups':len(subgens),'subgroup_classes':len(reps),'factorization_representatives':tested,'actual_factorizations':actual,'witness_sizes':sorted(witness_sizes),'associativity_triples':n**3}
def run():return [check(d) for d in json.loads((ROOT/'results/18.120-control-inputs.json').read_text())]
if __name__=='__main__':
 start=time.monotonic();rows=run();(ROOT/'results/18.120-controls.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('PASS_18120_CONTROLS',len(rows),'groups',sum(r['factorization_representatives'] for r in rows),'representatives',sum(r['actual_factorizations'] for r in rows),'actual factorizations',time.monotonic()-start,'seconds')
