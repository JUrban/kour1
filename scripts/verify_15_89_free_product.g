# Independent integer projective matrices and finite actual adjacency matrices.
SizeScreen([1000000,1000000]);;
(function()
 local Canon,Mul,Conv,Bit,A,B,I,U,V,Ui,W,Q,S,s1,s2,p,n,G,a,b,els,
       adj,gi,j,mat,r,finiteChecks,rows,coeff,entry,uv,power,seen;
 Canon:=function(M)
   local first;
   first:=First(Concatenation(M),x->x<>0);
   if first<0 then return -M; fi;
   return M;
 end;
 Mul:=function(X,Y) return Canon(X*Y); end;
 Bit:=function(value) if value then return 1; else return 0; fi; end;
 Conv:=function(X,Y)
   local out,x,y,M,pos;
   out:=[];
   for x in X do for y in Y do
     M:=Mul(x[1],y[1]);
     pos:=PositionProperty(out,z->z[1]=M);
     if pos=fail then
       Add(out,[M,x[2]*y[2]]);
     else out[pos][2]:=out[pos][2]+x[2]*y[2]; fi;
   od; od;
   return Filtered(out,x->x[2]<>0);
 end;
 I:=IdentityMat(2); A:=[[0,-1],[1,-1]]; B:=[[0,-1],[1,0]];
 Assert(0,Mul(Mul(A,A),A)=I and Mul(B,B)=I);
 U:=[[Canon(A),1],[Mul(A,A),1]]; V:=[[Canon(B),1]];
 Ui:=[[Canon(A),1/2],[Mul(A,A),1/2],[I,-1/2]];
 W:=Conv(Conv(U,V),U); Q:=Conv(Conv(Ui,V),Ui);
 Assert(0,Length(W)=4 and ForAll(W,x->x[2]=1 and x[1]<>I));
 Assert(0,Length(Q)=9);
 Assert(0,Conv(W,Q)=[[I,1]] and Conv(Q,W)=[[I,1]]);
 S:=List(W,x->x[1]);
 Assert(0,ForAll(S,x->Canon(x^-1) in S));
 s1:=Mul(Mul(A,B),A); s2:=Mul(Mul(Mul(A,A),B),A);
 Assert(0,Mul(s1,s2^-1)=Mul(A,A));
 Assert(0,Mul(Mul(Mul(A,A),s1),Mul(A,A))=Canon(B));
 uv:=Mul(A,B); power:=I; seen:=[I];
 for n in [1..100] do
   power:=Mul(power,uv);
   Assert(0,power=[[1,0],[n,1]] and not power in seen);
   Add(seen,power);
 od;
 Print("PASS_PROJECTIVE matrices=4 inverse_support=9 two_sided_products=2 power_controls=",Length(seen),"\n");
 finiteChecks:=0; rows:=[];
 for p in [3,5,7] do
   G:=PSL(2,p);
   a:=First(Elements(G),x->Order(x)=3);
   b:=First(Elements(G),x->Order(x)=2 and Group(a,x)=G);
   Assert(0,b<>fail);
   els:=Elements(G); S:=Set([a*b*a,a*b*a^2,a^2*b*a,a^2*b*a^2]);
   Assert(0,Length(S)=4 and not One(G) in S and Group(S)=G);
   mat:=List(els,g->List(els,h->Bit(g^-1*h in S)));
   Assert(0,mat=TransposedMat(mat) and ForAll(mat,x->Sum(x)=4));
   Assert(0,RankMat(mat)=Size(G));
   # Direct right-translation matrices verify the operator factorization.
   U:=List(els,g->List(els,h->Bit(g*a=h)+Bit(g*a^2=h)));
   V:=List(els,g->List(els,h->Bit(g*b=h)));
   Q:=(U-IdentityMat(Size(G)))*V*(U-IdentityMat(Size(G)))/4;
   Assert(0,U*V*U=mat and mat*Q=IdentityMat(Size(G)) and Q*mat=IdentityMat(Size(G)));
   finiteChecks:=finiteChecks+2*Size(G)^2;
   Add(rows,[p,Size(G),RankMat(mat)]);
 od;
 Print("PASS_FINITE_GRAPHS rows=",rows," identity_entries=",finiteChecks,"\n");
end)();
QUIT_GAP(0);
