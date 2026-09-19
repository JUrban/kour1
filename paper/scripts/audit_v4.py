#!/usr/bin/env python3
"""Check shared proofs, v3 preservation, statement evidence and edition scope."""
import hashlib,json,re
from pathlib import Path
from edition_sources import sources,select,content
from public_review_files import public_review_files
from render_editions import render
from render_v4_changes import render as render_changes
PAPER=Path(__file__).resolve().parents[1]
REV=PAPER/'reviews/v4-2026-09-19'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(text,before):
    # Undo only the enumerated editorial operations; no mathematical token edits.
    text=select(text,'full')
    text=re.sub(r'\\problemstatement\{[^}]+\}\n','',text)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',before))
    text=re.sub(r'\\label\{([^}]+)\}\n',lambda m:m[0] if m[1] in oldlabels else '',text)
    for command in [r'\comparisonlocation',r'\Comparisonlocation']:
        text=text.replace(command+'{}',r'Appendix~\ref{app:contemporary-comparison}')
        text=text.replace(command,r'Appendix~\ref{app:contemporary-comparison}')
    text=text.replace(r'\reproductionlocation{}',r'Appendix~\ref{app:reproduction}')
    text=text.replace(r'\reproductionlocation',r'Appendix~\ref{app:reproduction}')
    text=text.replace('Related work.','Version 2 attribution.')
    text=text.replace(r'The cyclic-vector argument of Lemma~\ref{lem:matrix-centralizer}',r'The cyclic-vector argument of Section~\ref{cand:10.35}')
    # Wrapping unchanged full-edition paragraphs can add boundary newlines.
    return re.sub(r'\s+',' ',text).strip()
