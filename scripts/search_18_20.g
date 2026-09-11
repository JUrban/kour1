# Kourovka 18.20: exact two-projective-ratio test, with common zeros ignored.
# Including zero/infinite ratios makes this screen at least as broad as any
# convention requiring nonzero proportionality constants on both pieces.
LoadPackage("ctbllib");;
RunSearch:=function()
local names,name,t,irr,i,j,k,d1,d2,u,v,found,ok,checked,pairs,hits,eqpairs;
names:=AllCharacterTableNames();
checked:=0; pairs:=0; hits:=0; eqpairs:=0;
for name in names do
    t:=CharacterTable(name);
    if t=fail then Error("unavailable table: ",name); fi;
    irr:=Irr(t);
    for i in [1..Length(irr)] do
        for j in [i+1..Length(irr)] do
            d1:=irr[i][1]; d2:=irr[j][1];
            if d1=d2 then eqpairs:=eqpairs+1; continue; fi;
            pairs:=pairs+1; found:=false; ok:=true;
            for k in [2..Length(irr[i])] do
                if irr[i][k]*d2=irr[j][k]*d1 then continue; fi;
                if not found then
                    u:=irr[i][k]; v:=irr[j][k]; found:=true;
                elif irr[i][k]*v<>irr[j][k]*u then
                    ok:=false; break;
                fi;
            od;
            if ok and found then
                hits:=hits+1;
                Print("HIT name=",name," rows=",[i,j]," degrees=",[d1,d2],
                      " second_ratio=",[u,v],"\n");
            fi;
        od;
    od;
    checked:=checked+1;
    Print("TABLE name=",name," rows=",Length(irr)," total_pairs=",pairs,"\n");
od;
Print("DONE tables=",checked," unequal_degree_pairs=",pairs,
      " equal_degree_pairs=",eqpairs," hits=",hits,"\n");
end;
RunSearch();
QUIT;
