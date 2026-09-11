# Exploratory character-table screen: no all-degree theorem is certified.
Explore1032 := function()
    local n,q,t,pars,a,b,missing,k,odd,coeff,checks,G,I,products;
    checks:=0;
    G:=AlternatingGroup(5); I:=Filtered(Elements(G),x->x^3=());
    products:=Set(Concatenation(List(I,x->List(I,y->x*y))));
    if Length(products)<>60 then Error("A5 cube-order control failed"); fi;
    Print("A5: order-dividing-three elements=",Length(I),
          " product-set-size=",Length(products),"\n");
    for n in [6..25] do
        t:=CharacterTable("Symmetric",n);
        pars:=List(ClassParameters(t),x->x[2]);
        odd:=Filtered([1..Length(pars)],k->(n-Length(pars[k])) mod 2=1);
        for q in Filtered([3..QuoInt(n,2)],IsPrimeInt) do
            if 2*q>=QuoInt(3*n,4)+1 then
                a:=Position(pars,Concatenation([2*q],List([1..n-2*q],i->1)));
                b:=Position(pars,Concatenation([q,q],List([1..n-2*q],i->1)));
                missing:=[];
                for k in odd do
                    coeff:=ClassMultiplicationCoefficient(t,a,b,k);
                    if not IsInt(coeff) or coeff<0 then Error("invalid coefficient"); fi;
                    if coeff=0 then Add(missing,pars[k]); fi;
                    checks:=checks+1;
                od;
                Print("n=",n," q=",q," odd_classes=",Length(odd),
                      " missing=",missing,"\n");
            fi;
        od;
    od;
    Print("class_coefficients=",checks,"\nPASS_1032_EXPLORATION\n");
end;
Explore1032();
QUIT;
