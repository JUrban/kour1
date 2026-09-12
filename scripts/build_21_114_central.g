LoadPackage("smallgrp");;
LoadPackage("polycyclic");;

ExportModel114 := function(g,label,path)
    local iso,h,els,gens,d,n,perms,edges;
    iso := IsomorphismPermGroup(g);
    h := Image(iso); els := Elements(h); gens := GeneratorsOfGroup(h);
    d := LargestMovedPoint(h); n := Size(h);
    perms := List(gens,a->List([1..d],i->i^a-1));
    edges := List(els,a->List(gens,b->Position(els,a*b)-1));
    PrintTo(path,"{\"catalogue_id\":",[n,label],",\"identity\":",Position(els,One(h))-1,
            ",\"permutations\":",perms,",\"cayley\":",edges,"}\n");
    return rec(iso:=iso,group:=h,elements:=els);
end;

RunCentral114 := function()
    local id,q,pcq,epi,iso,c,k,dd,subs,l,m,h,p,z,qhom,quot,
          pm,qm,zinds,map,info,path,n,r;
    for id in [854,860] do
        q := SmallGroup(128,id);
        pcq := Image(IsomorphismPcpGroup(q));
        epi := EpimorphismSchurCover(pcq);
        iso := IsomorphismPcGroup(Source(epi));
        c := Image(iso); k := Image(iso,Kernel(epi));
        dd := DerivedSubgroup(DerivedSubgroup(c));
        if Size(dd)=1 or not IsSubgroup(k,dd) then Error("missing derived witness"); fi;
        subs := List(ConjugacyClassesSubgroups(k),Representative);
        l := TrivialSubgroup(k);
        for m in subs do
            if Size(m)>Size(l) and not IsSubgroup(m,dd) then l:=m; fi;
        od;
        h := NaturalHomomorphismByNormalSubgroup(c,l);
        p := Image(h); z := Image(h,k);
        if not IsCyclic(z) or not IsSubgroup(Centre(p),z) or
           DerivedLength(p)<>3 then Error("invalid cyclic central extension"); fi;
        qhom := NaturalHomomorphismByNormalSubgroup(p,z);
        quot := Image(qhom);
        if IdGroup(quot)<>[128,id] then Error("wrong quotient"); fi;
        path := Concatenation("results/21.114-central-",String(id));
        pm := ExportModel114(p,0,Concatenation(path,"-p.json"));
        qm := ExportModel114(quot,id,Concatenation(path,"-q.json"));
        zinds := List(Elements(Image(pm.iso,z)),x->Position(pm.elements,x)-1);
        map := List(pm.elements,x->Position(qm.elements,
                    Image(qm.iso,Image(qhom,PreImagesRepresentative(pm.iso,x))))-1);
        PrintTo(Concatenation(path,"-map.json"),"{\"source_id\":",[128,id],
                ",\"central_kernel\":",zinds,",\"quotient_map\":",map,
                ",\"kernel_order\":",Size(z),",\"source_order\":",Size(p),
                ",\"constructed_order\":",Size(p)*Size(z)^2,"}\n");
        Print("CENTRAL_ROW ",[id,Size(c),Size(k),Size(l),Size(p),Size(z),
                              Size(DerivedSubgroup(DerivedSubgroup(p))),
                              NilpotencyClassOfGroup(p),Size(p)*Size(z)^2],"\n");
    od;
    Print("PASS_21114_CENTRAL_EXPORT\n");
end;
RunCentral114();
QUIT;
