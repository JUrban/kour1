# Exploratory only: rationality and real Schur-index constraints on
# characteristic-p projective characters. No table hit is a proof.
SetInfoLevel(InfoWarning,0);
ReducedRows455:=function(rows)
local mat,i,j,piv;
if Length(rows)=0 then return [];fi;
mat:=List(BaseMat(rows),ShallowCopy);
for i in Reversed([1..Length(mat)]) do
  piv:=PositionProperty(mat[i],x->not IsZero(x));
  mat[i]:=mat[i]/mat[i][piv];
  for j in [1..i-1] do
    mat[j]:=mat[j]-mat[j][piv]*mat[i];
  od;
od;
return mat;
end;
Screen455 := function()
local names, nam, t, p, b, d, n, cg, constraints, mat, r, support,
      fs, i, f, orb, orbs, df, parity, rank, rankaxis, axes, v,
      tables, available, complexhits, parityhits, gp, frob;
names:=AllCharacterTableNames();
tables:=0; available:=0; complexhits:=0; parityhits:=0;
for nam in names do
  t:=CharacterTable(nam); tables:=tables+1;
  cg:=GaloisMat(Irr(t)).generators;
  fs:=Indicator(t,2);
  for p in Set(FactorsInt(Size(t))) do
    b:=t mod p;
    if b=fail then continue; fi;
    d:=DecompositionMatrix(b);
    if d=fail then continue; fi;
    available:=available+1;
    n:=Length(Irr(b));
    frob:=PermList(List(Irr(b),x->Position(Irr(b),GaloisCyc(x,p))));
    orbs:=Orbits(Group(frob),[1..n]);
    df:=List(d,r->List(orbs,o->Sum(o,i->r[i])));
    constraints:=Set(Concatenation(List(cg,g->List([1..Length(d)],i->df[i]-df[i^g]))));
    constraints:=Filtered(constraints,r->not IsZero(r));
    if Length(constraints)>0 then
      mat:=ReducedRows455(constraints);
      if ForAny(mat,r->Number(r,x->x<>0)>2 or
                       (Number(r,x->x<>0)=2 and Sum(r)<>0)) then
        complexhits:=complexhits+1;
        Print("RATIONALITY_HIT ",nam," p=",p," orbits=",orbs,
              " constraints=",mat,"\n");
      fi;
    fi;
    # Parity screen is deliberately before rationality reduction, so it
    # may include hits removed by the rationality constraints above.
    parity:=List(Filtered([1..Length(fs)],i->fs[i]=-1),i->df[i]*One(GF(2)));
    parity:=Filtered(parity,r->not IsZero(r));
    if Length(parity)>0 then
      mat:=ReducedRows455(parity);
      if ForAny(mat,r->Number(r,x->x<>0*Z(2))>1) then
        parityhits:=parityhits+1;
        Print("PARITY_HIT ",nam," p=",p," orbits=",orbs,
              " constraints=",constraints," parity=",List(mat,r->List(r,Int)),"\n");
      fi;
    fi;
  od;
  if tables mod 100=0 then
    Print("PROGRESS tables=",tables," available=",available,"\n");
  fi;
od;
Print("DONE tables=",tables," available=",available," rationality_hits=",
      complexhits," parity_hits=",parityhits,"\n");
end;
Screen455();
QUIT;
