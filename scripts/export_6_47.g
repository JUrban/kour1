# Exact binary word-function group, reduced by automorphism orbits.
# The launcher calls Run647(n,id,cap,output) in a fresh GAP process.
Run647 := function(n,id,cap,output)
  local g,e,a,ap,orbits,reps,m,dp,x,y,i,emb,f,c,sz,trans,oi,p,t,
        values,op,d,pr,tab,identity,inv,orders,restr;
  g:=SmallGroup(n,id);;
  e:=Elements(g);;
  a:=AutomorphismGroup(g);;
  ap:=Group(List(GeneratorsOfGroup(a),
      u->PermList(List(e,z->Position(e,Image(u,z))))));;
  orbits:=Orbits(ap,Tuples([1..n],2),OnTuples);;
  reps:=List(orbits,o->o[1]);;
  m:=Length(reps);;
  Print("START_647 n=",n," id=",id," pair_orbits=",m,"\n");
  dp:=DirectProduct(List([1..m],i->g));;
  x:=One(dp);;y:=One(dp);;
  for i in [1..m] do
    emb:=Embedding(dp,i);;
    x:=x*Image(emb,e[reps[i][1]]);;
    y:=y*Image(emb,e[reps[i][2]]);;
  od;
  f:=Group(x,y);;c:=DerivedSubgroup(f);;sz:=Size(c);;
  Print("FUNCTION_GROUP_647 size=",Size(f)," normalized=",sz,"\n");
  if Size(f)/sz<>Exponent(g)^2 then
    Error("unexpected abelianization of the binary function group");
  fi;
  if sz>cap then
    PrintTo(output,"{\"n\":",n,",\"id\":",id,
      ",\"status\":\"SKIP_CAP\",\"pair_orbits\":",m,
      ",\"function_group_order\":",Size(f),
      ",\"normalized_count\":",sz,",\"cap\":",cap,"}\n");
    Print("PASS_647_EXPORT_SKIPPED\n");
    return;
  fi;
  trans:=[];;oi:=[];;
  for i in [1..m] do
    for p in orbits[i] do
      t:=RepresentativeAction(ap,reps[i],p,OnTuples);;
      if t=fail then Error("missing transporter");fi;
      oi[(p[1]-1)*n+p[2]]:=i;;
      trans[(p[1]-1)*n+p[2]]:=List([1..n],z->z^t);;
    od;
  od;
  pr:=List([1..m],i->Projection(dp,i));;
  values:=[];;
  for d in Elements(c) do
    op:=x*y*d;;
    Add(values,List(pr,q->Position(e,Image(q,op))));;
  od;
  tab:=List(e,u->List(e,v->Position(e,u*v)));;
  identity:=Position(e,One(g));;
  inv:=List(e,u->Position(e,u^-1));;
  orders:=List(e,Order);;
  PrintTo(output,"{\"n\":",n,",\"id\":",id,
    ",\"status\":\"EXPORTED\",\"pair_orbits\":",m,
    ",\"function_group_order\":",Size(f),
    ",\"normalized_count\":",sz,",\"cap\":",cap,
    ",\"exponent\":",Exponent(g),",\"identity\":",identity,
    ",\"table\":",tab,",\"inverse\":",inv,",\"orders\":",orders,
    ",\"representatives\":",reps,",\"orbit_index\":",oi,
    ",\"transporters\":",trans,",\"word_functions\":",values,"}\n");
  Print("PASS_647_EXPORT\n");
end;