def main():
    b=json.loads((REV/'baseline.json').read_text())
    bindings={r['path']:r['sha256'] for r in b['sources']}
    for n,h in bindings.items():assert sha(REV/'baseline-source'/n)==h,n
    assert sha(PAPER/b['pdf']['path'])==b['pdf']['sha256']
    preserved=[];proof_bindings=[]
    for n in bindings:
        if re.match(r'sections/(candidates|partials|prior|attribution)/',n):
            old=(REV/'baseline-source'/n).read_text();new=(PAPER/n).read_text()
            assert normalize(new,old)==normalize(old,old),('changed proof or attribution',n)
            preserved.append(n)
            proof_bindings.append({'before_path':n,'after_path':n,
                'v3_sha256':bindings[n],'v4_sha256':sha(PAPER/n)})
    assert len(preserved)==61,len(preserved)
    # Reassemble the three extracted representative arguments and compare exactly
    # up to whitespace, their new headings, question blocks and display references.
    old=(REV/'baseline-source/sections/representative.tex').read_text()
    starts=[m.start() for m in re.finditer(r'\\subsection\{',old)]
    end=old.index(r'\input{sections/candidates/19-56}')
    for i,n in enumerate(['21.106','21.68','20.108']):
        before=old[starts[i]:starts[i+1] if i<2 else end]
        after=(PAPER/'sections/candidates'/f'{n.replace(".","-")}.tex').read_text()
        after=after.replace(': Problem '+n+'}', '}')
        assert normalize(after,before)==normalize(before,before),('extracted proof changed',n)
        path='sections/candidates/'+n.replace('.','-')+'.tex'
        proof_bindings.append({'before_path':'sections/representative.tex',
            'before_problem':n,'after_path':path,
            'v3_excerpt_sha256':hashlib.sha256(before.encode()).hexdigest(),
            'v4_sha256':sha(PAPER/path)})
    for n in bindings:
        if n.startswith('appendices/correspondence/') or n.startswith('data/'):
            assert sha(PAPER/n)==bindings[n],('historical content changed',n)
    assert sha(PAPER/'appendices/carpet-tables.tex')==bindings['appendices/carpet-tables.tex']
    full=set(sources(PAPER,'full'));math=set(sources(PAPER,'mathematics'))
    ledger=json.loads((PAPER/'data/frozen-candidate-ledger.json').read_text())['candidates']
    expected=set()
    for r in ledger:
        n=r['problem'];stem='21-121a' if n=='21.121' else n.replace('.','-')
        path='sections/candidates/'+stem+'.tex'
        assert path in full
        if n=='10.35':assert path not in math
        else:expected.add(path);assert path in math
    assert len(expected)==45
    actual={x for x in math if x.startswith('sections/candidates/')}
    assert actual==expected
    shared=set(preserved)-{'sections/candidates/10-35.tex'}
    assert shared<=full&math,shared-(full&math)
    assert 'shared/matrix-centralizer.tex' in full&math
    assert 'cand:10.35' not in content(PAPER,'mathematics')
    assert not any(x.startswith('appendices/correspondence/') for x in math)
    assert 'sections/methods.tex' not in math and 'sections/external-review.tex' not in math
    assert 'Bounded exclusions with no general conclusion' not in content(PAPER,'mathematics')
    assert 'Bounded exclusions with no general conclusion' in content(PAPER,'full')
    assert r'\label{lem:matrix-centralizer}' in (PAPER/'shared/matrix-centralizer.tex').read_text()
    assert r'\ref{lem:matrix-centralizer}' in (PAPER/'sections/candidates/20-90.tex').read_text()
    # Only these two proof files contain an edition-dependent paragraph selection.
    conditional={n for n in full|math if re.match(r'sections/(candidates|partials|prior)/',n) and r'\iffullpaper' in (PAPER/n).read_text()}
    assert conditional=={'sections/candidates/21-106.tex','sections/partials/other.tex'},conditional
    records=json.loads((PAPER/'data/problem-statements.json').read_text())
    d=records['entries'];assert len(d)==69
    for n,r in d.items():
        assert r['authors_tex'] and r['question_tex'] and r['visual_source_checked']
        assert hashlib.sha256(r['question_tex'].encode()).hexdigest()==r['statement_sha256']
        for crop in r['source_crops']:assert sha(PAPER/crop['render_path'])==crop['sha256']
    assert r'\overline{\Q}' in d['10.35']['question_tex']
    assert 'communicated by' in d['6.47']['authors_tex'] and 'Cooper' in d['6.47']['authors_tex']
    assert 'Bauer' in d['20.33']['authors_tex'] and 'Grochow' in d['20.33']['authors_tex']
    for e in ['full','mathematics']:
        used=re.findall(r'\\problemstatement\{([\d.]+)\}',content(PAPER,e))
        want=set(d)-{'19.83'}-({'10.35'} if e=='mathematics' else set())
        assert set(used)==want,(e,want-set(used),set(used)-want)
        assert len(used)==len(want)+1 and used.count('21.121')==2
    assert (PAPER/'appendices/v4-changes.tex').read_text()==render_changes()
    for n,s in render().items():assert (PAPER/n).read_text()==s,n
    for name in ['editors-reply1.md','editors-reply2.md','editors-reply3.md']:
        assert PAPER/'external-reviews'/name not in public_review_files(PAPER)
    assert 'Version 4 --- 19 September 2026' in (PAPER/'document.tex').read_text()
    result={'status':'PASS','scope':'Shared-source coverage, explicit editorial transformations, historical preservation, statement-image bindings and edition separation; not a new theorem, novelty or human-review certification.',
      'v3_baseline_files':len(bindings),'preserved_proof_and_attribution_files':len(preserved),
      'extracted_representative_proofs':3,'candidate_proofs_shared':45,'question_records':69,
      'full_tex_inputs':len(full),'mathematical_tex_inputs':len(math),'historical_counts':[46,1,45],
      'centralizer_dependency_preserved':True,'all_three_editor_emails_excluded':True}
    preservation={'scope':'Exact source comparison after only the editorial operations enumerated below; no new mathematical verification.',
      'allowed_operations':['Select the full edition for the chronology and bounded-search paragraphs.',
        'Remove added question blocks and labels.',
        'Restore edition-dependent comparison and reproduction references, including macro spacing.',
        'Restore the attribution heading.',
        'Restore the old 20.90 reference to the centralizer argument.',
        'Remove the problem number appended to each extracted representative heading.',
        'Normalize whitespace.'],
      'files':proof_bindings}
    (REV/'source-preservation.json').write_text(json.dumps(preservation,indent=2)+'\n')
    (REV/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
