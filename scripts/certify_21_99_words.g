# Positive witnesses are multiplication circuits over the supplied generators.
SizeScreen([100000,100000]);;
Value2199:=function(ctx,a)
  if a=0 then return (); elif a<0 then return ctx.values[-a]^-1;
  else return ctx.values[a]; fi;
end;;
Node2199:=function(ctx,a,b)
  local value,known,index;
  if a=0 then return b; elif b=0 then return a; elif a=-b then return 0; fi;
  value:=Value2199(ctx,a)*Value2199(ctx,b);
  known:=LookupDictionary(ctx.dictionary,value);
  if known<>fail then return known; fi;
  Add(ctx.code,[a,b]); Add(ctx.values,value); index:=Length(ctx.values);
  AddDictionary(ctx.dictionary,value,index);
  if value<>value^-1 then AddDictionary(ctx.dictionary,value^-1,-index); fi;
  return index;
end;;
Witness2199:=function(ctx,c)
  local x,beta,word,queue,q,a,gamma,new;
  if Number([1..ctx.degree],i->i^Value2199(ctx,c)=i)=1 then return; fi;
  for x in [1..ctx.degree] do
    beta:=(x^Value2199(ctx,c))^Value2199(ctx,-ctx.transversals[x]);
    if ctx.witnesses[beta]<>fail then continue; fi;
    word:=Node2199(ctx,Node2199(ctx,ctx.transversals[x],c),-ctx.transversals[x]);
    ctx.witnesses[beta]:=word; queue:=[beta]; q:=1;
    while q<=Length(queue) do
      beta:=queue[q]; q:=q+1;
      for a in ctx.stabilizer do
        gamma:=beta^Value2199(ctx,a);
        if ctx.witnesses[gamma]=fail then
          new:=Node2199(ctx,Node2199(ctx,-a,ctx.witnesses[beta]),a);
          ctx.witnesses[gamma]:=new; Add(queue,gamma);
        fi;
      od;
    od;
  od;
end;;
Compress2199:=function(ctx)
  local used,visit,i,renumber,code,m,translate;
  m:=Length(ctx.generators); used:=[];
  visit:=function(a)
    local j;
    a:=AbsInt(a);
    if a<=m or a in used then return; fi;
    AddSet(used,a);
    for j in ctx.code[a-m] do visit(j); od;
  end;
  for i in ctx.witnesses do if i<>fail then visit(i); fi; od;
  renumber:=List([1..Length(ctx.values)],i->0);
  for i in [1..m] do renumber[i]:=i; od;
  for i in [1..Length(used)] do renumber[used[i]]:=m+i; od;
  translate:=function(a)
    if a=0 then return 0; elif a<0 then return -renumber[-a]; else return renumber[a]; fi;
  end;
  code:=List(used,i->List(ctx.code[i-m],translate));
  return [code,List(ctx.witnesses,translate)];
end;;
Certify2199:=function(n,id,cap)
  local g,ctx,i,queue,q,x,y,j,k,c,trials,compressed;
  g:=TransitiveGroup(n,id);
  ctx:=rec(degree:=n,generators:=GeneratorsOfGroup(g),code:=[],stabilizer:=[],
    transversals:=List([1..n],i->fail),witnesses:=List([1..n],i->fail));
  ctx.values:=ShallowCopy(ctx.generators); ctx.dictionary:=NewDictionary((),true);
  AddDictionary(ctx.dictionary,(),0);
  for i in [1..Length(ctx.generators)] do
    AddDictionary(ctx.dictionary,ctx.generators[i],i);
    if ctx.generators[i]<>ctx.generators[i]^-1 then
      AddDictionary(ctx.dictionary,ctx.generators[i]^-1,-i);
    fi;
  od;
  ctx.transversals[1]:=0; ctx.witnesses[1]:=0; queue:=[1]; q:=1;
  while q<=Length(queue) do
    x:=queue[q]; q:=q+1;
    for j in [1..Length(ctx.generators)] do
      y:=x^ctx.generators[j];
      if ctx.transversals[y]=fail then
        ctx.transversals[y]:=Node2199(ctx,ctx.transversals[x],j); Add(queue,y);
      fi;
    od;
  od;
  if Length(queue)<>n then Error("catalogue action not transitive"); fi;
  for x in [1..n] do
    for j in [1..Length(ctx.generators)] do
      y:=x^ctx.generators[j];
      k:=Node2199(ctx,Node2199(ctx,ctx.transversals[x],j),-ctx.transversals[y]);
      if k<>0 then AddSet(ctx.stabilizer,k); fi;
    od;
  od;
  for j in [1..Length(ctx.generators)] do
    Witness2199(ctx,j);
    if not fail in ctx.witnesses then break; fi;
  od;
  trials:=0; c:=0;
  while fail in ctx.witnesses and trials<cap do
    j:=Random([1..Length(ctx.generators)]);
    if Random([0,1])=0 then j:=-j; fi;
    c:=Node2199(ctx,c,j); trials:=trials+1; Witness2199(ctx,c);
  od;
  if fail in ctx.witnesses then
    return rec(status:="UNRESOLVED",degree:=n,id:=id,trials:=trials,
      missing:=Filtered([1..n],i->ctx.witnesses[i]=fail));
  fi;
  for i in [2..n] do
    c:=Value2199(ctx,ctx.witnesses[i]);
    if 1^c<>i or Number([1..n],x->x^c=x)=1 then Error("constructed witness invalid"); fi;
  od;
  compressed:=Compress2199(ctx);
  return [n,id,List(ctx.generators,g->List([1..n],i->i^g-1)),
    compressed[1],compressed[2],trials,Length(ctx.values)];
end;;
