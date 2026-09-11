# Exact degree-changing permutations within one rational conductor block.
CONTROL_ONLY142:=true;;Read("scripts/search_14_2.g");;

Perm142:=function(d,block,perm)
local changed,i,j,k,delta,M,monomial;
changed:=Filtered([1..Length(block)],i->i^perm<>i);
# The identity class coefficient is a cheap necessary integrality test.
for j in [1..d.classes] do
 delta:=Sum(changed,i->block[i].lambda[j]*
        (block[i^perm].degree^2-block[i].degree^2));
 if delta mod d.order<>0 then return fail;fi;
od;
M:=IdentityMat(d.classes);
for j in [1..d.classes] do
 for k in [1..d.classes] do
  delta:=Sum(changed,i->block[i].lambda[j]*
      (block[i^perm].numerator[k]-block[i].numerator[k]));
  if delta mod d.order<>0 then return fail;fi;
  M[j][k]:=M[j][k]+delta/d.order;
 od;
od;
Assert(0,ForAll(M,row->ForAll(row,IsInt)));
Assert(0,M^Order(perm)=IdentityMat(d.classes));
Assert(0,AbsInt(DeterminantMat(M))=1);
monomial:=ForAll(M,row->Number(row,x->x<>0)=1 and
                         ForAll(row,x->x in [-1,0,1]));
return rec(matrix:=M,monomial:=monomial);
end;

RunBlocks142:=function()
local names,index,name,t,d,cond,block,perm,tested,integral,hits,
 tableblocks,tabletested,tableintegral,tablehits,blocks,eligible,s;
names:=AllCharacterTableNames();blocks:=0;tested:=0;integral:=0;hits:=0;
Print("START_BLOCKS tables=",Length(names)," max_classes=100 max_block=6 gap=",
 GAPInfo.Version,"\n");
for index in [1..Length(names)] do
 name:=names[index];t:=CharacterTable(name);d:=Data142(t);
 tableblocks:=0;tabletested:=0;tableintegral:=0;tablehits:=0;
 eligible:=d.classes<=100;
 if eligible then
  for cond in Set(List(d.data,x->x.conductor)) do
   block:=Filtered(d.data,x->x.conductor=cond);
   if Length(block)<2 or Length(block)>6 or
      Length(Set(List(block,x->x.degree)))=1 then continue;fi;
   tableblocks:=tableblocks+1;
   for perm in SymmetricGroup(Length(block)) do
    if ForAll([1..Length(block)],i->block[i].degree=block[i^perm].degree)
     then continue;fi;
    tabletested:=tabletested+1;s:=Perm142(d,block,perm);
    if s=fail then continue;fi;
    tableintegral:=tableintegral+1;
    if not s.monomial then tablehits:=tablehits+1;fi;
    Print("BLOCK_MAP name=",name," conductor=",cond,
      " indices=",List(block,x->x.index)," degrees=",List(block,x->x.degree),
      " permutation=",perm," monomial=",s.monomial," matrix=",s.matrix,"\n");
   od;
  od;
 fi;
 blocks:=blocks+tableblocks;tested:=tested+tabletested;
 integral:=integral+tableintegral;hits:=hits+tablehits;
 Print("BLOCK_TABLE index=",index," name=",name," classes=",d.classes,
  " eligible=",eligible," blocks=",tableblocks," tested=",tabletested,
  " integral=",tableintegral," nonmonomial=",tablehits,"\n");
od;
Print("DONE_BLOCKS tables=",Length(names)," blocks=",blocks," tested=",tested,
 " integral=",integral," nonmonomial=",hits,"\n");
end;

if not IsBound(BLOCK_CONTROL_ONLY142) then RunBlocks142();QUIT_GAP(0);fi;
