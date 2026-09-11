# Independent explicit affine permutations for small IRREDSOL cases.
LoadPackage("irredsol");;
Control18114:=function(p,n,d,k)
local g,matrices,module,vectors,basis,linear,translations,complement,affine,
      pc,actual,expected,cyclic,els,x,y,i,sum,rank,horizontal,third;
g:=IrreducibleSolubleMatrixGroup(n,p,d,k);
matrices:=List(GeneratorsOfGroup(g),m->List(m,ShallowCopy));
module:=GModuleByMats(matrices,GF(p));
if not MTX.IsIrreducible(module) then Error("actual reducibility"); fi;
vectors:=Set(Tuples(Elements(GF(p)),n));
basis:=IdentityMat(n,GF(p));
linear:=List(matrices,m->PermList(List(vectors,v->Position(vectors,v*m))));
translations:=List(basis,u->PermList(List(vectors,v->Position(vectors,v+u))));
complement:=Group(linear);
affine:=Group(Concatenation(linear,translations));
if Size(complement)<>Size(g) or Size(affine)<>p^n*Size(g) then
    Error("permutation orders disagree");
fi;
cyclic:=IsCyclic(complement);
if cyclic<>IsCyclic(g) then Error("actual cyclicity mismatch"); fi;
actual:=Length(ConjugacyClasses(affine));
pc:=PrimitivePcGroupIrreducibleMatrixGroup(g);
expected:=NrConjugacyClasses(pc);
if actual<>expected then Error("pc versus permutation mismatch"); fi;
if cyclic and actual<>Size(g)+(p^n-1)/Size(g) then
    Error("cyclic formula mismatch");
fi;
third:=false;
if Size(g)<=32 then
    # Count commuting affine pairs by summing over commuting linear parts.
    # For a coprime commuting pair x,y, each contributes p^dim C_V(x,y).
    els:=Elements(g);sum:=0;i:=IdentityMat(n,GF(p));
    for x in els do
        for y in els do
            if x*y=y*x then
                horizontal:=TransposedMat(Concatenation(
                    TransposedMat(x-i),TransposedMat(y-i)));
                rank:=RankMat(horizontal);
                sum:=sum+p^(n-rank);
            fi;
        od;
    od;
    if sum<>actual*Size(g) then Error("commuting-pair formula mismatch"); fi;
    third:=true;
fi;
Print("PASS p=",p," n=",n," d=",d," k=",k,
    " complement_order=",Size(g)," classes=",actual," cyclic=",cyclic,
    " commuting_pairs=",third,"\n");
return [actual=p^n and not cyclic,third];
end;
RunControls18114:=function()
local p,n,d,k,g,r,total,positive,third;
total:=0;positive:=0;third:=0;
for p in [2,3,5] do
    for n in [1..3] do
        for d in DivisorsInt(n) do
            for k in IndicesIrreducibleSolubleMatrixGroups(n,p,d) do
                g:=IrreducibleSolubleMatrixGroup(n,p,d,k);
                if Size(g) mod p=0 then continue; fi;
                r:=Control18114(p,n,d,k);total:=total+1;
                if r[1] then positive:=positive+1; fi;
                if r[2] then third:=third+1; fi;
            od;
        od;
    od;
od;
if positive<2 then Error("missing noncyclic positive controls"); fi;
Print("ALL PASS controls=",total," noncyclic_equality_controls=",positive,
    " commuting_pair_controls=",third,"\n");
end;
RunControls18114();
QUIT;
