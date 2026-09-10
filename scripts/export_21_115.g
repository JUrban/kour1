# Export every coset avoiding the identity, as sets of element indices.
# Right cosets suffice: every left coset is a right coset of a conjugate.
LoadPackage("smallgrp");;
if not IsBound(START_ORDER) then START_ORDER:=2; fi;
if not IsBound(END_ORDER) then END_ORDER:=64; fi;
if not IsBound(DATA_DIR) then DATA_DIR:="results/21.115-data"; fi;
SizeScreen([1000000,1000000]);;
checked:=0;;
for ord in [START_ORDER..END_ORDER] do
  for number in [1..NumberSmallGroups(ord)] do
    G:=SmallGroup(ord,number);
    if IsAbelian(G) then continue; fi;
    # Skip the already proved odd-derived class-two case.
    if IsNilpotentGroup(G) and NilpotencyClassOfGroup(G)<=2
       and IsOddInt(Size(DerivedSubgroup(G))) then continue; fi;
    elts:=AsSSortedList(G);
    identity:=Position(elts,One(G));
    sets:=[];
    for cl in ConjugacyClassesSubgroups(G) do
      for H in AsList(cl) do
        if Size(H)=ord then continue; fi;
        for c in RightCosets(G,H) do
          if One(G) in c then continue; fi;
          Add(sets,Set(AsList(c),x->Position(elts,x)));
        od;
      od;
    od;
    sets:=Set(sets);
    path:=Concatenation(DATA_DIR,"/",String(ord),"-",String(number),".json");
    PrintTo(path,"{\"group_id\":",[ord,number],",\"identity\":",identity,
      ",\"cosets\":",sets,"}\n");
    checked:=checked+1;
    Print("EXPORTED id=",[ord,number]," cosets=",Length(sets),"\n");
  od;
od;
Print("DONE exported=",checked,"\n");
QUIT;
