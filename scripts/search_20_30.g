# Character-table screen; entries may duplicate isomorphism types.
LoadPackage("ctbllib");;
RunSearch:=function()
local names,name,t,irr,sizes,n,b,count,eligible,hits,linear,central;
names:=AllCharacterTableNames(); count:=0; eligible:=0; hits:=0;
for name in names do
    t:=CharacterTable(name);
    if t=fail then Error("missing table ",name); fi;
    count:=count+1;
    irr:=Irr(t); sizes:=SizesConjugacyClasses(t); n:=Size(t);
    linear:=Number(irr,c->c[1]=1);
    central:=Number(sizes,s->s=1);
    if linear<>1 or central<>1 then continue; fi;
    eligible:=eligible+1; b:=Maximum(sizes);
    if b*b<n then hits:=hits+1; Print("HIT "); fi;
    Print("TABLE name=",name," order=",n," max_class=",b,"\n");
od;
Print("DONE tables=",count," eligible=",eligible," hits=",hits,"\n");
end;
RunSearch();
QUIT;
