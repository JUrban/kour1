# Independent proof checker: integer presentations localized at small primes.
# Read this file, then the generated certificate. All nodes are checked in order.
SetAssertionLevel(2);
ProofRows := [];; ProofN := 0;; ProofPrimes := [];;
ProofEdges := 0;; ProofLeaves := 0;; ProofRelations := 0;;
ProofStarted := Runtime();;

StripSmall := function(x)
    local p;
    x := AbsInt(x);
    if x=0 then return 0; fi;
    for p in ProofPrimes do
        while x mod p=0 do x:=x/p; od;
    od;
    return x;
end;

StartProof := function(n,bound)
    Assert(0,ProofN=0 and n>=2 and bound=n+1);
    ProofN:=n;
    ProofPrimes:=Filtered([2..bound],IsPrimeInt);
    Print("START n=",n," prime_bound=",bound,"\n");
end;

PresentationRows := function(state)
    local rows,offset,part,m,ws,b,j,w,row;
    rows:=[]; offset:=0;
    for part in state do
        m:=part[1]; ws:=part[2]; b:=offset+1;
        Assert(0,IsInt(m) and m>=0 and Length(ws)>0);
        if m>0 then Assert(0,StripSmall(m)=m); fi;
        Assert(0,(m=1 and ForAll(ws,w->w=0)) or (m<>1 and ws[1]=1));
        if m>0 then
            row:=List([1..ProofN],i->0); row[b]:=m; Add(rows,row);
        fi;
        for j in [2..Length(ws)] do
            w:=ws[j];
            Assert(0,IsRat(w) and StripSmall(DenominatorRat(w))=1);
            row:=List([1..ProofN],i->0);
            row[offset+j]:=DenominatorRat(w); row[b]:=-NumeratorRat(w);
            Add(rows,row);
        od;
        offset:=offset+Length(ws);
    od;
    Assert(0,offset=ProofN);
    return rows;
end;

MembershipData := function(rows)
    local sf,j;
    if Length(rows)=0 then return fail; fi;
    sf:=SmithNormalFormIntegerMatTransforms(rows);
    Assert(0,sf.rowtrans*rows*sf.coltrans=sf.normal);
    Assert(0,AbsInt(DeterminantMat(sf.rowtrans))=1);
    Assert(0,AbsInt(DeterminantMat(sf.coltrans))=1);
    Assert(0,ForAll([1..Length(sf.normal)],i->ForAll([1..ProofN],j->i=j or sf.normal[i][j]=0)));
    sf.divisors:=List([1..sf.rank],j->StripSmall(sf.normal[j][j]));
    Assert(0,ForAll(sf.divisors,d->d>0));
    return sf;
end;

MemberLocalized := function(sf,v)
    local w,j;
    if sf=fail then return ForAll(v,x->x=0); fi;
    w:=v*sf.coltrans;
    for j in [1..ProofN] do
        if j<=sf.rank then
            if w[j] mod sf.divisors[j]<>0 then return false; fi;
        elif w[j]<>0 then return false;
        fi;
    od;
    return true;
end;

CheckNode := function(identifier,state,perm,children)
    local rows,sf,i,j,v,found,k,child,labels,source,row,mapped,a;
    Assert(0,identifier=Length(ProofRows)+1 and ProofN>0);
    rows:=PresentationRows(state);
    if Length(perm)=0 then
        Assert(0,Length(children)=0);
        sf:=MembershipData(rows); found:=false;
        for i in [1..ProofN-1] do
            for j in [i+1..ProofN] do
                v:=List([1..ProofN],x->0); v[i]:=1; v[j]:=-1;
                if MemberLocalized(sf,v) then found:=true; fi;
            od;
        od;
        Assert(0,found);
        ProofLeaves:=ProofLeaves+1;
    else
        Assert(0,Set(perm)=[1..ProofN] and Length(perm)=ProofN);
        Assert(0,Length(children)=Binomial(ProofN,2)); k:=0;
        for i in [1..ProofN-1] do
            for j in [i+1..ProofN] do
                k:=k+1; child:=children[k][1]; labels:=children[k][2];
                Assert(0,child>=1 and child<identifier);
                Assert(0,Length(labels)=ProofN and Set(labels)=[1..ProofN]);
                v:=List([1..ProofN],x->0); v[i]:=perm[i]; v[j]:=-perm[j];
                source:=Concatenation(rows,[v]); sf:=MembershipData(source);
                for row in ProofRows[child] do
                    mapped:=List([1..ProofN],x->0);
                    for a in [1..ProofN] do mapped[labels[a]]:=row[a]; od;
                    Assert(0,MemberLocalized(sf,mapped));
                    ProofRelations:=ProofRelations+1;
                od;
                ProofEdges:=ProofEdges+1;
            od;
        od;
    fi;
    Add(ProofRows,rows);
    if identifier mod 10000=0 then
        Print("CHECK nodes=",identifier," edges=",ProofEdges," cpu_ms=",Runtime()-ProofStarted,"\n");
    fi;
end;

FinishProof := function(root)
    Assert(0,root=Length(ProofRows) and Length(ProofRows[root])=0);
    Print("PASS n=",ProofN," nodes=",root," leaves=",ProofLeaves," edges=",ProofEdges,
          " relation_implications=",ProofRelations," cpu_ms=",Runtime()-ProofStarted,"\n");
end;
