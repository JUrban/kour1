# Actual witnesses, with bounded randomized search and exact verification.
# Random search is used only to discover finite witnesses, never for proof.
Verify1032 := function()
    local n,q,part,g,G,base,rs,a,b,target,tries,checks,attempts,out,
          MakePerm,Type,p,supp,nt,d,h,k,genus,r,s,R,S,x,y,odd,params,
          proofChecks,transpositions;
    MakePerm:=function(parts)
        local imgs,cursor,len,j;
        imgs:=[1..Sum(parts)]; cursor:=1;
        for len in parts do
            for j in [0..len-1] do imgs[cursor+j]:=cursor+((j+1) mod len); od;
            cursor:=cursor+len;
        od;
        return PermList(imgs);
    end;
    Type:=function(z,degree)
        return Reversed(SortedList(CycleLengths(z,[1..degree])));
    end;
    checks:=0; attempts:=0; proofChecks:=0; transpositions:=0;
    out:="results/10.32-witnesses.json"; PrintTo(out,"[\n");
    rs:=RandomSource(IsMersenneTwister,1032);
    for n in [10..25] do
        params:=Filtered([5..QuoInt(n,2)],
                         q->IsPrimeInt(q) and 8*q>3*n+8);
        if Length(params)>0 then
            G:=SymmetricGroup(n);
            for q in params do
                base:=MakePerm(Concatenation([q,q],List([1..n-2*q],i->1)));
                for part in Partitions(n) do
                    g:=MakePerm(part); odd:=SignPerm(g)=-1;
                    if odd then
                        supp:=NrMovedPoints(g);
                        nt:=Length(Filtered(part,p->p>1));
                        if supp-nt=1 then
                            transpositions:=transpositions+1;
                        else
                            d:=Maximum(supp,2*q); h:=nt+d-supp; k:=d-2*q+2;
                            genus:=(2*q-h-k+1)/2;
                            if not IsInt(genus) or genus<1 or d<2*q then
                                Error("positive-genus hypothesis failed");
                            fi;
                            proofChecks:=proofChecks+1;
                        fi;
                        target:=Concatenation([2*q],List([1..n-2*q],i->1));
                    else
                        target:=Concatenation([q,q],List([1..n-2*q],i->1));
                    fi;
                    tries:=0;
                    repeat
                        b:=base^Random(rs,G); a:=g/b; tries:=tries+1;
                    until Type(a,n)=target or tries=200000;
                    if Type(a,n)<>target or a*b<>g or Type(b,n)<>Type(base,n) then
                        Error("bounded witness discovery failed");
                    fi;
                    # Both exponent signs and both positions of the odd exponent.
                    for r in [2*q+1,-2*q-1] do for s in [2*q+2,-2*q-2] do
                        R:=InverseMod(r,Order(a)); S:=InverseMod(s,Order(b));
                        x:=a^R; y:=b^S;
                        if x^r*y^s<>g then Error("root identity failed"); fi;
                        if y^s*(y^-s*x*y^s)^r<>g then
                            Error("exponent-order interchange failed");
                        fi;
                    od; od;
                    if checks>0 then AppendTo(out,",\n"); fi;
                    AppendTo(out,String([n,q,part,ListPerm(a,n),ListPerm(b,n)]));
                    checks:=checks+1; attempts:=attempts+tries;
                od;
                Print("n=",n," q=",q," cumulative_witnesses=",checks,
                      " discovery_attempts=",attempts,"\n");
            od;
        fi;
    od;
    AppendTo(out,"\n]\n");
    Print("witnesses=",checks," positive_genus_checks=",proofChecks,
          " transpositions=",transpositions," root_identities=",8*checks,"\n");
    Print("PASS_1032_WITNESSES\n");
end;
Verify1032();
QUIT;
