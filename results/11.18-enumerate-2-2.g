# Bounded coset enumeration; fail is inconclusive.
Explore1118 := function(a,b)
    local f,x,y,rels,t,j,w;
    f:=FreeGroup("x","y"); x:=f.1; y:=f.2;
    w:=x; for j in [1..a] do w:=Comm(w,y); od;
    rels:=[x^-1*w];
    w:=y; for j in [1..b] do w:=Comm(w,x); od;
    Add(rels,y^-1*w);
    Print("a=",a," b=",b," relator_lengths=",List(rels,Length),"\n");
    t:=CosetTableFromGensAndRels([x,y],rels,[]:max:=500000,silent:=true);
    if t=fail then
        Print("INCONCLUSIVE_COSET_LIMIT\n");
    else
        Print("COMPLETED_COSET_TABLE index=",Length(t[1])," table=",t,"\n");
    fi;
    Print("DONE_1118_ENUM\n");
end;
Explore1118(2,2);
QUIT;
