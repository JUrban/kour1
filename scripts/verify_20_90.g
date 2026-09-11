# GAP controls, independent of the packed-polynomial Python implementation.
SetAssertionLevel(2);
f := GF(4);; w := Z(4);; e := One(f);; z := Zero(f);;
x := [[e,e],[z,e]];; y := [[z,e],[e,w]];;
g := Group(x,y);;
Assert(0, Size(g)=60 and IsSimpleGroup(g) and not IsSolvableGroup(g));
Assert(0, [Order(x),Order(y),Order(x*y)]=[2,5,5]);
Assert(0, IsomorphismGroups(g,AlternatingGroup(5))<>fail);
d := y^(-1)*x*y^(-2);;
Assert(0,d=[[w,z],[z,w^2]]);
Assert(0,y*x*y^(-1)=[[e,z],[e,e]]);
Assert(0,DerivedSubgroup(g)=g);
cs := [];;
for a in Elements(g) do
    if not IsOne(a) then
        c := Centralizer(g,a);
        Assert(0,IsAbelian(c));
        Add(cs,Size(c));
    fi;
od;
Assert(0,Collected(cs)=[[3,20],[4,15],[5,24]]);
Print("SL2(F4): order=60; generators/product=2,5,5; simple; A5: PASS\n");
Print("All59 nonidentity finite centralizers: ",Collected(cs)," PASS\n");
t := Indeterminate(f,"t");;
ep := One(t);; zp := Zero(t);;
yy := [[zp,ep],[ep,w+t]];;
identity := [[ep,zp],[zp,ep]];;
power := identity;; prev := zp;; cur := ep;;
for n in [1..128] do
    power := power*yy;
    nxt := (w+t)*cur+prev;
    Assert(0,power=[[prev,cur],[cur,nxt]]);
    Assert(0,DegreeOfLaurentPolynomial(nxt)=n);
    Assert(0,LeadingCoefficient(nxt)=e);
    Assert(0,power<>identity);
    prev := cur; cur := nxt;
od;
Print("128 polynomial matrix-power/leading-term controls: PASS\n");
Print("20.90 GAP controls: PASS\n");
QUIT;
