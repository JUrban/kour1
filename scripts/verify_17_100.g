LoadPackage("ctbllib");;
RunControls:=function()
local names,name,t,irr,faithful,i,j,checked,groups,g,cases,pairs,orders,sizes;
names:=AllCharacterTableNames(); checked:=0;
# Alternative simplicity criterion: every nonprincipal irreducible is faithful.
# Any proper nontrivial normal subgroup is contained in the kernel of a
# nonprincipal irreducible inflated from the corresponding quotient.
for name in names do
    t:=CharacterTable(name); irr:=Irr(t);
    faithful:=Size(t)>1 and ForAll(irr,chi->
        ForAll(chi,x->x=1) or
        ForAll([2..Length(chi)],j->chi[j]<>chi[1]));
    if faithful<>IsSimpleCharacterTable(t) then Error("simplicity mismatch ",name); fi;
    checked:=checked+1;
od;
groups:=[AlternatingGroup(5),AlternatingGroup(6),AlternatingGroup(7),
         PSL(2,7),PSL(2,8),PSL(2,11),PSL(2,13),PSL(3,3)];
cases:=0; pairs:=0;
for g in groups do
    if not IsSimpleGroup(g) then Error("control not simple"); fi;
    t:=CharacterTable(g); irr:=Irr(t);
    sizes:=SizesConjugacyClasses(t); orders:=OrdersClassRepresentatives(t);
    for i in [1..Length(irr)] do
        if irr[i][1] mod 2=0 then continue; fi;
        for j in [1..Length(sizes)] do
            if sizes[j] mod 2=0 then continue; fi;
            pairs:=pairs+1;
            if irr[i][j]=0 then Error("actual-group counterexample"); fi;
        od;
    od;
    cases:=cases+1;
    Print("GROUP order=",Size(g)," classes=",Length(irr)," PASS\n");
od;
Print("PASS simplicity_checks=",checked," actual_groups=",cases," pairs=",pairs,"\n");
end;
RunControls();
QUIT;
