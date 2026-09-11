LoadPackage("smallgrp");;
Read("scripts/lib_14_67.g");;
SizeScreen([1000000,1000000]);;
if not IsBound(K67_START) then K67_START:=2; fi;
if not IsBound(K67_END) then K67_END:=511; fi;
(function()
  local n,i,G,classes,minimum,j,a,C,r,enumerated,central,eligible,
        overgroups,hits,total,primepower,checked,ng,gs,ge,go;
  enumerated:=0; central:=0; eligible:=0; overgroups:=0;
  hits:=0; total:=0; primepower:=0; checked:=0;
  Print("PARAMETERS start=",K67_START," end=",K67_END,
        " gap=",GAPInfo.Version,"\n");
  for n in [K67_START..K67_END] do
    ng:=NumberSmallGroups(n); total:=total+ng;
    Print("ORDER_START order=",n," groups=",ng,"\n");
    if Length(PrimeDivisors(n))=1 then
      primepower:=primepower+ng;
      Print("PRIME_POWER_SKIPPED order=",n," groups=",ng,
            " reason=nontrivial_centre\n");
      continue;
    fi;
    gs:=0; ge:=0; go:=0;
    for i in [1..ng] do
      G:=SmallGroup(n,i); enumerated:=enumerated+1;
      if Size(Centre(G))>1 then
        central:=central+1; gs:=gs+1;
        Print("CENTRE_SKIPPED id=",[n,i],"\n");
        continue;
      fi;
      checked:=checked+1;
      classes:=ConjugacyClasses(G);
      minimum:=Minimum(List(Filtered(classes,c->Representative(c)<>One(G)),Size));
      ge:=0; go:=0;
      for j in [1..Length(classes)] do
        a:=Representative(classes[j]);
        if a=One(G) or Size(classes[j])<>minimum then continue; fi;
        C:=Centralizer(G,a);
        if Size(C)*minimum<>n then Error("Class-centralizer mismatch"); fi;
        r:=K67AtElement(G,a,C);
        eligible:=eligible+1; ge:=ge+1;
        overgroups:=overgroups+r.overgroups; go:=go+r.overgroups;
        if not r.passes then
          hits:=hits+Length(r.failures);
          Print("HIT_14_67 id=",[n,i]," class_index=",j," a=",a,
                " centralizer_order=",Size(C)," failures=",r.failures,"\n");
        fi;
      od;
      Print("CHECKED id=",[n,i]," minimum_class=",minimum,
            " eligible_classes=",ge," overgroups=",go,"\n");
    od;
    Print("ORDER_DONE order=",n," enumerated=",ng," centre_skipped=",gs,
          " runtime_ms=",Runtime(),"\n");
  od;
  Print("DONE catalogue=",total," prime_power_skipped=",primepower,
        " enumerated=",enumerated," centre_skipped=",central,
        " checked=",checked," eligible_classes=",eligible,
        " overgroups=",overgroups," hits=",hits," runtime_ms=",Runtime(),"\n");
end)();
QUIT;
