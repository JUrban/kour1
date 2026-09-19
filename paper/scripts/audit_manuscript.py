#!/usr/bin/env python3
"""Check both rendered editions, reference coverage and source/PDF binding."""
import collections,hashlib,json,re,subprocess
from pathlib import Path
from datetime import datetime,timezone
from edition_sources import ENTRIES,sources,content
PAPER=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    current=json.loads((PAPER/'data/current-assessment.json').read_text())
    assert (current['historical_candidates'],current['withdrawn_candidates'],current['remaining_candidates'])==(46,['10.35'],45)
    frozen=json.loads((PAPER/'data/frozen-candidate-ledger.json').read_text())['candidates']
    review=json.loads((PAPER/'reviews/candidate-review-ledger.json').read_text())['entries']
    assert len(frozen)==len(review)==46
    assert {r['problem'] for r in frozen}=={r['problem'] for r in review}
    assert all(r['final_pass']=='passed_internal_review' and r['final_pass_notes'] and r['outside_reviews']==0 and r['priority']=='unestablished' for r in review)
    bibkeys=re.findall(r'@\w+\s*\{\s*([^,\s]+)\s*,',(PAPER/'references.bib').read_text())
    assert len(bibkeys)==len(set(bibkeys))
    ancillary=json.loads((PAPER/'ancillary/manifest.json').read_text())
    for r in ancillary['files']:
        f=PAPER/'ancillary'/r['path'];assert f.stat().st_size==r['bytes'] and sha(f)==r['sha256']
    assert len(ancillary['files'])==24
    assert (PAPER/'appendices/carpet-tables.tex').read_text().count(r'\begin{minipage}')==19
    results={}
    for edition,entry in ENTRIES.items():
        b=PAPER/'build'/edition;stem=Path(entry).stem
        receipt=json.loads((b/'build-receipt.json').read_text())
        assert receipt['edition']==edition and receipt['exit_code']==0
        assert sha(b/f'{stem}.pdf')==receipt['pdf_sha256']
        for n,h in receipt['source_sha256'].items():assert sha(PAPER/n)==h,('stale build',edition,n)
        paths=sources(PAPER,edition);text=content(PAPER,edition)
        labels=re.findall(r'\\label\{([^}]+)\}',text)
        assert len(labels)==len(set(labels)),('duplicate labels',edition,[k for k,n in collections.Counter(labels).items() if n>1])
        refs=set(re.findall(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}',text))
        assert not refs-set(labels),(edition,refs-set(labels))
        cites={key.strip() for group in re.findall(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}',text) for key in group.split(',')}
        assert not cites-set(bibkeys)
        assert not re.search(r'\b(?:TODO|TBD|FIXME)\b',text)
        for name in [f'{stem}.log',f'{stem}.blg']:
            log=(b/name).read_text();assert not re.search(r'undefined|multiply defined|Overfull|Warning--|LaTeX Warning',log,re.I),(edition,name)
        # Log occurrences prove the shared question macros actually reached TeX.
        want=collections.Counter(re.findall(r'\\problemstatement\{([\d.]+)\}',text))
        got=collections.Counter(re.findall(r'KNSTATEMENT:([\d.]+)',(b/f'{stem}.log').read_text()))
        assert got==want,(edition,got-want,want-got)
        info=subprocess.check_output(['pdfinfo',str(b/f'{stem}.pdf')],text=True)
        results[edition]={'status':'PASS','pages':int(re.search(r'Pages:\s+(\d+)',info)[1]),'tex_files':len(paths),'labels':len(labels),'cited_works':len(cites),'rendered_question_blocks':sum(got.values()),'pdf_sha256':receipt['pdf_sha256']}
    result={'status':'PASS','checked_utc':datetime.now(timezone.utc).isoformat(),
      'scope':'Both edition input graphs, references, bibliography, actual rendered question coverage, source/build bindings and ancillary integrity. Not a mathematical theorem verification.',
      'historical_candidates':46,'withdrawn_claims':['10.35'],'remaining_candidates':45,'editions':results,
      'ancillary_original_files':24,'printed_carpet_derivations':19}
    (PAPER/'reviews/structure-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
