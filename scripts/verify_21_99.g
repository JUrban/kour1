# Compare orbital/class reduction with independent complete element enumeration.
LoadPackage("transgrp");;
RunVerification := function()
local count,n,i,g,s,orbits,labels,j,x,transport,covered,c,fixed,
      via_classes,via_elements;
count := 0;
for n in [2..8] do
    for i in [1..NrTransitiveGroups(n)] do
        g := TransitiveGroup(n,i);
        s := Stabilizer(g,1);
        orbits := Orbits(s,[1..n]);
        labels := List([1..n],x->0);
        for j in [1..Length(orbits)] do
            for x in orbits[j] do labels[x] := j; od;
        od;
        transport := List([1..n],x->RepresentativeAction(g,x,1));
        covered := [];
        for c in List(ConjugacyClasses(g),Representative) do
            fixed := Number([1..n],x->x^c=x);
            if fixed<>1 then
                for x in [1..n] do
                    AddSet(covered,labels[(x^c)^transport[x]]);
                od;
            fi;
        od;
        via_classes := Set(Concatenation(orbits{covered}));
        via_elements := Set(List(Filtered(Elements(g),c->
            Number([1..n],x->x^c=x)<>1),c->1^c));
        if via_classes<>via_elements then
            Error("orbital reduction mismatch",n,i);
        fi;
        count := count+1;
    od;
    Print("DEGREE_VERIFIED ",n,"\n");
od;
Print("PASS groups=",count," degrees=2..8; class/orbital method agrees with full element enumeration.\n");
end;
RunVerification();
QUIT;
