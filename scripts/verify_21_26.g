# Independent direct-element verification of profiles, conjugator fibers, and
# the all-tuples statement for every group of non-prime-power order <= 60.
LoadPackage("smallgrp");;
Read("scripts/lib_21_26.g");;
(function()
local order,index,G,elements,profiles,profile,p,H,hs,intersections,allowed,
      optimized,allallowed,choices,tuple,holds,r,checked,setschecked,k,sylows,
      current,J,DirectGood;
DirectGood:=function(elements,hs)
  local intersections,J,good,x;
  intersections:=List(elements,x->Intersection(hs,Set(List(hs,h->h^x))));
  good:=List(intersections,J->not ForAny(intersections,K->Length(K)<Length(J) and IsSubset(J,K)));
  return good;
end;
checked:=0; setschecked:=0;
for order in [2..60] do
  if Length(Set(FactorsInt(order)))<=1 then continue; fi;
  for index in [1..NumberSmallGroups(order)] do
    G:=SmallGroup(order,index); elements:=Set(AsList(G));
    profiles:=List(Set(FactorsInt(order)),p->KourovkaSylowProfile(G,p));
    allallowed:=[];
    for profile in profiles do
      optimized:=KourovkaSylowGoodSets(G,profile,elements);
      allowed:=[];
      for k in [1..Length(profile.sylows)] do
        current:=DirectGood(elements,Set(AsList(profile.sylows[k])));
        if current<>optimized[k] then Error("Direct conjugator set mismatch",order,index,profile.p,k); fi;
        Add(allowed,current); setschecked:=setschecked+1;
      od;
      Add(allallowed,allowed);
    od;
    holds:=true;
    for tuple in Cartesian(allallowed) do
      if not ForAny([1..order],k->ForAll(tuple,bits->bits[k])) then holds:=false; break; fi;
    od;
    r:=KourovkaCheck21_26(G);
    if r.holds<>holds then Error("Direct all-tuples result mismatch",order,index); fi;
    checked:=checked+1;
  od;
od;
Print("PASS groups=",checked," exact_conjugator_sets=",setschecked," orders=2..60\n");
end)();
QUIT;
