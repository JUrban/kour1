LoadPackage("smallgrp");;
Screen18120 := function()
local orders,out,first,n,id,g,cl,classes,subs,aa,bb,a,b,k,int,total,tested,skipped,groups,flags,row,els,ags,bgs,sgc;
orders := [32,64,81,125,128,243,343,625,729];
out := OutputTextFile("results/18.120-pilot.json",false);SetPrintFormattingStatus(out,false);
PrintTo(out,"{\"orders\":",orders,",\"rows\":[");first:=true;groups:=0;flags:=0;total:=0;
for n in orders do
 for id in [1..NumberSmallGroups(n)] do
  g:=SmallGroup(n,id);cl:=NilpotencyClassOfGroup(g);tested:=0;sgc:=0;
  if cl>4 then
   classes:=ConjugacyClassesSubgroups(g);sgc:=Length(classes);
   aa:=Concatenation(List(Filtered(classes,c->IsAbelian(Representative(c))),c->AsList(c)));
   bb:=List(Filtered(classes,c->NilpotencyClassOfGroup(Representative(c))=2),Representative);
   for b in bb do
    for a in aa do
     if Size(a)*Size(b)=n and Size(Intersection(a,b))=1 then
      tested:=tested+1;k:=ClosureGroup(a,DerivedSubgroup(b));int:=Intersection(k,b);
      if not IsAbelian(int) then
       flags:=flags+1;els:=Elements(g);ags:=List(GeneratorsOfGroup(a),x->Position(els,x)-1);bgs:=List(GeneratorsOfGroup(b),x->Position(els,x)-1);
       Print("FLAG_18120 ",n," ",id," A ",ags," B ",bgs," intersection ",Size(int),"\n");
      fi;
     fi;
    od;
   od;
  fi;
  if not first then PrintTo(out,",");fi;first:=false;
  PrintTo(out,"{\"order\":",n,",\"id\":",id,",\"class\":",cl,",\"subgroup_classes\":",sgc,",\"disjoint_factorizations\":",tested,"}");
  groups:=groups+1;total:=total+tested;
  if groups mod 100=0 then Print("PROGRESS_18120 ",n," ",id," groups ",groups," factorizations ",total," flags ",flags,"\n");fi;
 od;
 Print("ORDER_18120 ",n," groups ",groups," factorizations ",total," flags ",flags,"\n");
od;
PrintTo(out,"],\"groups\":",groups,",\"disjoint_factorizations\":",total,",\"flags\":",flags,"}\n");CloseStream(out);
Print("PASS_18120_PILOT\n");
end;;
Screen18120();;
QUIT;
