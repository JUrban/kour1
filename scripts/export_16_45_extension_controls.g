LoadPackage("smallgrp");;
Export1645 := function()
local cases,out,first,c,g,els,tab;
cases := [[81,14],[125,3],[128,133],[128,990],[128,163],[243,19],[343,3],[625,14]];
out := OutputTextFile("results/16.45-extension-control-inputs.json",false);
SetPrintFormattingStatus(out,false);
PrintTo(out,"["); first := true;
for c in cases do
  g := SmallGroup(c[1],c[2]); els := Elements(g);
  tab := List(els,x->List(els,y->Position(els,x*y)-1));
  if not first then PrintTo(out,","); fi; first := false;
  PrintTo(out,"{\"order\":",c[1],",\"id\":",c[2],",\"identity\":",Position(els,One(g))-1,",\"table\":",tab,"}");
od;
PrintTo(out,"]\n"); CloseStream(out);
PrintTo("results/16.45-extension-catalogue-counts.json",List([81,125,128,243,343,625],n->[n,NumberSmallGroups(n)]),"\n");
Print("PASS_1645_EXTENSION_EXPORT\n");
end;;
Export1645();;
QUIT;
