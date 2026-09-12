SetAssertionLevel(1);
Main2021:=function()
local n,i,G,ab,ns,k,q,cs,as,pair,rows,tested,eligible,both,total,iso,idsC,idsA,out;
out:=OutputTextFile("results/20.21-kernels.grows",false);
SetPrintFormattingStatus(out,false);
total:=0;
for n in [12,24,48,96,192,384] do
  tested:=0;eligible:=0;both:=0;
  for i in [1..NumberSmallGroups(n)] do
    G:=SmallGroup(n,i);tested:=tested+1;
    ab:=AbelianInvariants(G);
    if Lcm(ab) mod 12<>0 then continue;fi;
    eligible:=eligible+1;
    ns:=Filtered(NormalSubgroups(G),k->Index(G,k)=12);
    cs:=[];as:=[];
    for k in ns do
      q:=G/k;
      if IsCyclic(q) then Add(cs,k);
      elif IdGroup(q)=IdGroup(AlternatingGroup(4)) then Add(as,k);fi;
    od;
    if IsEmpty(cs) or IsEmpty(as) then continue;fi;
    both:=both+1;idsC:=List(cs,IdGroup);idsA:=List(as,IdGroup);
    AppendTo(out,[n,i,idsC,idsA],"\n");
    for pair in Cartesian([1..Length(cs)],[1..Length(as)]) do
      if idsC[pair[1]]=idsA[pair[2]] then
        iso:=IsomorphismGroups(cs[pair[1]],as[pair[2]]);
        Assert(0,iso<>fail);
        Print("CANDIDATE_2021 ",[n,i,pair],"\n");
      fi;
    od;
  od;
  total:=total+tested;
  Print("ORDER_2021 ",n," tested=",tested," eligible=",eligible," both=",both,"\n");
od;
CloseStream(out);
Print("PASS_2021_SEARCH tested=",total,"\n");
end;
Main2021();
QUIT;
