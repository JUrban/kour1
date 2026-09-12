# Native exact rational matrix arithmetic, with finite permutation sinks.
SizeScreen([4096,1000]);;
perms:=Filtered(Tuples([1..4],4),t->Length(Set(t))=4);;
Matrix7:=function(u,v,z,k,p)
    local a,j;
    a:=NullMat(7,7,Rationals);
    a[1][1]:=4^k;a[1][2]:=u*2^k;a[1][3]:=z;
    a[2][2]:=2^k;a[2][3]:=v;a[3][3]:=1;
    for j in [1..4] do a[j+3][p[j]+3]:=1;od;
    return a;
end;;
Encode:=function(a)
    local p;
    p:=List([4..7],j->Position(a[j]{[4..7]},1));
    return Concatenation(List([a[1][2],a[2][3],a[1][3]],q->[NumeratorRat(q),DenominatorRat(q)]),[p]);
end;;
for i in [0..719] do
    x:=Matrix7((i mod 7-3)/2^(i mod 3),((3*i) mod 7-3)/2^((i+1) mod 3),((5*i) mod 7-3)/2^((i+2) mod 3),i mod 7-3,perms[i mod 24+1]);
    a:=Matrix7(((2*i) mod 9-4)/2^((i+2) mod 3),((4*i) mod 9-4)/2^(i mod 3),((7*i) mod 9-4)/2^((i+1) mod 3),0,perms[(7*i+5) mod 24+1]);
    row:=[];
    for j in [1..3] do x:=Comm(x,a);Add(row,Encode(x));od;
    if x{[1..3]}{[1..3]}<>IdentityMat(3,Rationals) or SignPerm(PermList(row[3][4]))<>1 then Error("common kernel");fi;
    Print("ROW2089C ",[i,row],"\n");
od;
orbitrows:=[];;
for k in [-4,-3,-2,-1,1,2,3,4] do
    a:=Matrix7(2,-3,1,k,[1..4]);images:=[];
    if k=-1 then
        for b in [1..40] do
            x:=Matrix7(b,0,0,0,[1..4]);
            for j in [1..20] do x:=Comm(x,a);od;
            if x[1][2]<>b then Error("fixed coordinate");fi;Add(images,x[1][2]);
        od;
        if Length(Set(images))<>40 then Error("infinitely many starting points");fi;
    else
        x:=Matrix7(1,0,0,0,[1..4]);
        for j in [0..20] do
            if x[1][2]<>(2^(-k)-1)^j then Error("dilation recurrence");fi;
            Add(images,x[1][2]);x:=Comm(x,a);
        od;
        if Length(Set(images))<>21 then Error("orbit distinctness");fi;
    fi;
    Add(orbitrows,[k,Length(images)]);
od;
s4:=SymmetricGroup(4);;els:=Elements(s4);;sinks:=[];;
for a in els do
    e:=Set(els);
    repeat old:=e;e:=Set(old,x->Comm(x,a));until old=e;
    Add(sinks,e);
od;
all:=Union(sinks);;hist:=Collected(List(sinks,Length));;
if all<>Set(Elements(AlternatingGroup(4))) then Error("S4 sink union");fi;
nonsplit:=0;;torsion:=0;;
for m in [-20..20] do
    for p in Elements(SymmetricGroup(3)) do
        a:=NullMat(5,5,Rationals);a[1][1]:=1;a[1][2]:=m;a[2][2]:=1;
        for j in [1..3] do a[j+2][j^p+2]:=1;od;
        b:=a^6;
        if b[1][2]<>6*m or b{[3..5]}{[3..5]}<>IdentityMat(3,Rationals) then Error("nonsplit power");fi;
        if b=IdentityMat(5,Rationals) then torsion:=torsion+1;fi;
        nonsplit:=nonsplit+1;
    od;
od;
if torsion<>6 then Error("torsion lift");fi;
central:=[];;
for r in [1..8] do
    z:=E(3^r);
    if Order(z)<>3^r then Error("central order");fi;
    for j in [0..9] do if z^(-j)*z^(-2*j-1)*z^j*z^(2*j+1)<>1 then Error("central commutator");fi;od;
    Add(central,Order(z));
od;
Print("SUMMARY2089C {\"pairs\":720,\"commutators\":2160,\"excluded_dilations\":",orbitrows,",\"s4_sink_histogram\":",hist,",\"s4_sink_union\":",Length(all),",\"nonsplit_checks\":",nonsplit,",\"nonsplit_torsion\":",torsion,",\"central_torsion_orders\":",central,"}\n");
Print("PASS_20_89_CHAR0_NATIVE\n");
QUIT_GAP(0);
