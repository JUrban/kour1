# Independent matrix-inversion and actual class-product checks.
CONTROL_ONLY142:=true;;Read("scripts/search_14_2.g");;

Verify142:=function()
local groups,G,t,irr,cl,n,sizes,elements,positions,i,j,k,x,y,c,C,
      B,Binv,Bswap,M,d,pair,a,b,s,integral,products,valid,rejected,pairs,
      groupvalid,grouppairs,rhs,lhs,checked,groupnames;
groups:=[SymmetricGroup(3),DihedralGroup(IsPermGroup,8),
 QuaternionGroup(IsPermGroup,8),AlternatingGroup(4),SymmetricGroup(4),
 DihedralGroup(IsPermGroup,12),SL(2,3),AlternatingGroup(5),
 PSL(2,7),DirectProduct(SymmetricGroup(3),CyclicGroup(IsPermGroup,2))];
products:=0;valid:=0;rejected:=0;pairs:=0;checked:=0;
for G in groups do
 t:=CharacterTable(G);irr:=Irr(t);cl:=List(ConjugacyClasses(t),Elements);
 n:=Length(cl);sizes:=List(cl,Length);
 Assert(0,sizes=SizesConjugacyClasses(t));
 elements:=AsSortedList(G);positions:=List(elements,x->PositionProperty(cl,c->x in c));
 Assert(0,ForAll(positions,IsInt));
 C:=List([1..n],i->List([1..n],j->List([1..n],k->0)));
 for i in [1..n] do
  for j in [1..n] do
   for x in cl[i] do
    for y in cl[j] do
     k:=positions[Position(elements,x*y)];C[i][j][k]:=C[i][j][k]+1;
     products:=products+1;
    od;
   od;
   C[i][j]:=List([1..n],k->C[i][j][k]/sizes[k]);
   Assert(0,ForAll(C[i][j],IsInt));
  od;
 od;
 B:=List([1..n],j->List([1..n],i->sizes[j]*irr[i][j]/irr[i][1]));
 Binv:=B^-1;d:=Data142(t);groupvalid:=0;grouppairs:=0;
 for pair in Combinations(d.data,2) do
  a:=pair[1];b:=pair[2];grouppairs:=grouppairs+1;pairs:=pairs+1;
  Bswap:=List(B,ShallowCopy);
  for j in [1..n] do
   Bswap[j][a.index]:=B[j][b.index];Bswap[j][b.index]:=B[j][a.index];
  od;
  M:=Bswap*Binv;
  Assert(0,M*M=IdentityMat(n));
  integral:=ForAll(M,row->ForAll(row,IsInt));
  s:=Swap142(d,a,b);
  Assert(0,integral=(s<>fail));
  if not integral then rejected:=rejected+1;continue;fi;
  valid:=valid+1;groupvalid:=groupvalid+1;
  Assert(0,s.matrix=M);
  Assert(0,a.conductor=b.conductor);
  for i in [1..n] do
   for j in [1..n] do
    lhs:=Sum([1..n],a->Sum([1..n],b->M[i][a]*M[j][b]*C[a][b]));
    rhs:=C[i][j]*M;
    Assert(0,lhs=rhs);checked:=checked+1;
   od;
  od;
 od;
 Print("CONTROL order=",Size(G)," classes=",n," pairs=",grouppairs,
       " integral_swaps=",groupvalid,"\n");
od;
Assert(0,valid>0 and rejected>0);
Print("PASS groups=",Length(groups)," element_products=",products,
 " pairs=",pairs," integral_swaps=",valid," nonintegral_swaps=",rejected,
 " multiplicativity_checks=",checked,"\n");
end;
Verify142();
QUIT;
