# Kourovka 21.113(b), using known irreducible Brauer tables.
# Projective indecomposable characters and irreducible Brauer characters
# are dual under the ordinary class inner product restricted to p-regular
# elements. Thus these scalar products are the candidate PIM multiplicities.
# Reconstruct ordinary multiplicities with the decomposition matrix as a check.
LoadPackage("ctbllib");;
RunSearch := function()
local names,checked,cases,unavailable,hits,name,t,orders,exponent,sizes,
      p,pp,rest,power,values,i,bt,fusion,f,n,D,ordinary,reconstructed;
names := AllCharacterTableNames();
checked := 0; cases := 0; unavailable := 0; hits := 0;
for name in names do
    Print("TABLE_START ",name," runtime_ms=",Runtime(),"\n");
    t := CharacterTable(name);
    if t=fail then Error("ordinary table missing",name); fi;
    orders := OrdersClassRepresentatives(t);
    exponent := Lcm(orders); sizes := SizesConjugacyClasses(t);
    for p in PrimeDivisors(exponent) do
        bt := t mod p;
        if bt=fail then unavailable := unavailable+1; continue; fi;
        pp := 1; rest := exponent;
        while rest mod p=0 do pp:=pp*p; rest:=rest/p; od;
        power := PowerMap(t,pp);
        if not ForAll(power,IsInt) then Error("ambiguous power map",name,p); fi;
        values := List(sizes,x->0);
        for i in [1..Length(sizes)] do
            values[power[i]] := values[power[i]]+sizes[i];
        od;
        values := List([1..Length(sizes)],i->values[i]/sizes[i]);
        fusion := GetFusionMap(bt,t);
        f := ClassFunction(bt,values{fusion});
        n := List(Irr(bt),chi->ScalarProduct(bt,f,chi));
        D := DecompositionMatrix(bt);
        ordinary := List(Irr(t),chi->ScalarProduct(t,ClassFunction(t,values),chi));
        reconstructed := List(D,row->row*n);
        if reconstructed<>ordinary then
            Error("projective/Brauer duality reconstruction mismatch",name,p);
        fi;
        cases := cases+1;
        if not ForAll(n,x->IsInt(x) and x>=0) then
            Print("HIT table=",name," p=",p," PIM_coefficients=",n,
                  " ordinary_coefficients=",ordinary," values=",values,"\n");
            hits := hits+1;
        fi;
    od;
    checked := checked+1;
    if checked mod 100=0 then
        Print("PROGRESS tables=",checked," modular_cases=",cases,
              " unavailable=",unavailable," hits=",hits,"\n");
    fi;
od;
Print("DONE tables=",checked," modular_cases=",cases,
      " unavailable=",unavailable," hits=",hits,"\n");
end;
RunSearch();
QUIT;
