# Finite controls only: no finite run proves unbounded width.
SetAssertionLevel(1);
Main1993:=function()
local F1993,x1993,y1993,T1993,c1993,h1993,G1993,im1993,s1993,
widths1993,W1993,p1993,el1993,tor1993,gen1993,bad1993,u1993,v1993;
F1993:=FreeGroup("x","y");;
x1993:=F1993.1;; y1993:=F1993.2;;
T1993:=F1993/[x1993^7,y1993^7,(x1993*y1993)^7];;
for c1993 in [2..8] do
  h1993:=EpimorphismPGroup(T1993,7,c1993);;
  G1993:=Image(h1993);;
  im1993:=List(GeneratorsOfGroup(T1993),x->Image(h1993,x));;
  Assert(0,ForAll([im1993[1],im1993[2],im1993[1]*im1993[2]],x->x^7=One(G1993)));
  Assert(0,Size(Group(im1993))=Size(G1993));
  s1993:=PCentralSeries(G1993,7);;
  widths1993:=List([1..Length(s1993)-1],i->LogInt(Index(s1993[i],s1993[i+1]),7));;
  Assert(0,widths1993[1]=2);
  Print("TRIANGLE p=7 class=",c1993," log_order=",LogInt(Size(G1993),7)," widths=",widths1993,"\n");
od;
W1993:=Group(());;
for p1993 in [2,3] do
  W1993:=WreathProduct(CyclicGroup(IsPermGroup,p1993),CyclicGroup(IsPermGroup,p1993));;
  el1993:=Elements(W1993);;
  tor1993:=Filtered(el1993,x->x^p1993=One(W1993));;
  gen1993:=0;; bad1993:=0;;
  for u1993 in tor1993 do
    for v1993 in tor1993 do
      if Size(Group(u1993,v1993))=Size(W1993) then
        gen1993:=gen1993+1;
        Assert(0,Order(u1993*v1993)=p1993^2);
        if (u1993*v1993)^p1993=One(W1993) then bad1993:=bad1993+1;fi;
      fi;
    od;
  od;
  Assert(0,gen1993>0 and bad1993=0);
  Print("WREATH p=",p1993," order=",Size(W1993)," torsion=",Length(tor1993)," generating_torsion_pairs=",gen1993," bad=",bad1993,"\n");
od;
Print("PASS_1993_GAP\n");
end;
Main1993();
QUIT;
