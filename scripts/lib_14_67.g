# Exact reduction: H nilpotent and normalized by C implies H <= Fitting(HC).
K67Overgroups := function(G,C)
  local result;
  if G=C then return [G]; fi;
  result:=IntermediateSubgroups(G,C).subgroups;
  if not ForAll(result,K->K<>C and K<>G and IsSubgroup(K,C)) then
    Error("Unexpected intermediate-subgroup convention");
  fi;
  return Concatenation([C],result,[G]);
end;

K67AtElement := function(G,a,C)
  local overgroups,K,F,failures,nontrivial;
  overgroups:=K67Overgroups(G,C);
  failures:=[]; nontrivial:=0;
  for K in overgroups do
    F:=FittingSubgroup(K);
    if Size(F)>1 then nontrivial:=nontrivial+1; fi;
    if not ForAll(GeneratorsOfGroup(F),h->Comm(a,h)=One(G)) then
      Add(failures,rec(overgroup:=K,witness:=F));
    fi;
  od;
  return rec(overgroups:=Length(overgroups),nontrivial:=nontrivial,
             failures:=failures,passes:=IsEmpty(failures));
end;
