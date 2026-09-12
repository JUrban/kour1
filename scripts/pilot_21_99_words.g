Read("scripts/certify_21_99_words.g");;
Pilot2199:=function()
  local targets,n,id,target,row,out,count,unresolved;
  targets:=[];
  for n in [2..12] do
    for id in [1..NrTransitiveGroups(n)] do Add(targets,[n,id]); od;
  od;
  Append(targets,List([24990..25000],id->[24,id]));
  out:=OutputTextFile("results/21.99-words-pilot-certificate.jsonl",false);
  SetPrintFormattingStatus(out,false); count:=0; unresolved:=[];
  for target in targets do
    row:=Certify2199(target[1],target[2],5000);
    if IsRecord(row) then Add(unresolved,row); Print("UNRESOLVED ",row,"\n");
    else PrintTo(out,row,"\n"); count:=count+1; fi;
    if count mod 20=0 then Print("PROGRESS ",count," ",target,"\n"); fi;
  od;
  CloseStream(out);
  if Length(unresolved)>0 then Error("unresolved pilot cases"); fi;
  Print("PASS_2199_WORD_PILOT groups=",count,"\n");
end;;
Pilot2199();
QUIT_GAP(0);
