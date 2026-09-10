# Realize the binary model as a central product, then use independent GAP counts.
LoadPackage("smallgrp");;
Read("scripts/lib_19_20.g");;
(function()
local D,z,T,C,E,G,r,key;
D:=DihedralGroup(8); z:=First(Elements(Centre(D)),x->Order(x)=2);
T:=DirectProduct(D,D);
C:=Group(Image(Embedding(T,1),z)*Image(Embedding(T,2),z));
E:=FactorGroup(T,C); G:=DirectProduct(E,CyclicGroup(2));
if Size(E)<>32 or Size(G)<>64 or IdGroup(G)<>[64,264] then
  Error("Extraspecial realization failed");
fi;
r:=Kourovka19Counts(G);
if r.ends<>6074368 or r.partials<>3277312 then Error("Count mismatch"); fi;
Print("PASS group=SmallGroup(64,264) end=",r.ends," piso=",r.partials,"\n");
for key in SortedList(RecNames(r.types)) do
  Print("TYPE ",key," subgroup_count,quotient_count,aut_order=",r.types.(key),"\n");
od;
Print("DONE runtime_ms=",Runtime(),"\n");
end)();
QUIT;
