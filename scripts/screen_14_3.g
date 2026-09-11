# Necessary real-character obstruction for the central-unit factorization.
# A flag is a surviving central element, NOT a group-ring unit/counterexample.
LoadPackage("ctbllib");;SizeScreen([1000000,24]);;
Run143:=function()
local names,index,t,irr,sz,central,squarecentral,reals,pow,admissible,
      passed,flagged,flags,orders;
names:=AllCharacterTableNames();passed:=0;flagged:=0;flags:=0;
Print("START143 tables=",Length(names)," gap=",GAPInfo.Version,"\n");
for index in [1..Length(names)] do
 t:=CharacterTable(names[index]);irr:=Irr(t);sz:=SizesConjugacyClasses(t);
 central:=Filtered([1..Length(sz)],j->sz[j]=1);
 pow:=PowerMap(t,2);Assert(0,ForAll(pow,IsInt));
 squarecentral:=Set(List(central,j->pow[j]));
 reals:=Filtered(irr,c->ForAll(c,x->ComplexConjugate(x)=x));
 admissible:=Filtered(Difference(central,squarecentral),
                         j->ForAll(reals,c->c[j]=c[1]));
 if IsEmpty(admissible) then passed:=passed+1;else
  flagged:=flagged+1;flags:=flags+Length(admissible);
  orders:=OrdersClassRepresentatives(t);
  Print("FLAG143 name=",names[index]," central_indices=",admissible,
    " orders=",List(admissible,j->orders[j]),"\n");
 fi;
 Print("TABLE143 index=",index," name=",names[index]," order=",Size(t),
  " central_classes=",Length(central)," central_squares=",Length(squarecentral),
  " real_characters=",Length(reals)," surviving_elements=",Length(admissible),"\n");
od;
Print("DONE143 tables=",Length(names)," criterion_passed=",passed,
 " flagged_tables=",flagged," surviving_elements=",flags,"\n");
end;
Run143();QUIT;
