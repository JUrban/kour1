LoadPackage("fga");;
Run208:=function()
local f,a,b,u,v,h,j,k,d,t,x,y,kd,gm,hm,gens,w,cases,c,words,checks;
f:=FreeGroup("a","b");a:=f.1;b:=f.2;
u:=(a^-1*b)^2;v:=(a^-2*b^2)^2;
h:=Subgroup(f,[a,u,v]);j:=Subgroup(f,[b,u,v]);
k:=Subgroup(f,[u,a*u*a^-1,v,a^2*v*a^-2]);
if RankOfFreeGroup(h)<>3 or RankOfFreeGroup(j)<>3 or RankOfFreeGroup(k)<>4 then
    Error("incorrect target subgroup ranks");fi;
d:=FreeGroup("t","x","y");t:=d.1;x:=d.2;y:=d.3;
gens:=[x,t*x*t^-1,y,t^2*y*t^-2];kd:=Subgroup(d,gens);
if RankOfFreeGroup(kd)<>4 then Error("incorrect domain rank");fi;
gm:=GroupHomomorphismByImages(d,f,[t,x,y],[a,u,v]);
hm:=GroupHomomorphismByImages(d,f,[t,x,y],[b,u,v]);
if gm=fail or hm=fail then Error("homomorphism construction");fi;
if not ForAll(gens,w->Image(gm,w)=Image(hm,w)) then Error("not fixed");fi;
if Image(gm,t)=Image(hm,t) then Error("maps not distinct");fi;
# The two possible proper core-image quotients have ranks four.
cases:=[[kd,4],[Subgroup(d,Concatenation(gens,[t^2])),4],
        [Subgroup(d,Concatenation(gens,[t])),3]];
for c in cases do
    if RankOfFreeGroup(c[1])<>c[2] then Error("quotient rank");fi;
od;
checks:=0;
words:=[One(d)];
for c in [1..3] do
    words:=Set(Concatenation(words,List(Cartesian(words,Concatenation(gens,List(gens,Inverse))),w->w[1]*w[2])));
od;
for w in words do
    if Image(gm,w)<>Image(hm,w) then Error("short-word equality");fi;
    checks:=checks+1;
od;
Print("PASS target_ranks=3,3,4 domain_rank=4 quotient_ranks=4,4,3 fixed_words=",checks," maps_distinct=true\n");
end;
Run208();
QUIT;
