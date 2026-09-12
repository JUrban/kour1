SetAssertionLevel(1);
Diagnose2021:=function()
local ids,id,G,Z,D,inv,pair,a,b,j,counts,left,out;
ids:=Set(Concatenation(Pairs2021));inv:=[];
for id in ids do
  G:=SmallGroup(id);Z:=Center(G);D:=DerivedSubgroup(G);
  inv[id[2]]:=[Collected(List(Elements(G),Order)),
    Lcm(AbelianInvariants(G)),AbelianInvariants(G),
    Collected(List(Elements(Z),Order)),Collected(List(Elements(D),Order)),
    Collected(List(ConjugacyClasses(G),Size))];
od;
counts:=List([1..6],x->0);left:=[];
for pair in Pairs2021 do
  a:=inv[pair[1][2]];b:=inv[pair[2][2]];
  j:=PositionProperty([1..6],i->a[i]<>b[i]);
  if j=fail then Add(left,pair);else counts[j]:=counts[j]+1;fi;
od;
out:=OutputTextFile("results/20.21-order1536-invariant-diagnostic.grows",false);
SetPrintFormattingStatus(out,false);AppendTo(out,[Length(ids),counts,left],"\n");CloseStream(out);
Print("PASS_2021_INVARIANT_DIAGNOSTIC ",[Length(ids),counts,Length(left)],"\n");
end;
Diagnose2021();QUIT;
