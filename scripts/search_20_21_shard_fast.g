SetAssertionLevel(1);
SearchShard2021:=function()
local n,i,G,ab,ns,k,q,cs,as,pair,tested,eligible,both,iso,idsC,idsA,out,hits,last;
n:=SearchOrder2021;
Assert(0,SearchIndex2021>=0 and SearchIndex2021<SearchShards2021);
out:=OutputTextFile(SearchRows2021,false);
SetPrintFormattingStatus(out,false);
tested:=0;eligible:=0;both:=0;hits:=0;
last:=NumberSmallGroups(n)-((NumberSmallGroups(n)-SearchIndex2021-1) mod SearchShards2021);
for i in [SearchIndex2021+1,SearchIndex2021+1+SearchShards2021..last] do
  G:=SmallGroup(n,i);tested:=tested+1;
  if tested mod 10000=0 then
    Print("PROGRESS_2021_SHARD ",[n,SearchIndex2021,tested,i,eligible,both,hits],"\n");
  fi;
  ab:=AbelianInvariants(G);
  if Lcm(ab) mod 12<>0 then continue;fi;
  eligible:=eligible+1;
  # Every quotient of a nilpotent group is nilpotent; A4 is not.
  if IsNilpotentGroup(G) then continue;fi;
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
      Assert(0,iso<>fail);hits:=hits+1;
      Print("CANDIDATE_2021_SHARD ",[n,i,pair],"\n");
    fi;
  od;
od;
CloseStream(out);
Print("PASS_2021_SHARD ",[n,SearchIndex2021,SearchShards2021,tested,eligible,both,hits],"\n");
end;
SearchShard2021();
QUIT;
