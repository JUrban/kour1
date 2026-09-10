LoadPackage("smallgrp");;
SizeScreen([100000,100000]);;
Check:=function(test,message)
  if not test then Error(message); fi;
end;;

# The group E semidirect A4, E the even vectors in F2^4, acting affinely on E.
vectors:=Filtered(Tuples([0,1],4),v->Sum(v) mod 2=0);;
TranslateVector21168:=v->PermList(List(vectors,u->Position(vectors,List([1..4],j->(u[j]+v[j]) mod 2))));;
CoordinatePerm:=p->PermList(List(vectors,u->Position(vectors,Permuted(u,p))));;
egens:=List([[1,0,0,1],[0,1,0,1],[0,0,1,1]],TranslateVector21168);;
ag1:=CoordinatePerm((1,2)(3,4));;
ag2:=CoordinatePerm((2,3,4));;
K:=Group(Concatenation(egens,[ag1,ag2]));;
E2:=Group(egens);;
A4:=Group(ag1,ag2);;
x:=CoordinatePerm((1,2)(3,4))*TranslateVector21168([1,0,1,0]);;
y:=CoordinatePerm((1,3)(2,4))*TranslateVector21168([1,0,0,1]);;
r:=ag2;;
H:=Group(x,y,r);;
Q:=Group(x,y);;
Check(Size(K)=96 and Size(H)=24 and Size(Q)=8,"wrong orders");;
Check(IsomorphismGroups(Q,QuaternionGroup(8))<>fail,"Q is not quaternion");;
Check(IsomorphismGroups(H,SL(2,3))<>fail,"H is not SL2(3)");;
Check(IsAbelian(E2) and IsNormal(K,E2) and Size(E2)=8,"E2 structure");;
Check(Size(A4)=12 and Size(Intersection(E2,A4))=1,"K does not split");;
Check(Size(DerivedSubgroup(H))=8,"H abelianization");;
Print("BASE K_id=",IdGroup(K)," H_id=",IdGroup(H)," H_abelianization=",AbelianInvariants(H),"\n");

# The action on four H-cosets, with stabilizer exactly H.
cosets:=RightCosets(K,H);;
act:=ActionHomomorphism(K,cosets,OnRight);;
origin:=PositionProperty(cosets,c->One(K) in c);;
Check(PreImage(act,Stabilizer(Image(act),origin))=H,"point stabilizer");;

# Faithful permutation realization of B semidirect K on 12+8 points.
# B is the augmentation subspace of F3^4, with its four coordinates cyclic.
basegens:=[(1,2,3)*(10,11,12)^-1,(4,5,6)*(10,11,12)^-1,(7,8,9)*(10,11,12)^-1];;
LiftK:=function(k)
  local p,images,j,a;
  p:=Image(act,k); images:=[];
  for j in [1..4] do
    for a in [1..3] do Add(images,3*(j^p-1)+a); od;
  od;
  Append(images,List([1..8],i->12+i^k));
  return PermList(images);
end;;
ktopgens:=List(GeneratorsOfGroup(K),LiftK);;
B:=Group(basegens);;
G:=Group(Concatenation(basegens,ktopgens));;
Ktop:=Group(ktopgens);;
Htop:=Group(List(GeneratorsOfGroup(H),LiftK));;
I:=Group(Concatenation(basegens,GeneratorsOfGroup(Htop)));;
Check(Size(G)=2592 and Size(B)=27 and IsElementaryAbelian(B),"G or B order");;
Check(IsNormal(G,B) and Size(Intersection(B,Ktop))=1,"G split");;
Check(Size(I)=648 and Index(G,I)=4,"inertia group");;
pi:=GroupHomomorphismByImages(G,K,Concatenation(basegens,ktopgens),Concatenation(List(basegens,b->One(K)),GeneratorsOfGroup(K)));;
Check(pi<>fail and Kernel(pi)=B,"quotient map");;

# Extend the selected coordinate character to B semidirect H.
C:=Group((1,2,3));;
c:=GeneratorsOfGroup(C)[1];;
exponents:=[0,0,0];;
if origin=4 then exponents:=[2,2,2]; else exponents[origin]:=1; fi;
lambdaMap:=GroupHomomorphismByImages(I,C,Concatenation(basegens,GeneratorsOfGroup(Htop)),Concatenation(List(exponents,e->c^e),List(GeneratorsOfGroup(Htop),h->One(C))));;
Check(lambdaMap<>fail,"coordinate character did not extend");;
hclasses:=ConjugacyClasses(H);;
rho:=First(Irr(H),chi->chi[1]=2);;
psi:=ClassFunction(I,List(ConjugacyClasses(I),function(cl)
  local g,e,pos;
  g:=Representative(cl);
  e:=Position([One(C),c,c^2],Image(lambdaMap,g))-1;
  pos:=PositionProperty(hclasses,hcl->Image(pi,g) in hcl);
  return E(3)^e*rho[pos];
end));;
Check(ScalarProduct(psi,psi)=1,"inertia character reducible");;
chi:=InducedClassFunction(psi,G);;
Check(chi[1]=8 and ScalarProduct(chi,chi)=1,"induced character not irreducible degree8");;
Print("CHARACTER degree=",chi[1]," norm=",ScalarProduct(chi,chi)," values=",ValuesOfClassFunction(chi),"\n");
Print("MONOMIAL_TEST ",TestMonomial(chi),"\n");
Check(not IsMonomial(chi),"unexpected monomial character");;
Print("PASS G_order=",Size(G)," B_order=",Size(B)," I_order=",Size(I)," irreducible_degree=8 nonmonomial=true\n");
QUIT;
