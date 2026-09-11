# Reconstruct the relevant modular data from an actual permutation group.
# CTblLib Brauer rows are comparison targets, never input to the construction.
SetAssertionLevel(2);
SetInfoLevel(InfoWarning,0);
Read("scripts/group_4_55.g");
Verify455:=function()
local g,gs,F,t,lib,b,iso,reps,preg,lpreg,epi,fg,words,m,cf,x,tm,cf2,
      chars,mods,q,mats,phi,full,aligned,pos,positions,i,j,d,coords,
      row,actual,expected,orbs,rayvecs,v,psi,gal,counts,raw,rank,bas,out;
g:=Group455();
Assert(0,Size(g)=7560 and Size(Centre(g))=3 and IsPerfectGroup(g));
Assert(0,IsomorphismGroups(g/Centre(g),AlternatingGroup(7))<>fail);
gs:=GeneratorsOfGroup(g);F:=GF(25);
t:=CharacterTable(g);lib:=CharacterTable("3.A7");b:=lib mod 5;
iso:=TransformingPermutationsCharacterTables(t,lib);
Assert(0,iso<>fail);
for i in [1..Length(Irr(t))] do
  Assert(0,Permuted(Irr(t)[i],iso.columns)=Irr(lib)[i^iso.rows]);
od;
Print("ACTUAL_GROUP order=",Size(g)," degree=",LargestMovedPoint(g),
      " ordinary_table_equivalent=true\n");
reps:=List(ConjugacyClasses(t),Representative);
preg:=Filtered([1..Length(reps)],i->Order(reps[i]) mod 5<>0);
lpreg:=GetFusionMap(b,lib);
epi:=EpimorphismFromFreeGroup(g);fg:=GeneratorsOfGroup(Source(epi));
Assert(0,List(fg,w->Image(epi,w))=gs);
words:=List(reps{preg},r->PreImagesRepresentative(epi,r));
m:=GModuleByMats(List(gs,h->PermutationMat(h,45,F)),F);
cf:=MTX.CompositionFactors(m);
Print("PERMUTATION_FACTORS ",List(cf,MTX.Dimension),"\n");
x:=First(cf,h->MTX.Dimension(h)=15);
Assert(0,x<>fail and MTX.IsAbsolutelyIrreducible(x));
tm:=GModuleByMats(List(MTX.Generators(x),a->KroneckerProduct(a,a)),F);
cf2:=MTX.CompositionFactors(tm);
Print("TENSOR_FACTORS ",List(cf2,MTX.Dimension),"\n");
chars:=[];mods:=[];positions:=[];
for q in cf2 do
  Assert(0,MTX.IsAbsolutelyIrreducible(q));
  for j in [1,5] do
    mats:=List(MTX.Generators(q),a->List(a,r->List(r,z->z^j)));
    phi:=List(words,w->BrauerCharacterValue(MappedWord(w,fg,mats)));
    Assert(0,not fail in phi);
    full:=List(reps,r->0);full{preg}:=phi;
    aligned:=Permuted(full,iso.columns){lpreg};
    pos:=Position(Irr(b),aligned);
    Assert(0,pos<>fail);
    if not pos in positions then
      Add(positions,pos);Add(chars,aligned);Add(mods,mats);
    fi;
  od;
od;
Assert(0,Set(positions)=[9..20]);
Assert(0,RankMat(chars)=12);
Print("CONSTRUCTED_FAITHFUL_BRAUER ",positions," dimensions=",
      List(chars,r->r[1])," values_checked=",Length(chars)*Length(preg),"\n");
# Recompute each faithful ordinary reduction using only the constructed chars.
d:=DecompositionMatrix(b);counts:=0;
for i in [10..23] do
  coords:=SolutionMat(chars,Irr(lib)[i]{lpreg});
  Assert(0,coords<>fail and ForAll(coords,z->IsInt(z) and z>=0));
  actual:=List([1..20],j->0);actual{positions}:=coords;
  Assert(0,actual=d[i]);counts:=counts+1;
od;
Print("RECONSTRUCTED_DECOMPOSITION_ROWS ",counts,"\n");
orbs:=[[9,10],[11,12],[17,18],[19,20]];
Assert(0,ForAll(orbs,o->GaloisCyc(Irr(b)[o[1]],5)=Irr(b)[o[2]]));
expected:=[ [0,1,0,0], [0,0,0,1], [1,0,1,0], [1,0,0,1], [0,1,1,0] ];
for i in [1..5] do
  Assert(0,List(orbs,o->Sum(o,j->d[[10,16,18,20,22][i]][j]))=expected[i]);
od;
gal:=GaloisMat(Irr(lib));
Assert(0,Set(Orbit(Group(gal.generators),20))=[20,21,22,23]);
Assert(0,Set(Orbit(Group(gal.generators),10))=[10,11]);
Assert(0,Set(Orbit(Group(gal.generators),16))=[16,17]);
Assert(0,Set(Orbit(Group(gal.generators),18))=[18,19]);
rayvecs:=[[1,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,1]];
for v in rayvecs do
  row:=List([1..20],j->0);
  for i in [1..4] do row{orbs[i]}:=[v[i],v[i]];od;
  coords:=d*row;
  psi:=Sum([1..23],i->coords[i]*Irr(lib)[i]);
  Assert(0,ForAll(psi,IsRat));
  Assert(0,ForAll([1..23],i->coords[i]=0 or IsInt(168*coords[i]/Irr(lib)[i][1])));
  Print("RAY ",v," generic_degree=",psi[1]," ordinary_multiplicities=",coords,"\n");
od;
Assert(0,rayvecs[1]+rayvecs[4]=rayvecs[2]+rayvecs[3]);
PrintTo("results/4.55-modular-matrices.g","# Derived from PerfectGroup(7560,1), not Atlas matrix downloads.\n",
        "Positions455:=",positions,";\nModules455:=",mods,";\n");
bas:=Basis(F,[One(F),Z(25)]);
raw:=List(mods[Position(positions,9)],a->List(a,r->List(r,z->List(Coefficients(bas,z),Int))));
out:=OutputTextFile("results/4.55-three-dimensional-matrices.json",false);
SetPrintFormattingStatus(out,false);PrintTo(out,raw,"\n");CloseStream(out);
Print("FIELD_MINIMAL_POLYNOMIAL ",MinimalPolynomial(GF(5),Z(25)),"\n");
Print("PASS_4_55 actual_group=true ordinary_table=true faithful_simples=12 ",
      "brauer_values=",Length(chars)*Length(preg)," decomposition_rows=14 rays=4\n");
end;
Verify455();
QUIT;
