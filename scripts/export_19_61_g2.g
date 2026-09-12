SetAssertionLevel(1);
ExportG21961:=function()
local L,C,B,R,roots,powers,A,pow,row,k,x,out,alladj;
L:=SimpleLieAlgebra("G",2,Rationals);C:=ChevalleyBasis(L);
B:=Basis(L,Concatenation(C));R:=RootSystem(L);
roots:=Concatenation(PositiveRoots(R),NegativeRoots(R));powers:=[];
alladj:=List(B,x->AdjointMatrix(B,x));
for x in Concatenation(C[1],C[2]) do
  A:=AdjointMatrix(B,x);pow:=IdentityMat(14);row:=[];
  for k in [0..6] do
    Assert(0,ForAll(Concatenation(pow/Factorial(k)),IsInt));
    Add(row,pow/Factorial(k));pow:=pow*A;
    if IsZero(pow) then break;fi;
  od;
  Assert(0,IsZero(pow));Add(powers,row);
od;
out:=OutputTextFile("results/19.61-g2-integral.grows",false);
SetPrintFormattingStatus(out,false);AppendTo(out,[roots,powers,alladj,CartanMatrix(R)],"\n");CloseStream(out);
Print("PASS_1961_G2_INTEGRAL roots=",Length(roots)," dimension=14\n");
end;
ExportG21961();
QUIT;
