# Exact finite controls for the triangular filtration and a common ambient sink.
SetAssertionLevel(1);;
Check2089 := function(ok) if not ok then Error("20.89 check failed"); fi; end;;
field := GF(3);; one := One(field);;
gens := [];;
for i in [1..3] do
  m := IdentityMat(3,field);; m[i][i] := -one;; Add(gens,m);
od;
for ij in [[1,2],[1,3],[2,3]] do
  m := IdentityMat(3,field);; m[ij[1]][ij[2]] := one;; Add(gens,m);
od;
g := Group(gens);; el := Elements(g);;
Check2089(Size(g)=216);;
pairs := [[1,3],[1,2],[2,3]];;
u := Filtered(el,x->ForAll([1..3],i->x[i][i]=one));;
chain := [[One(g)]];;
for s in [1..3] do
  Add(chain,Filtered(u,x->ForAll([1..3],j->j<=s or x[pairs[j][1]][pairs[j][2]]=Zero(field))));
od;
Check2089(List(chain,Length)=[1,3,9,27]);;
count := 0;; centralCount := 0;;
for s in [1..3] do
  ij := pairs[s];;
  for x in chain[s+1] do
    for a in el do
      y := x^a;;
      Check2089(y in chain[s+1]);
      Check2089(y[ij[1]][ij[2]]=x[ij[1]][ij[2]]*a[ij[2]][ij[2]]/a[ij[1]][ij[1]]);
      count := count+1;
    od;
    for a in u do Check2089(Comm(x,a) in chain[s]); centralCount:=centralCount+1; od;
  od;
od;
Print("FILTRATION_2089 ",[Size(g),List(chain,Length),count,centralCount],"\n");

# Two affine blocks over F_(3^r). First translation block is only F_3.
mixedRows := [];;
for r in [1..3] do
  f := GF(3^r);; z := One(f);; gens := [];; pgens := [];;
  m := IdentityMat(4,f);; m[1][2]:=z;; Add(gens,m);; Add(pgens,m);
  m := IdentityMat(4,f);; m[1][1]:=-z;; Add(gens,m);; Add(pgens,m);
  for b in BasisVectors(Basis(f)) do
    m:=IdentityMat(4,f);; m[3][4]:=b;; Add(gens,m);; Add(pgens,m);
  od;
  m:=IdentityMat(4,f);; m[3][3]:=-z;; Add(gens,m);
  gg:=Group(gens);; pp:=Group(pgens);;
  Check2089(Size(gg)=12*3^r and Size(pp)=6*3^r);
  checks:=0;;
  for x in Elements(gg) do
    for a in Elements(pp) do
      y:=Comm(Comm(x,a),a);;
      Check2089(y[3][3]=z and IsZero(y[3][4]));
      checks:=checks+1;
    od;
  od;
  fixed:=0;;
  for b in Elements(f) do
    x:=IdentityMat(4,f);; x[3][4]:=b;;
    Check2089(Comm(x,m)=x); fixed:=fixed+1;
  od;
  Add(mixedRows,[r,Size(gg),Size(pp),checks,fixed]);
od;
Print("MIXED_2089 ",mixedRows,"\n");
# A finite minimal sink subgroup need not be normal in its ambient group.
f:=GF(3);; aa:=IdentityMat(3,f);; aa[1][1]:=-One(f);;
swap:=IdentityMat(3,f);; swap[1][1]:=Zero(f);; swap[2][2]:=Zero(f);;
swap[1][2]:=One(f);; swap[2][1]:=One(f);;
tx:=IdentityMat(3,f);; tx[1][3]:=One(f);;
ty:=IdentityMat(3,f);; ty[2][3]:=One(f);;
gg:=Group(aa,swap,tx,ty);; sink:=[];;
for x in Elements(gg) do
  orbit:=[];; y:=x;;
  while not y in orbit do Add(orbit,y); y:=Comm(y,aa); od;
  pos:=Position(orbit,y);;
  sink:=Union(sink,orbit{[pos..Length(orbit)]});
od;
dd:=Group(sink);;
Check2089(Size(gg)=72 and Length(sink)=3 and Size(dd)=3);
Check2089(not IsNormal(gg,dd) and Size(NormalClosure(gg,dd))=9);
Print("SINK_2089 ",[72,3,3,9],"\n");
Print("PASS_20_89_NATIVE\n");
QUIT_GAP(0);
