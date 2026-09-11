# Independent actual affine groups from PSNZ 2022, Section 5.
# Basis S,P,Q,R,1; matrices act on columns. No Python output is read.
Check2092 := function(ok, label)
  if not ok then Error(label); fi;
end;;
Log2092 := function(g)
  local n,t,r,v,i;
  n:=Length(g); t:=g-g^0; r:=0*g; v:=g^0;
  for i in [1..n-1] do
    v:=v*t; r:=r+((-1)^(i+1)/i)*v;
  od;
  Check2092(v*t=0*g,"log truncation");
  return r;
end;;
Exp2092 := function(g)
  local n,r,v,i;
  n:=Length(g); r:=g^0; v:=g^0;
  for i in [1..n-1] do v:=v*g/i; r:=r+v; od;
  Check2092(v*g=0*g,"exp truncation");
  return r;
end;;
Run2092 := function(p)
  local f,z,o,id,mP,mQ,mR,mS,grp,els,lambdas,logs,cols,index,
    g,col,x,idx,mat,basis,lefts,left,affine,i,j,a,l,t,avg,want,
    failures,first,ord,star,s,q,r,cycle,v,res,corr,checks;
  f:=GF(p); z:=Zero(f); o:=One(f); id:=IdentityMat(5,f);
  # The parameters i=k=0 and y=1 in the published brace.
  mP:=StructuralCopy(id); mP[1][4]:=o; mP[2][5]:=o;
  mQ:=StructuralCopy(id); mQ[1][3]:=-o; mQ[1][4]:=o/2; mQ[3][5]:=o;
  mR:=StructuralCopy(id); mR[1][2]:=o; mR[1][3]:=o/2; mR[4][5]:=o;
  mS:=StructuralCopy(id); mS[2][3]:=-o; mS[3][4]:=-o;
  mS[2][4]:=o; mS[1][4]:=-o/2; mS[1][5]:=o;
  grp:=Group(mP,mQ,mR,mS); els:=Elements(grp);
  Check2092(Length(els)=p^4,"published affine group order");
  lambdas:=[]; logs:=[]; cols:=[];
  index:=v->1+Sum([1..4],i->IntFFE(v[i])*p^(i-1));
  for g in els do
    col:=List([1..4],i->g[i][5]); idx:=index(col);
    Check2092(not IsBound(lambdas[idx]),"regular translation uniqueness");
    lambdas[idx]:=g{[1..4]}{[1..4]}; cols[idx]:=col;
    mat:=Log2092(g); x:=List([1..4],i->mat[i][5]);
    Check2092(not IsBound(logs[index(x)]),"log projection uniqueness");
    logs[index(x)]:=mat;
    Check2092(Exp2092(mat)=g,"matrix exp log inverse");
  od;
  Check2092(Length(lambdas)=p^4 and Length(logs)=p^4,"full projections");
  basis:=IdentityMat(4,f);
  lefts:=List(basis,v->logs[index(v)]{[1..4]}{[1..4]});
  left:=v->Sum([1..4],i->v[i]*lefts[i]);
  affine:=function(v)
    local out,i;
    out:=NullMat(5,5,f); out{[1..4]}{[1..4]}:=left(v);
    for i in [1..4] do out[i][5]:=v[i]; od;
    return out;
  end;
  for mat in logs do
    x:=List([1..4],i->mat[i][5]);
    Check2092(mat=affine(x),"linear graph of all group logarithms");
  od;
  for i in [1..4] do for j in [1..4] do
    v:=List([1..4],r->lefts[i][r][j]-lefts[j][r][i]);
    Check2092(lefts[i]*lefts[j]-lefts[j]*lefts[i]=left(v),"pre-Lie basis identity");
  od; od;
  failures:=0; first:=[]; ord:=Order(2*o); checks:=0;
  for a in cols do
    avg:=NullMat(4,4,f); t:=o;
    for i in [0..p-2] do
      avg:=avg-(lambdas[index(t*a)]-IdentityMat(4,f))/t; t:=2*t;
    od;
    want:=left(a);
    if avg<>want then
      failures:=failures+1;
      if first=[] then first:=List(a,IntFFE); fi;
    fi;
    # Test the constructive inverse on 101 actual input vectors per field.
    if checks<101 then
      x:=List([1..4],i->z);
      for i in [1..4] do
        g:=Exp2092(affine(x)); res:=a-List([1..4],j->g[j][5]);
        Check2092(ForAll([6-i..4],j->res[j]=z),"residual lies in flag");
        corr:=Log2092(g*Exp2092(affine(res)));
        x:=List([1..4],j->corr[j][5]);
        Check2092(corr=affine(x),"BCH graph closure");
      od;
      g:=Exp2092(affine(x));
      Check2092(List([1..4],j->g[j][5])=a,"four corrections invert W");
      checks:=checks+1;
    fi;
  od;
  star:=function(a,b)
    local m;
    m:=lambdas[index(a)]-IdentityMat(4,f);
    return List([1..4],i->Sum([1..4],j->m[i][j]*b[j]));
  end;
  s:=basis[1]; q:=basis[3]; r:=basis[4]; v:=s; cycle:=[];
  for a in [q,r,q,r] do v:=star(v,a); Add(cycle,List(v,IntFFE)); od;
  Check2092(v=s and ForAll(cycle,v->v<>[0,0,0,0]),"non-right-nilpotent cycle");
  Print("FIELD_RESULT ",[p,Length(els),ord,failures,first,checks,cycle],"\n");
end;;
for prime2092 in [5,7,11] do Run2092(prime2092); od;
Print("PASS_20_92A\n");
QUIT_GAP(0);
