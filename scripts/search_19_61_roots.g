SetAssertionLevel(1);
Assert(0,Size(Group(Concatenation(RootPerms1961)))=ExpectedOrder1961);
Print("PASS_1961_AMBIENT ",RingLabel1961," order=",ExpectedOrder1961,"\n");
Search1961:=function()
local nopts,m,contains,idx,row,gens,r,t,H,closure,params,p,edge,bad,expanded,hits,out,counts;
nopts:=Length(Subsets1961);m:=Length(RootPerms1961[1]);
contains:=List(Subsets1961,s->List([1..2^m-1],mask->
  IsSubset(s,Filtered([0..m-1],v->QuoInt(mask,2^v) mod 2=1))));
out:=OutputTextFile(Concatenation("results/19.61-",RingLabel1961,"-changes.grows"),false);
SetPrintFormattingStatus(out,false);
expanded:=0;hits:=0;counts:=[];
for idx in [1..Length(Carpets1961)] do
  row:=Carpets1961[idx];
  Assert(0,ForAll(Implications1961,e->contains[row[e[3]]][e[4][row[e[1]]][row[e[2]]]]));
  gens:=[];
  for r in [1..Length(RootPerms1961)] do
    for t in Subsets1961[row[r]] do
      if t<>0 then Add(gens,RootPerms1961[r][t+1]);fi;
    od;
  od;
  if IsEmpty(gens) then gens:=[()];fi;
  H:=Group(gens);closure:=[];
  for r in [1..Length(RootPerms1961)] do
    params:=Filtered([0..m-1],t->RootPerms1961[r][t+1] in H);
    p:=Position(Subsets1961,params);Assert(0,p<>fail);
    Assert(0,IsSubset(params,Subsets1961[row[r]]));Add(closure,p);
  od;
  bad:=Filtered([1..Length(Implications1961)],function(j)
    local e;e:=Implications1961[j];
    return not contains[closure[e[3]]][e[4][closure[e[1]]][closure[e[2]]]];
  end);
  if closure<>row then
    expanded:=expanded+1;AppendTo(out,[idx,row,closure,Size(H),bad],"\n");
  fi;
  if not IsEmpty(bad) then
    hits:=hits+1;Print("CANDIDATE_1961 ",RingLabel1961," ",[idx,row,closure,Size(H),bad],"\n");
  fi;
  if idx mod 1000=0 then Print("PROGRESS_1961 ",RingLabel1961," ",[idx,expanded,hits],"\n");fi;
od;
CloseStream(out);
Print("PASS_1961_SEARCH ",RingLabel1961," ",[Length(Carpets1961),expanded,hits],"\n");
end;
Search1961();
QUIT;
