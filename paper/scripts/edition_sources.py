"""Resolve the two manuscript entry points and their explicit edition switches."""
import re
from pathlib import Path
ENTRIES={'full':'main.tex','mathematics':'mathematics.tex'}
OUTPUTS={'full':'kourovka-experiment','mathematics':'kourovka-mathematics'}

def select(text,edition):
    """Select only our full-paper switch; leave ordinary TeX conditionals intact.

    Our switches contain no engine conditionals. The engine test lives separately
    in the common preamble. Unknown TeX macros are not evaluated by this helper.
    """
    out=[];stack=[];active=True;last=0
    for m in re.finditer(r'\\iffullpaper\b|\\else\b|\\fi\b',text):
        if active:out.append(text[last:m.start()])
        token=m[0]
        if token==r'\iffullpaper' and text[max(0,m.start()-6):m.start()]==r'\newif':
            if active:out.append(token)
        elif token==r'\iffullpaper':
            stack.append((active,edition=='full'));active=active and edition=='full'
        elif stack and token==r'\else':
            parent,condition=stack[-1];active=parent and not condition
        elif stack and token==r'\fi':
            active=stack.pop()[0]
        elif active:out.append(token)
        last=m.end()
    assert not stack,'unclosed edition switch'
    if active:out.append(text[last:])
    return ''.join(out)

def sources(paper,edition):
    seen=[]
    def visit(name):
        assert name not in seen,('duplicate or circular input',edition,name)
        seen.append(name)
        text=select((paper/name).read_text(),edition)
        for target in re.findall(r'\\input\{([^}]+)\}',text):
            visit(target if target.endswith('.tex') else target+'.tex')
    visit(ENTRIES[edition])
    return seen

def content(paper,edition):
    return '\n'.join(select((paper/n).read_text(),edition) for n in sources(paper,edition))
