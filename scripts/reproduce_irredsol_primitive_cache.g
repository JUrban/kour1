# A minimal local diagnostic. No library source is modified.
LoadPackage("irredsol");;
for k in [1,6] do
    g:=IrreducibleSolubleMatrixGroup(2,5,1,k);
    Print("ID=2,5,1,",k," complement=",Size(g),
        " indexed_affine=",Size(PrimitivePcGroup(2,5,1,k)),
        " matrix_affine=",Size(PrimitivePcGroupIrreducibleMatrixGroup(g)),
        " required=",25*Size(g),"\n");
od;
QUIT;
