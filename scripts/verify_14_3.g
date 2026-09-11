# Independent actual-element square roots and Frobenius--Schur indicators.
LoadPackage("ctbllib");;SizeScreen([1000000,24]);;
Verify143:=function()
local groups,G,t,irr,cl,els,pos,sqpos,indicators,reals,directreals,
      z,zi,central,squares,tablecentral,tablesquares,pow,sizes,
      rootclasses,roots,directroots,candidates,oddpass,total,fschecks,
      nonsquares,realreject,oddreject,passed;
groups:=Concatenation([CyclicGroup(IsPermGroup,4),
 SmallGroup(12,1),AlternatingGroup(4),AlternatingGroup(5),SL(2,3)],
 AllSmallGroups(16));
total:=0;fschecks:=0;nonsquares:=0;realreject:=0;oddreject:=0;passed:=0;
for G in groups do
 t:=CharacterTable(G);irr:=Irr(t);cl:=ConjugacyClasses(t);els:=AsSortedList(G);
 pos:=List(els,x->PositionProperty(cl,c->x in c));
 sqpos:=List(els,x->PositionProperty(cl,c->x*x in c));
 indicators:=List(irr,c->Sum(sqpos,j->c[j])/Size(G));
 Assert(0,ForAll(indicators,x->x in [-1,0,1]));
 reals:=Filtered([1..Length(irr)],i->ForAll(irr[i],x->ComplexConjugate(x)=x));
 directreals:=Filtered([1..Length(irr)],i->indicators[i]<>0);
 Assert(0,reals=directreals);fschecks:=fschecks+Length(irr);
 central:=AsSortedList(Centre(G));squares:=Set(List(central,x->x*x));
 sizes:=SizesConjugacyClasses(t);pow:=PowerMap(t,2);
 tablecentral:=Filtered([1..Length(cl)],j->sizes[j]=1);
 tablesquares:=Set(List(tablecentral,j->pow[j]));
 Assert(0,Set(List(central,x->PositionProperty(cl,c->x in c)))=tablecentral);
 Assert(0,Set(List(squares,x->PositionProperty(cl,c->x in c)))=tablesquares);
 for z in Difference(central,squares) do
  nonsquares:=nonsquares+1;zi:=PositionProperty(cl,c->z in c);
  roots:=Filtered([1..Length(cl)],j->pow[j]=zi and sizes[j] mod 2=1);
  rootclasses:=Union(List(roots,j->AsSortedList(cl[j])));
  directroots:=Filtered(els,x->x*x=z and Index(G,Centralizer(G,x)) mod 2=1);
  Assert(0,rootclasses=directroots);
  if ForAny(directreals,i->irr[i][zi]<>irr[i][1]) then
   realreject:=realreject+1;
  elif IsEmpty(directroots) then oddreject:=oddreject+1;
  else passed:=passed+1;fi;
 od;
 total:=total+1;Print("CONTROL143 order=",Size(G)," classes=",Length(cl),
 " real_characters=",Length(reals)," nonsquares=",Length(Difference(central,squares)),"\n");
od;
Assert(0,realreject>0 and oddreject>0);
Print("PASS143 groups=",total," indicator_checks=",fschecks,
 " nonsquares=",nonsquares," real_rejected=",realreject,
 " odd_root_rejected=",oddreject," surviving_elements=",passed,"\n");
end;
Verify143();QUIT;
