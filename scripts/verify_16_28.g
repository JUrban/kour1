# Exact rational-function checks for research/16.28-proof.md.
SizeScreen([200,10000]);;
F:=GF(5);; one:=One(F);;
Det2:=M->M[1][1]*M[2][2]-M[1][2]*M[2][1];;
Tr2:=M->M[1][1]+M[2][2];;
Mul2:=function(M,N)
  return List([1,2],i->List([1,2],j->
    M[i][1]*N[1][j]+M[i][2]*N[2][j]));
end;;
Eq2:=function(M,N)
  return ForAll([1,2],i->ForAll([1,2],j->IsZero(M[i][j]-N[i][j])));
end;;
s:=Indeterminate(F,"s");;
u:=s/(1+s);; w:=u*(1-u)-1;;
A:=[[u,one],[w,1-u]];;
D:=[[s,Zero(F)],[Zero(F),one/s]];;
# Use the explicit adjugate and verify it is the inverse. This avoids
# GAP's generic inversion dispatch for mixed rational-function matrices.
Ai:=[[1-u,-one],[-w,u]];;
B:=Mul2(Ai,D);;
if not IsZero(Det2(A)-one) or not IsZero(Tr2(A)-one) or
   not IsZero(Det2(B)-one) or not IsZero(Tr2(B)-one) or
   not Eq2(Mul2(A,B),D) or not Eq2(Mul2(A,Ai),IdentityMat(2,F)) or
   not Eq2(Mul2(Ai,A),IdentityMat(2,F)) then
  Error("rational-function factorization failed");
fi;
Print("PASS rational-function identities over GF(5)(s)\n");
# The characteristic polynomial X^2-X+1 has distinct roots.
testField:=GF(25);;
roots:=Filtered(Elements(testField),a->a^2-a+1=Zero(testField));;
if Length(roots)<>2 or roots[1]=roots[2] or Product(roots)<>One(testField) then
  Error("characteristic polynomial root control failed");
fi;
Print("PASS two distinct eigenvalues over GF(25)\n");
for q in [5,25,125,625] do
  testField:=GF(q);; count:=0;;
  for a in Elements(testField) do
    if a<>Zero(testField) and a<>-One(testField) then
      v:=a/(1+a);; c:=v*(1-v)-1;;
      M:=[[v,One(testField)],[c,1-v]];;
      N:=M^-1*DiagonalMat([a,a^-1]);;
      if DeterminantMat(M)<>One(testField) or TraceMat(M)<>One(testField) or
         DeterminantMat(N)<>One(testField) or TraceMat(N)<>One(testField) then
        Error("finite-field factorization failed");
      fi;
      count:=count+1;
    fi;
  od;
  Print("PASS field=",q," parameters=",count,"\n");
od;
t:=Indeterminate(F,"t");;
if Length(Set(List([0..100],j->t^j)))<>101 then
  Error("transcendental power control failed");
fi;
Print("PASS 101 distinct formal powers (finite control only)\n");
Print("DONE verify_16_28\n");
QUIT_GAP(0);
