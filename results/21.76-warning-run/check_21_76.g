# Independent finite-field and matrix-group calculation for Notebook 21.76.
F2176 := GF(9);;
j2176 := Z(9)^2;;
one2176 := One(F2176);;
zero2176 := Zero(F2176);;
if j2176^2 <> -one2176 then Error("wrong quadratic generator"); fi;
Decode2176 := x -> (x mod 3)*one2176 + QuoInt(x,3)*j2176;;
Encode2176 := x -> Position(List([0..8],Decode2176),x)-1;;
U2176 := [[one2176,one2176],[zero2176,one2176]];;
orders2176 := [24,24,120,720,720,120,720,720];;
for beta2176 in [1..8] do
  V2176 := [[one2176,zero2176],[Decode2176(beta2176),one2176]];
  G2176 := Group(U2176,V2176);
  if Size(G2176) <> orders2176[beta2176] then Error("wrong order"); fi;
  upper2176 := Filtered([0..8],a -> [[one2176,Decode2176(a)],[zero2176,one2176]] in G2176);
  lower2176 := Filtered([0..8],a -> [[one2176,zero2176],[Decode2176(a),one2176]] in G2176);
  Print("BETA ",beta2176," ORDER ",Size(G2176)," UPPER ",upper2176," LOWER ",lower2176,"\n");
  if beta2176 = 3 then
    if upper2176 <> [0,1,2] or lower2176 <> [0,3,6] then Error("wrong intersections"); fi;
    matrices2176 := SortedList(List(Elements(G2176),g -> List(Concatenation(g),Encode2176)));
    PrintTo("results/21.76-gap-matrices.json",matrices2176,"\n");
  fi;
od;
Print("PASS_2176_GAP cases=8 seed_order=120\n");
QUIT_GAP(0);
