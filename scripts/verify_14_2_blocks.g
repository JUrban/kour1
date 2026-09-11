# Full spectral matrix inversion controls, including all degree-preserving maps.
BLOCK_CONTROL_ONLY142:=true;;Read("scripts/search_14_2_blocks.g");;

VerifyBlocks142:=function()
local G,t,d,irr,sizes,B,Binv,block,cond,perm,Bp,M,i,j,s,
      groups,tested,valid,invalid,degreechanged,gtested,gvalid;
groups:=[WreathProduct(SymmetricGroup(3),CyclicGroup(IsPermGroup,2)),
         SymmetricGroup(4),DirectProduct(SymmetricGroup(3),CyclicGroup(4))];
tested:=0;valid:=0;invalid:=0;degreechanged:=0;
for G in groups do
 t:=CharacterTable(G);d:=Data142(t);irr:=Irr(t);sizes:=SizesConjugacyClasses(t);
 B:=List([1..d.classes],j->List([1..d.classes],i->sizes[j]*irr[i][j]/irr[i][1]));
 Binv:=B^-1;gtested:=0;gvalid:=0;
 for cond in Set(List(d.data,x->x.conductor)) do
  block:=Filtered(d.data,x->x.conductor=cond);
  if Length(block)<2 or Length(block)>6 then continue;fi;
  for perm in SymmetricGroup(Length(block)) do
   tested:=tested+1;gtested:=gtested+1;Bp:=List(B,ShallowCopy);
   for i in [1..Length(block)] do
    for j in [1..d.classes] do Bp[j][block[i^perm].index]:=B[j][block[i].index];od;
   od;
   M:=Bp*Binv;s:=Perm142(d,block,perm);
   Assert(0,(s<>fail)=ForAll(M,row->ForAll(row,IsInt)));
   if s=fail then invalid:=invalid+1;continue;fi;
   Assert(0,s.matrix=M);valid:=valid+1;gvalid:=gvalid+1;
   if ForAny([1..Length(block)],i->block[i].degree<>block[i^perm].degree)
    then degreechanged:=degreechanged+1;fi;
  od;
 od;
 Print("BLOCK_CONTROL order=",Size(G)," classes=",d.classes,
  " tested=",gtested," integral=",gvalid,"\n");
od;
Assert(0,valid>0 and invalid>0);
Print("PASS_BLOCK_CONTROLS groups=",Length(groups)," tested=",tested,
 " integral=",valid," nonintegral=",invalid," degree_changed=",degreechanged,"\n");
end;
VerifyBlocks142();QUIT;
