# Complete IRREDSOL coverage in the requested dimensions over F5.
# This library covers soluble linear groups only.
LoadPackage("irredsol");;
if not IsBound(SEARCH_DIMENSIONS) then SEARCH_DIMENSIONS:=[1..6]; fi;
Run18114:=function(dims)
local n,d,k,ids,g,sz,cyclic,affine,classes,total,eligible,hits,equalities,
      ndtotal,ndeligible,ndhits,ndeq,started,identifier;
total:=0;eligible:=0;hits:=0;equalities:=0;
for n in dims do
    ndtotal:=0;ndeligible:=0;ndhits:=0;ndeq:=0;
    Print("BEGIN dimension=",n," field=5\n");
    if not IsAvailableIrreducibleSolubleGroupData(n,5) then
        Error("missing IRREDSOL dimension ",n);
    fi;
    for d in DivisorsInt(n) do
        ids:=IndicesIrreducibleSolubleMatrixGroups(n,5,d);
        for k in ids do
            g:=IrreducibleSolubleMatrixGroup(n,5,d,k);
            sz:=Size(g);ndtotal:=ndtotal+1;
            if sz mod 5=0 then continue; fi;
            ndeligible:=ndeligible+1;started:=Runtime();
            cyclic:=IsCyclic(g);
            if cyclic then
                # An irreducible cyclic group is fixed-point-free off zero.
                if (5^n-1) mod sz<>0 then Error("cyclic order"); fi;
                classes:=sz+(5^n-1)/sz;
            else
                affine:=PrimitivePcGroupIrreducibleMatrixGroup(g);
                if Size(affine)<>5^n*sz then Error("wrong affine order"); fi;
                classes:=NrConjugacyClasses(affine);
            fi;
            Print("GROUP n=",n," d=",d," k=",k," order=",sz,
                " cyclic=",cyclic," affine_classes=",classes,
                " ms=",Runtime()-started,"\n");
            if classes>5^n then Error("violated kGV bound"); fi;
            if classes=5^n then
                ndeq:=ndeq+1;
                if not cyclic then
                    ndhits:=ndhits+1;
                    Print("HIT n=",n," d=",d," k=",k,"\n");
                fi;
            fi;
        od;
    od;
    Print("DONE_DIM n=",n," total=",ndtotal," eligible=",ndeligible,
        " equalities=",ndeq," hits=",ndhits,"\n");
    total:=total+ndtotal;eligible:=eligible+ndeligible;
    hits:=hits+ndhits;equalities:=equalities+ndeq;
od;
Print("DONE total=",total," eligible=",eligible," equalities=",equalities,
    " noncyclic_hits=",hits,"\n");
end;
Run18114(SEARCH_DIMENSIONS);
QUIT;
