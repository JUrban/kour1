Read("scripts/certify_21_99_words.g");;
if not IsBound(WordShard2199) then Error("WordShard2199 required"); fi;
if not IsBound(WordShards2199) then Error("WordShards2199 required"); fi;
SearchWords2199:=function()
  local n,id,total,row,out,bad,count,missing,groups,failures,degrees;
  out:=OutputTextFile(Concatenation("results/21.99-words-shard",String(WordShard2199),"-certificate.jsonl"),false);
  SetPrintFormattingStatus(out,false);
  bad:=OutputTextFile(Concatenation("results/21.99-words-shard",String(WordShard2199),"-unresolved.jsonl"),false);
  SetPrintFormattingStatus(bad,false); groups:=0; failures:=0;
  degrees:=Filtered([2..47],n->Length(Set(FactorsInt(n)))>1);
  for n in degrees do
    total:=NrTransitiveGroups(n); count:=0; missing:=0;
    if total=fail then Error("missing catalogue degree"); fi;
    for id in [1..total] do
      if (id-1) mod WordShards2199<>WordShard2199 then continue; fi;
      row:=Certify2199(n,id,5000);
      if IsRecord(row) then
        PrintTo(bad,[n,id,row.trials,row.missing],"\n");
        Print("UNRESOLVED ",[n,id,row.trials,row.missing],"\n"); missing:=missing+1;
      else PrintTo(out,row,"\n"); count:=count+1; fi;
      if (count+missing) mod 1000=0 then
        Print("PROGRESS ",[WordShard2199,n,id,count,missing,Runtime()],"\n");
      fi;
    od;
    Print("DEGREE_DONE ",[n,total,count,missing],"\n");
    groups:=groups+count; failures:=failures+missing;
  od;
  CloseStream(out); CloseStream(bad);
  if failures>0 then Error("unresolved action cases; not counterexamples"); fi;
  Print("PASS_2199_WORD_SHARD ",[WordShard2199,WordShards2199,groups,failures],"\n");
end;;
SearchWords2199();
QUIT_GAP(0);
