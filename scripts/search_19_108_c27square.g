# Exact 19.108 search in (C27 x C27) semidirect H, |H|=81.
# Subgroups are enumerated up to conjugacy in a Sylow 3-subgroup of GL(2,Z/27).
# A degree-81 irreducible is induced from a regular dual orbit. Smaller degrees
# are already covered by Wilde 2013, Theorem C. No other families are covered.
Run19108:=function()
local q,p,target,points,idx,perm,gens,s,iso,pc,subs,j,h,hp,orbs,o,
      regular,periodic,checks,hits,v,w,x,y,hist,a,b,c,val,found,started;
q:=27;p:=3;target:=81;started:=Runtime();
SizeScreen([1000000,1000000]);
points:=Tuples([0..q-1],2);
idx:=v->q*v[1]+v[2]+1;
perm:=m->PermList(List(points,v->idx([
    (v[1]*m[1][1]+v[2]*m[2][1]) mod q,
    (v[1]*m[1][2]+v[2]*m[2][2]) mod q])));
gens:=List([[[1,1],[0,1]],[[1,0],[3,1]],[[4,0],[0,1]],[[1,0],[0,4]]],perm);
s:=Group(gens);
if Size(s)<>3^9 then Error("wrong Sylow order"); fi;
Print("BEGIN modulus=27 module_order=729 complement_order=81 sylow_order=",Size(s),"\n");
iso:=IsomorphismPcGroup(s);pc:=Image(iso);
subs:=SubgroupsSolvableGroup(pc,rec(consider:=ExactSizeConsiderFunction(target)));
Print("ENUMERATOR_RETURNED classes=",Length(subs),"\n");
# The documented option permits extra intermediate subgroups in its result.
subs:=Filtered(subs,h->Size(h)=target);
Print("ENUMERATED subgroup_classes=",Length(subs)," ms=",Runtime()-started,"\n");
regular:=0;checks:=0;hits:=0;
for j in [1..Length(subs)] do
    h:=subs[j];if Size(h)<>target then Error("wrong subgroup order");fi;
    hp:=Group(List(GeneratorsOfGroup(h),g->PreImagesRepresentative(iso,g)));
    if Size(hp)<>target then Error("wrong lifted subgroup order");fi;
    Print("DATA class=",j," matrices=",
          List(GeneratorsOfGroup(hp),g->[points[(q+1)^g],points[2^g]]),"\n");
    orbs:=Orbits(hp,[1..q^2]);
    if Sum(orbs,Length)<>q^2 then Error("orbit coverage");fi;
    for o in orbs do
        if Length(o)<>target then continue;fi;
        regular:=regular+1;o:=Set(o);periodic:=true;
        for v in o do
            w:=points[v];
            if not idx([(w[1]+9) mod q,w[2]]) in o or
               not idx([w[1],(w[2]+9) mod q]) in o then
                periodic:=false;break;
            fi;
        od;
        checks:=checks+1;
        if not periodic then
            # Exact cyclotomic reduction, independent of the translation test.
            found:=false;
            for x in points do
                if x[1] mod p=0 and x[2] mod p=0 then continue;fi;
                hist:=List([1..q],z->0);
                for v in o do
                    y:=points[v];a:=(x[1]*y[1]+x[2]*y[2]) mod q;
                    hist[a+1]:=hist[a+1]+1;
                od;
                if ForAny([1..9],a->hist[a]<>hist[a+9] or hist[a]<>hist[a+18]) then
                    val:=Sum([0..26],a->hist[a+1]*E(27)^a);
                    if val=0 then Error("cyclotomic disagreement");fi;
                    hits:=hits+1;found:=true;
                    Print("HIT class=",j," orbit=",o," x=",x," value=",val,
                          " generators=",GeneratorsOfGroup(hp),"\n");break;
                fi;
            od;
            if not found then Error("Fourier criterion disagreement");fi;
        fi;
    od;
    Print("SUBGROUP class=",j," regular_orbits_total=",regular," hits=",hits,"\n");
od;
Print("DONE subgroup_classes=",Length(subs)," regular_orbits=",regular,
      " periodicity_checks=",checks," hits=",hits," ms=",Runtime()-started,"\n");
end;
Run19108();
QUIT;
