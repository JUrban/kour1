for n in [16,27,32,64] do
 for id in [1..NumberSmallGroups(n)] do
  g:=SmallGroup(n,id);;
  if not IsAbelian(g) and (n=27 or NilpotencyClassOfGroup(g)>2) then
   Print("CASE_647 ",n," ",id," ",NilpotencyClassOfGroup(g)," ",Exponent(g)," ",StructureDescription(g),"\n");
  fi;
 od;
od;
Print("PASS_647_CATALOG\n");
QUIT_GAP(0);
