# Independent literal subgroup/element tests, including ineligible negative controls.
LoadPackage("smallgrp");;
Read("scripts/lib_14_67.g");;
SizeScreen([1000000,1000000]);;
(function()
  local groups,n,i,G,els,subgroups,nilpotent,classes,a,C,ce,r,direct,H,
        groupsDone,elementCases,subgroupCases,positive,negative,candidates,
        maximum,allSizes,classIndex,eligible,gen;
  groups:=[];
  for n in [2..32] do
    for i in [1..NumberSmallGroups(n)] do
      Add(groups,SmallGroup(n,i));
    od;
  od;
  Append(groups,[SymmetricGroup(4),AlternatingGroup(5),SymmetricGroup(5),SL(2,3)]);
  groupsDone:=0; elementCases:=0; subgroupCases:=0; positive:=0; negative:=0;
  candidates:=0;
  for G in groups do
    els:=Elements(G);
    subgroups:=Concatenation(List(ConjugacyClassesSubgroups(G),AsList));
    if Length(Set(subgroups))<>Length(subgroups) then Error("Duplicate subgroups"); fi;
    nilpotent:=Filtered(subgroups,H->Size(Last(LowerCentralSeriesOfGroup(H)))=1);
    allSizes:=List(Filtered(els,x->x<>One(G)),
                   x->Number(els,y->Comm(x,y)=One(G)));
    maximum:=Maximum(allSizes);
    classes:=ConjugacyClasses(G); classIndex:=0;
    for gen in classes do
      classIndex:=classIndex+1; a:=Representative(gen);
      if a=One(G) then continue; fi;
      ce:=Filtered(els,c->Comm(a,c)=One(G));
      C:=Subgroup(G,ce);
      if Size(C)<>Length(ce) or Size(C)*Size(gen)<>Size(G) then
        Error("Direct centralizer mismatch");
      fi;
      eligible:=Length(ce)=maximum;
      r:=K67AtElement(G,a,C);
      direct:=true;
      for H in nilpotent do
        subgroupCases:=subgroupCases+1;
        if ForAll(ce,c->ForAll(Elements(H),h->h^c in H)) and
           ForAny(Elements(H),h->Comm(a,h)<>One(G)) then
          direct:=false;
        fi;
      od;
      if direct<>r.passes then Error("Literal predicate disagrees with reduction"); fi;
      if eligible and not direct then candidates:=candidates+1; fi;
      if direct then positive:=positive+1; else negative:=negative+1; fi;
      elementCases:=elementCases+1;
    od;
    groupsDone:=groupsDone+1;
    Print("CONTROL group_number=",groupsDone," order=",Size(G),
          " subgroups=",Length(subgroups)," nilpotent=",Length(nilpotent),"\n");
  od;
  if positive=0 or negative=0 then Error("Missing positive or negative controls"); fi;
  Print("PASS groups=",groupsDone," element_classes=",elementCases,
        " literal_subgroup_cases=",subgroupCases," positive=",positive,
        " negative=",negative," eligible_failures=",candidates,
        " runtime_ms=",Runtime(),"\n");
end)();
QUIT;
