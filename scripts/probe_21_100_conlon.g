# Reproduce the duplicate output and cache-order effect without modifying GAP.
SizeScreen([100000,100000]);;
Probe21100:=function()
  local g,i,c,u,h,d,j;
  g:=SmallGroup(729,268); i:=Irr(g); c:=IrrConlon(g); u:=Set(c);
  Print("STANDARD_FIRST ",[Length(i),Sum(i,x->x[1]^2),Length(c),Length(u),
    Sum(u,x->x[1]^2),Set(List(u,x->ScalarProduct(x,x))),Set(i)=u],"\n");
  if Length(i)<>105 or Length(c)<>153 or Sum(i,x->x[1]^2)<>729
    or Set(i)<>u then Error("unexpected Conlon control"); fi;
  h:=SmallGroup(729,268); d:=IrrConlon(h); j:=Irr(h);
  Print("CONLON_FIRST ",[Length(d),Length(j),Sum(j,x->x[1]^2),
    Length(Set(d)),Sum(Set(d),x->x[1]^2)],"\n");
  if Length(d)<>153 or Length(j)<>153 or Sum(j,x->x[1]^2)<>2025
    or Length(Set(d))<>105 then Error("unexpected Conlon cache control"); fi;
  Print("PASS_21100_CONLON_DUPLICATES\n");
end;;
Probe21100();
QUIT_GAP(0);
