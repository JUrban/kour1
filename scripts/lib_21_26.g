# Exact inclusion-minimal Sylow-intersection profiles and simultaneous test.
# IsSubset(X,Y) in GAP means Y is a subset of X.

KourovkaSylowProfile := function(G,p)
local H,sylows,he,intersections,distinct,minimal,good,i,J;
H:=SylowSubgroup(G,p);
if IsNormal(G,H) then
  return rec(p:=p,H:=H,sylows:=[H],good_positions:=[1],good_fraction:=1,
             minimal_orders:=[Size(H)]);
fi;
sylows:=AsList(ConjugacyClassSubgroups(G,H));
he:=Set(AsList(H));
intersections:=List(sylows,K->Intersection(he,Set(AsList(K))));
distinct:=Set(intersections);
minimal:=Filtered(distinct,J->not ForAny(distinct,K->Length(K)<Length(J) and IsSubset(J,K)));
good:=Filtered([1..Length(sylows)],i->intersections[i] in minimal);
if IsEmpty(good) then Error("No inclusion-minimal intersection"); fi;
return rec(p:=p,H:=H,sylows:=sylows,good_positions:=good,
           good_fraction:=Length(good)/Length(sylows),
           minimal_orders:=Set(List(minimal,Length)));
end;

KourovkaSylowGoodSets := function(G,profile,elements)
local normalizer,normal_elements,transport,good,x,i,sets,indices;
normalizer:=Normalizer(G,profile.H);
normal_elements:=AsList(normalizer);
transport:=List(profile.sylows,K->RepresentativeAction(G,profile.H,K));
if fail in transport then Error("Missing Sylow transporter"); fi;
good:=[];
for i in profile.good_positions do
  for x in normal_elements do Add(good,x*transport[i]); od;
od;
good:=Set(good);
if Length(good)<>Size(G)*profile.good_fraction then Error("Coset fiber count mismatch"); fi;
sets:=[];
for x in transport do
  indices:=List(good,g->PositionSorted(elements,g^x));
  Add(sets,BlistList([1..Length(elements)],indices));
od;
profile.transport:=transport;
return sets;
end;

KourovkaCheck21_26 := function(G)
local profiles,badsum,elements,allsets,Search,branches,pruned,witness,result,
      totals,k,first,firstpos;
profiles:=List(Set(FactorsInt(Size(G))),p->KourovkaSylowProfile(G,p));
badsum:=Sum(profiles,r->1-r.good_fraction);
result:=rec(holds:=true,method:="union_bound",bad_sum:=badsum,
            primes:=List(profiles,r->r.p),
            good_fractions:=List(profiles,r->r.good_fraction),
            minimal_orders:=List(profiles,r->r.minimal_orders),branches:=0,pruned:=0);
if badsum<1 then return result; fi;
profiles:=Filtered(profiles,r->r.good_fraction<1);
Sort(profiles,function(a,b)
  if a.good_fraction<>b.good_fraction then return a.good_fraction<b.good_fraction; fi;
  return a.p<b.p;
end);
elements:=Set(AsList(G));
allsets:=List(profiles,r->KourovkaSylowGoodSets(G,r,elements));
branches:=0; pruned:=0;
totals:=List([1..Length(profiles)],k->Sum(profiles{[k..Length(profiles)]},r->Size(G)*(1-r.good_fraction)));

Search:=function(k,current,choices)
  local i,next,hit;
  branches:=branches+1;
  if SizeBlist(current)=0 then return choices; fi;
  if k>Length(profiles) then return fail; fi;
  if SizeBlist(current)>totals[k] then pruned:=pruned+1; return fail; fi;
  for i in [1..Length(allsets[k])] do
    next:=IntersectionBlist(current,allsets[k][i]);
    hit:=Search(k+1,next,Concatenation(choices,[i]));
    if hit<>fail then return hit; fi;
  od;
  return fail;
end;

# Simultaneous conjugation allows fixing one Sylow subgroup.
firstpos:=Position(profiles[1].sylows,profiles[1].H);
if firstpos=fail then Error("Base Sylow missing from its class"); fi;
witness:=Search(2,allsets[1][firstpos],[firstpos]);
result.method:="all_choices";
result.branches:=branches; result.pruned:=pruned;
result.holds:=witness=fail;
if witness<>fail then
  # An early empty intersection already certifies failure; append arbitrary
  # Sylows for any primes not yet chosen.
  while Length(witness)<Length(profiles) do Add(witness,1); od;
  result.counterexample_sylows:=List([1..Length(profiles)],k->profiles[k].sylows[witness[k]]);
  result.counterexample_primes:=List(profiles,r->r.p);
fi;
return result;
end;
