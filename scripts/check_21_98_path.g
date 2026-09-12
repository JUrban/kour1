SetAssertionLevel(1);
Check2198Path:=function()
local t,I,a,b,j,M,X,u,v,P,N,F,k,i,n,coeffs;
t:=Indeterminate(Rationals,"t"); I:=IdentityMat(6,Rationals);
a:=[]; b:=[];
for j in [1..4] do
 M:=ShallowCopy(I); M:=List(M,ShallowCopy); M[j][j+1]:=1;Add(a,M);
 M:=List(I,ShallowCopy); M[j+1][j+2]:=1;Add(b,M);
od;
u:=Comm(Comm(a[1],a[2]),Comm(a[3],a[4]));
v:=Comm(Comm(b[1],b[2]),Comm(b[3],b[4]));
M:=List(I,ShallowCopy); M[1][5]:=1; Assert(1,u=M);
M:=List(I,ShallowCopy); M[2][6]:=1; Assert(1,v=M);
X:=List([1..4],j->(I+(1-t)*(a[j]-I))*(I+t*(b[j]-I)));
P:=Comm(Comm(X[1],X[2]),Comm(X[3],X[4])); N:=P-I;
F:=NullMat(6,6,Rationals);
for k in [1..5] do F:=F+(-1)^(k+1)*N^k/k;od;
Assert(1,F[1][5]=(1-t)^4); Assert(1,F[2][6]=t^4);
Assert(1,Maximum(List(Flat(F),DegreeOfLaurentPolynomial))=5);
for i in [1..6] do
 for j in [i+1..6] do
  if F[i][j]<>0 then
   Print("PATH row=",i," col=",j," polynomial=",F[i][j],"\n");
  fi;
 od;
od;
Print("PASS_2198_PATH_GAP endpoints_independent=true degree=5\n");
end;
Check2198Path();
QUIT;
