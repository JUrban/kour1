# Matrix controls of the noncommutative elimination in 18.76.
# Matrix algebras are NOT division rings, and these finite-dimensional models
# are not embeddings of F2 x F2. They only check the algebraic obstruction.
Check1876:=function(p)
    local field,o,zz,i2,i4,aa,bb,cc,dd,a,b,c,d,x,y,a0,b0,c0,d0,
          ai,ci,zm,blocks,mat,blockrow,j,target,augmented,relation;
    if p=0 then field:=Rationals; else field:=GF(p); fi;
    o:=One(field); zz:=Zero(field);
    i2:=IdentityMat(2,field); i4:=IdentityMat(4,field);
    aa:=[[zz,-o],[o,o]]; bb:=[[o,o],[zz,o]];
    cc:=aa; dd:=[[o,zz],[o,o]];
    a:=KroneckerProduct(aa,i2); b:=KroneckerProduct(bb,i2);
    c:=KroneckerProduct(i2,cc); d:=KroneckerProduct(i2,dd);
    if a*b=b*a or c*d=d*c then Error("lost noncommutativity"); fi;
    for x in [a,b] do
        for y in [c,d] do
            if x*y<>y*x then Error("cross commutation failed"); fi;
        od;
    od;
    a0:=a-i4; b0:=b-i4; c0:=c-i4; d0:=d-i4;
    ai:=a0^-1; ci:=c0^-1; zm:=NullMat(4,4,field);
    blocks:=[[-c0,zm,a0,zm],[-d0,zm,zm,a0],
             [zm,-c0,b0,zm],[zm,-d0,zm,b0]];
    mat:=[];
    for blockrow in blocks do
        for j in [1..4] do
            Add(mat,Concatenation(List(blockrow,block->block[j])));
        od;
    od;
    target:=Concatenation(List([1..12],x->zz),[o,zz,zz,zz]);
    augmented:=List([1..16],j->Concatenation(mat[j],[target[j]]));
    if RankMat(mat)<>12 or RankMat(mat{[1..12]})<>12
        or RankMat(augmented)<>13 then Error("rank obstruction failed"); fi;
    relation:=TransposedMat(Concatenation(List(
        [d0*ci*b0*ai,-b0*ai,-d0*ci,i4],TransposedMat)));
    if relation*mat<>NullMat(4,16,field) then
        Error("ordered obstruction relation failed");
    fi;
    if relation*List(target,x->[x])=NullMat(4,1,field) then
        Error("obstruction does not detect target");
    fi;
    Print("PASS characteristic=",p," ranks=12,12,13 noncommuting=true\n");
end;
for p in Concatenation([0],Filtered([2..101],IsPrimeInt)) do
    Check1876(p);
od;
Print("ALL PASS: rational and 26 prime-field matrix controls\n");
QUIT;
