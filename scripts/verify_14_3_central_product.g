# A true limitation of the two necessary tests, followed by a field obstruction.
LoadPackage("smallgrp");;
SizeScreen([1000000,1000000]);;
(function()
 local r,s,K,J,t,zK,zJ,W,N,q,G,z,x,ct,cl,irr,zi,real,roots,
       centralSquares,faithful,fieldRows,c,f,els,fs,rootSizes;
 r:=(1,2,3,4,5,6,7,8);
 s:=PermList(List([0..7],i->(3*i mod 8)+1));
 K:=Group(r,s); zK:=r^4;
 Assert(0,Size(K)=16 and r^s=r^3 and Centre(K)=Group(zK));
 J:=SmallGroup(12,1); t:=First(Elements(J),a->Order(a)=4); zJ:=t^2;
 Assert(0,Size(Centre(J))=2 and zJ in Centre(J));
 W:=DirectProduct(K,J);
 N:=Group(Image(Embedding(W,1),zK)*Image(Embedding(W,2),zJ));
 q:=NaturalHomomorphismByNormalSubgroup(W,N); G:=Image(q);
 z:=Image(q,Image(Embedding(W,1),zK));
 x:=Image(q,Image(Embedding(W,2),t));
 Assert(0,Size(G)=96 and Centre(G)=Group(z));
 centralSquares:=Set(List(Elements(Centre(G)),a->a^2));
 Assert(0,not z in centralSquares and x^2=z);
 Assert(0,Index(G,Centralizer(G,x))=3);
 ct:=CharacterTable(G); cl:=ConjugacyClasses(ct); irr:=Irr(ct);
 zi:=PositionProperty(cl,c->z in c);
 real:=Filtered(irr,c->ForAll(c,v->ComplexConjugate(v)=v));
 Assert(0,ForAll(real,c->c[zi]=c[1]));
 els:=Elements(G);
 fs:=List(irr,c->Sum(els,a->c[PositionProperty(cl,d->a^2 in d)])/Size(G));
 Assert(0,ForAll([1..Length(irr)],i->(irr[i] in real)=(fs[i]<>0)));
 roots:=Filtered(els,a->a^2=z and Index(G,Centralizer(G,a)) mod 2=1);
 rootSizes:=Collected(List(roots,a->Index(G,Centralizer(G,a))));
 Assert(0,not IsEmpty(roots));
 faithful:=Filtered(irr,c->c[zi]=-c[1]);
 fieldRows:=[];
 for c in faithful do
   f:=Field(Rationals,ValuesOfClassFunction(c));
   Print("FAITHFUL_Z degree=",c[1]," field=",f," values=",Set(c),"\n");
   if f=Field(Rationals,[E(8)+E(8)^3]) then Add(fieldRows,c); fi;
 od;
 Assert(0,Length(fieldRows)>0 and ForAll(fieldRows,c->c[1]=4));
 Print("PASS_CENTRAL_PRODUCT id=",IdGroup(G)," order=",Size(G),
       " centre_order=",Size(Centre(G))," real_characters=",Length(real),
       " irreducibles=",Length(irr)," indicator_checks=",Length(fs),
       " faithful_z_characters=",Length(faithful)," imaginary_quadratic_rows=",Length(fieldRows),
       " odd_root_elements=",Length(roots)," root_class_sizes=",rootSizes,"\n");
end)();
QUIT;
