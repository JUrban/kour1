# Reconstruct the small PSL2(11) input and check the alternative's characters.
# Library decomposition data remain an imported dependency.
SetAssertionLevel(2);
LoadPackage("ctbllib");;
field455v2 := GF(11);;
sl455v2 := SL(2,11);;
lines455v2 := Orbit(sl455v2,[1,0]*One(field455v2),OnLines);;
hom455v2 := ActionHomomorphism(sl455v2,lines455v2,OnLines);;
g455v2 := Image(hom455v2);;
r455v2 := Image(hom455v2,[[0,-1],[1,5]]*One(field455v2));;
s455v2 := Image(hom455v2,[[2,2],[3,9]]*One(field455v2));;
a455v2 := Image(hom455v2,[[0,-1],[1,0]]*One(field455v2));;
b455v2 := Image(hom455v2,[[0,5],[2,1]]*One(field455v2));;
h455v2 := Group(r455v2,s455v2);;
k455v2 := Group(a455v2,b455v2);;
Assert(0,Size(g455v2)=660 and Size(h455v2)=12 and Size(k455v2)=60);
Assert(0,Order(r455v2)=6 and Order(s455v2)=2 and r455v2^s455v2=r455v2^-1);
Assert(0,Order(a455v2)=2 and Order(b455v2)=3 and Order(a455v2*b455v2)=5);
th455v2 := CharacterTable(h455v2);;
reps455v2 := List(ConjugacyClasses(h455v2),Representative);;
epsilon455v2 := function(z)
  if z in Group(r455v2) then return 1; else return -1; fi;
end;;
eps455v2 := ClassFunction(th455v2,List(reps455v2,epsilon455v2));;
lambda455v2 := function(z)
  local i,j;
  for i in [0..5] do for j in [0..1] do
    if z=r455v2^i*s455v2^j then return (-1)^i; fi;
  od; od;
  Error("element outside dihedral subgroup");
end;;
lin455v2 := ClassFunction(th455v2,List(reps455v2,lambda455v2));;
tk455v2 := CharacterTable(k455v2);;
omega455v2 := ConjugacyClassSubgroups(k455v2,SylowSubgroup(k455v2,5));;
w455v2 := PermutationCharacter(k455v2,AsList(omega455v2),OnPoints)-TrivialCharacter(tk455v2);;
tg455v2 := CharacterTable(g455v2);;
irr455v2 := Irr(tg455v2);;
st455v2 := First(irr455v2,c->c[1]=11);;
B455v2 := InducedClassFunction(eps455v2,tg455v2)-st455v2;;
C455v2 := InducedClassFunction(w455v2,tg455v2)-st455v2;;
D455v2 := InducedClassFunction(lin455v2,tg455v2)-st455v2;;
A455v2 := B455v2+C455v2-D455v2;;
ord455v2 := OrdersClassRepresentatives(tg455v2);;
two455v2 := Position(ord455v2,2);;
Assert(0,List([A455v2,B455v2,C455v2,D455v2],c->c[1])=[44,44,44,44]);
Assert(0,List([A455v2,B455v2,C455v2],c->c[two455v2])=[0,-4,4]);
support455v2 := function(c)
 return SortedList(List(Filtered(irr455v2,i->ScalarProduct(tg455v2,c,i)<>0),
  i->[i[1],i[two455v2],ScalarProduct(tg455v2,c,i)]));
end;;
Assert(0,support455v2(B455v2)=[[10,-2,2],[12,0,1],[12,0,1]]);
Assert(0,support455v2(C455v2)=[[5,1,1],[5,1,1],[10,2,1],[12,0,1],[12,0,1]]);
Assert(0,support455v2(D455v2)=[[10,-2,1],[10,2,1],[12,0,1],[12,0,1]]);
Assert(0,ForAll([A455v2,B455v2,C455v2,D455v2],c->ForAll(irr455v2,
 i->IsInt(ScalarProduct(tg455v2,c,i)) and ScalarProduct(tg455v2,c,i)>=0)));
lib455v2 := CharacterTable("L2(11)");;
br455v2 := lib455v2 mod 11;;
Assert(0,List(Irr(lib455v2),c->c[1])=[1,5,5,10,10,11,12,12]);
Assert(0,List(Irr(br455v2),c->c[1])=[1,3,5,7,9,11]);
decomp455v2 := DecompositionMatrix(br455v2);;
expected455v2 := [[1,0,0,0,0,0],[0,0,1,0,0,0],[0,0,1,0,0,0],
 [0,1,0,1,0,0],[1,0,0,0,1,0],[0,0,0,0,0,1],[0,0,1,1,0,0],[0,1,0,0,1,0]];;
# Swapping the two degree-12 ordinary characters swaps the four-ray notation.
Assert(0,SortedList(decomp455v2)=SortedList(expected455v2));
pims455v2 := TransposedMat(decomp455v2)*List(Irr(lib455v2),ValuesOfClassFunction);;
Assert(0,List(pims455v2,c->c[1])=[11,22,22,22,22,11]);
five455v2 := Position(OrdersClassRepresentatives(lib455v2),5);;
Assert(0,ForAll([2..5],i->not IsRat(pims455v2[i][five455v2])));
Print("PASS 4.55: actual PSL2(11) and two subgroups; three induced projectives; ranks 44; involution traces 0,-4,4; library decomposition data and irrational individual PIM traces.\n");
Print("GAP ",GAPInfo.Version,"; CTblLib ",PackageInfo("ctbllib")[1].Version,"\n");
QUIT_GAP(0);
