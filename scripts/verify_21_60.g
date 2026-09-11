# Independent actual-group, group-ring and rational representation controls.
SetAssertionLevel(2);
(function()
local G,a,b,z,t,irr,fs,A,basis,emb,aa,bb,e,c,f,rad,radbasis,L,C,CJ,
      k,rows,x,y,r,dims,expected,Id,AQ,BQ,AK,BK,QG,KG,allidems;
G:=SmallGroup(12,1);
a:=First(Elements(G),x->Order(x)=3);
b:=First(Elements(G),x->Order(x)=4 and a^x=a^-1);
Assert(0,b<>fail and Size(Group(a,b))=12);
z:=b^2;
Assert(0,z in Centre(G) and Order(z)=2);
Assert(0,IdGroup(G/Group(z))=[6,1]);
Assert(0,not IsNormal(G,Group(b)));
t:=CharacterTable(G); irr:=Irr(t); fs:=Indicator(t,2);
Assert(0,Number(irr,x->x[1]=2)=2 and Number(fs,x->x=-1)=1);

AQ:=[[0,-1],[1,-1]]; BQ:=[[1,-1],[0,-1]]; Id:=IdentityMat(2,Rationals);
Assert(0,AQ^3=Id and BQ^2=Id and BQ*AQ*BQ^-1=AQ^-1);
QG:=Group(AQ,BQ);
Assert(0,Size(QG)=6 and IdGroup(QG)=[6,1]);
AK:=AQ*One(GF(2)); BK:=BQ*One(GF(2)); KG:=Group(AK,BK);
Assert(0,Size(KG)=6 and IsIrreducibleMatrixGroup(KG));
Assert(0,RankMat(List([One(KG),AK,BK,AK*BK],Concatenation))=4);

A:=GroupRing(GF(2),G); emb:=Embedding(G,A);
aa:=Image(emb,a); bb:=Image(emb,b);
e:=One(A)+aa+aa^2; c:=One(A)+e;
f:=c*(aa+aa*bb+One(A)+bb^2);
Assert(0,e^2=e and f^2=f and e*f=Zero(A) and f*e=Zero(A));
rad:=RadicalOfAlgebra(A); radbasis:=BasisVectors(Basis(rad));
Assert(0,Dimension(rad)=7);
rows:=radbasis; dims:=[];
for k in [1..4] do
  if Length(rows)=0 then Add(dims,0);
  else
    r:=VectorSpace(GF(2),rows); Add(dims,Dimension(r));
    rows:=List(Cartesian(BasisVectors(Basis(r)),radbasis),p->p[1]*p[2]);
    rows:=Filtered(rows,x->x<>Zero(A));
  fi;
od;
Assert(0,dims=[7,2,1,0]);
basis:=BasisVectors(Basis(A));
for x in [e,f] do
  L:=VectorSpace(GF(2),List(basis,y->y*x));
  C:=VectorSpace(GF(2),List(basis,y->x*y*x));
  CJ:=VectorSpace(GF(2),List(radbasis,y->x*y*x));
  Assert(0,Dimension(L)=4 and Dimension(C)-Dimension(CJ)=1);
  if x=e then Assert(0,Dimension(C)=4 and Dimension(CJ)=3);
  else Assert(0,Dimension(C)=2 and Dimension(CJ)=1); fi;
  Print("PASS PIM_dimension=",Dimension(L)," corner_dimension=",Dimension(C),
        " corner_radical_dimension=",Dimension(CJ),"\n");
od;
allidems:=Filtered(Elements(A),x->x^2=x);
Assert(0,Length(allidems)=52);
Print("DONE group_id=",IdGroup(G)," algebra_dimension=12 radical_powers=",dims,
      " idempotents=",Length(allidems)," rational_simple_lifts=2\n");
end)();
QUIT;
