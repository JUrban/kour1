# Exact finite controls for cyclic, semisimple, and regular semisimple matrices.
# This is not the analytic nonrationality proof.
SetAssertionLevel(2);
VerifyClassicalCase := function(family,q,n)
  local G,F,dim,orderformula,p,classes,cl,g,m,c,degree,powers,i,rank,
        cyclic,ss,rs,total,iscyclic,isss,isrs,classcount;
  if family="U" then
    G:=GU(n,q); F:=GF(q^2); dim:=n;
    orderformula:=q^(n*(n-1)/2)*Product([1..n],j->q^j-(-1)^j);
  else
    G:=Sp(2*n,q); F:=GF(q); dim:=2*n;
    orderformula:=q^(n^2)*Product([1..n],j->q^(2*j)-1);
  fi;
  p:=Characteristic(F);
  if Size(G)<>orderformula then Error("Wrong group order"); fi;
  classes:=ConjugacyClasses(G);
  cyclic:=0; ss:=0; rs:=0; total:=0; classcount:=0;
  for cl in classes do
    g:=Representative(cl);
    m:=MinimalPolynomial(F,g); c:=CharacteristicPolynomial(F,g);
    degree:=DegreeOfLaurentPolynomial(m);
    powers:=[One(g)];
    for i in [2..dim] do Add(powers,powers[Length(powers)]*g); od;
    rank:=RankMat(List(powers,x->Concatenation(x)));
    iscyclic:=degree=dim;
    isss:=DegreeOfLaurentPolynomial(Gcd(m,Derivative(m)))=0;
    isrs:=DegreeOfLaurentPolynomial(Gcd(c,Derivative(c)))=0;
    if iscyclic<>(rank=dim) then Error("Cyclicity/rank mismatch"); fi;
    if isss<>(Order(g) mod p<>0) then Error("Semisimplicity/order mismatch"); fi;
    if isrs<>(iscyclic and isss) then Error("Regular semisimplicity mismatch"); fi;
    if iscyclic then cyclic:=cyclic+Size(cl); fi;
    if isss then ss:=ss+Size(cl); fi;
    if isrs then rs:=rs+Size(cl); fi;
    total:=total+Size(cl); classcount:=classcount+1;
  od;
  if total<>Size(G) then Error("Incomplete conjugacy classes"); fi;
  Print("CLASSICAL_CONTROL ",family," ",q," ",n," ",Size(G)," ",
        cyclic," ",ss," ",rs," ",classcount,"\n");
end;
for qc in [[2,1],[2,2],[2,3],[2,4],[3,1],[3,2],[3,3],
           [4,1],[4,2],[4,3],[5,1],[5,2],[7,1],[7,2]] do
  VerifyClassicalCase("U",qc[1],qc[2]);
od;
for qc in [[2,1],[2,2],[2,3],[3,1],[3,2],[4,1],[4,2],[5,1],[7,1]] do
  VerifyClassicalCase("Sp",qc[1],qc[2]);
od;
Print("CLASSICAL_CONTROLS_DONE\n");
QUIT;
