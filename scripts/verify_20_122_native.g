SetAssertionLevel(2);
r:=(1,2,3,4);; s:=(2,4);; z:=(5,6);;
g:=Group((1,2),(1,2,3,4),z);;
a:=Group(r,s,z);; b:=Group(r*z,s);; c:=Group(r,z);;
t:=[r^2,(1,2)(3,4),(1,4)(2,3)];;
f:=Group(Concatenation(t,[z]));;
Assert(0,Size(g)=48 and IsSolvableGroup(g));
Assert(0,List([a,b,c],Size)=[16,8,8]);
Assert(0,ForAll([a,b,c],IsNilpotentGroup));
Assert(0,FittingSubgroup(g)=f);
elts:=SortedList(Elements(g),function(x,y)
    return List([1..6],i->i^x)<List([1..6],i->i^y);
end);;
encode:=h->SortedList(List(Elements(h),x->Position(elts,x)-1));;
bc:=Set(List(elts,x->encode(b^x)));;
cc:=Set(List(elts,x->encode(c^x)));;
family:=Set(Concatenation(List(elts,x->List(elts,y->
    encode(Intersection(a,b^x,c^y))))));;
minimal:=Filtered(family,h->not ForAny(family,k->Length(k)<Length(h) and IsSubset(h,k)));;
smallest:=Filtered(family,h->Length(h)=Minimum(List(family,Length)));;
upper:=Group(Concatenation(List(minimal,h->List(h,i->elts[i+1]))));;
lower:=Group(Concatenation(List(smallest,h->List(h,i->elts[i+1]))));;
Assert(0,Length(bc)=3 and Length(cc)=3 and Length(family)=6);
Assert(0,minimal=family and SortedList(List(family,Length))=[2,2,2,2,2,4]);
Assert(0,upper=a and lower=f and not IsSubgroup(f,upper));
out:=OutputTextFile("results/20.122-native-model.json",false);;
SetPrintFormattingStatus(out,false);
PrintTo(out,"{\"elements\":",List(elts,x->List([1..6],i->i^x)),
    ",\"table\":",List(elts,x->List(elts,y->Position(elts,x*y)-1)),
    ",\"a\":",encode(a),",\"b\":",encode(b),",\"c\":",encode(c),
    ",\"fit\":",encode(f),",\"b_orbit\":",bc,",\"c_orbit\":",cc,
    ",\"family\":",family,",\"minimal\":",minimal,",\"smallest\":",smallest,
    ",\"Min\":",encode(upper),",\"min\":",encode(lower),"}\n");
CloseStream(out);
Print("NATIVE_20122 ",[Size(g),List([a,b,c],Size),Length(bc),Length(cc),
    SortedList(List(family,Length)),Size(upper),Size(lower)],"\n");
Print("PASS_20_122_NATIVE pairs=2304\n");
QUIT;
