# Actual-group controls for the endpoint embedding and its linear orders.
SetAssertionLevel(2);
ReverseDigits := function(k,p,a)
    local v,i;
    v:=0;
    for i in [1..a] do v:=p*v+k mod p; k:=QuoInt(k,p); od;
    Assert(0,k=0);
    return v;
end;

CheckExtension := function(label,G,D)
    local d,sz,powers,ps,as,qs,ts,subgroups,coords,H,t,logs,row,i,vs,
          dim,k,j,actual,encoded,ranks,ordering,r,linencoded,fiberChecks;
    Assert(0,IsNormal(G,D) and IsCyclic(D));
    sz:=Size(D); d:=First(Elements(D),x->Order(x)=sz);
    powers:=List([0..sz-1],k->d^k);
    ps:=Set(FactorsInt(sz));
    as:=List(ps,p->Valuation(sz,p)); qs:=List([1..Length(ps)],i->ps[i]^as[i]);
    ts:=AsList(RightTransversal(G,D));
    subgroups:=Concatenation(List(ConjugacyClassesSubgroups(G),c->AsList(c)));
    coords:=[]; fiberChecks:=0;
    for H in subgroups do
        row:=[];
        for t in ts do
            logs:=Filtered([0..sz-1],k->powers[k+1]*t in H);
            if IsEmpty(logs) then
                for i in [1..Length(ps)] do Append(row,[-qs[i]-1,-1]); od;
            else
                r:=1;
                for i in [1..Length(ps)] do
                    vs:=Set(List(logs,k->ReverseDigits(k mod qs[i],ps[i],as[i])));
                    Assert(0,vs=[Minimum(vs)..Maximum(vs)]);
                    r:=r*Length(vs);
                    Append(row,[-Minimum(vs),Maximum(vs)]);
                od;
                Assert(0,r=Length(logs));
            fi;
            fiberChecks:=fiberChecks+1;
        od;
        Add(coords,row);
    od;
    dim:=2*Length(ps)*Length(ts);
    Assert(0,ForAll(coords,v->Length(v)=dim));
    ranks:=[];
    for k in [1..dim] do
        ordering:=[1..Length(subgroups)];
        Sort(ordering,function(i,j)
            return [coords[i][k],Size(subgroups[i]),i] < [coords[j][k],Size(subgroups[j]),j];
        end);
        r:=[]; for i in [1..Length(ordering)] do r[ordering[i]]:=i; od;
        Add(ranks,r);
    od;
    for i in [1..Length(subgroups)] do
        for j in [1..Length(subgroups)] do
            actual:=IsSubgroup(subgroups[j],subgroups[i]);
            encoded:=ForAll([1..dim],k->coords[i][k]<=coords[j][k]);
            linencoded:=ForAll(ranks,r->r[i]<=r[j]);
            Assert(0,actual=encoded and actual=linencoded);
        od;
    od;
    Print("PASS ",label," order=",Size(G)," D=",sz," index=",Length(ts),
          " subgroups=",Length(subgroups)," fibers=",fiberChecks,
          " pairs=",Length(subgroups)^2," linear_orders=",dim,"\n");
    return [Length(subgroups),fiberChecks,Length(subgroups)^2];
end;

totals:=[0,0,0];;
for n in [32,54,288] do
    G:=DihedralGroup(n);;
    d:=First(Elements(G),x->Order(x)=n/2);;
    totals:=totals+CheckExtension(Concatenation("dihedral",String(n)),G,Subgroup(G,[d]));
od;
G:=QuaternionGroup(32);; d:=First(Elements(G),x->Order(x)=16);;
totals:=totals+CheckExtension("quaternion32-nonsplit",G,Subgroup(G,[d]));
G:=DirectProduct(QuaternionGroup(32),SymmetricGroup(3));;
d:=First(Elements(G),x->Order(x)=48);;
totals:=totals+CheckExtension("quaternion32-times-S3",G,Subgroup(G,[d]));
G:=DirectProduct(CyclicGroup(9),SymmetricGroup(3));;
D:=Image(Embedding(G,1));;
Assert(0,not IsAbelian(FactorGroup(G,D)));
totals:=totals+CheckExtension("nonabelian-quotient-S3",G,D);
Print("11.116 GAP controls: PASS subgroups=",totals[1]," fibers=",totals[2]," pairs=",totals[3],"\n");
QUIT;
