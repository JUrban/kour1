LoadPackage("json");;
SetInfoLevel(InfoWarning,0);;
RunA5Control:=function(n)
  local s,g,pr,classes,c,h,images,full,r,b,border,bp,power,normalodd,k,
        best,bound,hist,key,entry,subgroups,odd,proper;
  s:=AlternatingGroup(5);
  proper:=List(Filtered(ConjugacyClassesSubgroups(s),c->Size(Representative(c))<60),Representative);
  if not ForAll(proper,IsSolvableGroup) or Maximum(List(proper,Size))<>12 then Error("proper subgroup control"); fi;
  odd:=Filtered(ConjugacyClassesSubgroups(s),c->IsOddInt(Size(Representative(c))));
  if not ForAll(odd,c->IsAbelian(Representative(c))) then Error("odd subgroup control"); fi;
  if n=1 then g:=s;pr:=[IdentityMapping(s)];
  else g:=DirectProduct(s,s);pr:=[Projection(g,1),Projection(g,2)];fi;
  classes:=ConjugacyClassesSubgroups(g);hist:=[];subgroups:=0;
  for c in classes do
    h:=Representative(c);images:=List(pr,f->Image(f,h));
    full:=Filtered([1..n],i->Size(images[i])=60);
    if Length(full)=0 then r:=0;b:=h;
    elif Length(full)=n then
      if Size(h)=60 then r:=1;elif Size(h)=3600 then r:=2;else Error("subdirect order");fi;
      b:=TrivialSubgroup(h);
    else
      r:=1;b:=Kernel(RestrictedMapping(pr[full[1]],h));
      if Size(h)<>60*Size(b) or Size(b)<>Size(images[3-full[1]]) then Error("mixed splitting");fi;
    fi;
    if not IsSolvableGroup(b) then Error("soluble factor");fi;
    border:=Size(b);bp:=Size(SylowSubgroup(b,2));power:=Size(SylowSubgroup(h,2));
    if power<>4^r*bp then Error("Sylow splitting");fi;
    normalodd:=Filtered(NormalSubgroups(h),k->IsOddInt(Size(k)));
    k:=First(normalodd,k->Size(k)=Maximum(List(normalodd,Size)));
    if not IsAbelian(k) then Error("odd radical nonabelian");fi;
    best:=Index(h,k);bound:=60^r*bp^2;
    if best>bound then Error("index bound");fi;
    key:=[Size(h),power,best,r,border,bp];
    entry:=First(hist,e->e[1]=key);
    if entry=fail then Add(hist,[key,Size(c)]);else entry[2]:=entry[2]+Size(c);fi;
    subgroups:=subgroups+Size(c);
  od;
  Sort(hist);
  Print(GapToJsonString(rec(model:="a5_power",factors:=n,subgroup_classes:=Length(classes),subgroups:=subgroups,histogram:=hist)),"\n");
end;;
RunA5Control(1);;
RunA5Control(2);;
Print("PASS_21_121B_A5_NATIVE\n");
QUIT_GAP(0);
