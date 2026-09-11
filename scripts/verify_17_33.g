# Independent GAP controls for the explicit finite presentation in 17.33.
# The infinite assertions are proved in research/17.33-proof.md.
Bit := function(v,j) return QuoInt(v,2^(j-1)) mod 2; end;
Presentation1733 := function(n)
    local m,f,x,t,g,rels,i,j,chi,k,l,w;
    m:=n*(2^n-1); f:=FreeGroup(m+n); x:=GeneratorsOfGroup(f);
    t:=x{[1..m]}; g:=x{[m+1..m+n]}; rels:=[];
    for k in [1..m] do
        for l in [k+1..m] do Add(rels,Comm(t[k],t[l])); od;
    od;
    for i in [1..n] do
        w:=One(f);
        for chi in [1..2^n-1] do
            for j in [1..n] do
                k:=(chi-1)*n+j;
                Add(rels,g[i]*t[k]*g[i]^-1*t[k]^(-(-1)^Bit(chi,i)));
            od;
            if Bit(chi,i)=0 then w:=w*t[(chi-1)*n+i]; fi;
        od;
        Add(rels,g[i]^2*w^-1);
        for j in [i+1..n] do
            w:=One(f);
            for chi in [1..2^n-1] do
                w:=w*t[(chi-1)*n+i]^Bit(chi,j)*t[(chi-1)*n+j]^(-Bit(chi,i));
            od;
            Add(rels,g[i]*g[j]*(w*g[j]*g[i])^-1);
        od;
    od;
    return rec(free:=f,rels:=rels,translations:=t);
end;
for n in [2..5] do
    p:=Presentation1733(n); gamma:=p.free/p.rels;
    ab:=AbelianInvariants(gamma);
    if not ForAll(ab,x->x=2 or x=4) then Error("infinite or wrong abelianization"); fi;
    Print("ABELIANIZATION n=",n," C2_factors=",Number(ab,x->x=2),
          " C4_factors=",Number(ab,x->x=4)," order=",Product(ab)," PASS\n");
od;
p:=Presentation1733(2);
finite:=p.free/Concatenation(p.rels,List(p.translations,x->x^2));
iso:=IsomorphismPermGroup(finite); g:=Image(iso);
if Size(g)<>256 or Size(Centre(g))<>64 or Exponent(g)<>4 then
    Error("finite presentation quotient mismatch");
fi;
if Set(Elements(Centre(g)))<>Set(Filtered(Elements(g),x->x^2=One(g))) then
    Error("central involution mismatch");
fi;
Print("FINITE_QUOTIENT order=",Size(g)," id=",IdGroup(g),
      " centre=",Size(Centre(g))," derived=",Size(DerivedSubgroup(g)),
      " exponent=",Exponent(g)," PASS\n");
Print("DONE 17.33 independent presentation controls PASS\n");
QUIT;
