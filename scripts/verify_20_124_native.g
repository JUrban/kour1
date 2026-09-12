# These are free-group identities, not identities in finite quotients.
Read("results/20.124-fixture.g");;
SetAssertionLevel(1);;
Check20124:=function(b) if not b then Error("20.124 check failed"); fi; end;;
ff:=FreeGroup(Length(Images20124));; gens:=GeneratorsOfGroup(ff);;
Word20124:=function(w) return Product(List(w,a->gens[AbsInt(a)]^SignInt(a)),One(ff)); end;;
images:=List(Images20124,Word20124);;
phi:=GroupHomomorphismByImages(ff,ff,gens,images);;
Check20124(phi<>fail);;
for i in [1..Length(images)] do
  Check20124(ForAll(Images20124[i],a->Levels20124[AbsInt(a)]<Levels20124[i]));
  Check20124(ForAll([1..Length(gens)],j->ExponentSumWord(images[i],gens[j])=0));
od;
Iter20124:=function(w)
  local out,v;out:=[];v:=Image(phi,w);
  while v<>One(ff) do Add(out,v);v:=Image(phi,v);Check20124(Length(out)<=4);od;
  return out;
end;;
B20124:=w->Product(Iter20124(w),One(ff));;
T20124:=w->w*B20124(w);;
D20124:=w->w*Image(phi,w)^-1;;
depths:=[];;maxlen:=0;;
for w0 in Words20124 do
  w:=Word20124(w0);;
  Check20124(D20124(T20124(w))=w and T20124(D20124(w))=w);
  Check20124(B20124(D20124(w))=Image(phi,w));
  AddSet(depths,Length(Iter20124(w))+1);;maxlen:=Maximum(maxlen,Length(B20124(w)));
od;
for pair in Pairs20124 do
  g:=Word20124(pair[1]);;h:=Word20124(pair[2]);;bg:=B20124(g);;
  Check20124(bg*B20124(h)=B20124(g*bg*h*bg^-1));
od;
for pair in Witnesses20124 do
  Check20124(B20124(gens[pair[1]]*Word20124(pair[2])^-1)=Word20124(pair[2]));
od;
Check20124(depths=[1,2,3,4,5]);;
Print("FREE_RB_20124 ",[Length(gens),Length(Words20124),Length(Pairs20124),Length(Witnesses20124),depths,maxlen],"\n");
Print("PASS_20_124_NATIVE\n");
QUIT_GAP(0);
