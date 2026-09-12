# Feasibility probe only: exponent 7 makes p-class equal ordinary class.
SetAssertionLevel(2);
if LoadPackage("anupq")<>true then Error("ANUPQ unavailable"); fi;
Probe20113 := function()
    local f, g, h, generators, lower, dimensions;
    f:=FreeGroup("a","b","c","d");
    generators:=GeneratorsOfGroup(f);
    g:=f/[Comm(generators[2],generators[1])*Comm(generators[4],generators[3])^-1];
    Print("PROBE_20113 GAP=",GAPInfo.Version," ANUPQ=",PackageInfo("anupq")[1].Version,
          " exponent=7 class_bound=8 pq_workspace_words=10000000\n");
    h:=Pq(g : Prime:=7, Exponent:=7, ClassBound:=8,
               PqWorkspace:=10000000, OutputLevel:=1);
    lower:=LowerCentralSeries(h);
    dimensions:=List([1..Length(lower)-1],i->LogInt(Index(lower[i],lower[i+1]),7));
    Assert(0,NilpotencyClassOfGroup(h)<=8);
    Print("PROBE_20113_RESULT log_order=",LogInt(Size(h),7),
          " class=",NilpotencyClassOfGroup(h)," lower_dimensions=",dimensions,"\n");
    Print("PASS_20_113_PQ_PROBE\n");
end;
Probe20113();
QUIT;
