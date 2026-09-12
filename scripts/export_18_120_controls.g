LoadPackage("smallgrp");;
Export18120 := function()
local cases,out,first,c,g,els,tab;
cases := [[128,134],[128,995],[729,99],[729,100]];
out := OutputTextFile("results/18.120-control-inputs.json",false);SetPrintFormattingStatus(out,false);
PrintTo(out,"[");first:=true;
for c in cases do
 g:=SmallGroup(c[1],c[2]);els:=Elements(g);tab:=List(els,x->List(els,y->Position(els,x*y)-1));
 if not first then PrintTo(out,",");fi;first:=false;
 PrintTo(out,"{\"order\":",c[1],",\"id\":",c[2],",\"identity\":",Position(els,One(g))-1,",\"table\":",tab,"}");
od;
PrintTo(out,"]\n");CloseStream(out);Print("PASS_18120_EXPORT\n");
end;;
Export18120();;QUIT;
