# Independent small controls: direct squares and central involution counts.
LoadPackage("smallgrp");;
SizeScreen([1000000,1000000]);;
(function()
local n,i,g,elts,gens,one,invols,centralInvols,central,squares,d,zrank,
      checked,admissible,exponentFour,rankViolations;
checked:=0; admissible:=0; exponentFour:=0; rankViolations:=0;
for n in [2,4,8,16,32,64] do
  for i in [1..NumberSmallGroups(n)] do
    g:=SmallGroup(n,i); elts:=Elements(g); gens:=GeneratorsOfGroup(g); one:=One(g);
    invols:=Filtered(elts,x->x^2=one);
    centralInvols:=Filtered(invols,x->ForAll(gens,y->x*y=y*x));
    central:=Length(invols)=Length(centralInvols);
    zrank:=LogInt(Length(centralInvols),2);
    squares:=Subgroup(g,Set(List(elts,x->x^2)));
    d:=LogInt(Index(g,squares),2);
    if Length(centralInvols)<>2^zrank then Error("central involution count"); fi;
    if squares<>FrattiniSubgroup(g) then Error("squares versus Frattini"); fi;
    if zrank<>Length(AbelianInvariants(Centre(g))) then Error("centre rank"); fi;
    if central<>IsSubgroup(Centre(g),Omega(g,2,1)) then Error("Omega condition"); fi;
    if d>2*zrank then rankViolations:=rankViolations+1; fi;
    if central then
      admissible:=admissible+1;
      if d>2*zrank then Error("counterexample in control range"); fi;
      if ForAll(elts,x->x^4=one) then
        exponentFour:=exponentFour+1;
        if LogInt(Index(g,Subgroup(g,invols)),2)>2*LogInt(Size(squares),2) then
          Error("quadratic dimension bound");
        fi;
      fi;
    fi;
    checked:=checked+1;
  od;
od;
Print("DONE checked=",checked," central_involution_groups=",admissible,
      " exponent_four_groups=",exponentFour," rank_violations_excluded=",
      rankViolations," ALL CHECKS PASS\n");
end)();
QUIT;
