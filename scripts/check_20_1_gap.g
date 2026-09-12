# Bounded controls for the coprime product argument; classification is imported.
SetAssertionLevel(1);
Closure201:=function(G,n)
local os,o,Q,gens,g,p,i,D,rels,r;
os:=List(Orbits(G,[1..n]),Set);gens:=[];
# Upper bound: independent 2-closures on each transitive constituent.
for o in os do
  Q:=TwoClosure(Action(G,o));
  for g in GeneratorsOfGroup(Q) do
    p:=[1..n];for i in [1..Length(o)] do p[o[i]]:=o[i^g];od;
    Add(gens,PermList(p));
  od;
od;
if IsEmpty(gens) then D:=Group(());else D:=Group(gens);fi;
# Intersect stabilizers of every labelled orbital, including cross-orbit pairs.
rels:=List(Orbits(G,Cartesian([1..n],[1..n]),OnTuples),Set);
for r in rels do
  if not ForAll(GeneratorsOfGroup(D),g->OnSetsTuples(r,g)=r) then
    D:=Stabilizer(D,r,OnSetsTuples);
  fi;
od;
Assert(0,IsSubgroup(D,G));
return D;
end;

Control201:=function(A,B,label,out)
local G,ga,gb,gens,cls,hs,choices,pair,k,indices,degree,perms,offset,h,act,
      i,j,x,hom,P,AP,BP,ao,bo,aq,bq,ac,bc,C,cs,a,b,meet,ind,row,count,
      cimages,aimages,bimages,amap,bmap,atoms;
G:=DirectProduct(A,B); ga:=Image(Embedding(G,1));gb:=Image(Embedding(G,2));
gens:=GeneratorsOfGroup(G);
cls:=ConjugacyClassesSubgroups(G);hs:=List(cls,Representative);
# Every single orbit, every pair, and selected triples, including repeats.
choices:=List([1..Length(hs)],i->[i]);
Append(choices,Combinations([1..Length(hs)],2));
Append(choices,List([1..Length(hs)],i->[i,i]));
Append(choices,Filtered(Combinations([1..Length(hs)],3),x->Sum(x,i->Index(G,hs[i]))<=30));
count:=0;
for indices in choices do
  degree:=Sum(indices,i->Index(G,hs[i]));
  if degree>60 then continue;fi;
  perms:=List(gens,g->[]);offset:=0;
  for k in indices do
    h:=hs[k];act:=ActionHomomorphism(G,RightCosets(G,h),OnRight);
    for i in [1..Length(gens)] do
      x:=Image(act,gens[i]);
      Append(perms[i],List([1..Index(G,h)],j->j^x+offset));
    od;
    offset:=offset+Index(G,h);
  od;
  perms:=List(perms,PermList);P:=Group(perms);
  if Size(P)<>Size(G) then continue;fi;
  hom:=GroupHomomorphismByImages(G,P,gens,perms);
  Assert(0,hom<>fail and Size(Kernel(hom))=1);
  AP:=Image(hom,ga);BP:=Image(hom,gb);
  atoms:=[1..degree];
  ao:=List(Orbits(AP,atoms),Set);bo:=List(Orbits(BP,atoms),Set);
  Assert(0,ForAll(ao,a->ForAll(bo,b->Length(Intersection(a,b))<=1)));
  # Action on the other factor's orbits.
  aq:=Action(AP,bo,OnSets);bq:=Action(BP,ao,OnSets);
  Assert(0,Size(aq)=Size(A) and Size(bq)=Size(B));
  ac:=Closure201(aq,Length(bo));bc:=Closure201(bq,Length(ao));C:=Closure201(P,degree);
  for x in GeneratorsOfGroup(C) do
    a:=PermList(List(bo,o->Position(bo,OnSets(o,x))));
    b:=PermList(List(ao,o->Position(ao,OnSets(o,x))));
    Assert(0,a in ac and b in bc);
  od;
  Assert(0,Size(C)<=Size(ac)*Size(bc));
  if Size(ac)=Size(A) and Size(bc)=Size(B) then Assert(0,C=P);fi;
  cimages:=List(Elements(C),x->List(atoms,i->i^x));
  aimages:=List(GeneratorsOfGroup(AP),x->List(atoms,i->i^x));
  bimages:=List(GeneratorsOfGroup(BP),x->List(atoms,i->i^x));
  row:=[label,indices,degree,Size(P),Size(C),Size(ac),Size(bc),
        List(Elements(P),x->List(atoms,i->i^x)),cimages,aimages,bimages];
  AppendTo(out,row,"\n");
  count:=count+1;
od;
Print("PRODUCT_CONTROL ",label," cases=",count,"\n");
return count;
end;

Main201:=function()
local out,count,A,B,V,cls,hs,gens,perms,offset,h,act,i,x,P,deg,t;
out:=OutputTextFile("results/20.1-actions.grows",false);
SetPrintFormattingStatus(out,false);
count:=0;
count:=count+Control201(CyclicGroup(IsPermGroup,2),CyclicGroup(IsPermGroup,3),"C2_C3",out);
count:=count+Control201(QuaternionGroup(IsPermGroup,8),CyclicGroup(IsPermGroup,3),"Q8_C3",out);
count:=count+Control201(SymmetricGroup(3),CyclicGroup(IsPermGroup,5),"S3_C5",out);
count:=count+Control201(AlternatingGroup(4),CyclicGroup(IsPermGroup,5),"A4_C5",out);
CloseStream(out);
# Shared-prime mutation: V4 on its three coset actions of degree two.
V:=ElementaryAbelianGroup(IsPermGroup,4);gens:=GeneratorsOfGroup(V);
hs:=Filtered(List(ConjugacyClassesSubgroups(V),Representative),h->Size(h)=2);
perms:=List(gens,g->[]);offset:=0;
for h in hs do
  act:=ActionHomomorphism(V,RightCosets(V,h),OnRight);
  for i in [1..Length(gens)] do
    x:=Image(act,gens[i]);Append(perms[i],List([1..2],j->j^x+offset));
  od;
  offset:=offset+2;
od;
P:=Group(List(perms,PermList));Assert(0,Size(P)=4 and Size(Closure201(P,6))=8);
Print("SHARED_PRIME_MUTATION degree=6 order=4 closure=8\n");
t:=CharacterTable("J1");Assert(0,Size(t)=175560 and Gcd(Size(t),13)=1);
Print("J1_TABLE_ORDER ",Size(t)," PRODUCT_ORDER ",13*Size(t),"\n");
Print("PASS_201_GAP cases=",count,"\n");
end;
Main201();
QUIT;
