# Multisets of ordinary degrees, screening 21.59(a) and 21.135.
# Collisions are candidates only: table names may describe isomorphic groups,
# and radical/structure conditions require separate proof.
LoadPackage("ctbllib");;
RunSearch := function()
local names,dict,name,t,degrees,key,prior,entry,checked,almost,count;
names := AllCharacterTableNames();
dict := NewDictionary("",true);
checked := 0; count := 0;
for name in names do
    t := CharacterTable(name);
    if t=fail then continue; fi;
    degrees := Collected(List(Irr(t),chi->chi[1]));
    key := String(degrees);
    almost := IsAlmostSimpleCharacterTable(t);
    entry := rec(name:=name,almost:=almost,order:=Size(t));
    prior := LookupDictionary(dict,key);
    if prior=fail then
        AddDictionary(dict,key,[entry]);
    else
        if almost or ForAny(prior,x->x.almost) then
            Print("CANDIDATE degree_multiset=",degrees," current=",entry,
                  " previous=",prior,"\n");
            count := count+1;
        fi;
        Add(prior,entry);
    fi;
    checked := checked+1;
    if checked mod 100=0 then
        Print("PROGRESS checked=",checked," runtime_ms=",Runtime(),"\n");
    fi;
od;
Print("DONE tables=",checked," candidate_collisions=",count,"\n");
end;
RunSearch();
QUIT;
