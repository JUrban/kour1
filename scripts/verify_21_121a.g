# Exact subgroup audit of the first two finite groups in the construction.
LoadPackage("smallgrp");;
(function()
local S,z,k,n,D,embeddings,codegens,bit,v,indices,zprod,C,G,
      classes,cl,H,U,A,A0,r,checked,subgroups;
S:=SmallGroup(24,3);
if IsomorphismGroups(S,SL(2,3))=fail then Error("Wrong base group"); fi;
z:=First(Elements(Centre(S)),x->Order(x)=2);
if z=fail then Error("Missing central involution"); fi;
for k in [1..2] do
  n:=2^k-1;
  D:=DirectProduct(List([1..n],i->S));
  embeddings:=List([1..n],i->Embedding(D,i));
  codegens:=[];
  for bit in [0..k-1] do
    zprod:=One(D);
    for v in [1..n] do
      if QuoInt(v,2^bit) mod 2=1 then zprod:=zprod*Image(embeddings[v],z); fi;
    od;
    Add(codegens,zprod);
  od;
  C:=Subgroup(D,codegens);
  if Size(C)<>2^k or not IsSubgroup(Centre(D),C) then Error("Code subgroup mismatch"); fi;
  G:=FactorGroup(D,C);
  if Size(G)<>24^n/2^k then Error("Group order mismatch"); fi;
  if Size(PCore(G,3))<>1 then Error("Unexpected odd normal subgroup"); fi;
  Print("GROUP k=",k," n=",n," order=",Size(G)," sylow2_order=",Size(SylowSubgroup(G,2)),"\n");
  classes:=ConjugacyClassesSubgroups(G);
  checked:=0; subgroups:=0;
  for cl in classes do
    H:=Representative(cl);
    U:=SylowSubgroup(H,2); A:=SylowSubgroup(H,3);
    if not IsNormal(H,U) or not IsElementaryAbelian(A) then Error("Subgroup decomposition mismatch"); fi;
    A0:=Centralizer(A,U);
    if not IsNormal(H,A0) or not IsAbelian(A0) or Size(A0) mod 2=0 then Error("Invalid abelian odd subgroup"); fi;
    r:=LogInt(Size(A)/Size(A0),3);
    if 3^r<>Size(A)/Size(A0) then Error("Non-integral action rank"); fi;
    if Size(U)*(r+1)<8^r then Error("Main subgroup bound failed",k,GeneratorsOfGroup(H),Size(U),r); fi;
    if Index(H,A0)<>Size(U)*3^r then Error("Index formula failed"); fi;
    checked:=checked+1; subgroups:=subgroups+Size(cl);
  od;
  Print("PASS k=",k," subgroup_classes=",checked," subgroups=",subgroups,
        " runtime_ms=",Runtime(),"\n");
od;
Print("DONE\n");
end)();
QUIT;
