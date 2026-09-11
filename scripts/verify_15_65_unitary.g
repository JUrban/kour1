# Finite controls only; nonrationality is proved analytically.
SetAssertionLevel(2);
VerifyUnitaryCase := function(q,n)
  local G,F,classes,cl,g,m,degree,powers,i,flat,rank,cyclic,total,
        classcount,orderformula;
  F:=GF(q^2);
  G:=GU(n,q);
  orderformula:=q^(n*(n-1)/2)*Product([1..n],j->q^j-(-1)^j);
  if Size(G)<>orderformula then Error("Wrong unitary group order"); fi;
  classes:=ConjugacyClasses(G);
  cyclic:=0; total:=0; classcount:=0;
  for cl in classes do
    g:=Representative(cl);
    m:=MinimalPolynomial(F,g);
    degree:=DegreeOfLaurentPolynomial(m);
    powers:=[One(g)];
    for i in [2..n] do Add(powers,powers[Length(powers)]*g); od;
    flat:=List(powers,x->Concatenation(x));
    rank:=RankMat(flat);
    if (degree=n)<>(rank=n) then Error("Minimal polynomial/rank mismatch"); fi;
    if degree=n then cyclic:=cyclic+Size(cl); fi;
    total:=total+Size(cl); classcount:=classcount+1;
  od;
  if total<>Size(G) then Error("Incomplete conjugacy classes"); fi;
  Print("UNITARY_CONTROL ",q," ",n," ",Size(G)," ",cyclic," ",classcount,"\n");
end;
for qc in [[2,1],[2,2],[2,3],[2,4],[3,1],[3,2],[3,3],
           [4,1],[4,2],[4,3],[5,1],[5,2],[7,1],[7,2]] do
  VerifyUnitaryCase(qc[1],qc[2]);
od;
Print("UNITARY_CONTROLS_DONE\n");
QUIT;
