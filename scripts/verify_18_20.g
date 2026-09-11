LoadPackage("ctbllib");;

# The sequential criterion used by the library screen, applied also to
# equal-degree rows so genuine positive controls are included.
TwoRatios:=function(phi,psi)
local k,d1,d2,u,v,found;
d1:=phi[1]; d2:=psi[1]; found:=false;
for k in [2..Length(phi)] do
    if phi[k]*d2=psi[k]*d1 then continue; fi;
    if not found then u:=phi[k]; v:=psi[k]; found:=true;
    elif phi[k]*v<>psi[k]*u then return false; fi;
od;
return found;
end;

# Ground truth: enumerate all partitions of the conjugacy classes, fixing
# the identity class in the first part, and test both restricted row ranks.
ProportionalOn:=function(phi,psi,positions)
local k,h;
h:=First(positions,k->phi[k]<>0 or psi[k]<>0);
if h=fail then return true; fi;
return ForAll(positions,k->phi[k]*psi[h]=psi[k]*phi[h]);
end;
ByAllPartitions:=function(phi,psi)
local k,subset,part,other,cols;
cols:=[1..Length(phi)];
if ProportionalOn(phi,psi,cols) then return false; fi;
for subset in Combinations([2..Length(phi)]) do
    part:=Concatenation([1],subset); other:=Difference(cols,part);
    if ProportionalOn(phi,psi,part) and ProportionalOn(phi,psi,other) then
        return true;
    fi;
od;
return false;
end;

RunControls:=function()
local groups,g,t,irr,i,j,fast,slow,checks,positive,negative,names,name;
groups:=[CyclicGroup(2),CyclicGroup(3),CyclicGroup(7),
         DihedralGroup(8),QuaternionGroup(8),SymmetricGroup(3),
         SymmetricGroup(4),AlternatingGroup(4),AlternatingGroup(5),
         SmallGroup(27,3)];
checks:=0; positive:=0; negative:=0;
for g in groups do
    t:=CharacterTable(g); irr:=Irr(t);
    for i in [1..Length(irr)] do
        for j in [i+1..Length(irr)] do
            fast:=TwoRatios(irr[i],irr[j]);
            slow:=ByAllPartitions(irr[i],irr[j]);
            if fast<>slow then Error("partition mismatch"); fi;
            checks:=checks+1;
            if fast then
                positive:=positive+1;
                if irr[i][1]<>irr[j][1] then Error("counterexample"); fi;
            else negative:=negative+1; fi;
        od;
    od;
    Print("GROUP order=",Size(g)," classes=",Length(irr)," PASS\n");
od;
if positive=0 or negative=0 then Error("missing control type"); fi;
Print("PASS group_cases=",Length(groups)," row_pairs=",checks,
      " positive=",positive," negative=",negative,"\n");
end;
RunControls();
QUIT;
