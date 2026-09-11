# Independent rational matrix algebra and actual automorphism controls.
SetAssertionLevel(2);
(function()
local n,I,N,k,j,m,c,X,H,A,B,gram,rad,radmats,a,b,E,G,elts,P,Q,
      generators,tuples,q,t,aut,orbs,ei,p,unit,tracechecks;
unit:=function(n,i,j)
  local e;
  e:=NullMat(n,n,Rationals); e[i][j]:=1; return e;
end;
tracechecks:=0;
for n in [1..6] do
  I:=IdentityMat(n,Rationals);
  generators:=[];
  for j in [1..n] do Add(generators,I-2*unit(n,j,j)); od;
  for j in [1..n-1] do Add(generators,I+unit(n,j,j+1)); od;
  A:=AlgebraWithOne(Rationals,generators);
  B:=BasisVectors(Basis(A));
  Assert(0,Dimension(A)=n*(n+1)/2);
  gram:=List(B,a->List(B,b->TraceMat(a*b)));
  rad:=NullspaceMat(gram);
  Assert(0,Length(rad)=n*(n-1)/2);
  if Length(rad)>0 then
    radmats:=List(rad,c->Sum([1..Length(B)],j->c[j]*B[j]));
    for a in radmats do
      Assert(0,ForAll([1..n],i->ForAll([1..i],j->a[i][j]=0)));
      Assert(0,a^n=0*I);
      for b in B do Assert(0,TraceMat(a*b)=0); tracechecks:=tracechecks+1; od;
    od;
  fi;
  if n>1 then
    N:=Sum([1..n-1],j->unit(n,j,j+1)); H:=I+N;
    Assert(0,N^(n-1)=unit(n,1,n));
    for k in [1..5] do
      m:=3^k; c:=1; X:=I;
      for j in [1..n-1] do c:=c*(1/m-j+1)/j; X:=X+c*N^j; od;
      Assert(0,X^m=H);
    od;
  fi;
  Print("PASS triangular n=",n," dimension=",Dimension(A),
        " trace_radical_dimension=",Length(rad),"\n");
od;

G:=AlternatingGroup(5); elts:=Elements(G);
Assert(0,Size(G)=60 and not IsSolvableGroup(G));
aut:=AutomorphismGroup(G);
orbs:=Orbits(aut,elts);
Assert(0,Length(orbs)=4 and SortedList(List(orbs,Length))=[1,15,20,24]);
P:=List(elts,p->DirectSumMat(PermutationMat(p,5,Rationals),IdentityMat(2,Rationals)));
I:=IdentityMat(7,Rationals); E:=unit(7,6,7);
A:=AlgebraWithOne(Rationals,Concatenation(P,[I+E]));
B:=BasisVectors(Basis(A));
Assert(0,Dimension(A)=18);
gram:=List(B,a->List(B,b->TraceMat(a*b)));
rad:=NullspaceMat(gram);
Assert(0,Length(rad)=1);
a:=Sum([1..Length(B)],j->rad[1][j]*B[j]);
Assert(0,a[6][7]<>0 and a=a[6][7]*E);
tuples:=[];
for p in P do
  t:=List(B,b->TraceMat(p*b)); Add(tuples,t);
  for q in [-2,-1/3,0,1/2,3] do
    Q:=p+q*E;
    Assert(0,List(B,b->TraceMat(Q*b))=t);
  od;
od;
Assert(0,Length(Set(tuples))=60);
X:=[[0,-1],[1,-1]];
for k in [1..24] do
  Assert(0,(X^(2^k mod 3))^(2^k)=X);
od;
Assert(0,TraceMat([[1,1],[0,1]]*[[1,0],[1,1]])=3);
Print("PASS A5_times_Q algebra_dimension=18 radical_dimension=1 quotient=60",
      " automorphism_orbit_upper_bound=8\n");
Print("DONE trace_pairing_controls=",tracechecks,
      " unipotent_root_controls=25 finite_order_root_controls=24\n");
end)();
QUIT;
