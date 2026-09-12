SetAssertionLevel(2);
pts:=Cartesian([0..2],[0..2]);;
perm:=f->PermList(List(pts,x->Position(pts,f(x))));;
tx:=perm(x->[(x[1]+1) mod 3,x[2]]);;
ty:=perm(x->[x[1],(x[2]+1) mod 3]);;
sx:=perm(x->[(-x[1]) mod 3,x[2]]);;
sw:=perm(x->[x[2],x[1]]);;
q:=Group(tx,ty,sx,sw);; h:=Stabilizer(q,1);;
lift:=p->PermList(List([1..18],j->2*((QuoInt(j-1,2)+1)^p-1)+((j-1) mod 2)+1));;
flips:=List([1..9],i->(2*i-1,2*i));;
g:=Group(Concatenation(flips,List(GeneratorsOfGroup(q),lift)));;
base:=Group(flips);; a:=Group(Concatenation([flips[1]],List(GeneratorsOfGroup(h),lift)));;
b:=Stabilizer(g,1);;
bs:=List([1..9],i->Stabilizer(g,2*i-1));;
Assert(0,Size(q)=72 and Size(h)=8 and Size(g)=36864);
Assert(0,Size(a)=16 and Size(b)=2048 and ForAll([a,b],IsNilpotentGroup));
Assert(0,IsSolvableGroup(g) and FittingSubgroup(g)=base and Size(base)=512);
Assert(0,Length(Set(bs))=9 and Set(Elements(ConjugacyClassSubgroups(g,b)))=Set(bs));
Assert(0,ForAll([1..9],i->Stabilizer(g,2*i)=bs[i]));
qe:=Elements(q);; ae:=Elements(a);;
enc:=k->SortedList(List(Elements(k),x->PositionSorted(ae,x)-1));;
pairtable:=List(bs,u->List(bs,v->enc(Intersection(a,u,v))));;
family:=Set(Concatenation(pairtable));;
minimal:=Filtered(family,u->not ForAny(family,v->Length(v)<Length(u) and IsSubset(u,v)));;
smallest:=Filtered(family,u->Length(u)=Minimum(List(family,Length)));;
lower:=Group(Concatenation(List(smallest,u->List(u,i->ae[i+1]))));;
upper:=Group(Concatenation(List(minimal,u->List(u,i->ae[i+1]))));;
Assert(0,SortedList(List(family,Length))=[2,2,2,2,2,4,4,4,4,8]);
Assert(0,Length(minimal)=5 and minimal=smallest and lower=a and upper=a);
outside:=Intersection(a,bs[1],bs[2]);;
Assert(0,Size(outside)=2 and not IsSubgroup(base,outside));
vec9:=p->List([1..9],i->i^p);; vec18:=p->List([1..18],i->i^p);;
out:=OutputTextFile("results/20.122-minimum-native-model.json",false);;
SetPrintFormattingStatus(out,false);
PrintTo(out,"{\"q_elements\":",List(qe,vec9),",\"q_table\":",List(qe,x->List(qe,y->PositionSorted(qe,x*y)-1)),
    ",\"g_generators\":",List(GeneratorsOfGroup(g),vec18),
    ",\"a_elements\":",List(ae,vec18),",\"a_table\":",List(ae,x->List(ae,y->PositionSorted(ae,x*y)-1)),
    ",\"b_generators\":",List(GeneratorsOfGroup(b),vec18),
    ",\"b_orbit_generators\":",List(bs,k->List(GeneratorsOfGroup(k),vec18)),
    ",\"b_orbit_orders\":",List(bs,Size),",\"a_meets_b\":",List(bs,k->enc(Intersection(a,k))),
    ",\"pair_table\":",pairtable,",\"family\":",family,",\"minimal\":",minimal,
    ",\"smallest\":",smallest,",\"Min\":",enc(upper),",\"min\":",enc(lower),
    ",\"outside\":",enc(outside),",\"orders\":[",Size(g),",",Size(q),",",Size(a),",",Size(b),",",Size(base),"]}\n");
CloseStream(out);
Print("MINIMUM_20122 ",[Size(g),Size(q),Size(a),Size(b),Size(base),Length(bs),Length(family),
    Length(smallest),Size(lower),Size(upper)],"\n");
Print("PASS_20_122_MINIMUM_NATIVE pairs=81\n");
QUIT;
