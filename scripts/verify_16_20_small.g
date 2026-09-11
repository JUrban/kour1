# Construct the entire smaller three-factor group and check its normal lattice.
# No enumeration of all homomorphisms of this large group is claimed.
primes := [5,7,13];;
factors := List(primes,p->Image(IsomorphismPermGroup(SL(2,p))));;
simpleOrders := List(primes,p->p*(p^2-1)/2);;
for i in [1..3] do
    f := factors[i];
    if Size(f) <> 2*simpleOrders[i] or Size(Centre(f)) <> 2 then
        Error("factor or centre order");
    fi;
    if DerivedSubgroup(f) <> f or not IsSimpleGroup(FactorGroup(f,Centre(f))) then
        Error("perfect central cover");
    fi;
    if SortedList(List(NormalSubgroups(f),Size)) <> [1,2,Size(f)] then
        Error("factor normal subgroup list");
    fi;
    for j in [1..3] do
        if i <> j and simpleOrders[j] mod simpleOrders[i] = 0 then
            Error("cross-factor order divisibility");
        fi;
    od;
od;
Print("factor_orders=",List(factors,Size)," simple_orders=",simpleOrders," PASS\n");
u := DirectProduct(factors);;
zz := List([1..3],i->Image(Embedding(u,i),
      First(Elements(Centre(factors[i])),x->Order(x)=2)));;
c := Subgroup(u,[Product(zz)]);;
if Size(c) <> 2 or not IsNormal(u,c) then Error("central kernel"); fi;
quotient := NaturalHomomorphismByNormalSubgroup(u,c);;
a := Image(quotient);;
w := Centre(a);;
if Size(a) <> 44029440 or Size(w) <> 4 or DerivedSubgroup(a) <> a then
    Error("whole-group invariants");
fi;
normalSubs := NormalSubgroups(a);;
normalOrders := SortedList(List(normalSubs,Size));;
if normalOrders <> [1,2,2,2,4,120,240,336,672,2184,4368,
                     40320,262080,733824,44029440] then
    Error("normal subgroup list");
fi;
# Check modularity directly in the actual subgroup lattice, using products
# represented by generated subgroups. Precompute all pairwise operations.
count := Length(normalSubs);;
meets := List([1..count],i->List([1..count],j->
    Position(normalSubs,Intersection(normalSubs[i],normalSubs[j]))));;
joins := List([1..count],i->List([1..count],j->
    Position(normalSubs,ClosureGroup(normalSubs[i],normalSubs[j]))));;
checks := 0;;
for i in [1..count] do
    for j in [1..count] do
        for k in [1..count] do
            if meets[i][k] = i then
                if joins[i][meets[j][k]] <> meets[joins[i][j]][k] then
                    Error("modular law");
                fi;
                checks := checks+1;
            fi;
        od;
    od;
od;
lines := Filtered(normalSubs,n->Size(n)=2);;
if Length(lines) <> 3 then Error("central lines"); fi;
for i in [1..3] do
    if not IsSubgroup(w,lines[i]) then Error("line not central"); fi;
    for j in [1..3] do
        if i <> j and (Size(Intersection(lines[i],lines[j])) <> 1 or
                        ClosureGroup(lines[i],lines[j]) <> w) then
            Error("diamond operations");
        fi;
    od;
od;
Print("group_order=",Size(a)," centre_order=",Size(w)," PASS\n");
Print("normal_count=",count," normal_orders=",normalOrders," PASS\n");
Print("modular_identities_checked=",checks," central_diamond=M3 PASS\n");
Print("DONE ALL CHECKS PASS\n");
QUIT;
