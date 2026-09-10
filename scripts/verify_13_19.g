# Direct-product certificate for the counterexample to 13.19.
LoadPackage("smallgrp");;
(function()
local D,s,t,z,W,e,x1,x2,y1,y2,Q,H,phi,diagS,diagT,cz,i,K;
s:=(1,2)(3,4); t:=(1,3); D:=Group(s,t); z:=Comm(s,t);
if Size(D)<>8 or Order(s)<>2 or Order(t)<>2 or Order(s*t)<>4 then
  Error("Invalid dihedral base");
fi;
W:=DirectProduct(D,D,D,D);
e:=List([1..4],i->Embedding(W,i));
x1:=Image(e[1],s)*Image(e[2],s);
x2:=Image(e[3],s)*Image(e[4],s);
y1:=Image(e[1],t)*Image(e[3],t);
y2:=Image(e[2],t)*Image(e[4],t);
Q:=Group(x1,x2,y1,y2);
diagS:=Product(List(e,f->Image(f,s)));
diagT:=Product(List(e,f->Image(f,t)));
cz:=List([2..4],i->Image(e[1],z)*Image(e[i],z));
H:=Group(Concatenation([diagS,diagT],cz));
if Size(Q)<>256 or Size(H)<>32 or not IsSubgroup(Q,H)
   or not IsNormal(Q,H) then Error("Subgroup hypotheses failed"); fi;
phi:=GroupHomomorphismByImages(Q,D,[x1,x2,y1,y2],[s,s,t,t]);
if phi=fail or not IsSurjective(phi) or Kernel(phi)<>H then
  Error("Quotient map failed");
fi;
for i in [1..4] do
  if Image(Projection(W,i),Q)<>D or Image(Projection(W,i),H)<>D then
    Error("Subdirect projection failed",i);
  fi;
  Print("PASS projection=",i," Q_image=8 H_image=8\n");
od;
K:=FactorGroup(Q,H);
if Size(K)<>8 or IsomorphismGroups(K,D)=fail or IsRegularPGroup(K) then
  Error("Irregular quotient failed");
fi;
if ForAny(Elements(DerivedSubgroup(D)),c->s^2*t^2=(s*t)^2*c^2) then
  Error("Explicit regularity obstruction failed");
fi;
Print("PASS Q_order=",Size(Q)," H_order=",Size(H)," quotient_order=",Size(K),
      " quotient_type=",StructureDescription(K)," regular=",IsRegularPGroup(K),"\n");
Print("Q_id=",IdGroup(Q)," H_id=",IdGroup(H)," H_type=",StructureDescription(H),"\n");
Print("DONE runtime_ms=",Runtime(),"\n");
end)();
QUIT;
