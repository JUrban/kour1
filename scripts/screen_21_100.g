# Configured prime-power cyclic coprime action screen on one group order.
SizeScreen([100000,100000]);;
if not IsBound(SearchOrder21100) then Error("SearchOrder21100 required"); fi;
if not IsBound(SearchShard21100) then Error("SearchShard21100 required"); fi;
if not IsBound(SearchShards21100) then Error("SearchShards21100 required"); fi;
Pilot21100:=function()
  local ord,id,g,ag,s,acs,aut,classes,dict,i,x,irr,fixed,c,cc,ci,ar,ap,
        classmap,cmap,invchars,chi,res,multiplicities,odd,never,linear,
        count,expected,actions,groups,hits,pointwise,allactions,allgroups,
        allhits,allpointwise,rows,subgroup,record,out;
  allactions:=0; allgroups:=0; allhits:=0; allpointwise:=0;
  out:=OutputTextFile(Concatenation("results/21.100-order",String(SearchOrder21100),"-shard",String(SearchShard21100),"-rows.jsonl"),false);
  SetPrintFormattingStatus(out,false);
  for ord in [SearchOrder21100] do
    actions:=0; groups:=0; hits:=0; pointwise:=0;
    for id in [1..NumberSmallGroups(ord)] do
      if (id-1) mod SearchShards21100<>SearchShard21100 then continue; fi;
      g:=SmallGroup(ord,id);
      if NilpotencyClassOfGroup(g)<3 then continue; fi;
      groups:=groups+1;
      ag:=AutomorphismGroup(g);
      ap:=Filtered(Set(FactorsInt(Size(ag))),r->r>1 and ord mod r<>0);
      if Length(ap)=0 then continue; fi;
      classes:=ConjugacyClasses(g); irr:=Irr(g);
      dict:=NewDictionary(One(g),true);
      for i in [1..Length(classes)] do
        for x in AsList(classes[i]) do AddDictionary(dict,x,i); od;
      od;
      for ar in ap do
      s:=SylowSubgroup(ag,ar);
      acs:=Filtered(ConjugacyClasses(s),cl->Order(Representative(cl))>1);
      for i in [1..Length(acs)] do
        aut:=Representative(acs[i]);
        if not IsBijective(aut) or Set(FactorsInt(Order(aut)))<>[ar] then Error("automorphism check"); fi;
        classmap:=List(classes,cl->LookupDictionary(dict,Image(aut,Representative(cl))));
        invchars:=Filtered([1..Length(irr)],j->ForAll([1..Length(classes)],k->irr[j][k]=irr[j][classmap[k]]));
        fixed:=Filtered(Elements(g),x->Image(aut,x)=x); c:=Subgroup(g,fixed);
        if Size(c)<>Length(fixed) then Error("fixed set closure"); fi;
        cc:=ConjugacyClasses(c); ci:=Irr(c);
        if Length(invchars)<>Length(ci) then Error("Glauberman count control"); fi;
        cmap:=List(cc,cl->LookupDictionary(dict,Representative(cl)));
        count:=0; rows:=[];
        for x in invchars do
          chi:=irr[x]; res:=ClassFunction(CharacterTable(c),List(cmap,j->chi[j]));
          multiplicities:=List(ci,theta->ScalarProduct(res,theta));
          if not ForAll(multiplicities,m->IsInt(m) and m>=0) then Error("restriction multiplicities"); fi;
          if Sum([1..Length(ci)],j->multiplicities[j]*ci[j][1])<>chi[1] then Error("restriction degree"); fi;
          odd:=Filtered([1..Length(ci)],j->multiplicities[j] mod ar<>0);
          if Length(odd)<>1 then Error("unique coprime-multiplicity constituent"); fi;
          never:=ForAll(ValuesOfClassFunction(res),v->v<>0);
          linear:=ci[odd[1]][1]=1;
          if never then count:=count+1; fi;
          if never<>linear then
            pointwise:=pointwise+1;
            Print("POINTWISE_HIT ",[ord,id,ar,Order(aut),i,x,chi[1],ci[odd[1]][1],never],"\n");
          fi;
          # Integer flags make every case row directly valid JSON.
          record:=[x,chi[1],ci[odd[1]][1],0,0];
          if never then record[4]:=1; fi;
          if linear then record[5]:=1; fi;
          Add(rows,record);
        od;
        expected:=Size(c)/Size(DerivedSubgroup(c));
        if count<>expected then hits:=hits+1; Print("COUNT_HIT ",[ord,id,ar,Order(aut),i,Size(c),count,expected],"\n"); fi;
        PrintTo(out,[ord,id,ar,Order(aut),i,Size(ag),Size(s),Size(c),Length(invchars),count,expected,rows],"\n");
        actions:=actions+1;
      od;
      od;
      if groups mod 10=0 then Print("PROGRESS ",[ord,id,groups,actions,hits,pointwise],"\n"); fi;
    od;
    Print("ORDER_DONE ",[ord,NumberSmallGroups(ord),groups,actions,hits,pointwise],"\n");
    allgroups:=allgroups+groups; allactions:=allactions+actions;
    allhits:=allhits+hits; allpointwise:=allpointwise+pointwise;
  od;
  CloseStream(out);
  Print("PASS_21100_SHARD ",[allgroups,allactions,allhits,allpointwise],"\n");
end;;
Pilot21100();
QUIT_GAP(0);
