SizeScreen([100000,100000]);;
Check1739:=function(b,s) if not b then Error(s); fi; end;;
Model1739:=function(p,d)
local f,n,id,us,vs,z,t,i,m,g,pp,tt,dd,cs,els,pairs,states,next,s,c,depth,hist,mins,chain,inter;
f:=GF(p);n:=d+2;id:=IdentityMat(n,f);us:=[];vs:=[];
for i in [1..d] do
 m:=MutableCopyMat(id);m[1][i+1]:=One(f);Add(us,m);
 m:=MutableCopyMat(id);m[i+1][n]:=One(f);Add(vs,m);
od;
z:=MutableCopyMat(id);z[1][n]:=One(f);
t:=MutableCopyMat(id);t[n][n]:=-One(f);
g:=Group(Concatenation(us,vs,[z,t]));pp:=Subgroup(g,Concatenation(us,vs,[z]));tt:=Subgroup(g,[t]);
dd:=Normalizer(g,tt);
Check1739(Size(g)=2*p^(2*d+1) and IsSolvableGroup(g),"group size or solubility");
Check1739(IsNormal(g,pp) and Size(pp)=p^(2*d+1),"Sylow p");
Check1739(Size(tt)=2 and Normalizer(g,pp)=g,"Sylow basis");
Check1739(dd=Centralizer(g,t) and dd=Subgroup(g,Concatenation(us,[t])),"system normalizer");
Check1739(Size(Centre(g))=1 and Size(Core(g,dd))=1,"center or core");
Check1739(Size(FrattiniSubgroup(g))=p,"Frattini");
cs:=AsList(ConjugacyClassSubgroups(g,dd));
Check1739(Length(cs)=p^(d+1),"number of normalizers");
# All intersections can be conjugated to contain the fixed first factor D.
# Retain element sets; deduplication removes paths, not possible states.
els:=Set(Elements(dd));pairs:=Set(List(cs,c->Intersection(els,Set(Elements(c)))));
states:=[els];hist:=[];mins:=[];depth:=1;
while true do
 Add(hist,Collected(List(states,Length)));Add(mins,Minimum(List(states,Length)));
 if 1 in List(states,Length) then break;fi;
 next:=[];for s in states do for c in pairs do AddSet(next,Intersection(s,c));od;od;
 Check1739(next<>states,"no progress");states:=next;depth:=depth+1;
od;
Check1739(depth=d+1,"exact minimum");
chain:=[Size(dd)];inter:=dd;
for i in [1..d] do inter:=Intersection(inter,dd^vs[i]);Add(chain,Size(inter));od;
Check1739(Last(chain)=1,"explicit witness");
Print("ROW1739 ",[p,d,Size(g),Size(dd),Length(cs),Length(pairs),mins,hist,chain],"\n");
end;;
for spec1739 in [[3,1],[3,2],[3,3],[3,4],[5,1],[5,2],[7,1]] do Model1739(spec1739[1],spec1739[2]);od;
Print("PASS_17_39_NATIVE\n");
QUIT_GAP(0);
