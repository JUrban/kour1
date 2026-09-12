# Independent maximal-subgroup search, with direct certificates.
SizeScreen([100000,100000]);;
ChainEdges20112:=0;;
FitTower20112:=function(g)
  local q,hom,tower,f,lift;
  q:=g; hom:=IdentityMapping(g); tower:=[TrivialSubgroup(g)];
  while Size(q)>1 do
    f:=FittingSubgroup(q);
    if Size(f)=1 then Error("nonsoluble control"); fi;
    lift:=PreImage(hom,f); Add(tower,lift);
    hom:=NaturalHomomorphismByNormalSubgroup(g,lift); q:=Image(hom);
  od;
  return tower;
end;;
Chain20112:=function(g,h,n)
  local m,c,t,tail;
  if g=h then return []; fi;
  for m in MaximalSubgroups(g) do
    if IsSubgroup(m,h) then
      c:=Core(g,m); t:=FitTower20112(g/c);
      ChainEdges20112:=ChainEdges20112+1;
      if Length(t)-1<=n then
        tail:=Chain20112(m,h,n);
        if tail<>fail then return Concatenation([[g,m,c]],tail); fi;
      fi;
    fi;
  od;
  return fail;
end;;
for control20112 in [[SymmetricGroup(3),1,false],
                    [SymmetricGroup(4),2,false],[SymmetricGroup(4),3,true]] do
  ok20112:=true;
  for p20112 in Set(FactorsInt(Size(control20112[1]))) do
    h20112:=Normalizer(control20112[1],SylowSubgroup(control20112[1],p20112));
    if Chain20112(control20112[1],h20112,control20112[2])=fail then ok20112:=false; fi;
  od;
  if ok20112<>control20112[3] then Error("maximal chain control"); fi;
  Print("CONTROL ",[Size(control20112[1]),control20112[2],ok20112],"\n");
od;
out20112:=OutputTextFile("results/20.112-chain-certificate.json",false);;
SetPrintFormattingStatus(out20112,false);;
PrintTo(out20112,"{\"groups\":[");;
ids20112:=Concatenation(List([2889..2892],i->[1296,i]),
  List([3081..3086],i->[1296,i]),[[1944,3453],[1944,3454]]);;
jobs20112:=List(ids20112,x->rec(id:=x,g:=SmallGroup(x[1],x[2])));;
for job20112 in ShallowCopy(jobs20112) do
  q20112:=job20112.g/FrattiniSubgroup(job20112.g); qi20112:=IdGroup(q20112);
  if not ForAny(jobs20112,x->x.id=qi20112) then
    Add(jobs20112,rec(id:=qi20112,g:=q20112));
  fi;
od;
for ji20112 in [1..Length(jobs20112)] do
  job20112:=jobs20112[ji20112];
  iso20112:=IsomorphismPermGroup(job20112.g); g20112:=Image(iso20112);
  smaller20112:=SmallerDegreePermutationRepresentation(g20112); g20112:=Image(smaller20112);
  elems20112:=AsSortedList(g20112); gens20112:=GeneratorsOfGroup(g20112);
  Ids20112:=h->List(GeneratorsOfGroup(h),x->Position(elems20112,x)-1);;
  if ji20112>1 then PrintTo(out20112,","); fi;
  PrintTo(out20112,"{\"catalogue_id\":",job20112.id,
    ",\"identity\":",Position(elems20112,One(g20112))-1,
    ",\"permutations\":",List(gens20112,x->List([1..LargestMovedPoint(g20112)],i->i^x-1)),
    ",\"cayley\":",List(elems20112,x->List(gens20112,y->Position(elems20112,x*y)-1)),
    ",\"frattini\":",Ids20112(FrattiniSubgroup(g20112)),",\"sylows\":[");
  primes20112:=Set(FactorsInt(Size(g20112)));
  for pi20112 in [1..Length(primes20112)] do
    p20112:=primes20112[pi20112]; s20112:=SylowSubgroup(g20112,p20112);
    h20112:=Normalizer(g20112,s20112); chain20112:=Chain20112(g20112,h20112,3);
    if chain20112=fail then Error("retained group failed independent chain"); fi;
    if pi20112>1 then PrintTo(out20112,","); fi;
    PrintTo(out20112,"{\"prime\":",p20112,",\"sylow\":",Ids20112(s20112),
      ",\"normalizer\":",Ids20112(h20112),",\"chain\":[");
    for ci20112 in [1..Length(chain20112)] do
      edge20112:=chain20112[ci20112];
      hom20112:=NaturalHomomorphismByNormalSubgroup(edge20112[1],edge20112[3]);
      tower20112:=List(FitTower20112(Image(hom20112)),x->PreImage(hom20112,x));
      if ci20112>1 then PrintTo(out20112,","); fi;
      PrintTo(out20112,"{\"upper\":",Ids20112(edge20112[1]),
        ",\"lower\":",Ids20112(edge20112[2]),",\"core\":",Ids20112(edge20112[3]),
        ",\"tower\":",List(tower20112,Ids20112),"}");
    od;
    PrintTo(out20112,"]}");
    Print("CHAIN ",[job20112.id,p20112,Size(h20112),List(chain20112,x->Size(x[1])),Size(h20112)],"\n");
  od;
  PrintTo(out20112,"]}");
od;
PrintTo(out20112,"]}\n"); CloseStream(out20112);
Print("PASS_20112_CHAINS groups=",Length(jobs20112)," edges_examined=",ChainEdges20112,"\n");
QUIT_GAP(0);
