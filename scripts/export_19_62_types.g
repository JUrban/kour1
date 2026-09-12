SetAssertionLevel(1);
ExportType1962:=function(letter,rank)
local L,C,B,R,roots,powers,A,pow,row,k,x,out,alladj,dim,tag;
L:=SimpleLieAlgebra(letter,rank,Rationals);C:=ChevalleyBasis(L);
B:=Basis(L,Concatenation(C));R:=RootSystem(L);dim:=Dimension(L);
roots:=Concatenation(PositiveRoots(R),NegativeRoots(R));powers:=[];
alladj:=List(B,x->AdjointMatrix(B,x));
for x in Concatenation(C[1],C[2]) do
  A:=AdjointMatrix(B,x);pow:=IdentityMat(dim);row:=[];
  for k in [0..6] do
    Assert(0,ForAll(Concatenation(pow/Factorial(k)),IsInt));
    Add(row,pow/Factorial(k));pow:=pow*A;
    if IsZero(pow) then break;fi;
  od;
  Assert(0,IsZero(pow));Add(powers,row);
od;
tag:=Concatenation(LowercaseString(letter),String(rank));
out:=OutputTextFile(Concatenation("results/19.62-",tag,"-integral.grows"),false);
SetPrintFormattingStatus(out,false);AppendTo(out,[roots,powers,alladj,CartanMatrix(R)],"\n");CloseStream(out);
Print("PASS_1962_INTEGRAL ",tag," roots=",Length(roots)," dimension=",dim,"\n");
end;
for pair1962 in [["A",2],["A",3],["A",4],["B",2],["B",3],["B",4],["C",3],["C",4],["D",4],["F",4]] do
  ExportType1962(pair1962[1],pair1962[2]);
od;
Print("PASS_1962_ALL_INTEGRAL types=10\n");
QUIT;
