SizeScreen([1000000,1000000]);;
Read("results/16.9-witnesses.g");;
(function()
 local F,gens,Eval,row,w,p,factors,checks,letters,paritybound,counts,a;
 F:=FreeGroup(22); gens:=GeneratorsOfGroup(F);
 Eval:=function(word)
   local value,a;
   value:=One(F);
   for a in word do value:=value*gens[AbsInt(a)]^SignInt(a); od;
   return value;
 end;
 checks:=0; letters:=0;
 for row in PalindromicCases do
   w:=row[1]; factors:=row[2];
   Assert(0,Length(factors)=row[3]);
   Assert(0,LetterRepAssocWord(Eval(w))=w);
   for p in factors do
     Assert(0,Length(p)>0 and Reversed(p)=p and LetterRepAssocWord(Eval(p))=p);
     letters:=letters+Length(p);
   od;
   if IsEmpty(factors) then Assert(0,Eval(w)=One(F));
   else Assert(0,Product(List(factors,Eval))=Eval(w)); fi;
   counts:=List([1..22],a->Number(w,x->AbsInt(x)=a));
   paritybound:=Number(counts,x->x mod 2=1);
   Assert(0,paritybound<=row[3]);
   checks:=checks+1;
 od;
 Print("PASS_FREE_GROUP_WITNESSES cases=",checks," palindrome_letters=",letters,
       " rank=",Length(gens)," parity_lower_bounds=",checks,"\n");
end)();
QUIT_GAP(0);
