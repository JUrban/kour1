#!/usr/bin/env python3
"""Finite assignments extendible to the infinite-rank construction."""
from itertools import product
import json
from pathlib import Path
import random


def reduce(word):
    out=[]
    for a in word:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return out


def inverse(w):return [-a for a in reversed(w)]
def comm(u,v):return reduce(inverse(u)+inverse(v)+u+v)


def main():
    rng=random.Random(201242026)
    images=[[],[],[]]
    levels=[0,0,0]
    for level in range(1,4):
        a=3*(level-1)+1;b=a+1;c=a+2
        images.extend([comm([a],[b]),comm([b],[c]),comm([c],[a])])
        levels.extend([level]*3)
    alphabet=list(range(1,13))+list(range(-1,-13,-1))
    words=[[]]
    for length in range(1,4):
        words.extend([list(w) for w in product(alphabet,repeat=length)
                      if all(w[i]!=-w[i+1] for i in range(length-1))])
    assert len(words)==13273
    words.extend(reduce([rng.choice(alphabet) for _ in range(rng.randrange(1,9))]) for _ in range(512))
    targets=[comm([10],[11])]
    for i in range(63):
        u=reduce([rng.choice(alphabet) for _ in range(1+i%3)])
        v=reduce([rng.choice(alphabet) for _ in range(1+(i+1)%3)])
        targets.append(comm(u,v))
    images.extend(targets);levels.extend([4]*len(targets))
    words.extend([[i] for i in range(13,77)])
    rbpairs=[[[i],[j]] for i in range(1,13) for j in range(1,13)]
    rbpairs.extend([[rng.choice(words[:13785]),rng.choice(words[:13785])] for _ in range(4096)])
    fixture=dict(levels=levels,images=images,words=words,rbpairs=rbpairs,
                 image_witnesses=[[i+13,w] for i,w in enumerate(targets)])
    Path('results/20.124-fixture.json').write_text(json.dumps(fixture,separators=(',',':'))+'\n')
    lines=['Levels20124 := '+json.dumps(levels)+';;',
           'Images20124 := '+json.dumps(images)+';;',
           'Words20124 := '+json.dumps(words)+';;',
           'Pairs20124 := '+json.dumps(rbpairs)+';;',
           'Witnesses20124 := '+json.dumps(fixture['image_witnesses'])+';;']
    Path('results/20.124-fixture.g').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(generators=len(images),words=len(words),rbpairs=len(rbpairs),image_witnesses=len(targets)),sort_keys=True))
    print('PASS_20_124_FIXTURE')


if __name__=='__main__':main()
