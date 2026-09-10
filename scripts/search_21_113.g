# Exact character-table search for Kourovka 21.113(a).
# For y in G, let y_(p') be its commuting p'-part. If m is 0 modulo
# the p-part of Exp(G), then y^m=(y_(p'))^m. The unique p'-root of a
# p-regular x has the same centralizer as x, so the fiber size is Psi(x).
# Thus a pure prime-power map suffices; no artificial composite exponent
# needs to be factored. Class sizes and this power map determine Psi exactly.
LoadPackage("ctbllib");;
RunSearch := function()
local names,checked,cases,skipped,name,t,orders,exponent,sizes,p,pp,rest,
      m,power,values,i,psi,coeffs;
names := AllCharacterTableNames();;
checked := 0;; cases := 0;; skipped := 0;;
for name in names do
    Print("TABLE_START ",name," runtime_ms=",Runtime(),"\n");
    t := CharacterTable(name);
    if t = fail then skipped := skipped + 1; continue; fi;
    orders := OrdersClassRepresentatives(t);
    if not ForAll(orders, IsInt) then
        Print("SKIP orders ", name, "\n"); skipped := skipped + 1; continue;
    fi;
    exponent := Lcm(orders);
    sizes := SizesConjugacyClasses(t);
    for p in PrimeDivisors(exponent) do
        pp := 1; rest := exponent;
        while rest mod p = 0 do pp := pp * p; rest := rest / p; od;
        m := pp;
        power := PowerMap(t,m);
        if not ForAll(power, IsInt) then
            Print("SKIP ambiguous power ",name," ",p,"\n");
            skipped := skipped + 1; continue;
        fi;
        values := List(sizes,x->0);
        for i in [1..Length(sizes)] do
            values[power[i]] := values[power[i]] + sizes[i];
        od;
        values := List([1..Length(sizes)],i->values[i]/sizes[i]);
        if not ForAll(values,IsInt) then Error("nonintegral fiber size"); fi;
        psi := ClassFunction(t,values);
        coeffs := List(Irr(t),chi->ScalarProduct(t,psi,chi));
        cases := cases + 1;
        if not ForAll(coeffs,x->IsInt(x) and x>=0) then
            Print("HIT table=",name," p=",p," exponent=",exponent,
                  " m=",m," values=",values," coefficients=",coeffs,"\n");
            Print("TABLEID ",Identifier(t)," order ",Size(t),"\n");
        fi;
    od;
    checked := checked + 1;
    if checked mod 100 = 0 then
        Print("PROGRESS tables=",checked," cases=",cases," skipped=",skipped,
              " latest=",name," runtime_ms=",Runtime(),"\n");
    fi;
od;
Print("DONE tables=",checked," cases=",cases," skipped=",skipped,"\n");
end;
RunSearch();
QUIT;
