#!/usr/bin/env python3
"""Replay Conder's cycle tables and joins. This is not a group enumeration.

Tables transcribed visually from his 1980 thesis, printed pp.92,94,97,99,
100,102,104,106,108,109,111,114,116. A token (aN) has length N+1.
For d>=2, only the multiplicity of 6-cycles grows, as the source states.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]

# name: degree intercept/slope, handle count, x parity, handle lengths
# for d=0,1,2, other cycles for these cases, extra 6-cycles per d above2.
DATA = {
 'S7': ([42,36],3,1,[(1,13),(1,10),(1,8)],
        [{},{3:3,12:3},{3:3,6:3,8:3,12:3}],6,92),
 'U7': ([36,30],1,1,[(1,11),(1,10),(1,8)],
        [{5:1,8:1,11:1},{3:2,4:1,8:2,9:2,11:1},
         {3:2,4:1,6:2,7:2,8:5,11:1}],5,94),
 'W8': ([24,18],3,-1,[(1,7),(1,10),(1,8)],
        [{},{3:3},{3:3,8:3}],3,99),
 'U8': ([51,36],1,-1,[(1,9),(1,6),(1,6)],
        [{3:1,5:1,10:1,11:1,12:1},{3:1,4:1,7:4,8:2,9:2,11:1},
         {3:1,4:1,5:3,6:1,7:3,8:7,11:1}],6,97),
 'S9': ([54,36],3,1,[(7,11),(14,4),(8,4)],
        [{},{3:3,9:3},{3:3,7:3,8:3,12:3}],6,100),
 'U9': ([46,30],1,1,[(13,5),(14,4),(8,4)],
        [{1:1,7:2,13:1},{1:1,3:1,4:2,5:1,9:2,10:1,13:1},
         {1:1,3:1,4:2,5:1,7:2,8:5,10:1,13:1}],5,102),
 'S10': ([60,36],3,1,[(10,10),(6,8),(6,6)],
         [{},{4:3,14:3},{4:3,8:6,12:3}],6,104),
 'U10': ([71,42],1,-1,[(10,12),(10,4),(8,4)],
         [{1:1,3:1,7:2,13:1,18:1},
          {1:1,3:2,4:1,5:2,6:1,7:1,8:3,13:1,28:1},
          {1:1,3:2,4:1,5:3,6:3,8:6,12:2,13:1,14:1}],7,106),
 'W10': ([30,18],1,-1,[(8,8),(6,8),(6,6)],
         [{3:1,4:1,7:1},{3:1,4:1,5:1,6:1,8:2},
          {3:1,4:1,5:1,6:3,8:3}],3,108),
 'S11': ([69,36],3,1,[(4,13),(4,10),(4,10)],
         [{6:3},{4:3,7:3,10:3},{4:3,5:3,7:3,8:3,9:3}],6,109),
 'U11': ([34,18],1,1,[(7,5),(7,8),(7,6)],
         [{6:1,7:1,9:1},{3:1,5:1,6:2,8:1,9:1},
          {3:1,5:1,6:3,7:1,8:3}],3,111),
 'W12': ([36,18],3,-1,[(5,7),(5,8),(5,6)],
         [{},{5:3},{5:3,8:3}],3,116),
 'U12': ([27,12],1,1,[(8,4),(8,4),(8,4)],
         [{1:1,2:1,6:2},{1:1,2:1,4:2,6:1,10:1},
          {1:1,2:1,4:2,6:1,7:2,8:1}],2,114),
}


def block(name, d):
    deg, nh, sign, pairs, other, slope, page = DATA[name]
    c = Counter(other[min(d,2)])
    if d >= 2:
        c[6] += slope*(d-2)
    handles = [pairs[min(d,2)]]*nh
    n = sum(k*v for k,v in c.items()) + sum(sum(h) for h in handles)
    assert n == deg[0]+deg[1]*d, (name,d,n,deg)
    return dict(n=n, sign=sign, handles=handles, cycles=c)


def join(a,b):
    """Each handle point belongs to its own cycle; joins merge paired cycles."""
    a,b = deepcopy(a),deepcopy(b)
    u,v = a['handles'].pop(0),b['handles'].pop(0)
    c = a['cycles']+b['cycles']
    c[u[0]+v[0]] += 1
    c[u[1]+v[1]] += 1
    return dict(n=a['n']+b['n'],sign=a['sign']*b['sign'],
                handles=a['handles']+b['handles'],cycles=c)


def stock(h,d):
    if h in (8,12):
        return join(block('W'+str(h),d),block('W'+str(h),d))
    return block('S'+str(h),d)


def cycle_lengths(a):
    c = a['cycles'].copy()
    for pair in a['handles']:
        c.update(pair)
    assert sum(k*v for k,v in c.items()) == a['n']
    return c


def power_cycles(c,e):
    result = Counter()
    for length,count in c.items():
        g = math.gcd(length,e)
        result[length//g] += g*count
    return result


def explicit_permutation(c):
    perm=[]
    for length,count in sorted(c.items()):
        for _ in range(count):
            start=len(perm)
            perm += list(range(start+1,start+length))+[start]
    return perm


def perm_power(a,e):
    result=list(range(len(a)))
    while e:
        if e&1:
            result=[a[i] for i in result]
        a=[a[i] for i in a]
        e//=2
    return result


def main():
    rows=[]
    for h in range(7,13):
        p=11 if h in (7,8,11) else 13
        exponent=720720//p
        assert exponent%2==0 and math.gcd(exponent,p)==1
        for d in (0,1,2,3,10):
            for k in (1,2,3,10,101):
                a=stock(h,d)
                for _ in range(k-1):
                    a=join(a,stock(h,d))
                a=join(a,block('U'+str(h),d))
                # U8 and U10 are odd; one W corrects the involution's parity.
                if h in (8,10):
                    a=join(a,block('W'+str(h),d))
                assert a['sign']==1
                c=cycle_lengths(a)
                assert c[p]==1, (h,d,k,c)
                assert all(length==p or length%p for length in c), (h,d,k,c)
                assert all(720720%length==0 for length in c), (h,d,k,c)
                powered=power_cycles(c,exponent)
                assert powered==Counter({1:a['n']-p,p:1}), (h,d,k,powered)
                # Independent binary powering of an actual permutation having
                # this cycle structure (not a reconstructed triangle action).
                v=perm_power(explicit_permutation(c),exponent)
                assert sum(i!=j for i,j in enumerate(v))==p
                rows.append(dict(h=h,d=d,r=h+6*d,chain_length=k,n=a['n'],p=p,
                                 word_exponent=exponent//2,
                                 cycle_structure=dict(sorted(c.items())),
                                 moved_points=p))
    # Every divisor permitted by the imported bound, not merely table entries.
    divisors=[d for d in range(1,720721) if 720720%d==0]
    for p in (11,13):
        assert all((720720//p)%d==0 for d in divisors if d%p)
    result=dict(status='PASS',scope='Cycle-table arithmetic and permutation powering; '
                'not independent reconstruction of the triangle-group generators.',
                source_sha256=hashlib.sha256((ROOT/'references/cache/'
                'conder-minimal-generating-pairs-thesis-1980.pdf').read_bytes()).hexdigest(),
                table_count=len(DATA),table_regimes=3,rows=rows,
                divisor_count=len(divisors))
    (ROOT/'results/15.92-cycle-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('15_92_CYCLE_CONTROLS_DONE',len(rows),len(divisors))


if __name__=='__main__':
    main()
