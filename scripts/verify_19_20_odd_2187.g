# Full GAP subgroup/quotient count for E_(3,2) x C3^2.
# Avoid IdGroup, which does not cover this order. These exponent-three,
# derived-order-at-most-three groups are classified by order and centre.
SizeScreen([1000000,1000000]);;
(function()
local field,gens,i,a,E,G,classify,data,cl,U,key,row,N,L,ends,partials,classes;
field:=GF(3); gens:=[];
for i in [2..3] do
  a:=IdentityMat(4,field); a[1][i]:=One(field); Add(gens,a);
  a:=IdentityMat(4,field); a[i][4]:=One(field); Add(gens,a);
od;
E:=Image(IsomorphismPcGroup(Group(gens)));
G:=DirectProduct(E,ElementaryAbelianGroup(9));
if Size(G)<>2187 or Exponent(G)<>3 or Size(DerivedSubgroup(G))<>3 then
  Error("Unexpected group");
fi;
classify:=function(H)
local n,z,t,s;
n:=LogInt(Size(H),3);
if IsAbelian(H) then return Concatenation("0_",String(n)); fi;
if Size(DerivedSubgroup(H))<>3 or Exponent(H)<>3 then Error("Unexpected type"); fi;
z:=LogInt(Size(Centre(H)),3); t:=(n-z)/2; s:=z-1;
if not IsInt(t) or t<1 or s<0 then Error("Type dimensions failed"); fi;
return Concatenation(String(t),"_",String(s));
end;
Print("START order=",Size(G),"\n"); data:=rec(); classes:=0;
for cl in ConjugacyClassesSubgroups(G) do
  U:=Representative(cl); key:=classify(U);
  if not IsBound(data.(key)) then
    Print("AUT_START type=",key," order=",Size(U),"\n");
    data.(key):=[0,0,Size(AutomorphismGroup(U))];
    Print("AUT_DONE type=",key," aut=",data.(key)[3],"\n");
  fi;
  data.(key)[1]:=data.(key)[1]+Size(cl); classes:=classes+1;
od;
Print("SUBGROUPS_DONE classes=",classes,"\n");
for N in NormalSubgroups(G) do
  L:=FactorGroup(G,N); key:=classify(L);
  if IsBound(data.(key)) then data.(key)[2]:=data.(key)[2]+1; fi;
od;
ends:=0; partials:=0;
for key in SortedList(RecNames(data)) do
  row:=data.(key); ends:=ends+row[1]*row[2]*row[3];
  partials:=partials+row[1]^2*row[3];
  Print("TYPE ",key," subgroup_count,quotient_count,aut_order=",row,"\n");
od;
if ends<>8241952876767369 or partials<>2607970224105603 then Error("Count mismatch"); fi;
Print("PASS order=2187 end=",ends," piso=",partials,"\n");
Print("DONE runtime_ms=",Runtime(),"\n");
end)();
QUIT;
