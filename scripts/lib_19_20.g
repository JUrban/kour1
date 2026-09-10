# Counts by isomorphism type; cache only scalar automorphism-group orders.
Kourovka19AutCache:=rec();;
Kourovka19Counts:=function(G)
local data,cl,U,id,key,N,L,row,ends,partials;
data:=rec();
for cl in ConjugacyClassesSubgroups(G) do
  U:=Representative(cl); id:=IdGroup(U);
  key:=Concatenation(String(id[1]),"_",String(id[2]));
  if not IsBound(Kourovka19AutCache.(key)) then
    Kourovka19AutCache.(key):=Size(AutomorphismGroup(U));
  fi;
  if not IsBound(data.(key)) then data.(key):=[0,0,Kourovka19AutCache.(key)]; fi;
  data.(key)[1]:=data.(key)[1]+Size(cl);
od;
for N in NormalSubgroups(G) do
  L:=FactorGroup(G,N); id:=IdGroup(L);
  key:=Concatenation(String(id[1]),"_",String(id[2]));
  # A quotient type absent among subgroups contributes no endomorphisms.
  if IsBound(data.(key)) then data.(key)[2]:=data.(key)[2]+1; fi;
od;
ends:=0; partials:=0;
for key in RecNames(data) do
  row:=data.(key);
  ends:=ends+row[1]*row[2]*row[3];
  partials:=partials+row[1]^2*row[3];
od;
return rec(ends:=ends,partials:=partials);
end;;
