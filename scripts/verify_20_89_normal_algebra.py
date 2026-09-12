#!/usr/bin/env python3
"""Independent prime-field matrix enumeration and functional-graph sinks."""
import itertools,json
from collections import deque

def mul(x,y,p):
    a,b,c,d=x;e,f,g,h=y
    return ((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)
def det(x,p):return (x[0]*x[3]-x[1]*x[2])%p
def inv(x,p):
    r=pow(det(x,p),-1,p);a,b,c,d=x
    return (r*d%p,-r*b%p,-r*c%p,r*a%p)
def reps(p):
    out=[]
    for a in range(1,p):out.extend([(a,0,0,a),(a,1,0,a)])
    for a in range(1,p):
        for b in range(a+1,p):out.append((a,0,0,b))
    for t in range(p):
        for d in range(1,p):
            if all((x*x-t*x+d)%p for x in range(p)):out.append((0,-d%p,1,t))
    assert len(set(out))==p*p-1
    return sorted(out)

identity=(1,0,0,1)
groups=classes=nontrivial=parameter_checks=0;bound_rows=[]
for p in [2,3,5,7]:
    all_gl=[x for x in itertools.product(range(p),repeat=4) if det(x,p)]
    inverses={x:inv(x,p) for x in all_gl}
    for kind in ['GL','SL']:
        els=all_gl if kind=='GL' else [x for x in all_gl if det(x,p)==1]
        index={x:i for i,x in enumerate(els)}
        selected=[a for a in reps(p) if kind=='GL' or det(a,p)==1]
        sizes=[];groups+=1
        for a in selected:
            ai=inverses[a]
            f=[index[mul(mul(mul(inverses[x],ai,p),x,p),a,p)] for x in els]
            indeg=[0]*len(els)
            for j in f:indeg[j]+=1
            queue=deque(i for i,d in enumerate(indeg) if d==0)
            while queue:
                i=queue.popleft();j=f[i];indeg[j]-=1
                if indeg[j]==0:queue.append(j)
            sink=sorted(els[i] for i,d in enumerate(indeg) if d>0)
            assert identity in sink
            params=[]
            for t in range(p):
                c=((1+t*a[0])%p,t*a[1]%p,t*a[2]%p,(1+t*a[3])%p)
                if det(c,p):params.append(c)
            r=len(params);eigenvalues=sum(det(((a[0]-s)%p,a[1],a[2],(a[3]-s)%p),p)==0 for s in range(1,p))
            assert r==p-eigenvalues and r>=p-2
            orbit=[]
            if len(sink)>1:
                e=next(e for e in sink if mul(e,a,p)!=mul(a,e,p))
                orbit=[mul(mul(inv(c,p),e,p),c,p) for c in params]
                assert len(set(orbit))==r and identity not in orbit and set(orbit)<=set(sink)
                assert len(sink)>=r+1
                nontrivial+=1;parameter_checks+=r
            print('ROW2089A '+json.dumps([p,kind,list(a),len(els),sink,r,orbit],separators=(',',':')))
            classes+=1;sizes.append(len(sink))
        bound_rows.append([p,kind,len(els),len(selected),min([m for m in sizes if m>1],default=0),max(sizes)])
p=7;a=(0,1,1,0);b=(0,6,1,6);b2=mul(b,b,p)
small={identity,b,b2,a,mul(a,b,p),mul(a,b2,p)}
sink={mul(mul(mul(inv(x,p),inv(a,p),p),x,p),a,p) for x in small}
assert sink=={identity,b,b2} and mul(mul(mul(inv(b,p),inv(a,p),p),b,p),a,p)==b
c=(1,2,2,1);bad=mul(mul(inv(c,p),b,p),c,p)
assert bad not in small
print('CONTROL2089A '+json.dumps([7,sorted(sink),5,list(bad)],separators=(',',':')))
summary=dict(groups=groups,classes=classes,nontrivial_sinks=nontrivial,parameter_conjugates=parameter_checks,group_rows=bound_rows)
print('SUMMARY2089A '+json.dumps(summary,sort_keys=True,separators=(',',':')))
print('PASS_20_89_NORMAL_ALGEBRA_WORDS')
