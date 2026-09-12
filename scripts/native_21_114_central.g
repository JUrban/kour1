Read("results/21.114-native-input.g");;
RunNative114 := function()
    local row,p,els,z,zgen,ip,pc,r,a,b,e,ie,ec,ez,d,u,v,diag,hom,g;
    for row in NativeInputs114 do
        p := Group(List(row[2],PermList)); els := Elements(p);
        zgen := els[row[3]]; z := Group(zgen);
        if Size(p)<>512 or Order(zgen)<>4 or not IsSubgroup(Centre(p),z)
           or DerivedLength(p)<>3 then Error("invalid input model"); fi;
        ip := IsomorphismPcGroup(p); pc := Image(ip);
        r := Integers mod 4;
        a := IdentityMat(3,r); a[1][2] := One(r);
        b := IdentityMat(3,r); b[2][3] := One(r);
        e := Group(a,b);
        if Size(e)<>64 or Order(Comm(a,b))<>4 or Size(Centre(e))<>4 then
            Error("invalid Heisenberg factor");
        fi;
        ie := IsomorphismPcGroup(e); ec := Image(ie); ez := Image(ie,Comm(a,b));
        d := DirectProduct(pc,ec);
        u := Embedding(d,1); v := Embedding(d,2);
        diag := Group(Image(u,Image(ip,zgen))*Image(v,ez)^-1);
        if not IsSubgroup(Centre(d),diag) or Size(diag)<>4 then Error("bad diagonal"); fi;
        hom := NaturalHomomorphismByNormalSubgroup(d,diag); g := Image(hom);
        if Size(g)<>8192 or DerivedLength(g)<>3 or Index(g,DerivedSubgroup(g))<>256 then
            Error("bad constructed group");
        fi;
        if Size(Image(hom,Image(u)))<>512 then Error("lost embedded source"); fi;
        Print("NATIVE_ROW ",[row[1],Size(g),Index(g,DerivedSubgroup(g)),
                            DerivedLength(g),NilpotencyClassOfGroup(g)],"\n");
    od;
    Print("PASS_21114_NATIVE_CENTRAL\n");
end;
RunNative114();
QUIT;
