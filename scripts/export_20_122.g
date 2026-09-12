# PILOT_ORDER and PILOT_OUTPUT are supplied by a retained input file.
SetAssertionLevel(2);
Export20122 := function()
    local n, out, count, i, g, fit, elts, gens, classes, active, data, regular,
          first, nilpotentCount, exportedCount, encode;
    n:=PILOT_ORDER; out:=OutputTextFile(PILOT_OUTPUT,false);
    SetPrintFormattingStatus(out,false);
    PrintTo(out,"{\"order\":",n,",\"catalogue_count\":",NumberSmallGroups(n),
            ",\"groups\":[\n");
    first:=true; nilpotentCount:=0; exportedCount:=0;
    for i in [1..NumberSmallGroups(n)] do
        g:=SmallGroup(n,i);
        if not first then AppendTo(out,",\n"); fi; first:=false;
        if IsNilpotentGroup(g) then
            nilpotentCount:=nilpotentCount+1;
            AppendTo(out,"{\"id\":",i,",\"nilpotent\":true}");
        else
            fit:=FittingSubgroup(g); elts:=Elements(g); gens:=GeneratorsOfGroup(g);
            Assert(0,elts[1]=One(g));
            encode:=h->List(Elements(h),x->PositionSorted(elts,x)-1);
            classes:=Filtered(ConjugacyClassesSubgroups(g),c->IsNilpotentGroup(Representative(c)));
            active:=Filtered(classes,c->not IsSubgroup(fit,Representative(c)));
            data:=List(active,c->[encode(Representative(c)),List(Elements(c),encode)]);
            regular:=List(gens,h->List(elts,x->PositionSorted(elts,x*h)-1));
            AppendTo(out,"{\"id\":",i,",\"nilpotent\":false,\"soluble\":",IsSolvableGroup(g),
                     ",\"nilpotent_classes\":",Length(classes),",\"fit\":",encode(fit),
                     ",\"right_generators\":",regular,",\"classes\":",data,"}");
            exportedCount:=exportedCount+1;
            Print("EXPORTED_20122 ",[n,i,Length(classes),Length(active)],"\n");
        fi;
    od;
    AppendTo(out,"\n]}\n"); CloseStream(out);
    Print("PASS_20_122_EXPORT order=",n," catalogue=",NumberSmallGroups(n),
          " nilpotent=",nilpotentCount," exported=",exportedCount,"\n");
end;
Export20122();
QUIT;
