SizeScreen([1000000,1000000]);;
(function()
 local Relators,F,f,K,Search,G,qs,q,n,rows,row,checks,start;
 Relators:=function(v)
   local A,B,C,D,E,H;
   A:=v[1]; B:=v[2]; C:=v[3]; D:=v[4]; E:=v[5]; H:=v[6];
   return [A^3,B^3,C^2,D^2,E^2,H^2,
     (A*C)^3,(A*D)^3,(A*E)^3,(A*H)^3,
     (B*C)^3,(B*D)^3,(B*E)^3,(B*H)^3,
     (A*B*A^-1*C)^2,(A*B*A^-1*D)^2,
     (A^-1*B*A*E)^2,(A^-1*B*A*H)^2,
     (B*A*B^-1*C)^2,(B^-1*A*B*D)^2,
     (B*A*B^-1*E)^2,(B^-1*A*B*H)^2];
 end;
 F:=FreeGroup(6); f:=GeneratorsOfGroup(F); K:=F/Relators(f);
 Assert(0,Length(Relators(f))=22 and AbelianInvariants(K)=[]);
 Print("PASS_ABELIANIZATION relators=22 invariants=[]\n");

 Search:=function(G,label)
   local classes,threes,twos,As,A,B,ia,ib,first,second,inv,one,
         candidates,sets,X,ok,vals,pairs,potential,passing,witnesses,
         v,image,fullchecks;
   classes:=ConjugacyClasses(G); one:=One(G);
   As:=List(Filtered(classes,c->Order(Representative(c))=3),Representative);
   threes:=Concatenation(List(Filtered(classes,c->Order(Representative(c))=3),AsList));
   twos:=Concatenation(List(Filtered(classes,c->Order(Representative(c))=2),AsList));
   pairs:=0; potential:=0; passing:=0; witnesses:=0; fullchecks:=0;
   for A in As do
     candidates:=Filtered(twos,X->(A*X)^3=one);
     ia:=A^-1;
     for B in threes do
       pairs:=pairs+1; ib:=B^-1;
       inv:=Filtered(candidates,X->(B*X)^3=one);
       potential:=potential+Length(inv);
       if IsEmpty(inv) then continue; fi;
       first:=[A*B*ia,ia*B*A]; second:=[B*A*ib,ib*A*B];
       sets:=[[],[],[],[]];
       for X in inv do
         vals:=[(first[1]*X)^2=one,(first[2]*X)^2=one,
                (second[1]*X)^2=one,(second[2]*X)^2=one];
         if vals[1] and vals[3] then Add(sets[1],X); fi;
         if vals[1] and vals[4] then Add(sets[2],X); fi;
         if vals[2] and vals[3] then Add(sets[3],X); fi;
         if vals[2] and vals[4] then Add(sets[4],X); fi;
       od;
       passing:=passing+Sum(List(sets,Length));
       if ForAll(sets,s->not IsEmpty(s)) then
         v:=Concatenation([A,B],List(sets,s->s[1]));
         Assert(0,ForAll(Relators(v),r->r=one)); fullchecks:=fullchecks+22;
         image:=Group(v); Assert(0,Size(image)>1 and IsPerfectGroup(image));
         witnesses:=witnesses+1;
         Print("HIT target=",label," image_order=",Size(image)," images=",v,"\n");
         PrintTo("results/16.46-first-witness.g","QuotientImages:=",v,";\n");
         break;
       fi;
     od;
     if witnesses>0 then break; fi;
   od;
   Print("TARGET label=",label," order=",Size(G)," classes3=",Length(As),
         " elements3=",Length(threes)," elements2=",Length(twos),
         " pairs=",pairs," cube_triples=",potential," square_slots=",passing,
         " witnesses=",witnesses," direct_relators=",fullchecks,"\n");
   return [label,Size(G),Length(As),Length(threes),Length(twos),pairs,
           potential,passing,witnesses,fullchecks];
 end;

 # A4 satisfies the order and cube relations with A=B and C=D=E=F;
 # the extra square relations must reject this tempting false witness.
 G:=AlternatingGroup(4);
 row:=[(1,2,3),(1,2,3),(1,2)(3,4),(1,2)(3,4),(1,2)(3,4),(1,2)(3,4)];
 Assert(0,ForAll(Relators(row){[1..14]},IsOne));
 Assert(0,not ForAll(Relators(row),IsOne));
 Print("PASS_FALSE_WITNESS first_relators=14 full_relators_reject=true\n");
 start:=Runtime(); rows:=[];
 for n in [5..8] do
   Add(rows,Search(AlternatingGroup(n),Concatenation("A",String(n))));
   if Last(rows)[9]>0 then break; fi;
 od;
 if ForAll(rows,r->r[9]=0) then
   qs:=Filtered([4..31],IsPrimePowerInt);
   for q in qs do
     Add(rows,Search(PSL(2,q),Concatenation("PSL2_",String(q))));
     if Last(rows)[9]>0 then break; fi;
   od;
 fi;
 Print("COMPLETE targets=",Length(rows)," witnesses=",Sum(List(rows,r->r[9])),
       " cpu_ms=",Runtime()-start," rows=",rows,"\n");
end)();
QUIT_GAP(0);
