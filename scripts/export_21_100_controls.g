# Inducing linear characters supply independently checkable character witnesses.
SizeScreen([100000,100000]);;
Monomial21100:=function(k,identify,m)
  local chars,basis,chi,h,lambda,restricted,candidates,roots,rows,values,j,classes,x;
  # IrrConlon can return repeated irreducibles (e.g. SmallGroup(729,268)).
  # Obtain the standard basis first, since Conlon can also populate its cache.
  basis:=Irr(k); chars:=Set(IrrConlon(k));
  if Set(basis)<>chars or Sum(chars,x->x[1]^2)<>Size(k)
     or not ForAll(chars,x->ScalarProduct(x,x)=1) then
    Error("deduplicated Conlon basis");
  fi;
  roots:=List([0..m-1],j->E(m)^j); rows:=[];
  for chi in chars do
    if chi[1]=1 then
      h:=k; lambda:=chi;
    else
      h:=TestMonomial(chi).subgroup;
      restricted:=RestrictedClassFunction(chi,CharacterTable(h));
      candidates:=Filtered(LinearCharacters(h),l->ScalarProduct(restricted,l)>0);
      if Length(candidates)=0 then Error("missing inducing character"); fi;
      lambda:=candidates[1];
    fi;
    if Index(k,h)<>chi[1] then Error("inducing index"); fi;
    classes:=ConjugacyClasses(h); values:=[];
    for j in [1..Length(classes)] do
      for x in AsList(classes[j]) do
        Add(values,[identify(x),Position(roots,lambda[j])-1]);
      od;
    od;
    Sort(values);
    Add(rows,[List(GeneratorsOfGroup(h),identify),values]);
  od;
  if Length(chars)<>Length(basis) then Error("Conlon completeness"); fi;
  return rows;
end;;
Export21100:=function()
  local targets,target,g,ag,s,aut,c,found,x,classes,cc,irr,ci,invchars,
        map1,map2,pg,es,gens,identify,m,actions,selected,out,ix,caseindex,
        pgens,cgens,automap,graph,perms,normalizer,expected,ar;
  targets:=[[243,51,81,9,3,2],[243,56,27,9,3,2],[729,138,243,9,3,2],
    [729,245,243,27,3,2],[729,258,81,27,3,2],[729,268,243,27,9,2],
    [729,402,243,9,9,2],[256,10331,64,16,4,3],[256,56065,16,4,2,5],
    [256,53054,32,8,4,7],[2187,8007,243,27,9,4],[2187,8007,243,27,9,8],
    [2187,9276,81,9,3,13]];
  out:=OutputTextFile("results/21.100-independent-certificate.json",false);
  SetPrintFormattingStatus(out,false); PrintTo(out,"{\"groups\":[");
  for caseindex in [1..Length(targets)] do
    target:=targets[caseindex]; g:=SmallGroup(target[1],target[2]);
    ar:=FactorsInt(target[6])[1];
    ag:=AutomorphismGroup(g); s:=SylowSubgroup(ag,ar); found:=false;
    for x in ConjugacyClasses(s) do
      aut:=Representative(x);
      if Order(aut)<>target[6] then continue; fi;
      c:=Subgroup(g,Filtered(Elements(g),y->Image(aut,y)=y));
      if Size(c)=target[3] and Size(c)/Size(DerivedSubgroup(c))=target[4]
         and Maximum(List(Irr(c),chi->chi[1]))=target[5] then found:=true; break; fi;
    od;
    if not found then Error("control fixed subgroup unavailable"); fi;
    map1:=IsomorphismPermGroup(g); map2:=SmallerDegreePermutationRepresentation(Image(map1));
    pg:=Image(map2); es:=AsSortedList(pg); gens:=GeneratorsOfGroup(pg);
    identify:=x->Position(es,Image(map2,Image(map1,x)))-1;
    m:=Exponent(g);
    graph:=List(es,x->List(gens,y->Position(es,x*y)-1));
    perms:=List(gens,x->List([1..LargestMovedPoint(pg)],i->i^x-1));
    automap:=List(es,x->identify(Image(aut,PreImage(map1,PreImage(map2,x)))));
    if caseindex>1 then PrintTo(out,","); fi;
    PrintTo(out,"{\"catalogue_id\":",target{[1,2]},",\"identity\":",Position(es,One(pg))-1,
      ",\"cayley\":",graph,",\"permutations\":",perms,",\"root_order\":",m,
      ",\"automorphism\":",automap,",\"action_prime\":",ar,",\"action_order\":",target[6],
      ",\"fixed_generators\":",List(GeneratorsOfGroup(c),identify),
      ",\"expected_fixed\":",target{[3,4,5]},
      ",\"group_characters\":",Monomial21100(g,identify,m),
      ",\"fixed_characters\":",Monomial21100(c,identify,m),"}");
    Print("CONTROL_EXPORTED ",target,"\n");
  od;
  PrintTo(out,"]}\n"); CloseStream(out);
  Print("PASS_21100_EXPORT models=",Length(targets),"\n");
end;;
Export21100();
QUIT_GAP(0);
