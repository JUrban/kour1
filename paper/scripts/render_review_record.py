#!/usr/bin/env python3
"""Render the supplied correspondence without editing its words.

Pandoc parses Markdown with smart typography disabled. Only layout metadata, table column widths and inline-code line breaking change. Raw originals and their digests accompany
the generated TeX, so the preservation claim is directly checkable.
"""
import argparse,copy,difflib,hashlib,json,subprocess
from pathlib import Path
PAPER=Path(__file__).resolve().parents[1]
REV=PAPER/'reviews/revision-2026-09-17'
DOCS=[('review.md','First external report (original version)','app:review-original'),
 ('reply.md','First author reply','app:reply-original'),
 ('review2.md','External follow-up report','app:review-followup'),
 ('reply2.md','Reply accompanying the revision','app:reply-final')]
def sha(b):return hashlib.sha256(b).hexdigest()
def words(node):
 if isinstance(node,list):return [v for n in node for v in words(n)]
 if not isinstance(node,dict):return []
 kind=node.get('t');c=node.get('c')
 if kind in ['Str','Code','CodeBlock','Math']:return [(kind,c if kind=='Str' else c[-1])]
 if kind=='Link':return words(c[1])
 if kind=='Header':return words(c[2])
 return words(c) if c is not None else [v for n in node.values() for v in words(n)]
def render(raw,prefix):
 ast=json.loads(subprocess.check_output(['pandoc','-f','markdown-smart','-t','json'],input=raw));before=words(ast)
 def transform(n):
  if isinstance(n,list):return [transform(v) for v in n]
  if not isinstance(n,dict):return n
  if n.get('t')=='Header':
   n['c'][0]=min(4,n['c'][0]+1);n['c'][1]=[prefix+'-'+n['c'][1][0],['unnumbered','unlisted'],[]]
  if n.get('t')=='Table':
   specs=n['c'][2]
   if len(specs)==3:
    for spec,width in zip(specs,[0.105,0.105,0.79]):spec[1]={'t':'ColWidth','c':width}
  return {k:transform(v) for k,v in n.items()}
 ast=transform(ast);assert words(ast)==before,'word-level AST changed'
 # Inline Code changes only representation: verbatim contents go to nolinkurl,
 # whose line-breaking permits long filenames/digests to fit a print column.
 def code_layout(n):
  if isinstance(n,list):return [code_layout(v) for v in n]
  if not isinstance(n,dict):return n
  if n.get('t')=='Code':
   literal=n['c'][1]
   assert literal.count('{')==literal.count('}'),literal
   return {'t':'RawInline','c':['latex',r'\nolinkurl{'+literal+'}']}
  return {k:code_layout(v) for k,v in n.items()}
 ast=code_layout(ast)
 tex=subprocess.check_output(['pandoc','-f','json','-t','latex','--wrap=auto'],input=json.dumps(ast).encode()).decode()
 return tex,sha(json.dumps(before,ensure_ascii=False).encode())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();outputs={};records=[]
 intro=r'''\clearpage
\section{Review correspondence: provenance}
\label{app:review-provenance}
The following four appendices reproduce the supplied documents in order,
with Markdown layout converted to print layout and no editorial changes
to their wording. Original section, theorem and appendix references point
to the 15 September paper, not to this revision. Assertions later withdrawn
remain in the original documents. The follow-up supersedes its author's
contradictory earlier assessments; the final reply corrects the first reply's
claims about completeness of the bundle and future certificate availability.
These are review records, not additional mathematical premises.

The original first report is undated in the supplied file. Both author
replies and the follow-up are dated 17 September 2026. The separately
supplied \artifact{review-update1.md} is a partial update of the first report;
it still contains some statements withdrawn in the follow-up. We retain its
raw text alongside an exact unified diff, rather than repeat the near-duplicate
report here. The originals, diff, and digest manifest are under
\artifact{paper/external-reviews/} in the repository and the full source archive.

The reviewer was Anthropic's Claude Opus[1m], model
\artifact{claude-opus-5[1m]}, with \texttt{xhigh} reasoning through
Claude Code. The organizers supplied this identification during the
subsequent editorial revision. Claude is credited with the independent
mathematical review and its computational and source checks; Codex wrote
the author replies. Section~\ref{sec:external-review} describes the process
and its mathematical outcomes.

The reviewer artifacts are in a separate repository,
\url{https://github.com/JUrban/kour1cl/tree/0d76dc7fc947a89a6f02e37b81da2320450efab6/review-other1}.
That pinned tree contains 83 files under \artifact{checks/} and five under
\artifact{checks2/}, together with the working notes. We inspected the
artifact index and follow-up logs; we have not rerun all the reviewer's
scripts. The reports distinguish external checking from the deadline record.
Claude's production account describes additional agent instances whose
findings it treated as leads and checked itself. This is separate-model
review, rather than an assertion of human specialist endorsement.
'''
 wrappers=[intro]
 for name,title,label in DOCS:
  raw=(PAPER/'external-reviews'/name).read_bytes();tex,wordhash=render(raw,name.replace('.','-'));dest='appendices/correspondence/'+name.replace('.md','.tex');outputs[dest]=tex
  wrappers.append('\\clearpage\n\\section{'+title+'}\n\\label{'+label+'}\n\\begingroup\n\\small\n\\input{'+dest.removesuffix('.tex')+'}\n\\endgroup\n')
  records.append({'path':'external-reviews/'+name,'bytes':len(raw),'sha256':sha(raw),'rendered_path':dest,'rendered_sha256':sha(tex.encode()),'word_ast_sha256':wordhash})
 original=(PAPER/'external-reviews/review.md').read_text();updated=(PAPER/'external-reviews/review-update1.md').read_text()
 diff=''.join(difflib.unified_diff(original.splitlines(True),updated.splitlines(True),fromfile='review.md',tofile='review-update1.md'))
 outputs['external-reviews/review-update1.diff']=diff
 raw=(PAPER/'external-reviews/review-update1.md').read_bytes();records.append({'path':'external-reviews/review-update1.md','bytes':len(raw),'sha256':sha(raw),'status':'Partial update preserved separately; superseded on disputed points by review2.md.'})
 outputs['appendices/review-correspondence.tex']='\n'.join(wrappers)
 outputs['external-reviews/manifest.json']=json.dumps({'conversion':'pandoc markdown-smart to latex; header metadata, table widths and verbatim inline-code line breaking adjusted; raw originals authoritative','pandoc_version':subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0],'documents':records,'update_diff_sha256':sha(diff.encode())},indent=2)+'\n'
 for name,value in outputs.items():
  p=PAPER/name
  if args.check:assert p.read_bytes()==value.encode(),('stale',name)
  else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value.encode())
 print('Correspondence: four unchanged word streams; raw inputs and partial-update diff bound by SHA-256.')
if __name__=='__main__':main()
