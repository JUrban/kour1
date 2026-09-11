# Independent finite-field point, orbit and tangent-space controls.
SetAssertionLevel(2);
(function()
local q,F,z,ii,Pts,x,y,u,v,p,sigma,power,t,orb,orbits,seen,idx,
      fixed,fixed2,jac,coords,values,fibers,k,rank,fixedrank,quotient,
      total,totalorbits,totalfixed,totalpairs,a,d,key;
total:=0; totalorbits:=0; totalfixed:=0; totalpairs:=0;
for q in [5,13,17,29,37] do
  F:=GF(q); z:=Zero(F); ii:=Z(q)^((q-1)/4);
  Assert(0,ii^2=-One(F));
  Pts:=[];
  for x in F do for y in F do
    if y^2=x^3-x then
      if x<>z then
        for u in F do Add(Pts,[x,y,u,y*u/x]); od;
      else
        for v in F do Add(Pts,[x,y,z,v]); od;
      fi;
    fi;
  od; od;
  Pts:=Set(Pts);
  sigma:=p->[-p[1],ii*p[2],ii*p[3],p[4]];
  fixed:=Filtered(Pts,p->sigma(p)=p);
  fixed2:=Filtered(Pts,p->sigma(sigma(p))=p);
  Assert(0,fixed=Set(List(F,v->[z,z,z,v])));
  Assert(0,Length(fixed2)=q+2);
  Assert(0,Difference(fixed2,fixed)=Set([[One(F),z,z,z],[-One(F),z,z,z]]));
  values:=[]; fibers:=[];
  for p in Pts do
    x:=p[1]; y:=p[2]; u:=p[3]; v:=p[4];
    Assert(0,y*u=x*v and (x^2-1)*u=y*v);
    t:=p;
    for k in [1..4] do t:=sigma(t); Assert(0,t in Pts); od;
    Assert(0,t=p);
    jac:=[[1-3*x^2,2*y,z,z],[-v,u,y,-x],[2*x*u,-v,x^2-1,-y]];
    Assert(0,RankMat(jac)=2);
    if p in fixed then
      fixedrank:=RankMat(Concatenation(jac,[[One(F),z,z,z],[z,One(F),z,z],[z,z,One(F),z]]));
      Assert(0,fixedrank=3);
    fi;
    a:=x^2; d:=x*u^2-v^2;
    Assert(0,v^2=(a-1)*d and x*d=u^2);
    key:=[a,v,d]; idx:=Position(values,key);
    if idx=fail then Add(values,key); Add(fibers,[p]);
    else Add(fibers[idx],p); fi;
  od;
  # The proposed global invariants must separate every rational G-orbit.
  for orb in fibers do
    p:=orb[1]; t:=p; seen:=[];
    for k in [1..4] do AddSet(seen,t); t:=sigma(t); od;
    Assert(0,Set(orb)=seen);
    totalpairs:=totalpairs+Length(orb)^2;
  od;
  # The node has zero gradient; every other rational quotient point is smooth.
  quotient:=[];
  for a in F do for v in F do for d in F do
    if v^2=(a-1)*d then
      Add(quotient,[a,v,d]);
      Assert(0,([-d,2*v,1-a]=[z,z,z])=([a,v,d]=[One(F),z,z]));
    fi;
  od; od; od;
  Assert(0,Length(fibers[Position(values,[One(F),z,z])])=2);
  Print("PASS q=",q," smooth_surface_points=",Length(Pts)," fixed_line_points=",Length(fixed),
        " proper_stabilizer_points=2 orbits=",Length(fibers),
        " quotient_points=",Length(quotient),"\n");
  total:=total+Length(Pts); totalorbits:=totalorbits+Length(fibers);
  totalfixed:=totalfixed+Length(fixed);
od;
Print("DONE surface_points=",total," orbits=",totalorbits," fixed_points=",totalfixed,
      " orbit_pair_controls=",totalpairs,"\n");
end)();
QUIT;
