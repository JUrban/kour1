# Manuscript-phase check of the published/library input in Appendix C (4.55).
# This checks row numbering and field orbits; it is not a reconstruction of
# the character table from the permutation group. That separate historical
# computation is preserved in scripts/verify_4_55.g in the research archive.
SetAssertionLevel(2);
Print("GAP ",GAPInfo.Version,"; CTblLib ",PackageInfo("ctbllib")[1].Version,"\n");
table455 := CharacterTable("3.A7");;
brauer455 := table455 mod 5;;
matrix455 := DecompositionMatrix(brauer455);;
pairs455 := [[9,10],[11,12],[17,18],[19,20]];;
rows455 := [10,16,18,20,22];;
conjugates455 := [11,17,19,23,21];;
expected455 := [[0,1,0,0],[0,0,0,1],[1,0,1,0],[1,0,0,1],[0,1,1,0]];;
Assert(0,Size(table455)=7560);
Assert(0,List(pairs455,o->Sum(o,j->Irr(brauer455)[j][1]))=[6,12,36,42]);
Assert(0,ForAll(pairs455,o->GaloisCyc(Irr(brauer455)[o[1]],5)=Irr(brauer455)[o[2]]
    and GaloisCyc(Irr(brauer455)[o[2]],5)=Irr(brauer455)[o[1]]));
for i455 in [1..5] do
    Assert(0,List(pairs455,o->Sum(o,j->matrix455[rows455[i455]][j]))=expected455[i455]);
    Assert(0,List(pairs455,o->Sum(o,j->matrix455[conjugates455[i455]][j]))=expected455[i455]);
    Assert(0,GaloisCyc(Irr(table455)[rows455[i455]],-1)=Irr(table455)[conjugates455[i455]]);
od;
Assert(0,ForAll(Difference([1..Length(Irr(table455))],Concatenation(rows455,conjugates455)),
    i->ForAll(Concatenation(pairs455),j->matrix455[i][j]=0)));
Assert(0,List(pairs455,o->Sum([1..Length(Irr(table455))],
    i->Irr(table455)[i][1]*Sum(o,j->matrix455[i][j])))=[90,60,90,90]);
galois455 := Group(GaloisMat(Irr(table455)).generators);;
for o455 in [[10,11],[16,17],[18,19],[20,21,22,23]] do
    Assert(0,Set(Orbit(galois455,o455[1]))=o455);
od;
Print("PASS manuscript 4.55 input: 10 rows, 4 Frobenius pairs, 4 Galois orbits, 4 projective dimensions\n");
QUIT_GAP(0);
