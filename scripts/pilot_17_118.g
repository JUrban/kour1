SetAssertionLevel(1);
Pilot17118:=function()
local F,gens,rels,i,j,T,h,G,ims,D,maps,Hs,a,cyc,bad,rank;
F:=FreeGroup("a","b","c"); gens:=GeneratorsOfGroup(F);
rels:=List(gens,x->x^3);
for i in [1..3] do
 for j in [1..3] do
  if i<>j then Add(rels,Comm(Comm(gens[i],gens[j]),gens[i]));fi;
 od;
od;
T:=F/rels; h:=EpimorphismPGroup(T,3,3); G:=Image(h);
ims:=List(GeneratorsOfGroup(T),x->Image(h,x)); D:=DerivedSubgroup(G);
Print("PILOT order=",Size(G)," class=",NilpotencyClassOfGroup(G),
 " exponent=",Exponent(G)," derived_order=",Size(D)," abelian=",AbelianInvariants(G),"\n");
Print("PILOT abc_order=",Order(Product(ims))," lower_orders=",List(LowerCentralSeries(G),Size),"\n");
Hs:=List([1..3],i->ClosureGroup(D,Filtered(ims,x->x<>ims[i])));
Print("PILOT hyperplane_orders=",List(Hs,Size)," exponents=",List(Hs,Exponent),"\n");
cyc:=GroupHomomorphismByImages(G,G,ims,[ims[2],ims[3],ims[1]]);
Print("PILOT cycle_valid=",cyc<>fail,"\n");
if cyc<>fail then Print("PILOT cycle_bijective=",IsBijective(cyc),"\n");fi;
bad:=Number(Elements(G),x->x^3<>One(G));
Print("PILOT noncubes=",bad," root_count=",Size(G)-bad,"\n");
Print("PASS_17118_PILOT\n");
end;
Pilot17118();
QUIT;
