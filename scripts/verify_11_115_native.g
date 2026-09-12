# Exact free-group checks; no finite quotient is used to assert the theorem.
SetAssertionLevel(2);
Native11115 := function()
    local m, f, a, b, r, s, basis, t, u, ub, forward, backward, alpha, beta,
          phi, i, ci, expected, rows, path;
    rows:=[];
    for m in [2,3,4,5,7,8,11] do
        f:=FreeGroup("a","b"); a:=f.1; b:=f.2; r:=a^m;
        s:=List([0..m-1],i->a^i*b*a^-i);
        basis:=Concatenation([r],s); t:=Subgroup(f,basis);
        Assert(0,Index(f,t)=m and IsNormal(f,t));
        Assert(0,b in t and not a in t and RankOfFreeGroup(t)=m+1);
        Assert(0,r<>One(f) and Comm(r,b)<>One(f));
        u:=FreeGroup(m+1); ub:=GeneratorsOfGroup(u);
        forward:=Concatenation([ub[1]],ub{[3..m+1]},[ub[1]*ub[2]*ub[1]^-1]);
        backward:=Concatenation([ub[1],ub[1]^-1*ub[m+1]*ub[1]],ub{[2..m]});
        alpha:=GroupHomomorphismByImages(u,u,ub,forward);
        beta:=GroupHomomorphismByImages(u,u,ub,backward);
        phi:=GroupHomomorphismByImages(u,t,ub,basis);
        for i in [1..m+1] do
            Assert(0,Image(phi,forward[i])=a*basis[i]*a^-1);
            Assert(0,Image(phi,backward[i])=a^-1*basis[i]*a);
            Assert(0,Image(alpha,backward[i])=ub[i]);
            Assert(0,Image(beta,forward[i])=ub[i]);
        od;
        for i in [1..m] do
            ci:=Comm(ub[1],ub[i+1]);
            if i<m then expected:=Comm(ub[1],ub[i+2]);
            else expected:=ub[1]*Comm(ub[1],ub[2])*ub[1]^-1; fi;
            Assert(0,Image(alpha,ci)=expected);
        od;
        # The wrap is conjugation in the free group, not simple substitution.
        Assert(0,a*s[m]*a^-1<>s[1]);
        path:=Concatenation("results/11.115-model-",String(m),".json");
        PrintTo(path,"{\"m\":",m,",\"index\":",Index(f,t),
                ",\"rank\":",RankOfFreeGroup(t),",\"basis\":",List(basis,LetterRepAssocWord),
                ",\"forward\":",List(forward,LetterRepAssocWord),
                ",\"backward\":",List(backward,LetterRepAssocWord),"}\n");
        Add(rows,[m,Index(f,t),RankOfFreeGroup(t),4*(m+1)+m]);
    od;
    Print("NATIVE_11115_ROWS ",rows,"\nPASS_11_115_NATIVE models=7\n");
end;
Native11115();
QUIT;
