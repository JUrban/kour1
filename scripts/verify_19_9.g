# Independent exact spin-matrix controls for the braid-cover obstruction.
# These finite controls do not prove the infinite tensor-square assertion.
Run199:=function()
local n,p,sgn,m,g,z,i,j,checks,cases,quot,characteristics;
checks:=0;cases:=0;
for n in [4..8] do
    # Generic characteristic-zero Size at n=7 was stopped as expensive.
    # The completed scope is char0 at n<=6, and char3,5 at n<=8.
    if n<=6 then characteristics:=[0,3,5]; else characteristics:=[3,5]; fi;
    for p in characteristics do
        for sgn in [-1,1] do
            m:=BasicSpinRepresentationOfSymmetricGroup(n,p,sgn);
            z:=-One(m[1]);g:=Group(m);
            if Size(g)<>2*Factorial(n) then Error("wrong actual cover order"); fi;
            if Order(z)<>2 or not z in g then Error("central sign absent"); fi;
            for i in [1..n-1] do
                if m[i]*z<>z*m[i] then Error("not central"); fi;
                if (sgn=-1 and m[i]^2<>One(g)) or
                   (sgn=1 and m[i]^2<>z) then Error("wrong square"); fi;
                if i<n-1 and m[i]*m[i+1]*m[i]<>m[i+1]*m[i]*m[i+1] then
                    Error("braid relation");
                fi;
                for j in [i+2..n-1] do
                    if Comm(m[i],m[j])<>z then Error("commuting relator lost"); fi;
                    checks:=checks+1;
                od;
            od;
            if n<=5 then
                quot:=FactorGroup(g,Subgroup(g,[z]));
                if IsomorphismGroups(quot,SymmetricGroup(n))=fail then
                    Error("actual central quotient is not symmetric");
                fi;
            fi;
            cases:=cases+1;
            Print("PASS n=",n," characteristic=",p," sign=",sgn,
                " dimension=",Length(m[1])," actual_order=",Size(g),"\n");
        od;
    od;
od;
Print("ALL PASS matrix_cases=",cases," distant_commutators=",checks,"\n");
end;
Run199();
QUIT;
