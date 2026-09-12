# Native groups and repeated image sets, independent of the Python orbit walk.
Sink20189:=function(el,a)
 local old,s;
 s:=Set(el);
 repeat old:=s;s:=Set(s,x->Comm(x,a));until s=old;
 return s;
end;
Analyze20189:=function(label,g,meta)
 local el,der,sinks,a,b,k,products,hist,sizes;
 el:=Elements(g);der:=DerivedSubgroup(g);
 if IsAbelian(der)<>meta then Error("derived check");fi;
 sinks:=List(el,a->Sink20189(el,a));
 if meta then
  for a in [1..Length(el)] do
   k:=Subgroup(g,sinks[a]);
   if Size(k)<>Length(sinks[a]) or not IsNormal(g,k) then Error("sink normal subgroup");fi;
   if sinks[Position(el,el[a]^-1)]<>sinks[a] then Error("inverse sink");fi;
   for b in [1..Length(el)] do
    products:=Set(Cartesian(sinks[a],sinks[b]),xy->xy[1]*xy[2]);
    if not IsSubset(products,sinks[Position(el,el[a]*el[b])]) then Error("product sink");fi;
   od;
  od;
 elif ForAll(sinks,s->Size(Subgroup(g,s))=Length(s)) then Error("negative control");fi;
 sizes:=List(sinks,Length);hist:=List(Set(sizes),s->[s,Number(sizes,x->x=s)]);
 return [label,Size(g),Size(der),hist,Size(g)^2,Size(g)^3];
end;
rows20189:=[];
for n20189 in [3,4,5,6,15] do
 Add(rows20189,Analyze20189(Concatenation("D",String(2*n20189)),DihedralGroup(IsPermGroup,2*n20189),true));
od;
Add(rows20189,Analyze20189("A4",AlternatingGroup(4),true));
m20189:=IdentityMat(3,GF(3));;m20189[1][2]:=One(GF(3));;
n20189:=IdentityMat(3,GF(3));;n20189[2][3]:=One(GF(3));;
Add(rows20189,Analyze20189("H27",Group(m20189,n20189),true));
Add(rows20189,Analyze20189("W18",WreathProduct(Group((1,2,3)),Group((1,2))),true));
control20189:=Analyze20189("S4",SymmetricGroup(4),false);;
family20189:=[];
s20189:=[];
for r20189 in [0..8] do
 for m20189 in [1,3,5,15] do
  n20189:=2^r20189*m20189;
  # The native additive cyclic group realizes exactly the rotation layer.
  a20189:=CyclicGroup(IsPermGroup,n20189);el20189:=Elements(a20189);
  old20189:=[];s20189:=Set(el20189);
  while old20189<>s20189 do old20189:=s20189;s20189:=Set(s20189,x->x^-2);od;
  if Length(s20189)<>m20189 then Error("odd sink");fi;
  if not ForAll(el20189,x->x^((-2)^r20189) in s20189) then Error("entry time");fi;
  if r20189>0 and ForAll(el20189,x->x^((-2)^(r20189-1)) in s20189) then Error("sharp entry time");fi;
  Add(family20189,[r20189,m20189,n20189,Length(s20189),r20189]);
 od;
od;
Print("ROWS20189 ",rows20189,"\nCONTROL20189 ",control20189,"\nFAMILY20189 ",family20189,"\n");
Print("PASS_20_89_METABELIAN_NATIVE\n");
QUIT;
