# Actual affine permutation groups and induced character computations.
Run19108Controls:=function()
local cases,c,q,u,translation,mult,g,a,ca,cg,ta,tg,pos,lambda,chi,
      units,z,x,expected,k,bound,checks,failures,localfailures;
SizeScreen([1000000,1000000]);
cases:=[[4,3],[8,3],[8,5],[8,7],[9,4],[27,4],[27,10],[25,6],[81,4]];
checks:=0;failures:=0;
for c in cases do
    q:=c[1];u:=c[2];
    translation:=PermList(List([0..q-1],x->(x+1) mod q+1));
    mult:=PermList(List([0..q-1],x->(u*x) mod q+1));
    g:=Group(translation,mult);a:=Group(translation);
    units:=[1];z:=u;
    while z<>1 do Add(units,z);z:=z*u mod q;od;
    if Size(g)<>q*Length(units) then Error("affine group size");fi;
    ca:=ConjugacyClasses(a);cg:=ConjugacyClasses(g);
    ta:=CharacterTable(a);tg:=CharacterTable(g);
    pos:=PositionProperty(ca,k->translation in k);
    lambda:=First(Irr(ta),x->x[pos]=E(q));
    if lambda=fail then Error("missing faithful character");fi;
    chi:=InducedClassFunction(lambda,tg);
    if ScalarProduct(chi,chi)<>1 or chi[1]<>Length(units) then Error("induced character");fi;
    bound:=Size(g)/chi[1]^2;localfailures:=0;
    for x in [0..q-1] do
        expected:=Sum(units,z->E(q)^(z*x));
        k:=PositionProperty(cg,c->translation^x in c);
        if chi[k]<>expected then Error("orbit sum disagrees with character table");fi;
        if chi[k]<>0 and bound mod Order(translation^x)<>0 then
            localfailures:=localfailures+1;
        fi;
        checks:=checks+1;
    od;
    if q mod 2=1 and localfailures<>0 then Error("odd-prime control failure");fi;
    if q=8 and u in [3,7] and localfailures=0 then Error("missing positive failure control");fi;
    failures:=failures+localfailures;
    Print("PASS q=",q," unit=",u," group_order=",Size(g)," degree=",chi[1],
          " bound=",bound," violating_elements=",localfailures,"\n");
od;
Print("DONE actual_groups=",Length(cases)," exact_character_values=",checks,
      " known_even_prime_violations=",failures,"\n");
end;
Run19108Controls();
QUIT;
