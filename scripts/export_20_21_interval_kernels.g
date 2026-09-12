SetAssertionLevel(1);
ExportKernels2021:=function()
local out,id,G,ns,k,q,kind,elts,tab,count,done;
out:=OutputTextFile(ExportRows2021,false);
SetPrintFormattingStatus(out,false);count:=0;done:=0;
for id in Targets2021 do
  G:=SmallGroup(id);ns:=Filtered(NormalSubgroups(G),k->Index(G,k)=12);
  for k in ns do
    q:=G/k;kind:=fail;
    if IsCyclic(q) then kind:=0;elif IdGroup(q)=[12,3] then kind:=1;fi;
    if kind=fail then continue;fi;
    elts:=Elements(k);Assert(0,IsSSortedList(elts) and elts[1]=One(k));
    tab:=List(elts,a->List(elts,b->PositionSorted(elts,a*b)-1));
    AppendTo(out,[id,kind,IdGroup(k),tab],"\n");count:=count+1;
  od;
  done:=done+1;
  if done mod 100=0 then Print("PROGRESS_2021_KERNEL_EXPORT ",[done,count],"\n");fi;
od;
CloseStream(out);Print("PASS_2021_KERNEL_EXPORT ",[done,count],"\n");
end;
ExportKernels2021();
QUIT;
