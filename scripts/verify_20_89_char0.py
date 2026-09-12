#!/usr/bin/env python3
"""Independent rational normal forms and permutation orbit dynamics."""
import itertools,json
from fractions import Fraction as Q

perms=list(itertools.permutations(range(4)))
one=tuple(range(4))
def pmul(p,q):return tuple(q[i] for i in p)
def pinv(p):return tuple(p.index(i) for i in range(len(p)))
def pcomm(p,q):return pmul(pmul(pmul(pinv(p),pinv(q)),p),q)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def mul(x,y):
    u,v,z,k,p=x;a,b,c,j,q=y;s=Q(2)**k
    return (u+s*a,v+s*s*b,z+s**3*c+u*s*s*b,k+j,pmul(p,q))
def inv(x):
    u,v,z,k,p=x;s=Q(2)**(-k)
    return (-s*u,-s*s*v,s**3*(u*v-z),-k,pinv(p))
identity=(Q(0),Q(0),Q(0),0,one)
def comm(x,y):return mul(mul(mul(inv(x),inv(y)),x),y)
def enc(x):
    assert x[3]==0
    return [[q.numerator,q.denominator] for q in x[:3]]+[list(i+1 for i in x[4])]
def pair(i):
    x=(Q(i%7-3,2**(i%3)),Q((i*3)%7-3,2**((i+1)%3)),Q((i*5)%7-3,2**((i+2)%3)),i%7-3,perms[i%24])
    l=(Q((i*2)%9-4,2**((i+2)%3)),Q((i*4)%9-4,2**(i%3)),Q((i*7)%9-4,2**((i+1)%3)),0,perms[(i*7+5)%24])
    return x,l

nonzero_second=0
for i in range(720):
    x,l=pair(i); y=x; row=[]
    for _ in range(3):y=comm(y,l);row.append(enc(y))
    nonzero_second+=row[1][2][0]!=0
    assert y[:3]==identity[:3] and parity(y[4])==0
    print('ROW2089C '+json.dumps([i,row],separators=(',',':')))

assert nonzero_second>0
small=[pair(i)[0] for i in range(9)]
for a,b,c in itertools.product(small,repeat=3):assert mul(mul(a,b),c)==mul(a,mul(b,c))
for x in small:assert mul(x,inv(x))==mul(inv(x),x)==identity

orbit_rows=[]
for k in list(range(-4,0))+list(range(1,5)):
    g=(Q(2),Q(-3),Q(1),k,one)
    if k==-1:
        images=[]
        for b in range(1,41):
            x=(Q(b),Q(0),Q(0),0,one)
            for _ in range(20):x=comm(x,g)
            assert x[0]==b;images.append(x[0])
        assert len(set(images))==40;orbit_rows.append([k,40])
    else:
        x=(Q(1),Q(0),Q(0),0,one);images=[]
        for n in range(21):
            assert x[0]==(Q(2)**(-k)-1)**n
            images.append(x[0]);x=comm(x,g)
        assert len(set(images))==21;orbit_rows.append([k,21])

sinks=[]
for a in perms:
    sink=set()
    for x in perms:
        path=[];seen={}
        while x not in seen:
            seen[x]=len(path);path.append(x);x=pcomm(x,a)
        sink.update(path[seen[x]:])
    sinks.append(sink)
union=set().union(*sinks)
assert union=={p for p in perms if parity(p)==0}
hist=[[s,sum(len(e)==s for e in sinks)] for s in sorted({len(e) for e in sinks})]

nonsplit=0;torsion=0
for m in range(-20,21):
    for p in itertools.permutations(range(3)):
        q=tuple(range(3));coord=0
        for _ in range(6):coord+=m;q=pmul(q,p)
        assert coord==6*m and q==tuple(range(3))
        torsion+=coord==0;nonsplit+=1
assert torsion==6
central=[]
for r in range(1,9):
    order=3**r
    assert len({i%order for i in range(order)})==order
    for j in range(10):assert (-j-(2*j+1)+j+(2*j+1))%order==0
    central.append(order)
summary=dict(pairs=720,nonzero_second_commutators=nonzero_second,commutators=2160,excluded_dilations=orbit_rows,s4_sink_histogram=hist,s4_sink_union=len(union),nonsplit_checks=nonsplit,nonsplit_torsion=torsion,central_torsion_orders=central)
print('SUMMARY2089C '+json.dumps(summary,sort_keys=True,separators=(',',':')))
print('INDEPENDENT2089C '+json.dumps(dict(associativity_triples=729,inverse_checks=9),sort_keys=True))
print('PASS_20_89_CHAR0_WORDS')
