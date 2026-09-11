# Export the finite group and its coordinate transporters, without G^m.
Run647Input := function(n,id,output)
  local g,e,a,ap,orbits,reps,m,i,trans,oi,p,t,tab,identity,inv,orders;
  g:=SmallGroup(n,id);;
  e:=Elements(g);;
  a:=AutomorphismGroup(g);;
  ap:=Group(List(GeneratorsOfGroup(a),
      u->PermList(List(e,z->Position(e,Image(u,z))))));;
  orbits:=Orbits(ap,Tuples([1..n],2),OnTuples);;
  reps:=List(orbits,o->o[1]);;
  m:=Length(reps);;
  trans:=[];;oi:=[];;
  for i in [1..m] do
    for p in orbits[i] do
      t:=RepresentativeAction(ap,reps[i],p,OnTuples);;
      if t=fail then Error("missing transporter");fi;
      oi[(p[1]-1)*n+p[2]]:=i;;
      trans[(p[1]-1)*n+p[2]]:=List([1..n],z->z^t);;
    od;
  od;
  tab:=List(e,u->List(e,v->Position(e,u*v)));;
  identity:=Position(e,One(g));;
  inv:=List(e,u->Position(e,u^-1));;
  orders:=List(e,Order);;
  PrintTo(output,"{\"n\":",n,",\"id\":",id,
    ",\"status\":\"GROUP_INPUT_EXPORTED\",\"pair_orbits\":",m,
    ",\"exponent\":",Exponent(g),",\"identity\":",identity,
    ",\"nilpotency_class\":",NilpotencyClassOfGroup(g),
    ",\"table\":",tab,",\"inverse\":",inv,",\"orders\":",orders,
    ",\"representatives\":",reps,",\"orbit_index\":",oi,
    ",\"transporters\":",trans,"}\n");
  Print("PASS_647_INPUT\n");
end;
