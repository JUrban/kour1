# Finite controls of a prior construction; the proof is in the report.
SetAssertionLevel(1);
Main17113:=function()
local F,a,b,p,n,T,h,G,im,lc,ab,count;
F:=FreeGroup("a","b"); a:=F.1; b:=F.2; count:=0;
for p in [2,3,5,7,11] do
  for n in [1..6] do
    T:=F/[b^-1*a*b*a^(-1-p),b^(p^n)*a^(-p^n)];
    h:=EpimorphismPGroup(T,p,n+2);
    G:=Image(h);
    im:=List(GeneratorsOfGroup(T),x->Image(h,x));
    lc:=LowerCentralSeries(G);
    ab:=AbelianInvariants(G);
    Assert(0,Size(G)=p^(2*n+1));
    Assert(0,Length(lc)-1=n+1);
    Assert(0,ab=[p,p^n]);
    Assert(0,Order(im[1])=p^(n+1) and Order(im[2])=p^(n+1));
    Assert(0,im[2]^-1*im[1]*im[2]=im[1]^(1+p));
    Assert(0,im[2]^(p^n)=im[1]^(p^n));
    Assert(0,List(lc,Size)=Concatenation([p^(2*n+1)],List([1..n+1],r->p^(n+1-r))));
    count:=count+1;
    Print("CASE p=",p," n=",n," size=",Size(G)," class=",Length(lc)-1,
      " abelian=",ab," lower_sizes=",List(lc,Size),"\n");
  od;
od;
Print("PASS_17113_GAP cases=",count,"\n");
end;
Main17113();
QUIT;
