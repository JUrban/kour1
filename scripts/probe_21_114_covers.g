LoadPackage("smallgrp");;
LoadPackage("polycyclic");;
Read("results/21.114-cover-input.g");;

RunCovers114 := function()
    local pair,g,iso,q,epi,p,k,dl,checked,hits;
    checked := 0; hits := 0;
    for pair in CoverInputs114 do
        Print("COVER_START ",pair," runtime_ms=",Runtime(),"\n");
        g := SmallGroup(pair[1],pair[2]);
        iso := IsomorphismPcpGroup(g);
        q := Image(iso);
        epi := EpimorphismSchurCover(q);
        p := Source(epi);
        k := Kernel(epi);
        if not IsFinite(p) or not IsSubgroup(Centre(p),k) or
           Size(p) <> Size(q)*Size(k) then Error("invalid finite central cover"); fi;
        dl := Length(DerivedSeriesOfGroup(p))-1;
        checked := checked+1;
        if dl > DerivedLength(g) then hits := hits+1; fi;
        Print("COVER_ROW ",[pair[1],pair[2],Size(p),AbelianInvariants(k),dl,
                            NilpotencyClassOfGroup(p)],"\n");
    od;
    Print("PASS_21114_COVERS checked=",checked," increased_derived_length=",hits,"\n");
end;
RunCovers114();
QUIT;
