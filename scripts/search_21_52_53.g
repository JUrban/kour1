# Exact colored involution-class graph search. Run through bin/gap.
LoadPackage("digraphs");;
SetInfoLevel(InfoDigraphs,0);;

(function()
local cases,n,q,item,G,classes,c,D,m,orders,i,j,vals,adj,fullcols,
      shortcols,digraph,full,short,hom,inner,gens,p,checked,skipped,
      bad52,bad53,t,perm,PreservesOrders,NormalizesInner,dgens,sub,
      extends,map,images;

PreservesOrders := function(perm,orders)
  local i,j;
  for i in [1..Length(orders)] do
    for j in [i+1..Length(orders)] do
      if orders[i][j] <> orders[i^perm][j^perm] then return false; fi;
    od;
  od;
  return true;
end;
NormalizesInner := function(perm,inner)
  return ForAll(GeneratorsOfGroup(inner), g -> g^perm in inner);
end;

cases := [];
for n in [5..9] do Add(cases,rec(name:=Concatenation("A",String(n)),group:=AlternatingGroup(n))); od;
for q in [5,7,8,9,11,13,16,17,19,23,25,27,29,31,32,37,41,43] do
  Add(cases,rec(name:=Concatenation("PSL2(",String(q),")"),group:=PSL(2,q)));
od;
for q in [2,3,4] do Add(cases,rec(name:=Concatenation("PSL3(",String(q),")"),group:=PSL(3,q))); od;
Add(cases,rec(name:="PSU3(3)",group:=PSU(3,3)));
checked:=0; skipped:=0; bad52:=0; bad53:=0;
for item in cases do
  G:=item.group;
  if not IsSimpleGroup(G) then Error("Non-simple input"); fi;
  p:=Filtered(Set(FactorsInt(Size(G))),x->x>2)[1];
  Print("GROUP_START ",item.name," order=",Size(G)," runtime_ms=",Runtime(),"\n");
  classes:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);
  for c in classes do
    m:=Size(c);
    if m>1000 then
      Print("SKIP ",item.name," involution_class_size=",m," cutoff=1000\n");
      skipped:=skipped+1; continue;
    fi;
    D:=Set(AsList(c));
    orders:=List([1..m],i->List([1..m],j->1));
    for i in [1..m] do for j in [i+1..m] do
      t:=Order(D[i]*D[j]); orders[i][j]:=t; orders[j][i]:=t;
    od; od;
    vals:=Set(Concatenation(orders));
    adj:=List([1..m],i->Difference([1..m],[i]));
    fullcols:=List([1..m],i->List(adj[i],j->Position(vals,orders[i][j])));
    # Compact colors must be 1..k without gaps.
    vals:=Set(Concatenation(fullcols));
    fullcols:=List(fullcols,row->List(row,x->Position(vals,x)));
    shortcols:=List([1..m],i->List(adj[i],function(j)
      if orders[i][j]=2 then return 1; elif orders[i][j]=p then return 2; else return 3; fi;
    end));
    vals:=Set(Concatenation(shortcols));
    shortcols:=List(shortcols,row->List(row,x->Position(vals,x)));
    digraph:=Digraph(adj);
    if OutNeighbours(digraph)<>adj then Error("Adjacency ordering changed"); fi;
    hom:=ActionHomomorphism(G,D,OnPoints);
    inner:=Image(hom);
    if Size(inner)<>Size(G) then Error("Conjugation action not faithful"); fi;
    dgens:=[]; sub:=TrivialSubgroup(G);
    for t in D do
      if not t in sub then Add(dgens,t); sub:=Group(dgens); fi;
      if Size(sub)=Size(G) then break; fi;
    od;
    if Size(sub)<>Size(G) then Error("Involution class did not generate simple group"); fi;
    full:=AutomorphismGroup(digraph,fail,fullcols);
    short:=AutomorphismGroup(digraph,fail,shortcols);
    if not ForAll(GeneratorsOfGroup(full),g->PreservesOrders(g,orders)) then Error("Full color check failed"); fi;
    if not IsSubgroup(full,inner) or not IsSubgroup(short,full) then Error("Expected group inclusion failed"); fi;
    checked:=checked+1;
    Print("CASE ",item.name," class_size=",m," orders=",Set(Concatenation(orders)),
          " full_aut=",Size(full)," two_color_aut=",Size(short)," runtime_ms=",Runtime(),"\n");
    for perm in GeneratorsOfGroup(full) do
      extends:=NormalizesInner(perm,inner);
      if extends then
        images:=List(dgens,t->D[PositionSorted(D,t)^perm]);
        map:=GroupHomomorphismByImages(G,G,dgens,images);
        extends:=map<>fail and IsBijective(map);
        if extends then
          extends:=ForAll([1..m],i->Image(map,D[i])=D[i^perm]);
        fi;
      fi;
      if not extends then
        bad52:=bad52+1;
        Print("HIT_21_52 ",item.name," class_representative=",D[1]," class=",D," witness=",perm,"\n");
        break;
      fi;
    od;
    if Size(short)<>Size(full) then
      perm:=First(GeneratorsOfGroup(short),g->not PreservesOrders(g,orders));
      if perm=fail then Error("Size discrepancy without a witness"); fi;
      bad53:=bad53+1;
      Print("HIT_21_53 ",item.name," class_representative=",D[1]," class=",D," witness=",perm,"\n");
    fi;
  od;
od;
Print("DONE groups=",Length(cases)," classes_checked=",checked," classes_skipped=",skipped,
      " hits_21_52=",bad52," hits_21_53=",bad53," runtime_ms=",Runtime(),"\n");
end)();
QUIT;
