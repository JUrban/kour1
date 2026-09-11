SizeScreen([1000000,1000000]);;
(function()
 local Check,rows,total,pcases,n,id,G,entry,F,o,z,i,j,k,t,a,b,p,q,lam,
       U,V,d,one,c,theta,vfun,addchecks,matrows,els,P,y,u,w,cen,pi,S,
       abar,gbar,c0,r,cbar,L,R,liftrows,g,gg;
 Check:=function(G,name)
  local els,orders,prime,stars,x,y,p,ps,P,res,gen,sub,good,primarygood,
        a,b,oa,ob,checked,wit,meta,lc,hyps;
  els:=Elements(G); orders:=List(els,Order);
  prime:=List(orders,n->Set(FactorsInt(n)));
  stars:=[One(G)]; checked:=0;
  for x in [1..Length(els)] do
   if Length(prime[x])<>1 then continue; fi;
   for y in [1..Length(els)] do
    if Length(prime[y])=1 and prime[x]<>prime[y] then
     AddSet(stars,Comm(els[x],els[y])); checked:=checked+1;
    fi;
   od;
  od;
  hyps:=[];
  for p in Set(FactorsInt(Size(G))) do
   P:=SylowSubgroup(G,p);
   res:=Group(Filtered(els,x->Order(x) mod p<>0));
   sub:=Intersection(P,res);
   gen:=Group(Filtered(stars,x->x in P));
   Assert(0,gen=sub);
   if IsPerfectGroup(G) then Assert(0,gen=P); fi;
   Add(hyps,[p,Size(P),Size(sub),Size(gen)]);
  od;
  good:=true; primarygood:=true; wit:=[];
  for a in stars do for b in stars do
   oa:=Order(a); ob:=Order(b);
   if Gcd(oa,ob)=1 and Order(a*b)<oa*ob then
    good:=false;
    if Length(Set(FactorsInt(oa)))=1 and Length(Set(FactorsInt(ob)))=1 then
     primarygood:=false;
    fi;
    if wit=[] then wit:=[oa,ob,Order(a*b)]; fi;
   fi;
  od; od;
  lc:=LowerCentralSeriesOfGroup(G); meta:=IsNilpotentGroup(Last(lc));
  Assert(0,good=meta and primarygood=meta);
  Assert(0,not good or IsSolvableGroup(G));
  return [name,Size(G),Length(stars),checked,good,primarygood,hyps,wit];
 end;
 rows:=[];
 for n in [1..64] do
  for id in [1..NumberSmallGroups(n)] do
   Add(rows,Check(SmallGroup(n,id),Concatenation("small_",String(n),"_",String(id))));
  od;
  Print("ORDER_DONE ",n," ",NumberSmallGroups(n),"\n");
 od;
 for entry in [["S3",SymmetricGroup(3)],["A4",AlternatingGroup(4)],
               ["S4",SymmetricGroup(4)],["A5",AlternatingGroup(5)],
               ["SL2_5",SL(2,5)],["PSL2_7",PSL(2,7)],
               ["A6",AlternatingGroup(6)]] do
  Add(rows,Check(entry[2],entry[1]));
 od;
 Print("PASS_GROUPS ",rows,"\n");

 matrows:=[];
 for q in [3,5,7,9,11,13,17,19,23,25,27,31,49,81,125] do
  F:=GF(q); o:=One(F); z:=Zero(F); one:=IdentityMat(2,F);
  a:=fail; b:=fail;
  for i in F do
   for j in F do
    if i^2+j^2=-o then a:=i; b:=j; break; fi;
   od;
   if a<>fail then break; fi;
  od;
  Assert(0,a<>fail);
  i:=[[z,o],[-o,z]]; j:=[[a,b],[b,-a]]; k:=i*j;
  t:=(-one+i+j+k)/(2*o);
  Assert(0,i^2=-one and j^2=-one and k^2=-one and i*j=-j*i);
  Assert(0,Size(Group(i,j))=8 and DeterminantMat(t)=o and Order(t)=3);
  Assert(0,i^t=j and j^t=k and k^t=i and Size(Group(i,j,t))=24);
  Add(matrows,["odd_PSL2",q,8,24]);
 od;
 for q in [4,8,16,32,64] do
  F:=GF(q); o:=One(F); z:=Zero(F);
  p:=Set(FactorsInt(q-1))[1]; lam:=Z(q)^((q-1)/p);
  d:=DiagonalMat([lam,lam^-1]);
  V:=List(F,c->[[o,c],[z,o]]);
  Assert(0,Order(d)=p);
  for c in F do
   Assert(0,[[o,c],[z,o]]^d=[[o,c*lam^-2],[z,o]]);
  od;
  Assert(0,V[2]^d<>V[2] or V[1]^d<>V[1]);
  Add(matrows,["even_PSL2",q,p,Size(Group(V))]);
 od;
 F:=GF(3); o:=One(F); z:=Zero(F);
 V:=Group(DiagonalMat([o,-o,-o]),DiagonalMat([-o,o,-o]));
 d:=[[z,o,z],[z,z,o],[o,z,z]];
 Assert(0,Size(V)=4 and Order(d)=3 and Size(Group(Concatenation(GeneratorsOfGroup(V),[d])))=12);
 Assert(0,ForAll(GeneratorsOfGroup(V),v->v^d in V) and not d in Centralizer(GL(3,3),V));
 Add(matrows,["PSL3",3,4,12]);

 addchecks:=0;
 for q in [8,32,128] do
  F:=GF(q); o:=One(F); z:=Zero(F); theta:=2^((LogInt(q,2)+1)/2);
  vfun:=b->[[o,z,z,z],[z,o,z,z],[b,z,o,z],[b^theta,b,z,o]];
  p:=Set(FactorsInt(q-1))[1]; lam:=Z(q)^((q-1)/p);
  d:=DiagonalMat([lam^(theta+1),lam,lam^-1,lam^(-theta-1)]);
  Assert(0,Gcd(theta+2,q-1)=1 and Order(d)=p);
  for b in F do
   Assert(0,vfun(b)^d=vfun(lam^(theta+2)*b));
   Assert(0,b=z or vfun(b)^d<>vfun(b));
   for c in F do Assert(0,vfun(b)*vfun(c)=vfun(b+c)); addchecks:=addchecks+1; od;
  od;
  V:=Group(List(F,vfun)); Assert(0,Size(V)=q and IsElementaryAbelian(V));
  if q=8 then
   U:=[[o,z,z,z],[o,o,z,z],[o,o,o,z],[o,z,o,o]];
   t:=[[z,z,z,o],[z,z,o,z],[z,o,z,z],[o,z,z,z]];
   G:=Group(U,d,t); Assert(0,Size(G)=q^2*(q^2+1)*(q-1));
   Assert(0,ForAll(GeneratorsOfGroup(V),x->x in G));
  fi;
  Add(matrows,["Suzuki",q,p,Size(V)]);
 od;
 Print("PASS_MATRICES ",matrows," additive_checks=",addchecks,"\n");

 liftrows:=[];
 for q in [5,7,9] do
  G:=SL(2,q); cen:=Centre(G); pi:=NaturalHomomorphismByNormalSubgroup(G,cen); S:=Image(pi);
  # Construct the projective Klein four via a quaternion Sylow (q=5,7,9).
  P:=SylowSubgroup(G,2);
  # For q=7,9 the Sylow is larger: select an order-eight quaternion subgroup
  # using the already proved explicit matrix construction, then normalize it.
  F:=GF(q); o:=One(F); z:=Zero(F); one:=IdentityMat(2,F);
  a:=fail;
  for i in F do
   for j in F do if i^2+j^2=-o then a:=i; b:=j; break; fi; od;
   if a<>fail then break; fi;
  od;
  i:=[[z,o],[-o,z]]; j:=[[a,b],[b,-a]]; k:=i*j;
  y:=(-one+i+j+k)/(2*o); P:=Group(i,j); u:=i; w:=Comm(u,y);
  Assert(0,Order(w)=4 and w^2 in cen and not w in cen);
  abar:=Image(pi,w);
  g:=First(Elements(G),g->Length(Difference(Set(FactorsInt(Order(abar*Image(pi,w^g)))),[2]))>0);
  Assert(0,g<>fail);
  c0:=abar*Image(pi,w^g); r:=First(Set(FactorsInt(Order(c0))),p->p<>2);
  cbar:=c0^(Order(c0)/r); L:=PreImage(pi,Group(cbar)); R:=SylowSubgroup(L,r);
  Assert(0,IsAbelian(L) and Image(pi,R)=Group(cbar) and R^w=R);
  b:=First(Elements(R),b->Comm(w,b)<>One(G));
  Assert(0,b<>fail and Order(b) mod r=0);
  c:=Comm(w,b);
  Assert(0,Order(w*c)=Order(w) and Order(w*c)<Order(w)*Order(c));
  Add(liftrows,[q,Size(G),Order(u),Order(y),Order(w),r,Order(b),Order(c),Order(w*c)]);
 od;
 Print("PASS_LIFTS ",liftrows,"\n");
 Print("PASS_19_56\n");
end)();
QUIT_GAP(0);
