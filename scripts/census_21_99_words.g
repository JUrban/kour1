SizeScreen([100000,100000]);;
Census2199:=List(Filtered([2..47],n->Length(Set(FactorsInt(n)))>1),
  n->[n,NrTransitiveGroups(n)]);;
if ForAny(Census2199,r->r[2]=fail) then Error("missing transitive catalogue degree"); fi;
Out2199:=OutputTextFile("results/21.99-words-census.json",false);;
SetPrintFormattingStatus(Out2199,false);;
PrintTo(Out2199,Census2199,"\n");; CloseStream(Out2199);;
Print("PASS_2199_CENSUS ",Census2199," total=",Sum(Census2199,r->r[2]),"\n");
QUIT_GAP(0);
