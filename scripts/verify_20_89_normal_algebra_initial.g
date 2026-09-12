# Native GAP finite-field matrices and eventual images of commutator maps.
SizeScreen([4096,1000]);;
Encode2089A:=x->List(Flat(x),IntFFE);;
Reps2089A:=function(p)
    local out,a,b,t,d;
    out:=[];
    for a in [1..p-1] do Add(out,[a,0,0,a]);Add(out,[a,1,0,a]);od;
    for a in [1..p-1] do
        for b in [a+1..p-1] do Add(out,[a,0,0,b]);od;
    od;
    for t in [0..p-1] do
        for d in [1..p-1] do
            if ForAll([0..p-1],x->(x*x-t*x+d) mod p<>0) then Add(out,[0,(-d) mod p,1,t]);fi;
        od;
    od;
    Sort(out);
    if Length(Set(out))<>p*p-1 then Error("class count");fi;
    return out;
end;;
groups:=0;;classes:=0;;nontrivial:=0;;parameters:=0;;grouprows:=[];;
for p in [2,3,5,7] do
    field:=GF(p);one:=One(field);identity:=IdentityMat(2,field);
    for kind in ["GL","SL"] do
        if kind="GL" then group:=GL(2,p);else group:=SL(2,p);fi;
        els:=Elements(group);fitting:=FittingSubgroup(group);
        selected:=Filtered(Reps2089A(p),r->kind="GL" or (r[1]*r[4]-r[2]*r[3]) mod p=1);
        sizes:=[];groups:=groups+1;
        for rep in selected do
            a:=[rep{[1,2]}*one,rep{[3,4]}*one];e:=Set(els);
            repeat old:=e;e:=Set(old,x->Comm(x,a));until e=old;
            if (Length(e)=1)<>(a in fitting) then Error("finite Engel radical");fi;
            encoded:=List(e,Encode2089A);Sort(encoded);
            params:=[];
            for t in [0..p-1] do
                c:=identity+t*a;
                if DeterminantMat(c)<>Zero(field) then Add(params,c);fi;
            od;
            r:=Length(params);
            eigenvalues:=Number([1..p-1],s->DeterminantMat(a-s*identity)=Zero(field));
            if r<>p-eigenvalues or r<p-2 then Error("parameter count");fi;
            orbit:=[];
            if Length(e)>1 then
                e0:=First(encoded,v->Comm([v{[1,2]}*one,v{[3,4]}*one],a)<>identity);
                e0:=[e0{[1,2]}*one,e0{[3,4]}*one];
                orbit:=List(params,c->e0^c);
                if Length(Set(orbit))<>r or identity in orbit or not IsSubset(e,Set(orbit)) or Length(e)<r+1 then Error("sink orbit lower bound");fi;
                orbit:=List(orbit,Encode2089A);nontrivial:=nontrivial+1;parameters:=parameters+r;
            fi;
            Print("ROW2089A [",p,",\"",kind,"\",",rep,",",Length(els),",",encoded,",",r,",",orbit,"]\n");
            classes:=classes+1;Add(sizes,Length(e));
        od;
        positive:=Filtered(sizes,m->m>1);
        if IsEmpty(positive) then minimum:=0;else minimum:=Minimum(positive);fi;
        Add(grouprows,[p,kind,Length(els),Length(selected),minimum,Maximum(sizes)]);
    od;
od;
Print("SUMMARY2089A {\"groups\":",groups,",\"classes\":",classes,",\"nontrivial_sinks\":",nontrivial,",\"parameter_conjugates\":",parameters,",\"group_rows\":",grouprows,"}\n");
Print("PASS_20_89_NORMAL_ALGEBRA_NATIVE\n");
QUIT_GAP(0);
