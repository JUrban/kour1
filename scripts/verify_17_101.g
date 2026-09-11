# Independent exact Laurent-polynomial realization of the enlargement example.
for p in [2,3,5,7] do
    k:=GF(p); z:=Indeterminate(k,"z"); one:=One(z); zero:=Zero(z);
    # Keep constants in the polynomial family, including its zero.
    g:=[[one,one],[zero,one]];
    t:=[[z,zero],[zero,z]];
    idmat:=[[one,zero],[zero,one]];
    if g*t<>t*g or g^p<>idmat or g=idmat then
        Error("HNN representation relation");
    fi;
    e1:=[one,zero]; e2:=[zero,one]; e3:=[z,zero];
    # Matrices act on column vectors; transpose for GAP's row-vector action.
    if e1*TransposedMat(t)<>e3 then Error("stable letter map"); fi;
    checks:=0;
    for a in k do for b in k do for c in k do
        v:=a*e1+b*e2+c*e3;
        if v=[zero,zero] and [a,b,c]<>[Zero(k),Zero(k),Zero(k)] then
            Error("original vector space collapsed");
        fi;
        expected:=(a+b)*e1+b*e2+c*e3;
        if v*TransposedMat(g)<>expected then Error("original group action changed"); fi;
        checks:=checks+1;
    od;od;od;
    for i in [-8..8] do
        if (z^i=one)<>(i=0) then Error("Laurent power control"); fi;
    od;
    Print("LAURENT_EXTENSION p=",p," vectors=",checks," PASS\n");
od;
Print("DONE 17.101 independent Laurent extension controls PASS\n");
QUIT;
