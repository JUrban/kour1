SetAssertionLevel(1);
ControlInterval2021:=function()
local i,G,flags,expected;
Assert(0,NumberSmallGroups(1536)=408641062);
for i in [1,10494213,10494214,408526597,408526598,408544625,408544626,408641062] do
  G:=SmallGroup(1536,i);
  flags:=[IsNormal(G,SylowSubgroup(G,2)),IsNormal(G,SylowSubgroup(G,3))];
  if i<=10494213 then expected:=[true,true];
  elif i<=408526597 then expected:=[false,true];
  elif i<=408544625 then expected:=[true,false];
  else expected:=[false,false];fi;
  Assert(0,flags=expected);
  Print("BOUNDARY_2021 ",[1536,i,flags],"\n");
od;
Print("PASS_2021_INTERVAL_BOUNDARIES 8\n");
end;
ControlInterval2021();QUIT;
