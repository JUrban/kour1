#!/usr/bin/env python3
"""Bind the v4 change excerpts to the preserved v3 and current shared sources."""
import argparse,json
from pathlib import Path
from make_inventory import tex
from revision_sources import v3_source
PAPER=Path(__file__).resolve().parents[1]
def render():
    rows=json.loads((PAPER/'reviews/v4-2026-09-19/changes.json').read_text())
    out=[r'''\subsection{Version 4: two editions from shared mathematical sources}
The complete v3 PDF is preserved as
\artifact{paper/versions/kourovka-experiment-2026-09-19-v3.pdf}.
The following literal source excerpts identify the version and dependency
changes. Appendix~\ref{app:two-editions} describes the two presentations.
''']
    for r in rows:
        assert r['before'] in v3_source(PAPER,r['before_path']).decode(),r['title']
        assert r['after'] in (PAPER/r['after_path']).read_text(),r['title']
        out.append('\\paragraph{'+tex(r['title'])+'}\n')
        for k,v in [('before','Version 3'),('after','Version 4')]:
            out.append('\\noindent\\textbf{'+v+'.}\\begin{quote}\\small\n'+r[k]+'\n\\end{quote}\n')
        out.append(tex(r['reason'])+'\n')
    out.append(r'''The original question and author blocks are additions, drawn from the
shared metadata. Three representative arguments were extracted into
separate input files; their mathematical text is preserved. The same
partial and prior-work arguments appear in both editions, while the
mathematical edition omits the experimental narrative, review correspondence,
bounded unsuccessful searches and withdrawn 10.35 application. The current
index is generated separately from the frozen deadline ledger. Preservation
checks and the source changes are recorded in
\artifact{paper/reviews/v4-2026-09-19/}.
''')
    return '\n'.join(out)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    s=render();p=PAPER/'appendices/v4-changes.tex'
    if a.check:assert p.read_text()==s,'stale v4 change excerpts'
    else:p.write_text(s)
    print('PASS: three exact v3/v4 change pairs.')
if __name__=='__main__':main()
