# Explicit order-four coset in the multiple holomorph of a centerless group.
# Construct the regular group on triples, then identify its GAP SmallGroup ID.
RunCheck:=function()
local p,l,pts,idx,perm,left,regular,hol,theta,aut,g,h,multi;
p:=11; l:=3;
pts:=Cartesian([0..p-1],[0..p-1],[0..4]);
idx:=v->1+55*(v[1] mod p)+5*(v[2] mod p)+(v[3] mod 5);
perm:=f->PermList(List(pts,v->idx(f(v))));
left:=[perm(v->[v[1]+1,v[2],v[3]]),
       perm(v->[v[1],v[2]+1,v[3]]),
       perm(v->[l*v[1],l^2*v[2],v[3]+1])];
regular:=Group(left);
if Size(regular)<>605 or Size(Centre(regular))<>1 or
   not IsRegular(regular,[1..605]) then Error("group hypotheses failed"); fi;
Print("GROUP id=",IdGroup(regular)," order=",Size(regular)," center=1\n");
hol:=Group([
    perm(v->[2*v[1],v[2],v[3]]),
    perm(v->[v[1]+1,v[2],v[3]]),
    perm(v->[v[1]+l^v[3],v[2],v[3]]),
    perm(v->[v[1],2*v[2],v[3]]),
    perm(v->[v[1],v[2]+1,v[3]]),
    perm(v->[v[1],v[2]+l^(2*v[3]),v[3]]),
    perm(v->[v[1],v[2],v[3]+1])
]);
if not IsSubgroup(hol,regular) then Error("missing translations"); fi;
for h in GeneratorsOfGroup(hol) do
    for g in left do
        if not g^h in regular then Error("not a normalizer element"); fi;
    od;
od;
aut:=AutomorphismGroup(SmallGroup(605,5));
if Size(aut)<>12100 or Size(hol)<>605*Size(aut) then
    Error("full holomorph order failed");
fi;
Print("HOLOMORPH order=",Size(hol)," automorphism_order=",Size(aut),"\n");
theta:=perm(v->[v[2],l^((-v[3]) mod 5)*v[1],2*v[3]]);
for h in GeneratorsOfGroup(hol) do
    if not h^theta in hol then Error("theta does not normalize holomorph"); fi;
od;
if Order(theta)<>4 or theta^2 in hol then Error("coset order failed"); fi;
multi:=Group(Concatenation(GeneratorsOfGroup(hol),[theta]));
if Index(multi,hol)<>4 then Error("extension quotient order failed"); fi;
Print("CERTIFICATE theta_order=4 square_in_holomorph=false generated_index=4\n");
Print("DONE all605points_checked=true normalizer_generator_checks=7 PASS\n");
end;
RunCheck();
QUIT;
