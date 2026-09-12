#!/usr/bin/env python3
"""Exploratory exact root partitions of full upper unitriangular groups."""
from itertools import combinations
import json
from pathlib import Path
out=[];flags=[]
for n in range(2,7):
 roots=list(combinations(range(n),2));idx={e:i for i,e in enumerate(roots)};full=(1<<len(roots))-1
 triples=[(idx[i,j],idx[j,k],idx[i,k]) for i,j,k in combinations(range(n),3)]
 paths=[(idx[i,j],idx[j,k],idx[k,l]) for i,j,k,l in combinations(range(n),4)]
 count=0
 for a in range(full+1):
  b=full^a
  if any(a>>x&1 and a>>y&1 for x,y,z in triples):continue
  if any(b>>x&1 and b>>y&1 and not b>>z&1 for x,y,z in triples):continue
  if any(all(b>>x&1 for x in path) for path in paths):continue
  count+=1;derived=sum(1<<z for z in {z for x,y,z in triples if b>>x&1 and b>>y&1});k=a|derived
  while True:
   nxt=k
   for x,y,z in triples:
    if k>>x&1 and k>>y&1:nxt|=1<<z
   if nxt==k:break
   k=nxt
  bad=any((k&b)>>x&1 and (k&b)>>y&1 for x,y,z in triples)
  if bad:flags.append({'n':n,'A':[roots[i] for i in range(len(roots)) if a>>i&1],'B':[roots[i] for i in range(len(roots)) if b>>i&1],'K':[roots[i] for i in range(len(roots)) if k>>i&1]})
 out.append({'n':n,'root_partitions':count});print(out[-1],flush=True)
p={'scope':'Exploratory coordinate root subgroups only; no general claim','counts':out,'flags':flags}
Path('results/18.120-root-partitions.json').write_text(json.dumps(p,indent=2)+'\n');print('FLAGS',len(flags));print(flags[:1])
