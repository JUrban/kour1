#!/usr/bin/env python3
"""Exact controls for the full 15.65 extension; the proof is analytic."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,re,subprocess,time
from check_15_65 import counts,divisors,mobius,mul,log_from_series,first_logs
ROOT=Path(__file__).resolve().parents[1]
DEGREE=40

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def one(n): return [Q(1)]+[Q(0)]*n
def power(a,k,n):
    out=one(n)
    while k:
        if k%2: out=mul(out,a,n)
        k//=2
        if k: a=mul(a,a,n)
    return out

def star_counts(d,kind,e):
    if kind=='J':
        out={}
        for a in divisors(d):
            if a%2:
                out[d//a]=out.get(d//a,Q(0))+Q(mobius(a),2*d)
                out[0]=out.get(0,Q(0))+Q(mobius(a)*(1-e),2*d)
    elif d==1: out={1:Q(1,2),0:Q(-e-1,2)}
    else:
        out={d//a:Q(mobius(a),2*d) for a in divisors(d)}
        if d%2==0:
            for k,v in star_counts(d//2,'J',e).items():
                out[k]=out.get(k,Q(0))-v/2
    return {k:v for k,v in out.items() if v}

def group_order(kind,m,q):
    out=q**(m*(m-1)//2 if kind in ('U','GL') else m*m)
    for i in range(1,m+1):
        out*=q**i-(-1)**i if kind=='U' else q**i-1 if kind=='GL' else q**(2*i)-1
    return out

def finite_formula(family,q,n,mode):
    e=1 if q%2==0 else 2
    out=one(n)
    if family=='Sp' and mode!='RS':
        f=one(n)
        for a in range(1,n+1):
            f[a]=Q(1,q**a) if mode=='C' else Q(1,group_order('Sp',a,q))
        out=power(f,e,n)
    for d in range(1,n+1):
        if family=='U':
            kinds=[('N',d,'U'),('M',2*d,'GL')]
        else: kinds=[('J',d,'U'),('K',d,'GL')]
        for kind,step,central_kind in kinds:
            if kind=='N' and d%2==0: continue
            poly=counts(d,kind) if family=='U' else star_counts(d,kind,e)
            exponent=sum(v*q**k for k,v in poly.items())
            assert exponent.denominator==1 and exponent>=0
            f=one(n); field=q**step
            for a in range(1,n//step+1):
                if mode=='RS' and a>1: break
                central=(field+1 if central_kind=='U' else field-1)*field**(a-1)
                if mode=='SS': central=group_order(central_kind,a,field)
                f[a*step]=Q(1,central)
            out=mul(out,power(f,exponent.numerator,n),n)
    return out[n]

def reciprocal_sum(kind,n):
    out=one(n)
    for m in range(1,n+1):
        shift=m*m if kind in ('U','L') else m*(2*m+1) if kind=='P' else m*(2*m-1)
        if shift>n: break
        f=one(n-shift)
        for i in range(1,m+1):
            step=i if kind in ('U','L') else 2*i
            sign=(-1)**i if kind=='U' else 1
            # Coefficients of division by 1-sign*t^step.
            for j in range(step,n-shift+1): f[j]+=sign*f[j-step]
        for j,v in enumerate(f): out[j+shift]+=v
    return out

def exponential(ll):
    out=[Q(1)]
    for k in range(1,len(ll)):
        out.append(sum(j*ll[j]*out[k-j] for j in range(1,k+1))/k)
    return out

def product_series(family,mode,e,n):
    size=n+2
    if mode=='C': la,lb=first_logs(size)
    elif mode=='RS':
        v=one(size)
        for k in range(2,size+1): v[k]=Q(2*(-1)**(k-1))
        la=log_from_series(v); lb=[Q(0)]*(size+1)
    else:
        la,lb=[log_from_series(mul([Q(1),Q(-1)],reciprocal_sum(kind,size),size))
               for kind in ('U','L')]
    ll=[Q(0)]*(n+1)
    for d in range(1,n+1):
        kinds=[('N',d,la),('M',2*d,lb)] if family=='U' else [('J',d,la),('K',d,lb)]
        for kind,step,base in kinds:
            if kind=='N' and d%2==0: continue
            poly=counts(d,kind) if family=='U' else star_counts(d,kind,e)
            for k,v in poly.items():
                for j in range(1,min(len(base),(n+k)//step+1)):
                    if base[j]:
                        assert step*j-k>0
                        ll[step*j-k]+=v*base[j]
    out=exponential(ll)
    if family=='U': out=mul(out,[Q(1),Q(1)],n)
    elif mode=='RS': out=mul(out,power([Q(1),Q(-1)],e,n),n)
    elif mode=='SS':
        pref=mul([Q(1),Q(-1)],reciprocal_sum('P',n),n)
        out=mul(out,power(pref,e,n),n)
    return out

def all_series(n):
    out={}
    for mode in ('C','SS','RS'):
        out[f'U_{mode}']=product_series('U',mode,0,n)
        for e in (1,2):
            sp=product_series('Sp',mode,e,n)
            out[f'Sp{e}_{mode}']=sp
            if mode=='C':
                odd=mul(sp,[Q(1),Q(-1)],n)
                pref=power([Q(1),Q(-1)],e,n); pref[0]+=1
                even=[v/2 for v in mul(sp,pref,n)]
            elif mode=='RS': odd=sp; even=[Q(2)**(e-2)*v for v in sp]
            else:
                # Compute T_e independently of the Sp prefactor by division.
                p=reciprocal_sum('P',n); q=reciprocal_sum('Q',n)
                pp=power(p,e,n)
                base=[Q(0)]*(n+1)
                for k in range(n+1): base[k]=sp[k]-sum(pp[j]*base[k-j] for j in range(1,k+1))
                odd=mul(base,mul(power(q,e-1,n),p,n),n)
                pref=[a+(e-1)*b for a,b in zip(power(q,e,n),power(p,2,n))]
                even=[v/2 for v in mul(base,pref,n)]
            out[f'Oodd{e}_{mode}']=odd
            out[f'Opm{e}_{mode}']=even
    return out

PUBLISHED={
 'U_C':[1,0,0,-1,0,-1,1,-2,3,-5],
 'Sp1_C':[1,0,0,-2,1,-2,4,-5,9,-14],
 'Sp2_C':[1,0,0,-3,2,-3,8,-11,19,-32],
 'Oodd1_C':[1,-1,0,-2,3,-3,6,-9,14,-23],
 'Oodd2_C':[1,-1,0,-3,5,-5,11,-19,30,-51],
 'Opm1_C':[1,Q(-1,2),0,-2,2,Q(-5,2),5,-7,Q(23,2),Q(-37,2)],
 'Opm2_C':[1,-1,Q(1,2),-3,5,Q(-13,2),12,Q(-41,2),34,Q(-113,2)],
 'U_SS':[1,-1,0,-1,2,-2,5,-9,11,-20],
 'Sp1_SS':[1,-2,2,-2,3,-5,8,-15,29,-52],
 'Sp2_SS':[1,-3,5,-7,11,-19,32,-56,104,-195],
 'Oodd2_SS':[1,-2,2,-2,3,-5,8,-16,34,-64],
 'Opm1_SS':[Q(1,2),Q(-1,2),0,0,0,0,Q(1,2),-2,Q(9,2),Q(-15,2)],
 'Opm2_SS':[1,-2,Q(5,2),Q(-7,2),Q(11,2),Q(-19,2),Q(33,2),Q(-61,2),Q(117,2),Q(-215,2)],
 'U_RS':[1,-1,0,-2,4,-6,14,-28,52,-106],
 'Sp1_RS':[1,-2,2,-4,9,-17,32,-64,130,-258],
 'Sp2_RS':[1,-3,5,-10,23,-49,100,-208,439,-915],
}

def analytic_controls():
    def a(r,m):
        den=Q(1)
        for i in range(1,m+1): den*=1-r**i
        return r**(m*m)/den
    lower=1+sum((-1)**m*a(Q(1,2),m) for m in range(1,4))
    upper=1+sum((-1)**m*a(Q(3,5),m) for m in range(1,5))
    assert lower==Q(9,56)>0 and upper==Q(-1128797279,26656000000)<0
    r=Q(3,7); majorant=(r/(1-r))/(1-r**3/(1-r*r))
    assert majorant==Q(210,253)<1
    R=Q(13,20)
    assert R*R<Q(3,7)<Q(1,2)<R
    assert R**3/(1-R*R)<1
    # Check the paired full orthogonal reciprocal orders underlying Q.
    order_checks=0
    for q in (2,3,4,5,7):
        for m in range(1,8):
            common=2*q**(m*(m-1))
            for i in range(1,m): common*=q**(2*i)-1
            s=Q(1,common*(q**m-1))+Q(1,common*(q**m+1))
            t=Q(1,q); expected=t**(m*(2*m-1))
            for i in range(1,m+1): expected/=1-t**(2*i)
            assert s==expected; order_checks+=1
    return dict(lower=str(lower),upper=str(upper),zero_free_majorant=str(majorant),
                higher_argument_bound=str(R*R),orthogonal_order_checks=order_checks)

def main():
    series=all_series(DEGREE)
    for k,v in PUBLISHED.items(): assert series[k][:10]==v,(k,series[k][:10],v)
    assert series['Oodd1_SS']==series['Sp1_SS']
    original=json.loads((ROOT/'results/15.65-controls.json').read_text())
    assert series['U_C']==original['coefficients'][:DEGREE+1]
    analytic=analytic_controls()
    script=ROOT/'scripts/verify_15_65_classical.g'
    logpath=ROOT/'results/15.65-classical-gap.log'; start=time.time()
    with logpath.open('w') as log:
        p=subprocess.run([str(ROOT/'bin/gap'),str(script)],cwd=ROOT,
                         stdout=log,stderr=subprocess.STDOUT,timeout=600)
    proc=dict(actual_exit=p.returncode,elapsed_seconds=time.time()-start,
              hashes={str(f.relative_to(ROOT)):sha(f) for f in (script,logpath)})
    (ROOT/'results/15.65-classical-gap-process.json').write_text(json.dumps(proc,indent=2)+'\n')
    log=logpath.read_text()
    assert p.returncode==0 and log.rstrip().endswith('CLASSICAL_CONTROLS_DONE'),log
    assert not re.search(r'Error|Syntax warning|Syntax error|Traceback|#I',log),log
    rows=[]
    for match in re.findall(r'^CLASSICAL_CONTROL (U|Sp) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)$',log,re.M):
        family=match[0]; q,n,order,c,ss,rs,classes=map(int,match[1:])
        values={}
        for mode,count in [('C',c),('SS',ss),('RS',rs)]:
            expected=finite_formula(family,q,n,mode)
            assert Q(count,order)==expected,(family,q,n,mode,count,order,expected)
            values[mode]=dict(count=count,proportion=str(expected))
        rows.append(dict(family=family,q=q,n=n,order=order,classes=classes,values=values))
    assert len(rows)==23
    artifact=dict(status='PASS',series_degree=DEGREE,
        series={k:list(map(str,v)) for k,v in series.items()},
        published_rows_checked=len(PUBLISHED),published_coefficients_checked=10*len(PUBLISHED),
        finite_cases=rows,class_checks=sum(r['classes'] for r in rows),
        finite_formula_checks=3*len(rows),analytic_controls=analytic,
        actual_gap_exit=p.returncode,
        hashes={str(f.relative_to(ROOT)):sha(f) for f in
                (Path(__file__).resolve(),script,logpath,ROOT/'scripts/check_15_65.py',
                 ROOT/'results/15.65-classical-gap-process.json',ROOT/'results/15.65-controls.json')})
    (ROOT/'results/15.65-classical-controls.json').write_text(json.dumps(artifact,indent=2)+'\n')
    print('15_65_CLASSICAL_CONTROLS_DONE',len(rows),artifact['class_checks'],artifact['published_coefficients_checked'])

if __name__=='__main__': main()
