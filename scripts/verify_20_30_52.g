# Actual-element conjugacy orbits, independent of character-table class sizes.
DirectClassSizes:=function(g)
local els,seen,gens,i,j,queue,head,x,a,sizes;
els:=AsSSortedList(g); seen:=List(els,x->false);
gens:=Set(Concatenation(GeneratorsOfGroup(g),List(GeneratorsOfGroup(g),Inverse)));
sizes:=[];
for i in [1..Length(els)] do
    if seen[i] then continue; fi;
    queue:=[i]; seen[i]:=true; head:=1;
    while head<=Length(queue) do
        x:=els[queue[head]]; head:=head+1;
        for a in gens do
            j:=Position(els,x^a);
            if not seen[j] then seen[j]:=true; Add(queue,j); fi;
        od;
    od;
    Add(sizes,Length(queue));
od;
if Sum(sizes)<>Size(g) then Error("orbit partition failed"); fi;
return SortedList(sizes);
end;

RunControls:=function()
local n,j,g,rows,pair,sizes,ct,eligible,actual,groups,count52,count30;
count52:=0; count30:=0;
rows:=[];
for n in [3,5..99] do
    for j in [1..NumberSmallGroups(n)] do Add(rows,[n,j]); od;
od;
Append(rows,List([9..12],j->[1161,j]));
for pair in rows do
    g:=Image(IsomorphismPermGroup(SmallGroup(pair[1],pair[2])));
    sizes:=DirectClassSizes(g);
    if Length(sizes)<>NrConjugacyClasses(g) then Error("class count failed"); fi;
    count52:=count52+1;
    Print("CONTROL52 order=",pair[1]," id=",pair[2]," classes=",Length(sizes),"\n");
od;
groups:=[Group(()),SymmetricGroup(3),DihedralGroup(IsPermGroup,8),
    AlternatingGroup(5),AlternatingGroup(6),
    Image(IsomorphismPermGroup(SL(2,5))),
    DirectProduct(AlternatingGroup(5),CyclicGroup(IsPermGroup,61)),
    DirectProduct(AlternatingGroup(5),AlternatingGroup(5)),
    DerivedSubgroup(WreathProduct(CyclicGroup(IsPermGroup,2),AlternatingGroup(5)))];
for g in groups do
    sizes:=DirectClassSizes(g); ct:=CharacterTable(g);
    if sizes<>SortedList(SizesConjugacyClasses(ct)) then Error("table class sizes failed"); fi;
    eligible:=Number(Irr(ct),c->c[1]=1)=1 and Number(sizes,x->x=1)=1;
    actual:=Size(DerivedSubgroup(g))=Size(g) and Size(Centre(g))=1;
    if eligible<>actual then Error("perfect/centerless predicate failed"); fi;
    if eligible and Maximum(sizes)^2<Size(g) then Error("counterexample in controls"); fi;
    count30:=count30+1;
    Print("CONTROL30 order=",Size(g)," classes=",Length(sizes),
          " max_class=",Maximum(sizes)," eligible=",eligible,"\n");
od;
Print("DONE controls52=",count52," controls30=",count30," PASS\n");
end;
RunControls();
QUIT;
