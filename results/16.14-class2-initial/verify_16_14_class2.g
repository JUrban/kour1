# Native controls for the class-two square map, including exponent eight.
SetAssertionLevel(2);
ClassTwo1614 := function()
    local family, groups, names, k, g, z, phi, z2, zp, a, v, s, projection,
          elts, table, qi, n, r, c, dimS, central, zeros, x, y, rows, expected,
          gens, modA, modC, triples, right, label, path;
    family := function(modA, modC)
        local triples, right, aa, bb, cc;
        triples := Tuples([[0..modA-1],[0..modA-1],[0..modC-1]]);
        right := function(v)
            return PermList(List(triples,u->Position(triples,
                [(u[1]+v[1]) mod modA,(u[2]+v[2]) mod modA,
                 (u[3]+v[3]+u[1]*v[2]) mod modC])));
        end;
        aa:=right([1,0,0]); bb:=right([0,1,0]); cc:=right([0,0,1]);
        return Group(aa,bb,cc);
    end;
    groups := [TrivialGroup(),CyclicGroup(64),AbelianGroup([2,4,8]),
               DihedralGroup(8),QuaternionGroup(8),
               DirectProduct(QuaternionGroup(8),CyclicGroup(8)),
               DirectProduct(QuaternionGroup(8),QuaternionGroup(8)),
               DirectProduct(DihedralGroup(8),CyclicGroup(4)),
               family(4,2),family(8,4)];
    names := ["trivial","C64","C2xC4xC8","D8","Q8","Q8xC8",
              "Q8xQ8","D8xC4","coordinates_4_2","coordinates_8_4"];
    rows:=[];
    for k in [1..Length(groups)] do
        g:=groups[k]; z:=Centre(g); phi:=FrattiniSubgroup(g);
        Assert(0,IsAbelian(g/z));
        z2:=Subgroup(z,List(Elements(z),x->x^2)); zp:=Intersection(z,phi);
        a:=g/z; v:=Omega(a,2,1); s:=zp/z2;
        n:=LogInt(Size(v),2); r:=LogInt(Index(z,z2),2);
        c:=LogInt(Index(z,zp),2); dimS:=LogInt(Size(s),2);
        projection:=NaturalHomomorphismByNormalSubgroup(g,z);
        zeros:=0;
        for x in Elements(v) do
            y:=PreImagesRepresentative(projection,x);
            Assert(0,y^2 in zp);
            if y^2 in z2 then zeros:=zeros+1; fi;
        od;
        central:=ForAll(g,x->x^2<>One(g) or x in z);
        Assert(0,(zeros=1)=central);
        Assert(0,LogInt(Index(g,phi),2)=n+c and r=c+dimS);
        if central then Assert(0,n<=2*dimS); fi;
        if k=10 then
            Assert(0,Size(g)=256 and Exponent(g)=8 and Exponent(DerivedSubgroup(g))=4);
        fi;
        expected := [Size(g),Exponent(g),LogInt(Index(g,phi),2),r,c,n,dimS,
                     Int(central),zeros,Number(g,x->x^2=One(g))];
        Add(rows,expected);
        elts:=Concatenation([One(g)],Filtered(Elements(g),x->x<>One(g)));
        table:=List(elts,x->List(elts,y->Position(elts,x*y)-1));
        gens:=List(GeneratorsOfGroup(g),x->Position(elts,x)-1);
        path:=Concatenation("results/16.14-class2-model-",String(k),".json");
        PrintTo(path,"{\"label\":\"",names[k],"\",\"expected\":",expected,
                ",\"generators\":",gens,",\"table\":",table,"}\n");
    od;
    Assert(0,not IsAbelian(QuaternionGroup(16)/Centre(QuaternionGroup(16))));
    Print("NATIVE_1614_CLASS2_ROWS ",rows,"\nPASS_16_14_CLASS2_NATIVE models=10\n");
end;
ClassTwo1614();
QUIT;
