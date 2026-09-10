# Configure START_ORDER and END_ORDER before Read, or use defaults 2..255.
LoadPackage("smallgrp");;
Read("scripts/lib_21_26.g");;
if not IsBound(START_ORDER) then START_ORDER:=2; fi;
if not IsBound(END_ORDER) then END_ORDER:=255; fi;
if not IsBound(MIN_PRIMES) then MIN_PRIMES:=2; fi;

(function()
local order,index,count,G,r,checked,bound,allchoices,hits,primepower,theory;
checked:=0; bound:=0; allchoices:=0; hits:=0; primepower:=0; theory:=0;
for order in [START_ORDER..END_ORDER] do
  if Length(Set(FactorsInt(order)))<=1 then
    primepower:=primepower+1; continue;
  fi;
  if Length(Set(FactorsInt(order)))<MIN_PRIMES then
    theory:=theory+1; continue;
  fi;
  count:=NumberSmallGroups(order);
  Print("ORDER_START ",order," groups=",count," runtime_ms=",Runtime(),"\n");
  for index in [1..count] do
    G:=SmallGroup(order,index);
    r:=KourovkaCheck21_26(G);
    checked:=checked+1;
    if r.method="union_bound" then bound:=bound+1; else
      allchoices:=allchoices+1;
      Print("ALL_CHOICES order=",order," index=",index," result=",r,"\n");
    fi;
    if not r.holds then
      hits:=hits+1;
      Print("HIT order=",order," index=",index," result=",r,"\n");
    fi;
    if checked mod 100=0 then
      Print("PROGRESS checked=",checked," union_bound=",bound," all_choices=",allchoices,
            " hits=",hits," runtime_ms=",Runtime(),"\n");
    fi;
  od;
od;
Print("DONE orders=",[START_ORDER,END_ORDER]," checked=",checked," union_bound=",bound,
      " all_choices=",allchoices," prime_power_orders_trivial=",primepower," hits=",hits,
      " min_primes=",MIN_PRIMES," other_orders_excluded=",theory," runtime_ms=",Runtime(),"\n");
end)();
QUIT;
