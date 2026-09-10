# Kourovka 21.99: enumerate conjugacy classes and orbital supports.
# A conjugacy class C meets {g: alpha^g=beta} iff some representative c
# has (gamma,gamma^c) in the same G-orbital as (alpha,beta).
# This avoids enumeration of all elements of potentially large groups.
LoadPackage("transgrp");;
RunSearch := function()
local checked,twotransitive,n,total,index,g,stab,suborbits,labels,i,x,
      transport,covered,classes,cl,c,fixed;
checked := 0;; twotransitive := 0;;
for n in [2..20] do
    total := NrTransitiveGroups(n);
    for index in [1..total] do
        g := TransitiveGroup(n,index);
        stab := Stabilizer(g,1);
        suborbits := Orbits(stab,[1..n]);
        if Length(suborbits)=2 then
            # Jordan's elementary derangement theorem settles rank two:
            # every off-diagonal pair lies in the unique non-diagonal orbital.
            twotransitive := twotransitive+1;
            continue;
        fi;
        labels := List([1..n],x->0);
        for i in [1..Length(suborbits)] do
            for x in suborbits[i] do labels[x] := i; od;
        od;
        transport := List([1..n],x->RepresentativeAction(g,x,1));
        covered := [labels[1]];
        classes := ConjugacyClasses(g);
        for cl in classes do
            c := Representative(cl);
            fixed := Number([1..n],x->x^c=x);
            if fixed=1 then continue; fi;
            for x in [1..n] do
                AddSet(covered,labels[(x^c)^transport[x]]);
            od;
            if Length(covered)=Length(suborbits) then break; fi;
        od;
        if Length(covered)<>Length(suborbits) then
            Print("HIT n=",n," index=",index," order=",Size(g),
                  " suborbits=",suborbits," covered=",covered,"\n");
        fi;
        checked := checked+1;
        if checked mod 100=0 then
            Print("PROGRESS checked=",checked," n=",n," index=",index,
                  " runtime_ms=",Runtime(),"\n");
        fi;
    od;
    Print("DEGREE_DONE n=",n," total=",total," checked=",checked,
          " rank_two=",twotransitive,"\n");
od;
Print("DONE checked=",checked," rank_two=",twotransitive,"\n");
end;
RunSearch();
QUIT;
