# Refine every flag in the completed real-character screen by odd class roots.
LoadPackage("ctbllib");;SizeScreen([1000000,24]);;
Refine143:=function()
local file,line,names,words,name,t,irr,sizes,pow,central,squares,reals,
      candidates,survivors,z,roots,flagged,elements,left;
file:=InputTextFile("results/14.3-real-character-screen.log");names:=[];
while not IsEndOfStream(file) do
 line:=ReadLine(file);
 if line=fail then break;fi;
 if StartsWith(line,"FLAG143 name=") then
  words:=SplitString(line," ","");Add(names,words[2]{[6..Length(words[2])]});
 fi;
od;CloseStream(file);
Assert(0,Length(names)=Length(Set(names)));
Print("START_REFINE143 flagged_tables=",Length(names),"\n");
flagged:=0;elements:=0;left:=0;
for name in names do
 t:=CharacterTable(name);irr:=Irr(t);sizes:=SizesConjugacyClasses(t);
 pow:=PowerMap(t,2);central:=Filtered([1..Length(sizes)],j->sizes[j]=1);
 squares:=Set(List(central,j->pow[j]));
 reals:=Filtered(irr,c->ForAll(c,x->ComplexConjugate(x)=x));
 candidates:=Filtered(Difference(central,squares),j->ForAll(reals,c->c[j]=c[1]));
 survivors:=[];
 for z in candidates do
  roots:=Filtered([1..Length(sizes)],j->pow[j]=z and sizes[j] mod 2=1);
  if not IsEmpty(roots) then Add(survivors,z);fi;
  Print("ELEMENT143 name=",name," central_index=",z," odd_root_classes=",roots,"\n");
 od;
 elements:=elements+Length(candidates);left:=left+Length(survivors);
 if not IsEmpty(survivors) then flagged:=flagged+1;fi;
 Print("REFINED143 name=",name," candidates=",Length(candidates),
  " surviving_elements=",Length(survivors),"\n");
od;
Print("DONE_REFINE143 tables=",Length(names)," candidates=",elements,
 " flagged_tables=",flagged," surviving_elements=",left,"\n");
end;
Refine143();QUIT;
