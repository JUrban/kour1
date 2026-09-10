# Independent subgroup/quotient counts for small odd-exponent examples.
LoadPackage("smallgrp");;
Read("scripts/lib_19_20.g");;
SizeScreen([1000000,1000000]);;
(function()
local p,m,r,n,field,gens,i,a,E,G,c,key;
for p in [3,5] do
  for m in [1,2] do
    for r in [0,1,2] do
      n:=p^(2*m+1+r);
      if n>500 then continue; fi;
      field:=GF(p); gens:=[];
      for i in [2..m+1] do
        a:=IdentityMat(m+2,field); a[1][i]:=One(field); Add(gens,a);
        a:=IdentityMat(m+2,field); a[i][m+2]:=One(field); Add(gens,a);
      od;
      E:=Image(IsomorphismPcGroup(Group(gens)));
      if Size(E)<>p^(2*m+1) or Exponent(E)<>p or Size(DerivedSubgroup(E))<>p then
        Error("Heisenberg realization failed");
      fi;
      if r=0 then G:=E; else G:=DirectProduct(E,ElementaryAbelianGroup(p^r)); fi;
      Print("START p=",p," m=",m," r=",r," order=",n,"\n");
      c:=Kourovka19Counts(G);
      Print("COUNTS p=",p," m=",m," r=",r," order=",n," end=",c.ends," piso=",c.partials,"\n");
      for key in SortedList(RecNames(c.types)) do
        Print("TYPE p=",p," m=",m," r=",r," id=",key," values=",c.types.(key),"\n");
      od;
    od;
  od;
od;
Print("DONE runtime_ms=",Runtime(),"\n");
end)();
QUIT;
