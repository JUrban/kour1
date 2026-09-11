# Exact integer-lattice verification, independent HNF and bounded box search.
Read("results/9.45-cases.g");
Check945 := function(ok, label)
    if not ok then Error(label); fi;
end;
NonzeroRows945 := function(mat)
    return Filtered(mat, x -> ForAny(x, y -> y <> 0));
end;
SearchBasis945 := function(vs, wanted, remaining)
    local i, w, q, rest, answer;
    if wanted = 0 then
        if remaining = 1 then return []; else return fail; fi;
    fi;
    if Length(vs) < wanted then return fail; fi;
    for i in [1..Length(vs)] do
        w := vs[i]; q := w*w;
        if remaining mod q = 0 then
            rest := Filtered(vs{[i+1..Length(vs)]}, v -> v*w=0);
            answer := SearchBasis945(rest, wanted-1, QuoInt(remaining,q));
            if answer <> fail then return Concatenation([w],answer); fi;
        fi;
    od;
    return fail;
end;

Run945 := function()
local counts945, case945, r945, m945, ws945, witness945, n945, gens945,
    h945, w945, coeff945, c945, i945, j945, positive945, inv945,
    boxvs945, q945, answer945;
counts945 := rec(cases:=0, positive:=0, negative:=0, splitting_vectors:=0,
    basis_equalities:=0, box_cases:=0, box_points:=0, box_short_vectors:=0);
for case945 in Cases945 do
    r945:=case945[1]; m945:=case945[2]; ws945:=case945[3];
    witness945:=case945[4]; n945:=Length(r945);
    gens945:=Concatenation(m945*IdentityMat(n945),[r945]);
    h945:=NonzeroRows945(HermiteNormalFormIntegerMat(gens945));
    Check945(Length(h945)=n945,"HNF dimension");
    Check945(AbsInt(DeterminantMat(h945))=m945^(n945-1),"cyclic index");
    for w945 in ws945 do
        coeff945:=SolutionIntMat(h945,w945);
        Check945(coeff945<>fail,"splitting vector membership");
        Check945(coeff945*h945=w945,"integer membership witness");
        c945:=m945*w945/(w945*w945);
        Check945(ForAll(c945,IsInt),"integer dual coordinates");
        Check945(ForAll(h945,x->IsInt((x*c945)/m945)),"dual HNF membership");
        counts945.splitting_vectors:=counts945.splitting_vectors+1;
    od;
    for i945 in [1..Length(ws945)] do
        for j945 in [i945+1..Length(ws945)] do
            Check945(ws945[i945]*ws945[j945]=0,"mutual orthogonality");
        od;
    od;
    positive945:=Length(ws945)=n945;
    Check945(positive945=(witness945<>fail),"Python verdict consistency");
    if positive945 then
        Check945(HermiteNormalFormIntegerMat(ws945)=h945,"candidate HNF equality");
        Check945(HermiteNormalFormIntegerMat(witness945)=h945,"independent HNF equality");
        Check945(ForAll([1..n945],i->ForAll([i+1..n945],
            j->witness945[i]*witness945[j]=0)),"independent witness orthogonality");
        counts945.positive:=counts945.positive+1;
        counts945.basis_equalities:=counts945.basis_equalities+2;
    else
        counts945.negative:=counts945.negative+1;
    fi;
    # Small cases: enumerate the whole integer box, not the cosets or dual.
    if (n945=1) or (n945=2 and m945<=10) or (n945=3 and m945<=5)
        or (n945=4 and m945<=3) or (n945=5 and m945<=2) then
        inv945:=Inverse(h945); boxvs945:=[];
        for w945 in Tuples([-m945..m945],n945) do
            counts945.box_points:=counts945.box_points+1;
            q945:=w945*w945;
            if q945>0 and q945<=m945^2 and First(w945,x->x<>0)>0
                and ForAll(w945*inv945,IsInt) then
                Add(boxvs945,w945);
            fi;
        od;
        Check945(Length(boxvs945)=case945[5],"independent short-vector enumeration");
        answer945:=SearchBasis945(boxvs945,n945,m945^(2*n945-2));
        Check945((answer945<>fail)=positive945,"independent GAP basis search");
        counts945.box_cases:=counts945.box_cases+1;
        counts945.box_short_vectors:=counts945.box_short_vectors+Length(boxvs945);
    fi;
    counts945.cases:=counts945.cases+1;
od;
return counts945;
end;
counts945 := Run945();
Print("PASS_945_GAP ",counts945,"\n");
QUIT_GAP(0);
