# Bounded exploratory test of saturation for F=N^3.
Residual20112:=function(g,n)
  local r,i;
  r:=g;
  for i in [1..n] do r:=Last(LowerCentralSeriesOfGroup(r)); od;
  return r;
end;;
Subnormal20112:=function(g,h,n)
  local k,next,path;
  k:=g; path:=[Size(k)];
  while k<>h do
    next:=ClosureGroup(h,Residual20112(k,n));
    if next=k then return [false,path]; fi;
    k:=next; Add(path,Size(k));
  od;
  return [true,path];
end;;
Wstar20112:=function(g,n)
  local p,h,res,rows;
  rows:=[];
  for p in Set(FactorsInt(Size(g))) do
    if p<>1 then
      h:=Normalizer(g,SylowSubgroup(g,p));
      res:=Subnormal20112(g,h,n); Add(rows,[p,Size(h),res]);
      if not res[1] then return [false,rows]; fi;
    fi;
  od;
  return [true,rows];
end;;
if Wstar20112(SymmetricGroup(3),1)[1] then Error("N control"); fi;
if Wstar20112(SymmetricGroup(4),2)[1] then Error("N^2 control"); fi;
if not Wstar20112(SymmetricGroup(4),3)[1] then Error("N^3 control"); fi;
for ord20112 in [648,1296,1944] do
  count20112:=NumberSmallGroups(ord20112); outside20112:=0;
  phin20112:=0; quot20112:=0; hit20112:=0;
  for id20112 in [1..count20112] do
    g20112:=SmallGroup(ord20112,id20112);
    if Size(Residual20112(g20112,3))>1 then
      outside20112:=outside20112+1;
      phi20112:=FrattiniSubgroup(g20112);
      if Size(phi20112)>1 then
        phin20112:=phin20112+1;
        q20112:=g20112/phi20112; qr20112:=Wstar20112(q20112,3);
        if qr20112[1] then
          quot20112:=quot20112+1; gr20112:=Wstar20112(g20112,3);
          Print("ELIGIBLE ",[ord20112,id20112,Size(phi20112),qr20112,gr20112],"\n");
          if not gr20112[1] then hit20112:=hit20112+1; fi;
        fi;
      fi;
    fi;
    if id20112 mod 250=0 then Print("PROGRESS ",[ord20112,id20112],"\n"); fi;
  od;
  Print("ORDER_DONE ",[ord20112,count20112,outside20112,phin20112,quot20112,hit20112],"\n");
od;
Print("PASS_SCREEN_20_112\n");
QUIT_GAP(0);
