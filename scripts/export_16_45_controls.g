LoadPackage("smallgrp");;
Export1645 := function()
local cases,out,first,c,g,els,tab;
cases := [[4,1],[8,4],[16,9],[16,12],[16,13],[27,3],[32,8],[32,49],[64,1],[64,34],[64,182],[64,267]];
out := OutputTextFile("results/16.45-control-inputs.json",false);
SetPrintFormattingStatus(out,false);
PrintTo(out,"["); first := true;
for c in cases do
  g := SmallGroup(c[1],c[2]); els := Elements(g);
  tab := List(els,x->List(els,y->Position(els,x*y)-1));
  if not first then PrintTo(out,","); fi; first := false;
  PrintTo(out,"{\"order\":",c[1],",\"id\":",c[2],",\"identity\":",Position(els,One(g))-1,",\"table\":",tab,"}");
od;
PrintTo(out,"]\n"); CloseStream(out);
Print("PASS_1645_EXPORT\n");
end;;
Export1645();;
QUIT;
