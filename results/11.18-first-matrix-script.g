# Canonical two-by-two pair: common polynomial conditions for exact return.
Explore1118Matrices:=function()
    local l,t,x,y,w,n,pols,p,g,e,all,a,b,Step,i,j,pair,G,k,z,seen;
    l:=Indeterminate(Rationals,"l");
    t:=l^2+l^-2-l-l^-1;
    x:=[[l,t],[0,l^-1]]; y:=[[l^-1,0],[1,l]];
    w:=x; all:=[];
    for n in [1..7] do
        w:=w^-1*y^-1*w*y;
        pols:=[];
        for i in [1..2] do for j in [1..2] do
            Add(pols,NumeratorOfRationalFunction(w[i][j]-x[i][j]));
        od; od;
        g:=Gcd(pols); Add(all,g);
        Print("period=",n," common_factors=",Factors(g),"\n");
    od;
    pairs:=[[(1,7,2,4,5,3,6),(1,4,3,7,6,2,5)],
            [(1,2)(3,4,5,6),(2,3)(4,7,5,6)],
            [(1,2,3)(4,5)(6,7),(1,6,5)(2,7)(3,4)]];
    for pair in pairs do
        G:=Group(pair); pols:=[];
        for i in [1..2] do
            a:=pair[i]; b:=pair[3-i]; z:=a; seen:=[a];k:=0;
            repeat
                z:=Comm(z,b); k:=k+1;
                if z=a then break; fi;
                if z in seen then Error("pair is not mutually periodic"); fi;
                Add(seen,z);
            until k>=100000;
            Add(pols,k);
        od;
        Print("A7_pair=",pair," group_order=",Size(G)," periods=",pols,"\n");
    od;
    Print("DONE_1118_MATRIX_SCREEN\n");
end;
Explore1118Matrices();
QUIT;
