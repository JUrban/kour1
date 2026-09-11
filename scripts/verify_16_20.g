# Exact small-factor checks; the huge central quotient is handled by
# its proved factor/centre description, not by enumerating its elements.
primes := [7,11,13,17,19,23,29];;
simpleOrders := [];;
factorOrders := [];;
for p in primes do
    matrixGroup := SL(2,p);
    permutationGroup := Image(IsomorphismPermGroup(matrixGroup));
    z := Centre(permutationGroup);
    if Size(permutationGroup) <> p*(p^2-1) then Error("factor order"); fi;
    if Size(z) <> 2 then Error("centre order"); fi;
    if DerivedSubgroup(permutationGroup) <> permutationGroup then Error("not perfect"); fi;
    simpleQuotient := FactorGroup(permutationGroup,z);
    if Size(simpleQuotient) <> p*(p^2-1)/2 then Error("simple quotient order"); fi;
    if not IsSimpleGroup(simpleQuotient) then Error("quotient not simple"); fi;
    normalSubs := NormalSubgroups(permutationGroup);
    normalOrders := SortedList(List(normalSubs,Size));
    if normalOrders <> [1,2,Size(permutationGroup)] then Error("normal subgroups"); fi;
    Add(simpleOrders,Size(simpleQuotient));
    Add(factorOrders,Size(permutationGroup));
    Print("p=",p," order=",Size(permutationGroup)," centre=",Size(z),
          " quotient=",Size(simpleQuotient)," normals=",normalOrders," PASS\n");
od;
for i in [1..Length(primes)] do
    for j in [1..Length(primes)] do
        if i <> j and simpleOrders[j] mod simpleOrders[i] = 0 then
            Error("simple-order divisibility");
        fi;
    od;
od;
Print("central_kernel_order=16 centre_order=8 total_order=",Product(factorOrders)/16," PASS\n");
Print("DONE ALL CHECKS PASS\n");
QUIT;
