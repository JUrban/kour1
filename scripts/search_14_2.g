# Exact restricted screen for Problem 14.2.
# Only automorphisms transposing two rational primitive central idempotents
# and fixing all other primitive idempotents are considered.
LoadPackage("ctbllib");;
SizeScreen([1000000,24]);;

Data142:=function(t)
local irr,sizes,n,rats,i,c,d,lambda,num,conductor,data;
irr:=Irr(t); sizes:=SizesConjugacyClasses(t); n:=Size(t);
data:=[];
for i in [1..Length(irr)] do
    c:=List(irr[i]);
    if not ForAll(c,IsRat) then continue; fi;
    Assert(0,ForAll(c,IsInt));
    d:=c[1]; lambda:=List([1..Length(c)],j->sizes[j]*c[j]/d);
    Assert(0,ForAll(lambda,IsInt));
    num:=d*c;
    conductor:=n/Gcd(Concatenation([n],num));
    Add(data,rec(index:=i,degree:=d,chi:=c,lambda:=lambda,
                 numerator:=num,conductor:=conductor));
od;
return rec(order:=n,data:=data,classes:=Length(irr));
end;

Swap142:=function(d,a,b)
local delta,num,g1,g2,M,j,k,monomial;
delta:=b.lambda-a.lambda; num:=a.numerator-b.numerator;
g1:=Gcd(delta);g2:=Gcd(num);
if (g1*g2) mod d.order<>0 then return fail; fi;
M:=IdentityMat(d.classes);
for j in [1..d.classes] do
 for k in [1..d.classes] do
  M[j][k]:=M[j][k]+delta[j]*num[k]/d.order;
 od;
od;
Assert(0,ForAll(M,row->ForAll(row,IsInt)));
Assert(0,M*M=IdentityMat(d.classes));
monomial:=ForAll(M,row->Number(row,x->x<>0)=1 and
                          ForAll(row,x->x in [-1,0,1]));
return rec(matrix:=M,monomial:=monomial,gcd_lambda:=g1,gcd_num:=g2);
end;

Run142:=function()
local names,name,t,d,pair,a,b,s,count,pairs,matched,valid,hits,
      ratrows,tablepairs,tablematched,tablevalid,tablehits;
names:=AllCharacterTableNames();
count:=0;pairs:=0;matched:=0;valid:=0;hits:=0;ratrows:=0;
Print("START tables=",Length(names)," gap=",GAPInfo.Version,"\n");
for name in names do
 t:=CharacterTable(name);Assert(0,t<>fail);
 d:=Data142(t);count:=count+1;ratrows:=ratrows+Length(d.data);
 tablepairs:=0;tablematched:=0;tablevalid:=0;tablehits:=0;
 for pair in Combinations(d.data,2) do
  a:=pair[1];b:=pair[2];
  tablepairs:=tablepairs+1;
  if a.conductor<>b.conductor then continue;fi;
  tablematched:=tablematched+1;
  s:=Swap142(d,a,b);
  if s=fail then continue;fi;
  tablevalid:=tablevalid+1;
  if not s.monomial then
   tablehits:=tablehits+1;
   Print("HIT name=",name," indices=",a.index,",",b.index,
    " degrees=",a.degree,",",b.degree," matrix=",s.matrix,"\n");
  fi;
 od;
 pairs:=pairs+tablepairs;matched:=matched+tablematched;
 valid:=valid+tablevalid;hits:=hits+tablehits;
 Print("TABLE index=",count," name=",name," order=",d.order,
  " rational_rows=",Length(d.data)," pairs=",tablepairs,
  " conductor_matched=",tablematched," integral_swaps=",tablevalid,
  " nonmonomial=",tablehits,"\n");
od;
Print("DONE tables=",count," rational_rows=",ratrows," pairs=",pairs,
 " conductor_matched=",matched," integral_swaps=",valid,
 " nonmonomial=",hits,"\n");
end;

if not IsBound(CONTROL_ONLY142) then
 Run142();
 QUIT_GAP(0);
fi;
