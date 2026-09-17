# Targeted checks for Appendix M, written during the Codex review.
# Run from the repository root: gap-4.16.1/gap -q -b --quitonbreak \
#   paper/reviews/parallel-fable-2026-09-17/checks.g
# Only standard GAP and SmallGrp are used; no remote scripts are executed.
LoadPackage("smallgrp");;
Check := function(condition, message)
  if not condition then Error(message); fi;
end;;
Print("GAP ", GAPInfo.Version, " SmallGrp ",
      PackageInfo("smallgrp")[1].Version, "\n");

# 18.46: search directly for dihedral generators, without subgroup enumeration.
# Squares form a conjugacy-invariant set. Thus taking one representative of
# each class of order-four elements loses no possible D8 embedding.
HasSquareD8 := function(H)
  local squares, rotations, reflections, r, s, j;
  squares := Set(List(Elements(H), x -> x^2));
  rotations := Filtered(List(ConjugacyClasses(H), Representative),
                        x -> Order(x) = 4 and x in squares);
  reflections := Filtered(squares, x -> Order(x) = 2);
  for r in rotations do
    for s in reflections do
      if s <> r^2 and r^s = r^-1 and
         ForAll([0..3], j -> r^j*s in squares) then
        return true;
      fi;
    od;
  od;
  return false;
end;;
total := 0;;
for order in [8,16..120] do
  count := NrSmallGroups(order);
  for index in [1..count] do
    Check(not HasSquareD8(SmallGroup(order,index)),
          Concatenation("Unexpected witness ", String([order,index])));
  od;
  total := total + count;
  Print("18.46 excluded order ", order, ": ", count, " groups\n");
od;
Print("18.46 total groups below 128: ", total, "\n");
working := Filtered([1..NrSmallGroups(128)],
                    i -> HasSquareD8(SmallGroup(128,i)));;
Check(working = [134,136,138,139,140,141,144,146,928,929,930,931,932,933],
      "Order-128 list differs");
Print("18.46 order-128 witnesses: ", working, "\n");
W := WreathProduct(DihedralGroup(8), SymmetricGroup(2));;
Check(Size(W) = 128 and IdGroup(W) = [128,928] and HasSquareD8(W),
      "Wreath-product witness failed");
Print("18.46 wreath-product witness: ", IdGroup(W), "\n");

# 2.78: check the numerical invariant in a few members of the proposed family.
# This is a finite spot check, not a proof for all p,n,r or a priority claim.
SubgroupOrderData := function(H)
  local representatives, orders, badorders;
  representatives := List(ConjugacyClassesSubgroups(H), Representative);
  orders := Set(List(representatives, Size));
  badorders := Set(List(Filtered(representatives, S -> not IsNormal(H,S)), Size));
  return [Length(orders), Length(badorders)];
end;;
ModularGroup := function(p,n)
  local F,x,y;
  F := FreeGroup(2); x := F.1; y := F.2;
  return Image(IsomorphismPcGroup(F/[x^(p^(n-1)), y^p,
                                     y^-1*x*y*x^-(1+p^(n-2))]));
end;;
Check(SubgroupOrderData(AlternatingGroup(5)) = [9,7], "A5 count failed");
for parameters in [[3,3,0],[3,3,1],[3,4,1],[5,3,1],[7,3,0],[7,3,1],[7,4,0]] do
  p := parameters[1]; n := parameters[2]; r := parameters[3];
  P := DirectProduct(ModularGroup(p,n), CyclicGroup(p^r));
  data := SubgroupOrderData(P);
  Check(Size(P) = p^(n+r) and data = [n+r+1,r+1], "Family count failed");
  Print("2.78 p,n,r=", parameters, " order=", Size(P), " [|Ord|,f]=",data,"\n");
od;
basevalues := List([3..11], n -> 7*n+9);;
Check(Set(List(basevalues, x -> x mod 9)) = [0..8] and Maximum(basevalues)=86,
      "Residue coverage failed");
Print("2.78 bases ",basevalues,": all residues modulo 9, maximum 86\n");
Check(ForAll([78..86], k -> ForAny(basevalues, b -> k>=b and (k-b) mod 9=0)),
      "Improved threshold failed");
Check(not ForAny(basevalues, b -> 77>=b and (77-b) mod 9=0),
      "Unexpected representation of 77 in this family");
Print("2.78 same family covers every k >= 78; 77 is not represented\n");
# The supplementary assertion f(G)=7 iff G=A5 needs G nonsoluble.
D := DihedralGroup(512);;
badorders := Set(List(Filtered(List(ConjugacyClassesSubgroups(D), Representative),
                              S -> not IsNormal(D,S)), Size));;
Check(IsSolvableGroup(D) and badorders = [2,4,8,16,32,64,128],
      "Dihedral qualification check failed");
Print("2.78 soluble dihedral group of order 512: nonnormal orders ",badorders,
      ", f=7; nonsolubility hypothesis is necessary\n");
Print("ALL TARGETED CHECKS PASSED\n");
QUIT;
