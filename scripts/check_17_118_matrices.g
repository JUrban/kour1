SetAssertionLevel(1);
Check17118Matrices:=function()
local basis,k,w,dim,gens,i,M,j,pos,Q,iso,P,pgens,D,Hs,cyc,bad,
 F,fgens,rels,T,h,U,ugens,link;
basis:=[[]];
for k in [1..3] do
 Append(basis,Filtered(Tuples([1..3],k),w->Length(Set(w))=k));
od;
dim:=Length(basis); Assert(1,dim=16); gens:=[];
for i in [1..3] do
 M:=IdentityMat(dim,GF(3));
 for j in [1..dim] do
  if not i in basis[j] then
   w:=Concatenation(basis[j],[i]); pos:=Position(basis,w);
   Assert(1,pos<>fail); M[j][pos]:=M[j][pos]+One(GF(3));
  fi;
 od;
 Add(gens,M);
od;
Q:=Group(gens); iso:=IsomorphismPcGroup(Q); P:=Image(iso);
pgens:=List(gens,x->Image(iso,x)); D:=DerivedSubgroup(P);
Assert(1,Size(P)=6561); Assert(1,Exponent(P)=9);
Assert(1,NilpotencyClassOfGroup(P)=3);
Assert(1,List(LowerCentralSeries(P),Size)=[6561,243,9,1]);
Assert(1,AbelianInvariants(P)=[3,3,3]);
Hs:=List([1..3],i->ClosureGroup(D,List(Filtered([1..3],j->j<>i),j->pgens[j])));
Assert(1,List(Hs,Size)=[2187,2187,2187]);
Assert(1,List(Hs,Exponent)=[3,3,3]);
cyc:=GroupHomomorphismByImages(P,P,pgens,[pgens[2],pgens[3],pgens[1]]);
Assert(1,cyc<>fail and IsBijective(cyc));
bad:=Number(Elements(P),x->x^3<>One(P)); Assert(1,bad=1944);
F:=FreeGroup("a","b","c"); fgens:=GeneratorsOfGroup(F);
rels:=List(fgens,x->x^3);
for i in [1..3] do
 for j in [1..3] do
  if i<>j then Add(rels,Comm(Comm(fgens[i],fgens[j]),fgens[i]));fi;
 od;
od;
T:=F/rels; h:=EpimorphismPGroup(T,3,3); U:=Image(h);
ugens:=List(GeneratorsOfGroup(T),x->Image(h,x));
link:=GroupHomomorphismByImages(U,P,ugens,pgens);
Assert(1,link<>fail and IsBijective(link));
Print("MATRIX dimension=16 order=",Size(P)," class=3 exponent=9 derived_order=",Size(D),"\n");
Print("MATRIX lower_orders=",List(LowerCentralSeries(P),Size)," noncubes=",bad,"\n");
Print("MATRIX hyperplane_orders=",List(Hs,Size)," exponents=",List(Hs,Exponent),"\n");
Print("MATRIX cycle_bijective=true pilot_isomorphic=true\n");
Print("PASS_17118_MATRICES\n");
end;
Check17118Matrices();
QUIT;
