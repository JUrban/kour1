# Exploratory degree screen. Missing tables are retained explicitly.
Run1240 := function()
  local names,out,nam,t,p,b,degrees,pp,parts,available,missing,total;
  names:=AllCharacterTableNames();;
  out:=OutputTextFile("results/12.40-table-degrees.txt",false);;
  SetPrintFormattingStatus(out,false);;
  available:=0;; missing:=0;; total:=0;;
  for nam in names do
    t:=CharacterTable(nam);;
    for p in Filtered(Set(FactorsInt(Size(t))),IsPrimeInt) do
      b:=t mod p;;
      if b=fail then
        missing:=missing+1;;
        PrintTo(out,nam,"|",Size(t),"|",p,"|MISSING\n");
      else
        available:=available+1;;
        degrees:=List(Irr(b),chi->chi[1]);;
        if not ForAll(degrees,IsPosInt) then Error("invalid degree"); fi;
        PrintTo(out,nam,"|",Size(t),"|",p,"|",degrees,"\n");
        pp:=p^Number(FactorsInt(Size(t)),q->q=p);;
        parts:=List(degrees,d->p^Number(FactorsInt(d),q->q=p));;
        if Maximum(parts)>pp then
          Print("EXCESS ",nam," p=",p," order_p=",pp," max_degree_p=",Maximum(parts),"\n");
        fi;
      fi;
    od;
    total:=total+1;;
    if total mod 250=0 then
      Print("PROGRESS names=",total," available=",available," missing=",missing,"\n");
    fi;
  od;
  CloseStream(out);
  out:=OutputTextFile("results/12.40-table-catalog.json",false);;
  SetPrintFormattingStatus(out,false);;
  PrintTo(out,"{\"names\":",names,",\"table_count\":",total,
    ",\"available\":",available,",\"missing\":",missing,"}\n");
  CloseStream(out);
  Print("PASS_1240_TABLE_SCREEN\n");
end;
Run1240();
QUIT_GAP(0);
