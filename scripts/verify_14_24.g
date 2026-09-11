# Actual free-group maps and independently computed fixed lattices.
SizeScreen([1000000,24]);;
Verify1424:=function()
local r,n,F,x,ai,bi,ci,ainv,binv,cinv,a,b,c,av,bv,cv,i,j,A,B,C,
      KA,KB,expectedA,expectedB,eqs,total,rankchecks;
eqs:=0;total:=0;rankchecks:=0;
for r in [3..40] do
 n:=2*r-1;F:=FreeGroup(n);x:=GeneratorsOfGroup(F);
 ai:=ShallowCopy(x);bi:=ShallowCopy(x);ci:=ShallowCopy(x);
 ainv:=ShallowCopy(x);binv:=ShallowCopy(x);cinv:=ShallowCopy(x);
 for i in [1..r] do
  if i=1 then ai[i]:=x[i]*x[r+i];ainv[i]:=x[i]*x[r+i]^-1;
  elif i=r then ai[i]:=x[r+i-1]^-1*x[i];ainv[i]:=x[r+i-1]*x[i];
  else ai[i]:=x[r+i-1]^-1*x[i]*x[r+i];ainv[i]:=x[r+i-1]*x[i]*x[r+i]^-1;fi;
  if i<r then bi[i]:=x[i]*x[r+i];binv[i]:=x[i]*x[r+i]^-1;fi;
  ci[i]:=Product(x{[1..i]});
  if i>1 then cinv[i]:=x[i-1]^-1*x[i];fi;
 od;
 a:=GroupHomomorphismByImages(F,F,x,ai);av:=GroupHomomorphismByImages(F,F,x,ainv);
 b:=GroupHomomorphismByImages(F,F,x,bi);bv:=GroupHomomorphismByImages(F,F,x,binv);
 c:=GroupHomomorphismByImages(F,F,x,ci);cv:=GroupHomomorphismByImages(F,F,x,cinv);
 Assert(0,ForAll([a,av,b,bv,c,cv],h->h<>fail));
 for j in [1..n] do
  Assert(0,Image(a,Image(av,x[j]))=x[j] and Image(av,Image(a,x[j]))=x[j]);
  Assert(0,Image(b,Image(bv,x[j]))=x[j] and Image(bv,Image(b,x[j]))=x[j]);
  Assert(0,Image(c,Image(cv,x[j]))=x[j] and Image(cv,Image(c,x[j]))=x[j]);
  Assert(0,Image(a,Image(c,x[j]))=Image(c,Image(b,x[j])));eqs:=eqs+7;
 od;
 Assert(0,Maximum(List(ai,Length))=3 and Maximum(List(bi,Length))=2);
 Assert(0,Maximum(List(ci,Length))=r);
 A:=List(ai,w->List(x,y->ExponentSumWord(w,y)));
 B:=List(bi,w->List(x,y->ExponentSumWord(w,y)));
 C:=List(ci,w->List(x,y->ExponentSumWord(w,y)));
 # Row-vector convention: first c then a has matrix C*A.
 Assert(0,C*A=B*C and AbsInt(DeterminantMat(C))=1);
 KA:=NullspaceIntMat(A-IdentityMat(n));KB:=NullspaceIntMat(B-IdentityMat(n));
 expectedA:=IdentityMat(n){[r..n]};expectedA[1]:=Concatenation(List([1..r],i->1),List([r+1..n],i->0));
 expectedB:=IdentityMat(n){[r..n]};
 Assert(0,RankMat(KA)=r and RankMat(KB)=r);
 Assert(0,RankMat(Concatenation(KA,expectedA))=r and RankMat(Concatenation(KB,expectedB))=r);
 Assert(0,expectedB*C=expectedA);
 rankchecks:=rankchecks+1;total:=total+1;
 Print("CONTROL1424 r=",r," rank=",n," alpha_norm=3 beta_norm=2 conjugator_norm=",r,"\n");
od;
Print("PASS1424 cases=",total," generator_equations=",eqs," fixed_lattice_checks=",rankchecks,"\n");
end;
Verify1424();QUIT;
