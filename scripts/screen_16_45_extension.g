LoadPackage("smallgrp");;
SetInfoLevel(InfoWarning,0);;
Run1645 := function()
local orders,output,first,total,unresolved,n,id,g,classes,subs,ranks,rank,tops,abelian,normalphi;
orders := [81,125,128,243,343,625];;
output := OutputTextFile("results/16.45-extension.json",false);;
SetPrintFormattingStatus(output,false);;
PrintTo(output,"{\"orders\":",orders,",\"rows\":[");;
first := true;; total := 0;; unresolved := 0;;
for n in orders do
  for id in [1..NumberSmallGroups(n)] do
    g := SmallGroup(n,id);;
    classes := ConjugacyClassesSubgroups(g);;
    subs := List(classes,Representative);;
    ranks := List(subs,s->Length(MinimalGeneratingSet(s)));;
    rank := Maximum(ranks);;
    tops := Filtered([1..Length(subs)],j->ranks[j]=rank);;
    abelian := Number(tops,j->IsAbelian(subs[j]));;
    normalphi := Number(tops,j->IsNormal(g,FrattiniSubgroup(subs[j])));;
    if abelian=0 and normalphi=0 then
      unresolved := unresolved+1;
      Print("UNRESOLVED_1645 ",n," ",id," rank ",rank,"\n");
    fi;
    if not first then PrintTo(output,","); fi;
    first := false;
    PrintTo(output,"{\"order\":",n,",\"id\":",id,
      ",\"subgroup_classes\":",Length(subs),
      ",\"subgroups\":",Sum(classes,Size),
      ",\"rank\":",rank,",\"rank_frequencies\":",Collected(ranks),
      ",\"top_rank_classes\":",Length(tops),
      ",\"abelian_witness_classes\":",abelian,
      ",\"normal_frattini_witness_classes\":",normalphi,"}");
    total := total+1;
    if total mod 25 = 0 then Print("PROGRESS_1645_EXTENSION ",n," ",id," completed ",total," unresolved ",unresolved,"\n"); fi;
  od;
  Print("PROGRESS_1645 order ",n," completed ",total," unresolved ",unresolved,"\n");
od;
PrintTo(output,"],\"groups\":",total,",\"unresolved\":",unresolved,"}\n");;
CloseStream(output);;
Print("PASS_1645_EXTENSION\n");;
end;;
Run1645();;
QUIT;
