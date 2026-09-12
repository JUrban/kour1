g:=SmallGroup(48,48);;
f:=FittingSubgroup(g);; e:=Elements(g);;
cl:=Filtered(ConjugacyClassesSubgroups(g),c->IsNilpotentGroup(Representative(c)) and not IsSubgroup(f,Representative(c)));;
Print(StructureDescription(g),"\n");
s:=DirectProduct(SymmetricGroup(4),CyclicGroup(IsPermGroup,2));;
iso:=IsomorphismGroups(g,s);;
Print("GENS ", List(GeneratorsOfGroup(g),x->Image(iso,x)),"\n");
for i in [17,12,13] do
 h:=Image(iso,Representative(cl[i]));;
 Print("H ",[i,StructureDescription(h),GeneratorsOfGroup(h),Elements(h)],"\n");
od;
Print("FIT ",Elements(Image(iso,f)),"\n");
Print("LABELS ",List([1..48],i->[i-1,Image(iso,e[i])]),"\n");
Print("PASS_20_122_DIAGNOSE\n");
QUIT;
