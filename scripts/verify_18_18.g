SizeScreen([1000000,1000000]);;
(function()
 local CheckSigmaClass,G,n,t,positives,negatives,entry,classes,c,answer,
       h,id,H,els,one,Index,aimg,bimg,a,b,A,L,l,g,j,k,degree,C,
       left,main,extended,controlrows,points,starchecks,transchecks;
 CheckSigmaClass:=function(G,t)
   local C,m,adj,quad,stars,s,inc,i,j,c,images,moved,u,central,qs,counts;
   C:=AsList(ConjugacyClass(G,t)); m:=Length(C);
   Print("CLASS_START order=",Size(G)," class=",m,"\n");
   central:=Centralizer(G,Group(C));
   Print("CLASS_CENTRALIZER size=",Size(central),"\n");
   if Size(central)<>1 then return [false,"centralizer",m,0,0]; fi;
   adj:=List([1..m],i->List([1..m],j->i<>j and C[i]*C[j]<>C[j]*C[i]));
   stars:=[]; qs:=0; counts:=List([1..m],i->0);
   for quad in Combinations([1..m],4) do
     if not ForAll(Combinations(quad,2),p->adj[p[1]][p[2]]) then continue; fi;
     qs:=qs+1;
     s:=Filtered([1..m],i->ForAll(quad,j->i=j or adj[i][j]));
     if not s in stars then
       AddSet(stars,s);
       for i in s do counts[i]:=counts[i]+1; od;
       if Maximum(counts)>2 then
         return [false,"three_endpoints",m,Length(stars),qs];
       fi;
     fi;
   od;
   Print("CLASS_STARS count=",Length(stars)," quadruples=",qs,"\n");
   if Length(stars)<5 then return [false,"vertices",m,Length(stars),qs]; fi;
   inc:=List([1..m],i->Filtered([1..Length(stars)],j->i in stars[j]));
   if not ForAll(inc,s->Length(s)=2) then
     return [false,"two_endpoints",m,Length(stars),qs];
   fi;
   if not ForAll(Combinations(stars,2),p->Length(Intersection(p[1],p[2]))=1) then
     return [false,"unique_edge",m,Length(stars),qs];
   fi;
   for c in [1..m] do
     images:=List([1..m],i->Position(C,C[c]*C[i]*C[c]^-1));
     for u in [1..Length(stars)] do
       s:=Set(List(stars[u],i->images[i]));
       Assert(0,s in stars);
       if (s=stars[u])<>(not c in stars[u]) then
         return [false,"transposition_action",m,Length(stars),qs];
       fi;
     od;
   od;
   return [true,"PASS",m,Length(stars),qs];
 end;
 positives:=[];
 for n in [5..9] do
   G:=SymmetricGroup(n); answer:=CheckSigmaClass(G,(1,2));
   Assert(0,answer[1] and answer[3]=Binomial(n,2) and answer[4]=n);
   Assert(0,answer[5]=n*Binomial(n-1,4));
   Add(positives,[n,answer]);
 od;
 answer:=CheckSigmaClass(SymmetricGroup(6),(1,2)(3,4)(5,6));
 Assert(0,answer[1]); Add(positives,[6,answer]);
 negatives:=[];
 for entry in [["S4",SymmetricGroup(4)],["A4",AlternatingGroup(4)],
               ["A5",AlternatingGroup(5)],["A6",AlternatingGroup(6)],
               ["D10",DihedralGroup(IsPermGroup,10)],
               ["SL2_5",SL(2,5)],
               ["S5xC2",DirectProduct(SymmetricGroup(5),CyclicGroup(IsPermGroup,2))]] do
   G:=entry[2]; classes:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);
   for c in classes do
     answer:=CheckSigmaClass(G,Representative(c)); Assert(0,not answer[1]);
     Add(negatives,[entry[1],answer]);
   od;
 od;
 Print("PASS_SIGMA positives=",positives," negatives=",negatives,"\n");

 controlrows:=[];
 for h in [1..8] do
   for id in [1..NumberSmallGroups(h)] do
     Print("CENTRALIZER_CASE order=",h," id=",id,"\n");
     H:=SmallGroup(h,id); els:=Elements(H); one:=One(H);
     els:=Concatenation([one],Filtered(els,g->g<>one));
     Index:=function(g,j) return (Position(els,g)-1)*h+j+1; end;
     aimg:=[]; bimg:=[];
     for g in els do for j in [0..h-1] do
       Add(aimg,Index(g,(j+1) mod h)); Add(bimg,Index(g*els[j+1],j));
     od; od;
     a:=PermList(aimg); b:=PermList(bimg); A:=Group(a,b);
     Assert(0,IsTransitive(A,[1..h*h]));
     L:=[];
     for l in els do
       left:=[];
       for g in els do for j in [0..h-1] do Add(left,Index(l*g,j)); od; od;
       Add(L,PermList(left));
     od;
     main:=Centralizer(SymmetricGroup(h*h),A);
     Assert(0,Size(main)=h and main=Group(L));
     for degree in [2*h*h+3,2*h*h+4] do
       k:=degree-h*h;
       aimg:=Concatenation(ListPerm(a,h*h),[h*h+2..degree],[h*h+1]);
       bimg:=Concatenation(ListPerm(b,h*h),[h*h+2,h*h+1],[h*h+3..degree]);
       a:=PermList(aimg); b:=PermList(bimg);
       A:=Group(a,b); Assert(0,Set(List(Orbits(A,[1..degree]),Length))=[h*h,k]);
       extended:=Centralizer(SymmetricGroup(degree),A);
       Assert(0,Size(extended)=h and extended=Group(L));
       Assert(0,IdGroup(extended)=[h,id]);
       Add(controlrows,[h,id,degree,Size(extended)]);
       # Restore the main restrictions before constructing the next padding.
       a:=RestrictedPerm(a,[1..h*h]); b:=RestrictedPerm(b,[1..h*h]);
     od;
   od;
 od;
 Print("PASS_CENTRALIZERS groups=14 padded_cases=",Length(controlrows),
       " rows=",controlrows,"\n");
end)();
QUIT_GAP(0);
