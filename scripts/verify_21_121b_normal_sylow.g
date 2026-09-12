# New finite controls for the Frattini bound; no infinite assertion is tested.
(function()
local qs,q,f,felms,perms,a,b,G,models,model,p,classes,cl,K,P,H,
      normals,A,B,j,phi,bound,checks,total,hist,row,found,best,N,
      optimal,representatives,allclasses,allsubgroups,allchecks;
qs:=[2,3,4,5,7,8,9,16]; models:=[];
for q in qs do
  f:=GF(q); felms:=Elements(f); perms:=[];
  for a in felms do
    if a<>Zero(f) then
      for b in felms do
        Add(perms,PermList(List(felms,x->Position(felms,a*x+b))));
      od;
    fi;
  od;
  G:=Group(perms);
  if Size(G)<>q*(q-1) then Error("Wrong affine order"); fi;
  Add(models,[Concatenation("affine_",String(q)),G,Characteristic(f)]);
od;
Add(models,["quaternion_complement",SL(2,3),2]);
Add(models,["affine4_times_c5",DirectProduct(models[3][2],CyclicGroup(5)),2]);
Add(models,["nonabelian_hall",DirectProduct(SL(2,3),SmallGroup(27,3)),2]);
allclasses:=0; allsubgroups:=0; allchecks:=0;
for model in models do
  G:=model[2]; p:=model[3]; classes:=ConjugacyClassesSubgroups(G);
  hist:=[]; checks:=0; total:=0;
  for cl in classes do
    K:=Representative(cl); P:=SylowSubgroup(K,p);
    if not IsNormal(K,P) then Error("Nonnormal Sylow subgroup"); fi;
    if Size(P)=1 then H:=K;
    elif Size(P)=Size(K) then H:=TrivialSubgroup(K);
    else
      representatives:=ComplementClassesRepresentatives(K,P);
      if Length(representatives)=0 then Error("Missing complement"); fi;
      H:=representatives[1];
    fi;
    if Size(H)*Size(P)<>Size(K) or Size(Intersection(H,P))<>1
       or Gcd(Size(H),p)<>1 then Error("Bad Hall complement"); fi;
    phi:=FrattiniSubgroup(P);
    normals:=Filtered(NormalSubgroups(H),IsAbelian);
    for A in normals do
      j:=Index(H,A); B:=Centralizer(A,P);
      if not IsNormal(K,B) or not IsAbelian(B) or Gcd(Size(B),p)<>1 then
        Error("Invalid normal abelian p-prime subgroup");
      fi;
      if Size(P)=1 then bound:=j;
      else bound:=j*Size(P)*(Index(P,phi)-1); fi;
      if Index(K,B)>bound then Error("Frattini index bound failed"); fi;
      if Index(K,B)<>Size(P)*j*Index(A,B) then Error("Index identity failed"); fi;
      checks:=checks+1;
    od;
    optimal:=Filtered(NormalSubgroups(K),N->IsAbelian(N) and Gcd(Size(N),p)=1);
    best:=Minimum(List(optimal,N->Index(K,N)));
    row:=[Size(K),Size(P),best]; found:=PositionProperty(hist,r->r{[1..3]}=row);
    if found=fail then Add(hist,Concatenation(row,[Size(cl)]));
    else hist[found][4]:=hist[found][4]+Size(cl); fi;
    total:=total+Size(cl);
  od;
  Sort(hist);
  if PositionSublist(model[1],"affine_")=1 then
    for row in hist do
      if row[2]=1 then
        if row[3]<>1 then Error("Affine p-prime subgroup nonabelian"); fi;
      elif row[3]<>row[1] then Error("Affine p-prime radical not trivial");
      fi;
    od;
  fi;
  Print("{\"model\":\"",model[1],"\",\"order\":",Size(G),
        ",\"p\":",p,",\"subgroup_classes\":",Length(classes),
        ",\"subgroups\":",total,",\"abelian_complement_choices\":",checks,
        ",\"histogram\":",hist,"}\n");
  allclasses:=allclasses+Length(classes); allsubgroups:=allsubgroups+total;
  allchecks:=allchecks+checks;
od;
Print("PASS_21_121B_NATIVE models=",Length(models)," classes=",allclasses,
      " subgroups=",allsubgroups," choices=",allchecks,"\n");
end)();
QUIT;
