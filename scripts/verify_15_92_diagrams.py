#!/usr/bin/env python3
"""Independent dart reconstruction of Conder's S(7,0), U(7,0).

Source: thesis printed pp92,94, geometrical triangles and joining edges.
Anticlockwise triangle vertices encode y. Unjoined x vertices are fixed.
This controls the r=7 case only; the all-r proof imports Conder's construction.
"""
from pathlib import Path
from collections import Counter
import json
import subprocess
import datetime
import hashlib

ROOT=Path(__file__).resolve().parents[1]


class Diagram:
    def __init__(self):
        self.vertices={}
        self.x=[]
        self.y=[]
        self.reflected={}

    def tri(self,name,orientation,mirror):
        ports={'up':'LRT','down':'LBR','left':'LDU','right':'RUD'}[orientation]
        ids=list(range(len(self.x),len(self.x)+3))
        for port,i in zip(ports,ids):
            self.vertices[name,port]=i
        self.x+=ids
        self.y+=ids[1:]+ids[:1]
        self.reflected[name]=mirror

    def edge(self,a,b):
        i,j=self.vertices[a],self.vertices[b]
        assert self.x[i]==i and self.x[j]==j
        self.x[i],self.x[j]=j,i

    def finish(self):
        reflect={'L':'R','R':'L','T':'T','B':'B','U':'U','D':'D'}
        t=[None]*len(self.x)
        for (name,port),i in self.vertices.items():
            t[i]=self.vertices[self.reflected[name],reflect[port]]
        return dict(x=self.x,y=self.y,t=t)


def add_rect(D,prefix,mode='handle'):
    D.tri(prefix+'l','left',prefix+'r')
    D.tri(prefix+'r','right',prefix+'l')
    D.tri(prefix+'b','up',prefix+'b')
    D.edge((prefix+'l','D'),(prefix+'b','L'))
    D.edge((prefix+'b','R'),(prefix+'r','D'))
    if mode=='handle':
        D.tri(prefix+'h','down',prefix+'h')
        D.edge((prefix+'h','B'),(prefix+'b','T'))
        D.edge((prefix+'l','U'),(prefix+'r','U'))
    else:
        D.tri(prefix+'h','down',prefix+'h')
        D.edge((prefix+'h','B'),(prefix+'b','T'))
        D.edge((prefix+'h','L'),(prefix+'h','R'))
        D.tri(prefix+'u','up',prefix+'u')
        D.edge((prefix+'l','U'),(prefix+'u','L'))
        D.edge((prefix+'u','R'),(prefix+'r','U'))


def basic(which):
    D=Diagram()
    D.tri('ol','right','orr')
    D.tri('orr','left','ol')
    if which=='S':
        for i in range(3):
            add_rect(D,str(i))
        for i,port in enumerate(('U','R','D')):
            D.edge((str(i)+'l','L'),('ol',port))
            D.edge((str(i)+'r','R'),('orr','L' if port=='R' else port))
        handles=[(D.vertices[str(i)+'h','R'],D.vertices[str(i)+'h','L'])
                 for i in range(3)]
    else:
        add_rect(D,'0')
        add_rect(D,'2',mode='loop')
        D.tri('star','up','star')
        D.edge(('ol','R'),('star','L'))
        D.edge(('star','R'),('orr','L'))
        for prefix,port in [('0','U'),('2','D')]:
            D.edge((prefix+'l','L'),('ol',port))
            D.edge((prefix+'r','R'),('orr',port))
        handles=[(D.vertices['0h','R'],D.vertices['0h','L'])]
    out=D.finish();out['handles']=handles
    return out


def compose(a,b):
    n=len(a['x'])
    out={g:a[g]+[i+n for i in b[g]] for g in ('x','y','t')}
    ha=a['handles'][0];hb=[i+n for i in b['handles'][0]]
    for u,v in zip(ha,hb):
        assert out['x'][u]==u and out['x'][v]==v
        out['x'][u],out['x'][v]=v,u
    out['handles']=a['handles'][1:]+[tuple(i+n for i in h) for h in b['handles'][1:]]
    return out


def main():
    S,U=basic('S'),basic('U')
    actions=[dict(label='S7',**S),dict(label='U7',**U)]
    for k in (1,2,3,5,10):
        d=S
        for _ in range(k-1): d=compose(d,S)
        d=compose(d,U)
        actions.append(dict(label='chain'+str(k),**d))
    data=ROOT/'results/15.92-r7-diagrams.json'
    data.write_text(json.dumps(actions,indent=2)+'\n')
    lines=[]
    for a in actions:
        for gen in ('x','y','t'):
            lines.append(gen+':=PermList('+str([i+1 for i in a[gen]])+');;')
        n=len(a['x'])
        lines += [f'n:={n};;',
          'if not (x^2=() and y^3=() and (x*y)^7=() and t^2=() '
          'and (x*t)^2=() and (y*t)^2=()) then Error("relations"); fi;',
          'if (x*y*t)^2<>x*y*x*y^-1 then Error("word identity"); fi;',
          'w:=x*y*t;; g:=Group(x,y);;',
          f'Print("DIAGRAM {a["label"]} ",n," ",Collected(CycleLengths(w,[1..n])),"\\n");']
        if a['label'].startswith('chain'):
            lines += ['v:=(x*y*x*y^-1)^32760;;',
             'if NrMovedPoints(v)<>11 or Order(v)<>11 then Error("support"); fi;',
             'if SignPerm(x)<>1 or SignPerm(y)<>1 then Error("parity"); fi;',
             'if not IsTransitive(g,[1..n]) then Error("intransitive"); fi;',
             'if not IsPrimitive(g,[1..n]) then Error("imprimitive"); fi;',
             # Jordan: primitive + single 11-cycle with >=3 fixed points
             # contains A_n; even generators then give equality.
             'if n<14 then Error("Jordan degree bound"); fi;',
             'Print("ALTERNATING_CONTROL ",n," ",NrMovedPoints(v),"\\n");']
    lines += ['Print("15_92_GAP_DIAGRAMS_DONE\\n");','QUIT_GAP(0);']
    gapfile=ROOT/'results/15.92-r7-diagrams.g'
    gapfile.write_text('\n'.join(lines)+'\n')
    log=ROOT/'results/15.92-r7-diagrams.log'
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with log.open('w') as f:
        p=subprocess.run([str(ROOT/'bin/gap'),str(gapfile)],stdout=f,stderr=subprocess.STDOUT)
    process={'started_utc':start,'returncode':p.returncode,
             'input_sha256':hashlib.sha256(gapfile.read_bytes()).hexdigest(),
             'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
    (ROOT/'results/15.92-r7-diagram-process.json').write_text(json.dumps(process,indent=2)+'\n')
    contents=log.read_text()
    print(contents)
    assert p.returncode==0 and '15_92_GAP_DIAGRAMS_DONE' in contents
    assert not any(s in contents for s in ('Error','Syntax warning','brk>'))
    print('15_92_DIAGRAM_RECONSTRUCTION_DONE')


if __name__=='__main__':
    main()
