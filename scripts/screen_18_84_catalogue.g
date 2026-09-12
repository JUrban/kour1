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

Catalogue1884:=function()
 local names,name,n,g,info,aut,seen,climit,on,og,pr,pg,sq,sets,i,j,bad,tests,groups,skipped;
 names:=AllCharacterTableNames(IsSimple,true);seen:=[];tests:=0;groups:=0;skipped:=0;climit:=150;
 for name in names do
  n:=CharacterTable(name);
  if Identifier(n) in seen then continue;fi;
  Add(seen,Identifier(n));
  if not HasExtensionInfoCharacterTable(n) then continue;fi;
  info:=ExtensionInfoCharacterTable(n);
  if info[2]="" then continue;fi;
  aut:=Concatenation(Identifier(n),".",info[2]);
  g:=CharacterTable(aut);
  if g=fail then Print("MISSING ",Identifier(n)," ",aut,"\n");skipped:=skipped+1;continue;fi;
  if Length(Irr(n))>climit or Length(Irr(g))>climit then
   Print("CLASS_CAP ",Identifier(n)," ",aut,"\n");skipped:=skipped+1;continue;
  fi;
  groups:=groups+1;on:=OrdersClassRepresentatives(n);og:=OrdersClassRepresentatives(g);
  pg:=Set(FactorsInt(Size(n)));sets:=[];
  Print("PAIR ",Identifier(n)," ",Identifier(g),"\n");
  for i in [1..Length(on)] do
   if on[i]<>2 then continue;fi;
   pr:=SquarePrimes1884(n,i);
   if IsSubset(pr,pg) or pr in sets then continue;fi;
   Add(sets,pr);tests:=tests+1;bad:=[];
   for j in [1..Length(og)] do
    if og[j]<>2 then continue;fi;
    sq:=SquarePrimes1884(g,j);
    if IsSubset(pr,sq) then Add(bad,j);fi;
   od;
   Print("TEST normal_class=",i," pi=",pr," G_involution_obstructions=",bad,"\n");
   if IsEmpty(bad) then Print("NEEDS_FURTHER_TEST ",Identifier(n)," ",Identifier(g)," ",i," ",pr,"\n");fi;
  od;
 od;
 Print("PASS_1884_CATALOGUE groups=",groups," tests=",tests," skipped=",skipped,"\n");
end;;
Catalogue1884();
QUIT;
