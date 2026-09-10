# Exact extension of Cameron's published range (through order 63).
LoadPackage("smallgrp");;
Read("scripts/lib_19_20.g");;
if not IsBound(START_ORDER) then START_ORDER:=2; fi;
if not IsBound(END_ORDER) then END_ORDER:=255; fi;
(function()
local n,i,G,c,checked,abelian,hits,reverse,minimum,minimumId;
checked:=0; abelian:=0; hits:=0; reverse:=0; minimum:=infinity; minimumId:=fail;
Print("PARAMETERS start=",START_ORDER," end=",END_ORDER,"\n");
for n in [START_ORDER..END_ORDER] do
  Print("ORDER_START order=",n," groups=",NumberSmallGroups(n),"\n");
  for i in [1..NumberSmallGroups(n)] do
    G:=SmallGroup(n,i);
    c:=Kourovka19Counts(G);
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
      " reversed=",reverse," closest=",minimumId," min_ratio=",minimum,
      " runtime_ms=",Runtime(),"\n");
end)();
QUIT;
