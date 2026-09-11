LoadPackage("smallgrp");;
SizeScreen([1000000,1000000]);;
(function()
  local n,total;
  total:=0;
  for n in [2..511] do
    Print("CATALOGUE order=",n," groups=",NumberSmallGroups(n),"\n");
    total:=total+NumberSmallGroups(n);
  od;
  Print("CATALOGUE_DONE orders=510 groups=",total,"\n");
end)();
QUIT;
