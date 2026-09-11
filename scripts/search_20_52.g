# Complete odd-order SmallGrp screen for m<=64 using |G|<=27m.
RunSearch:=function()
local n,j,g,k,count,nonab,hit,seen,m,ng;
count:=0; nonab:=0; seen:=[];
Print("START GAP=",GAPInfo.Version," max_order=1727 max_target_m=64\n");
for n in [3,5..1727] do
    if not SmallGroupsAvailable(n) then Error("missing order ",n); fi;
    ng:=NumberSmallGroups(n);
    for j in [1..ng] do
        g:=SmallGroup(n,j);
        if Size(g)<>n then Error("order mismatch"); fi;
        k:=NrConjugacyClasses(g);
        count:=count+1;
        if not IsAbelian(g) then
            nonab:=nonab+1;
            if 27*k>11*n or (n-k) mod 16<>0 then
                Error("odd group bound or Burnside divisibility failed");
            fi;
            m:=(n-k)/16;
            AddSet(seen,m);
        elif k<>n then Error("abelian control failed");
        fi;
        Print("GROUP order=",n," id=",j," classes=",k," diff=",n-k,"\n");
    od;
od;
Print("MISSING ",Difference([1..64],seen),"\n");
Print("DONE groups=",count," nonabelian=",nonab," distinct_m=",Length(seen),"\n");
end;
RunSearch();
QUIT;
