# Actual projective permutation modules in three small controls.
Run1240Modules := function()
  local pairs,out,first,pair,n,q,g,v,points,p,m,cf,dims,abs,order,degree;
  Reset(GlobalMersenneTwister,1240);
  PrintTo("results/12.40-gap-environment.json","{\"gap_version\":\"",
    GAPInfo.Version,"\",\"ctbllib_version\":\"",PackageInfo("ctbllib")[1].Version,
    "\",\"workspace_gib\":4,\"seed\":1240}\n");
  pairs:=[[4,3],[4,5],[6,3]];
  out:=OutputTextFile("results/12.40-modules.json",false);
  SetPrintFormattingStatus(out,false);
  PrintTo(out,"[\n"); first:=true;
  for pair in pairs do
    n:=pair[1]; q:=pair[2];
    g:=SL(n,q);
    v:=List([1..n],i->Zero(GF(q))); v[1]:=One(GF(q));
    points:=Orbit(g,v,OnLines);
    degree:=(q^n-1)/(q-1);
    if Length(points)<>degree then Error("point count"); fi;
    p:=Action(g,points,OnLines);
    order:=Size(p);
    if order<>q^(n*(n-1)/2)*Product([2..n],i->q^i-1)/Gcd(n,q-1)
      then Error("group order"); fi;
    m:=PermutationGModule(p,GF(2));
    cf:=MTX.CompositionFactors(m);
    dims:=SortedList(List(cf,MTX.Dimension));
    abs:=List(cf,MTX.IsAbsolutelyIrreducible);
    if dims<>[1,1,degree-2] or not ForAll(abs,x->x=true)
      then Error("composition factors"); fi;
    if not first then PrintTo(out,",\n"); fi; first:=false;
    PrintTo(out,"{\"n\":",n,",\"q\":",q,",\"order\":",order,
      ",\"projective_degree\":",degree,",\"composition_dimensions\":",dims,
      ",\"all_absolutely_irreducible\":true}");
    Print("MODULE n=",n," q=",q," degree=",degree," factors=",dims,"\n");
  od;
  PrintTo(out,"\n]\n"); CloseStream(out);
  Print("PASS_1240_MODULES\n");
end;
Run1240Modules();
QUIT_GAP(0);
