# Exact library screen for Kourovka 17.100. Library entries need not be
# pairwise nonisomorphic; the reported coverage is character tables.
LoadPackage("ctbllib");;
RunSearch := function()
local names,name,t,irr,sizes,orders,oddrows,oddcols,i,j,checked,simple,
      pairs,hits,non2pairs,non2tables,non2cols;
names:=AllCharacterTableNames();
checked:=0; simple:=0; pairs:=0; hits:=0; non2pairs:=0; non2tables:=0;
for name in names do
    t:=CharacterTable(name);
    if t=fail then Error("unavailable ordinary table: ",name); fi;
    checked:=checked+1;
    if not IsSimpleCharacterTable(t) then continue; fi;
    simple:=simple+1;
    irr:=Irr(t); sizes:=SizesConjugacyClasses(t);
    orders:=OrdersClassRepresentatives(t);
    oddrows:=Filtered([1..Length(irr)],i->irr[i][1] mod 2=1);
    oddcols:=Filtered([1..Length(sizes)],j->sizes[j] mod 2=1);
    non2cols:=Filtered(oddcols,j->not ForAll(PrimeDivisors(orders[j]),p->p=2));
    if Length(non2cols)>0 then non2tables:=non2tables+1; fi;
    non2pairs:=non2pairs+Length(oddrows)*Length(non2cols);
    for i in oddrows do
        for j in oddcols do
            pairs:=pairs+1;
            if irr[i][j]=0 then
                hits:=hits+1;
                Print("HIT name=",name," row=",i," column=",j,
                    " degree=",irr[i][1]," class_size=",sizes[j],
                    " element_order=",orders[j],"\n");
            fi;
        od;
    od;
    Print("TABLE name=",name," order=",Size(t)," odd_rows=",Length(oddrows),
          " odd_columns=",Length(oddcols)," non2_columns=",Length(non2cols),"\n");
od;
Print("DONE tables=",checked," simple_tables=",simple," pairs=",pairs,
      " non2_tables=",non2tables," non2_pairs=",non2pairs," hits=",hits,"\n");
end;
RunSearch();
QUIT;
