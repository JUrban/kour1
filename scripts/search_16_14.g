# Exhaustive SmallGroups search for the exact printed hypothesis of 16.14.
LoadPackage("smallgrp");;
SizeScreen([1000000,1000000]);;
if not IsBound(SEARCH_ORDERS) then SEARCH_ORDERS := [2,4,8,16,32,64,128,256]; fi;
(function()
local n,i,g,z,d,zrank,witness,checked,rankExcluded,involutionExcluded,hits,
      byRank,byInvolution,orderHits,start,pc;
checked:=0; rankExcluded:=0; involutionExcluded:=0; hits:=0; start:=Runtime();
Print("PARAMETERS orders=",SEARCH_ORDERS," GAP=",GAPInfo.Version,"\n");
for n in SEARCH_ORDERS do
  if n <> 2^LogInt(n,2) then Error("order is not a power of two"); fi;
  byRank:=0; byInvolution:=0; orderHits:=0;
  Print("ORDER_START order=",n," groups=",NumberSmallGroups(n),"\n");
  for i in [1..NumberSmallGroups(n)] do
    g:=SmallGroup(n,i); z:=Centre(g);
    d:=LogInt(Index(g,FrattiniSubgroup(g)),2);
    zrank:=Length(AbelianInvariants(z));
    if d <= 2*zrank then
      byRank:=byRank+1;
    else
      witness:=First(g,x->x^2=One(g) and not x in z);
      if witness=fail then
        orderHits:=orderHits+1;
        Print("HIT_16_14 id=",[n,i]," d=",d," zrank=",zrank,"\n");
      else
        # An explicit noncentral involution certifies failure of the hypothesis.
        if witness=One(g) or witness^2<>One(g) or witness in z then
          Error("invalid exclusion witness");
        fi;
        pc:=Pcgs(g);
        Print("INVOLUTION_EXCLUSION id=",[n,i]," d=",d," zrank=",zrank,
              " witness=",ExponentsOfPcElement(pc,witness),"\n");
        byInvolution:=byInvolution+1;
      fi;
    fi;
    checked:=checked+1;
    if i mod 1000=0 then
      Print("PROGRESS order=",n," id=",i," total=",checked,
            " elapsed_ms=",Runtime()-start,"\n");
    fi;
  od;
  if byRank+byInvolution+orderHits<>NumberSmallGroups(n) then Error("coverage"); fi;
  rankExcluded:=rankExcluded+byRank;
  involutionExcluded:=involutionExcluded+byInvolution;
  hits:=hits+orderHits;
  Print("ORDER_DONE order=",n," rank_excluded=",byRank,
        " involution_excluded=",byInvolution," hits=",orderHits,"\n");
od;
Print("DONE checked=",checked," rank_excluded=",rankExcluded,
      " involution_excluded=",involutionExcluded," hits=",hits,
      " elapsed_ms=",Runtime()-start," PASS\n");
end)();
QUIT;
