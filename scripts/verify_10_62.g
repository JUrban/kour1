# Finite controls for the application; not a verification of the infinite
# small cancellation theorem. GAP 4.16.1, no extra packages required.
Run1062 := function()
    local n,F,a,b,c,rels,H,K,oddPresentations,evenPresentations,
          r,s,refs,x,y,t,d,z,V,pairs,oddPairs,evenPairs,i,j,
          assignment,valid,withoutOddRelation;
    oddPresentations:=0; evenPresentations:=0;
    F:=FreeGroup("a","b","c");
    a:=F.1; b:=F.2; c:=F.3;
    for n in [2..101] do
        rels:=[a^2,b^2,c^2,(a*b)^n,(b*c)^n,(c*a)^n];
        H:=F/rels;
        K:=F/Concatenation(rels,[(a*b*c)^n]);
        if n mod 2=1 then
            if AbelianInvariants(H)<>[2] or AbelianInvariants(K)<>[] then
                Error("odd presentation abelianization failed");
            fi;
            oddPresentations:=oddPresentations+1;
        else
            if AbelianInvariants(H)<>[2,2,2] or
               AbelianInvariants(K)<>[2,2,2] then
                Error("even exponent negative control failed");
            fi;
            evenPresentations:=evenPresentations+1;
        fi;
    od;
    # Independently enumerate every possible map of the three generators to C2.
    valid:=[]; withoutOddRelation:=[];
    for assignment in Tuples([0,1],3) do
        if (assignment[1]+assignment[2]) mod 2=0 and
           (assignment[2]+assignment[3]) mod 2=0 and
           (assignment[3]+assignment[1]) mod 2=0 then
            Add(withoutOddRelation,assignment);
            if Sum(assignment) mod 2=0 then Add(valid,assignment); fi;
        fi;
    od;
    if valid<>[[0,0,0]] or withoutOddRelation<>[[0,0,0],[1,1,1]] then
        Error("literal C2 homomorphism enumeration failed");
    fi;
    pairs:=0; oddPairs:=0; evenPairs:=0;
    # Actual permutations of Z/n, including the n=2 Klein-four control.
    for n in [3..40] do
        r:=PermList(Concatenation([2..n],[1]));
        s:=PermList(List([0..n-1],i->((-i) mod n)+1));
        refs:=List([0..n-1],i->r^i*s);
        if Length(Set(refs))<>n or not ForAll(refs,x->Order(x)=2) then
            Error("reflection construction failed");
        fi;
        for x in refs do for y in refs do
            if x<>y then
                pairs:=pairs+1; t:=x*y; d:=Order(t);
                if d mod 2=1 then
                    if x^(t^((d+1)/2))<>y then
                        Error("dihedral conjugator failed");
                    fi;
                    oddPairs:=oddPairs+1;
                else
                    z:=t^(d/2); V:=Group(x,z);
                    if z=x or Order(z)<>2 or x*z<>z*x or Size(V)<>4 or
                       AbelianInvariants(V)<>[2,2] then
                        Error("even product Klein-four witness failed");
                    fi;
                    evenPairs:=evenPairs+1;
                fi;
            fi;
        od; od;
    od;
    V:=Group((1,2),(3,4)); x:=(1,2); y:=(3,4);
    if Order(x*y)<>2 or Size(V)<>4 then Error("V4 control failed"); fi;
    Print("odd_presentations=",oddPresentations," even_presentations=",
          evenPresentations," c2_assignments=8\n");
    Print("dihedral_pairs=",pairs," odd_pairs=",oddPairs,
          " even_pairs=",evenPairs,"\n");
    Print("PASS_1062_GAP\n");
end;
Run1062();
QUIT;
