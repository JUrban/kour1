LoadPackage("ctbllib");;
SetInfoLevel(InfoWarning,0);;

SquarePrimes1884 := function(t,i)
    local orders,k,c,pr;
    orders:=OrdersClassRepresentatives(t);
    pr:=Set(Filtered(FactorsInt(orders[i]),p->p>1));
    for k in [1..Length(orders)] do
        c:=ClassMultiplicationCoefficient(t,i,i,k);
        if not IsInt(c) or c<0 then Error("invalid coefficient");fi;
        if c>0 then UniteSet(pr,Set(Filtered(FactorsInt(orders[k]),p->p>1)));fi;
    od;
    return pr;
end;;

Pilot1884 := function()
    local pairs,pair,n,g,on,og,i,j,pr,pg,bad,sq,seen,tests,passes;
    pairs:=[
      ["O8+(2)","O8+(2).2"],["O8+(2)","O8+(2).3"],
      ["O8+(2)","O8+(2).S3"],["S4(4)","S4(4).2"],
      ["S4(4)","S4(4).4"],["G2(3)","G2(3).2"],
      ["U4(3)","U4(3).D8"],["L3(4)","L3(4).D12"],
      ["U4(2)","U4(2).2"],["S6(2)","S6(2)"],
      ["O8+(3)","O8+(3).S4"]
    ];
    tests:=0;passes:=0;
    for pair in pairs do
        n:=CharacterTable(pair[1]);g:=CharacterTable(pair[2]);
        if n=fail or g=fail then Print("MISSING ",pair,"\n");continue;fi;
        Print("PAIR ",pair," orders ",[Size(n),Size(g)],"\n");
        on:=OrdersClassRepresentatives(n);og:=OrdersClassRepresentatives(g);
        pg:=Set(FactorsInt(Size(n)));seen:=[];
        for i in Filtered([1..Length(on)],i->on[i]=2) do
            pr:=SquarePrimes1884(n,i);
            if IsSubset(pr,pg) or pr in seen then continue;fi;
            Add(seen,pr);tests:=tests+1;bad:=[];
            for j in [2..Length(og)] do
                if IsSubset(pr,Set(Filtered(FactorsInt(og[j]),p->p>1))) then
                    sq:=SquarePrimes1884(g,j);
                    if IsSubset(pr,sq) then Add(bad,j);fi;
                fi;
            od;
            Print("TEST normal_class=",i," pi=",pr," unresolved_G_classes=",bad,"\n");
            if IsEmpty(bad) then
                passes:=passes+1;
                Print("CANDIDATE_1884 ",pair," ",i," ",pr,"\n");
            fi;
        od;
    od;
    Print("PASS_1884_PILOT tests=",tests," candidates=",passes,"\n");
end;;
for pair in [["F4(2)","F4(2).2"],["G2(3)","G2(3).2"],["O8+(2).3","O8+(2).S3"]] do
 n:=CharacterTable(pair[1]);g:=CharacterTable(pair[2]);;
 Print("PAIR ",pair,"\n");
 on:=OrdersClassRepresentatives(n);og:=OrdersClassRepresentatives(g);;
 for i in [1..Length(on)] do
  if not IsPrimeInt(on[i]) then continue;fi;
  pr:=SquarePrimes1884(n,i);;
  if IsSubset(pr,Set(FactorsInt(Size(n)))) then continue;fi;
  bad:=[];;
  for j in [2..Length(og)] do
   if IsSubset(pr,Set(Filtered(FactorsInt(og[j]),p->p>1))) then
    sq:=SquarePrimes1884(g,j);;
    if IsSubset(pr,sq) then Add(bad,j);fi;
   fi;
  od;
  Print("TEST class=",i," order=",on[i]," pi=",pr," unresolved=",bad,"\n");
 od;
od;
Print("PASS_1884_EXCEPTIONAL\n");
QUIT;
