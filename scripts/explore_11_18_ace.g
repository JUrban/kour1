if LoadPackage("ace")<>true then Error("ACE unavailable"); fi;
Explore1118ACE:=function(a,b,strategy)
    local f,x,y,w,rels,j,s;
    f:=FreeGroup("x","y");x:=f.1;y:=f.2;
    w:=x;for j in [1..a] do w:=Comm(w,y);od;rels:=[x^-1*w];
    w:=y;for j in [1..b] do w:=Comm(w,x);od;Add(rels,y^-1*w);
    Print("a=",a," b=",b," strategy=",strategy," lengths=",List(rels,Length),"\n");
    if strategy="hard" then
        s:=ACEStats([x,y],rels,[]:hard,workspace:=10000000,time:=20);
    else
        s:=ACEStats([x,y],rels,[]:hlt,workspace:=10000000,time:=20);
    fi;
    Print("ACE_STATS=",s,"\nDONE_1118_ACE\n");
end;
Explore1118ACE(PARAM_A,PARAM_B,"PARAM_STRATEGY");
QUIT;
