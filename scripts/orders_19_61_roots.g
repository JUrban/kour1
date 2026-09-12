SetAssertionLevel(1);
Orders1961:=function()
local out,i,row,gens,r,t,H;
out:=OutputTextFile(Concatenation("results/19.61-",RingLabel1961,"-orders.grows"),false);
SetPrintFormattingStatus(out,false);
for i in [1..Length(Carpets1961)] do
  row:=Carpets1961[i];gens:=[];
  for r in [1..Length(RootPerms1961)] do
    for t in Subsets1961[row[r]] do
      if t<>0 then Add(gens,RootPerms1961[r][t+1]);fi;
    od;
  od;
  if IsEmpty(gens) then gens:=[()];fi;H:=Group(gens);
  AppendTo(out,[i,Size(H)],"\n");
od;
CloseStream(out);Print("PASS_1961_ORDERS ",RingLabel1961," ",Length(Carpets1961),"\n");
end;
Orders1961();QUIT;
