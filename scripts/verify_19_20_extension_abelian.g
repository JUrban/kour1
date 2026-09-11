# Reconstruct all abelian library IDs from the classification, independently
# of the search's IsAbelian decisions on supplied SmallGroup objects.
SizeScreen([1000000,24]);;
VerifyAbelianExtension1920:=function()
local n,factors,partlists,parts,invariants,i,G,id,ids,expected,total;
total:=0;
for n in [257..511] do
 factors:=Collected(FactorsInt(n));
 partlists:=List(factors,pe->Partitions(pe[2]));
 expected:=Product(List(partlists,Length));ids:=[];
 for parts in Cartesian(partlists) do
  invariants:=[];
  for i in [1..Length(factors)] do
   Append(invariants,List(parts[i],e->factors[i][1]^e));
  od;
  G:=AbelianGroup(invariants);id:=IdGroup(G);
  Assert(0,Size(G)=n and id[1]=n and not id[2] in ids);Add(ids,id[2]);
  Print("ABELIAN_ID1920 order=",n," id=",id[2]," invariants=",AbelianInvariants(G),"\n");
 od;
 Assert(0,Length(ids)=expected);total:=total+Length(ids);
 Print("ABELIAN_ORDER1920 order=",n," count=",Length(ids),"\n");
od;
Print("PASS_ABELIAN1920 orders=255 groups=",total,"\n");
end;
VerifyAbelianExtension1920();QUIT;
