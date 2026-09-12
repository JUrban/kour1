# Controls for the soluble extension of the exponent-two bound.
(function()
local models,model,G,p,classes,K,ns,j,J,N,R,F,H,A,B,cd,m,measures,
      phi,bound,P,normalprime,automorphisms,optimal,record,checked;
models:=[
 ["s3",SymmetricGroup(3),2],["s3",SymmetricGroup(3),3],
 ["s4",SymmetricGroup(4),2],["s4",SymmetricGroup(4),3],
 ["sl2_3",Image(IsomorphismPermGroup(SL(2,3))),2],
 ["sl2_3",Image(IsomorphismPermGroup(SL(2,3))),3],
 ["gl2_3",Image(IsomorphismPermGroup(GL(2,3))),2],
 ["gl2_3",Image(IsomorphismPermGroup(GL(2,3))),3],
 ["heisenberg3_times_c2",DirectProduct(SmallGroup(27,3),CyclicGroup(2)),2],
 ["s4_times_heisenberg3",DirectProduct(SymmetricGroup(4),SmallGroup(27,3)),2],
 ["a5_negative_control",AlternatingGroup(5),2]
];
checked:=0;
for model in models do
  G:=model[2]; p:=model[3]; classes:=ConjugacyClassesSubgroups(G); J:=1;
  for K in List(classes,Representative) do
    if Gcd(Size(K),p)=1 then
      ns:=Filtered(NormalSubgroups(K),IsAbelian);
      j:=Minimum(List(ns,A->Index(K,A))); J:=Maximum(J,j);
    fi;
  od;
  P:=SylowSubgroup(G,p); bound:=J^3*Size(P)^2;
  if not IsSolvableGroup(G) then
    optimal:=Minimum(List(Filtered(NormalSubgroups(G),A->
                 IsAbelian(A) and Gcd(Size(A),p)=1),A->Index(G,A)));
    if model[1]<>"a5_negative_control" or J<>1 or optimal<=bound
       or Size(FittingSubgroup(G))<>1 then Error("Negative control failed"); fi;
    Print("{\"model\":\"",model[1],"\",\"p\":",p,
      ",\"J\":",J,",\"order\":",Size(G),",\"sylow_order\":",Size(P),
      ",\"minimum_index\":",optimal,",\"quadratic_bound\":",bound,"}\n");
  else
    normalprime:=Filtered(NormalSubgroups(G),K->Gcd(Size(K),p)=1);
    N:=First(normalprime,K->Size(K)=Maximum(List(normalprime,Size)));
    if not ForAll(normalprime,K->IsSubgroup(N,K)) then Error("Wrong p-prime core"); fi;
    cd:=List(ConjugacyClassesSubgroups(N),Representative);
    measures:=List(cd,K->Size(K)*Size(Centralizer(N,K))); m:=Maximum(measures);
    cd:=Filtered(cd,K->Size(K)*Size(Centralizer(N,K))=m);
    B:=First(cd,K->Size(K)=Minimum(List(cd,Size)));
    if not IsNormal(N,B) or not IsAbelian(B) or not ForAll(cd,K->IsSubgroup(K,B))
       or Index(N,B)>J^2 then Error("Characteristic abelian lemma failed"); fi;
    automorphisms:=GeneratorsOfGroup(AutomorphismGroup(N));
    if not ForAll(automorphisms,a->Image(a,B)=B) then Error("B not characteristic in N"); fi;
    if not IsNormal(G,B) or Gcd(Size(B),p)<>1 or Index(G,B)>bound then
      Error("Soluble bound failed");
    fi;
    R:=FactorGroup(G,N); F:=FittingSubgroup(R); phi:=FrattiniSubgroup(F);
    if Size(R)>1 then
      if Size(F)=1 or Size(F)<>Size(SylowSubgroup(F,p)) or
         not IsSubgroup(F,Centralizer(R,F)) then Error("Fitting reduction failed"); fi;
      H:=HallSubgroup(R,Filtered(Set(FactorsInt(Size(R))),q->q<>p));
      if Size(Centralizer(H,F))<>1 then Error("Hall action not faithful"); fi;
      if Size(R)>J*Size(P)*(Index(F,phi)-1) then Error("Quotient order bound failed"); fi;
    fi;
    Print("{\"model\":\"",model[1],"\",\"p\":",p,
      ",\"J\":",J,",\"order\":",Size(G),",\"sylow_order\":",Size(P),
      ",\"p_prime_core_order\":",Size(N),",\"cd_order\":",Size(B),
      ",\"quotient_order\":",Size(R),",\"fitting_order\":",Size(F),
      ",\"frattini_index\":",Index(F,phi),",\"constructed_index\":",Index(G,B),
      ",\"quadratic_bound\":",bound,"}\n");
    checked:=checked+1;
  fi;
od;
Print("PASS_21_121B_SOLUBLE_NATIVE soluble_models=",checked," negative_controls=1\n");
end)();
QUIT;
