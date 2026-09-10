# Exact extension of Cameron's published range (through order 63).
LoadPackage("smallgrp");;
Read("scripts/lib_19_20.g");;
if not IsBound(START_ORDER) then START_ORDER:=2; fi;
if not IsBound(END_ORDER) then END_ORDER:=255; fi;
if not IsBound(START_ID) then START_ID:=1; fi;
if not IsBound(END_ID) then END_ID:=infinity; fi;
if not IsBound(SKIP_ABELIAN) then SKIP_ABELIAN:=false; fi;
if not IsBound(LOG_ALL) then LOG_ALL:=false; fi;
SizeScreen([1000000,1000000]);;
(function()
local n,i,G,c,checked,abelian,skipped,hits,reverse,minimum,minimumId;
checked:=0; abelian:=0; skipped:=0; hits:=0; reverse:=0; minimum:=infinity; minimumId:=fail;
Print("PARAMETERS start=",START_ORDER," end=",END_ORDER," start_id=",START_ID,
      " end_id=",END_ID," skip_abelian=",SKIP_ABELIAN," log_all=",LOG_ALL,"\n");
for n in [START_ORDER..END_ORDER] do
  Print("ORDER_START order=",n," groups=",NumberSmallGroups(n),"\n");
  for i in [START_ID..Minimum(END_ID,NumberSmallGroups(n))] do
    G:=SmallGroup(n,i);
    if SKIP_ABELIAN and IsAbelian(G) then
      skipped:=skipped+1;
      Print("ABELIAN_SKIPPED id=",[n,i]," reason=known_equality\n");
      continue;
    fi;
    c:=Kourovka19Counts(G);
    if LOG_ALL then
      Print("COUNTS id=",[n,i]," end=",c.ends," piso=",c.partials,"\n");
    fi;
    checked:=checked+1;
    if IsAbelian(G) then
      abelian:=abelian+1;
      if c.ends<>c.partials then Error("Abelian control failed",n,i,c); fi;
    else
      if c.ends=c.partials then
        hits:=hits+1;
        Print("HIT_19_20 id=",[n,i]," count=",c.ends,"\n");
      fi;
      if c.ends>c.partials then
        reverse:=reverse+1;
        Print("STRONG_INEQUALITY_COUNTEREXAMPLE id=",[n,i]," end=",c.ends,
              " piso=",c.partials,"\n");
      fi;
      if c.partials/c.ends<minimum then
        minimum:=c.partials/c.ends; minimumId:=[n,i];
        Print("CLOSEST id=",[n,i]," end=",c.ends," piso=",c.partials,
              " ratio=",minimum,"\n");
      fi;
    fi;
    if checked mod 100=0 then
      Print("PROGRESS checked=",checked," hits=",hits," reversed=",reverse,
            " runtime_ms=",Runtime(),"\n");
    fi;
  od;
od;
Print("DONE checked=",checked," abelian=",abelian," hits=",hits,
      " reversed=",reverse," skipped_abelian=",skipped," closest=",minimumId," min_ratio=",minimum,
      " runtime_ms=",Runtime(),"\n");
end)();
QUIT;
