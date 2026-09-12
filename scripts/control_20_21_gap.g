SetAssertionLevel(1);
MainControl2021:=function()
local out,ids,id,G,elts,n,tab,ns,cs,as,k,q,row,count,i;
ids:=Concatenation(List([1..NumberSmallGroups(12)],i->[12,i]),
                   List([1..NumberSmallGroups(24)],i->[24,i]),
                   [[48,31],[96,69],[96,73],[96,74],[96,196]]);
out:=OutputTextFile("results/20.21-tables.grows",false);SetPrintFormattingStatus(out,false);
count:=0;
for id in ids do
 G:=SmallGroup(id);n:=Size(G);elts:=Concatenation([One(G)],Difference(Elements(G),[One(G)]));
 tab:=List(elts,a->List(elts,b->Position(elts,a*b)-1));
 ns:=Filtered(NormalSubgroups(G),k->Index(G,k)=12);cs:=[];as:=[];
 for k in ns do
  q:=G/k;
  if IsCyclic(q) then Add(cs,Set(Elements(k),a->Position(elts,a)-1));
  elif IdGroup(q)=[12,3] then Add(as,Set(Elements(k),a->Position(elts,a)-1));fi;
 od;
 row:=[id,tab,Set(cs),Set(as),Lcm(AbelianInvariants(G)) mod 12=0];
 AppendTo(out,row,"\n");count:=count+1;
od;
CloseStream(out);
Print("PASS_2021_TABLE_EXPORT cases=",count,"\n");
end;
MainControl2021();
QUIT;
