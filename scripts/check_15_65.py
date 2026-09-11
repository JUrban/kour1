#!/usr/bin/env python3
"""Exact series and finite unitary controls for 15.65; not a proof of nonrationality."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,re,subprocess,time
ROOT=Path(__file__).resolve().parents[1]
N=80

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def mobius(n):
    sign=1; p=2
    while p*p<=n:
        if n%p==0:
            n//=p; sign=-sign
            if n%p==0: return 0
            while n%p==0: n//=p
        p+=1
    return -sign if n>1 else sign

def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def counts(d,kind):
    out={}
    def add(e,v): out[e]=out.get(e,Q(0))+v
    if kind=='N':
        assert d%2
        for e in divisors(d):
            add(d//e,Q(mobius(e),d)); add(0,Q(mobius(e),d))
    elif d==1:
        out={2:Q(1,2),1:Q(-1,2),0:Q(-1)}
    else:
        for e in divisors(d):
            add(2*d//e,Q(mobius(e),2*d))
            if d%2: add(d//e,Q(-mobius(e),2*d))
    return {e:v for e,v in out.items() if v}

def log_from_series(f):
    # f'/f, then integrate, all exact.
    n=len(f)-1; ratio=[Q(0)]*n
    for k in range(n):
        ratio[k]=(k+1)*f[k+1]-sum(f[j]*ratio[k-j] for j in range(1,k+1))
    return [Q(0)]+[ratio[k-1]/k for k in range(1,n+1)]

def first_logs(n):
    a=[Q(1)]+[Q(0)]*n; b=a.copy()
    for k in range(2,n+1): a[k]=Q((-1)**(k-1)); b[k]=Q(1)
    return log_from_series(a),log_from_series(b)

def second_logs(n):
    # A numerator roots have power sums L_k=-L_(k-1)+L_(k-2).
    L=[2,-1]
    for k in range(2,n+1): L.append(-L[-1]+L[-2])
    a=[Q(0)]+[Q((-1)**k-L[k],k) for k in range(1,n+1)]
    # B(u)=(1+u^3)/(1-u^2).
    b=[Q(0)]+[Q((3*(-1)**(k//3+1) if k%3==0 else 0)
                    +(2 if k%2==0 else 0),k) for k in range(1,n+1)]
    return a,b

def limit_series(logs):
    la,lb=logs(N+2)
    ll=[Q(0)]+[Q((-1)**(k+1),k) for k in range(1,N+1)]
    for d in range(1,N+1):
        for kind,step,base in [('N',d,la),('M',2*d,lb)]:
            if kind=='N' and d%2==0: continue
            for e,v in counts(d,kind).items():
                for k in range(1,min(len(base),(N+e)//step+1)):
                    j=k*step-e
                    if base[k]:
                        assert j>0
                        ll[j]+=v*base[k]
    out=[Q(1)]
    for k in range(1,N+1):
        out.append(sum(j*ll[j]*out[k-j] for j in range(1,k+1))/k)
    return out

def mul(a,b,n):
    c=[Q(0)]*(n+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b[:n-i+1]): c[i+j]+=x*y
    return c

def finite_formula(q,n):
    out=[Q(1)]+[Q(0)]*n
    for d in range(1,n+1):
        for kind,step,central in [('N',d,q**d+1),('M',2*d,q**(2*d)-1)]:
            if kind=='N' and d%2==0: continue
            exponent=sum(v*q**e for e,v in counts(d,kind).items())
            assert exponent.denominator==1 and exponent>=0
            factor=[Q(1)]+[Q(0)]*n
            for a in range(1,n//step+1):
                factor[step*a]=Q(1,q**(step*(a-1))*central)
            power=exponent.numerator
            while power:
                if power%2: out=mul(out,factor,n)
                power//=2
                if power: factor=mul(factor,factor,n)
    return out[n]

def main():
    a=limit_series(first_logs); b=limit_series(second_logs)
    assert a==b
    assert all(x.denominator==1 for x in a)
    published=[1,0,0,-1,0,-1,1,-2,3,-5,8,-11,21]
    assert a[:13]==published
    # Compare the known GL formula modulo two (a prior integrality result).
    gl=[0]*(N+1)
    for k in range(0,N+1,3): gl[k]+=(-1)**(k//3)
    for k in range(5,N+1,3): gl[k]-=(-1)**((k-5)//3)
    assert all((a[i].numerator-gl[i])%2==0 for i in range(N+1))
    script=ROOT/'scripts/verify_15_65_unitary.g'
    logpath=ROOT/'results/15.65-unitary-controls.log'
    started=time.time()
    with logpath.open('w') as log:
        process=subprocess.run([str(ROOT/'bin/gap'),str(script)],cwd=ROOT,
                               stdout=log,stderr=subprocess.STDOUT,timeout=600)
    log=logpath.read_text()
    assert process.returncode==0,(process.returncode,log[-4000:])
    assert 'UNITARY_CONTROLS_DONE' in log,log[-4000:]
    assert not re.search(r'Error|Syntax warning|Syntax error|Traceback',log),log
    cases=[]
    for q,n,order,cyclic,classes in re.findall(r'^UNITARY_CONTROL (\d+) (\d+) (\d+) (\d+) (\d+)$',log,re.M):
        q,n,order,cyclic,classes=map(int,(q,n,order,cyclic,classes))
        expected=finite_formula(q,n)
        assert Q(cyclic,order)==expected,(q,n,expected,cyclic,order)
        cases.append(dict(q=q,n=n,order=order,cyclic=cyclic,classes=classes,
                          proportion=str(expected)))
    assert len(cases)==14,cases
    # Rational isolating interval for alpha, and log-series majorants.
    lo,hi=Q(-619,1000),Q(-618,1000)
    assert 1+lo-lo*lo<0<1+hi-hi*hi
    assert Q(-3,4)<lo<hi<Q(-1,2)
    R=Q(3,4)
    majorants=[R**6/(1-R**3),R**4/(1-R**2)]
    assert majorants==[Q(729,2368),Q(81,112)] and max(majorants)<1
    artifact=dict(status='PASS',scope='Exact controls; analytic proof is separate',
        series_degree=N,coefficients=[x.numerator for x in a],
        published_coefficients_checked=13,mod_two_GL_checks=N+1,
        finite_cases=cases,class_minpoly_rank_checks=sum(x['classes'] for x in cases),
        alpha_isolating_interval=[str(lo),str(hi)],
        log_majorants=[str(x) for x in majorants],
        actual_gap_exit=process.returncode,gap_seconds=time.time()-started,
        hashes={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__).resolve(),script,logpath]})
    (ROOT/'results/15.65-controls.json').write_text(json.dumps(artifact,indent=2)+'\n')
    print('15_65_CONTROLS_DONE',len(cases),artifact['class_minpoly_rank_checks'])

if __name__=='__main__': main()
