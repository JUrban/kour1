#!/usr/bin/env python3
"""Check preservation and navigation obligations of the reader-focused revision."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
PAPER=Path(__file__).resolve().parents[1]
R=PAPER/'reviews/polish-2026-09-17'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 baseline=json.loads((R/'baseline.json').read_text());checked=[]
 for old,digest in baseline['source_sha256'].items():
  if not re.match(r'appendices/(candidates|partials|prior)/',old):continue
  new=old.replace('appendices/','sections/',1);raw=(PAPER/new).read_bytes()
  if new=='sections/candidates/20-90.tex':
   raw=raw.replace(rb'Section~\ref{cand:10.35}',rb'Appendix~\ref{cand:10.35}')
  assert sha(raw)==digest,('mathematical source changed',old,new)
  checked.append({'old':old,'new':new,'baseline_sha256':digest})
 assert len(checked)==50,len(checked)
 # Every live TeX source is reachable exactly once from main.tex. This also
 # checks that relocation did not leave an unused proof or double inclusion.
 seen={}
 def visit(path):
  seen[path]=seen.get(path,0)+1;assert seen[path]==1,('duplicate input',path)
  text=(PAPER/path).read_text()
  for target in re.findall(r'\\input\{([^}]+)\}',text):visit(target+'.tex')
 visit('main.tex')
 actual={'main.tex'}|{str(p.relative_to(PAPER)) for d in ['sections','appendices'] for p in (PAPER/d).rglob('*.tex')}
 assert set(seen)==actual,('unreachable source',actual-set(seen))
 # Supplied correspondence remains identical to the inputs from the first revision.
 historical=json.loads((PAPER/'reviews/revision-2026-09-17/baseline.json').read_text())
 for name in ['review.md','review-update1.md','review2.md','reply.md']:
  path='external-reviews/'+name;assert sha((PAPER/path).read_bytes())==historical['inputs'][path]['sha256']
 for name,digest in baseline['data_sha256'].items():
  assert sha((PAPER/name).read_bytes())==digest,('historical data changed',name)
 meta=json.loads((PAPER/'data/reviewer-metadata.json').read_text())
 assert (meta['model'],meta['provider'],meta['reasoning_effort'],meta['harness'])==('claude-opus-5[1m]','Anthropic','xhigh','Claude Code')
 text='\n'.join((PAPER/p).read_text() for p in seen if p.startswith('sections/'))
 assert not re.search(r'Appendix~\\ref\{(?:cand:|app:(?:inventory|candidates|partials|prior))',text)
 result={'status':'PASS','baseline_commit':baseline['baseline_commit'],'mathematical_source_files_checked':len(checked),
  'allowed_mathematical_source_change':'20.90: Appendix to Section in the cross-reference to 10.35; proof text otherwise byte-identical.',
  'reachable_tex_files':len(seen),'historical_data_files_checked':len(baseline['data_sha256']),'original_correspondence_preserved':True,'reviewer_metadata':meta,
  'mathematical_sources':checked}
 (R/'preservation-audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS: 50 mathematical sources preserved; all TeX inputs reachable once; original correspondence and reviewer metadata checked.')
if __name__=='__main__':main()
