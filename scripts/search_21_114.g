# Exact pilot of weak ab-maximality, restricted to nilpotency class >=3.
LoadPackage("smallgrp");;

CheckWeakAb114 := function(g)
    local bound,z,hom,q,classes,c,h,a,tested;
    bound := Index(g,DerivedSubgroup(g));
    z := Centre(g);
    hom := NaturalHomomorphismByNormalSubgroup(g,z);
    q := Image(hom);
    classes := ConjugacyClassesSubgroups(q);
    tested := 0;
    for c in classes do
        h := PreImage(hom,Representative(c));
        if Size(h) > bound then
            a := Index(h,DerivedSubgroup(h));
            tested := tested+1;
            if a > bound then
                return rec(weak:=false,tested:=tested,quotientclasses:=Length(classes),
                           subgrouporder:=Size(h),abelianization:=a);
            fi;
        fi;
    od;
    return rec(weak:=true,tested:=tested,quotientclasses:=Length(classes));
end;

Run114 := function()
    local orders,ord,id,g,cl,dl,a,r,total,eligible,weak,checks;
    orders := [64,81,128,243,729];
    total := 0; eligible := 0; weak := 0; checks := 0;
    for ord in orders do
        Print("ORDER_START ",ord," count=",NumberSmallGroups(ord),"\n");
        for id in [1..NumberSmallGroups(ord)] do
            g := SmallGroup(ord,id);
            cl := NilpotencyClassOfGroup(g);
            total := total+1;
            if cl >= 3 then
                eligible := eligible+1;
                dl := DerivedLength(g);
                a := Index(g,DerivedSubgroup(g));
                r := CheckWeakAb114(g);
                checks := checks+r.tested;
                Print("ROW114 ",[ord,id,cl,dl,a,r.weak,r.tested,r.quotientclasses]);
                if not r.weak then
                    Print(" WITNESS ",[r.subgrouporder,r.abelianization]);
                else weak := weak+1;
                fi;
                Print("\n");
            fi;
        od;
        Print("ORDER_DONE ",ord," total=",total," eligible=",eligible,
              " weak=",weak," checks=",checks," runtime_ms=",Runtime(),"\n");
    od;
    Print("PASS_21114_PILOT total=",total," eligible=",eligible,
          " weak=",weak," checks=",checks,"\n");
end;
Run114();
QUIT;
