#!/usr/bin/env python3
"""Check v2 coverage, provenance bindings and preservation, not theorem truth."""
import hashlib
import json
from pathlib import Path
import re
from public_review_files import public_review_files
from render_v2_changes import render
from revision_sources import preserved_mathematical_source, v2_source

PAPER = Path(__file__).resolve().parents[1]
REV = PAPER / 'reviews/v2-2026-09-19'
EXPECTED = {'4.55', '14.22', '15.89', '16.9', '16.28', '17.101',
            '18.76', '21.40', '21.68', '21.106', '21.121'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads((REV / 'baseline.json').read_text())
    assert sha(PAPER / baseline['pdf']['path']) == baseline['pdf']['sha256']
    records = {row['path']: row for row in baseline['sources']}
    preserved = []
    for name, row in records.items():
        if re.match(r'sections/(candidates|partials|prior)/', name):
            assert hashlib.sha256(preserved_mathematical_source(PAPER, name)).hexdigest() == row['sha256'], name
            preserved.append(name)
    assert len(preserved) == 50
    raw = (PAPER / 'sections/representative.tex').read_text()
    for stem in ['21-106', '21-68']:
        line = r'\input{sections/attribution/' + stem + '}\n'
        assert raw.count(line) == 1
        raw = raw.replace(line, '')
    assert hashlib.sha256(raw.encode()).hexdigest() == records['sections/representative.tex']['sha256']

    rows = json.loads((REV / 'comparison.json').read_text())['entries']
    assert len(rows) == 11 and {r['ledger_problem'] for r in rows} == EXPECTED
    source_data = json.loads((REV / 'sources.json').read_text())
    sources = {r['problem']: r for r in source_data['sources']}
    annotations = json.loads((PAPER / 'data/review-annotations.json').read_text())['entries']
    wrappers = ((PAPER / 'sections/candidate-proofs.tex').read_text()
                + (PAPER / 'sections/representative.tex').read_text())
    appendix = (PAPER / 'appendices/contemporary-comparison.tex').read_text()
    bib = (PAPER / 'references.bib').read_text()
    for r in rows:
        assert r['result_comparison'] and r['argument_comparison'] and r['review_scope']
        assert 'Unassigned' in r['priority']
        note = (PAPER / r['note_path']).read_text()
        assert wrappers.count(r'\input{' + r['note_path'].removesuffix('.tex') + '}') == 1
        assert r'\ref{app:contemporary-comparison}' in note
        assert annotations[r['ledger_problem']]['contemporary_sources'] == r['bibliography_keys']
        for key in r['bibliography_keys']:
            assert re.search(r'@\w+\{' + re.escape(key) + ',', bib), key
            assert key in note or (key == 'zhang-li-concise' and key in wrappers), key
        assert r['bibliography_keys'][0] in appendix
        s = sources[r['source_id']]
        meta = REV / 'metadata' / (s['problem'] + '-zenodo.json')
        assert sha(meta) == s['metadata_sha256']
        data = json.loads(meta.read_text())
        assert (data['created'], data['updated'], data['metadata']['publication_date']) == (
            s['record_created'], s['record_updated'], s['publication_date'])
        registry = json.loads((REV / 'metadata' / (s['problem'] + '-datacite.json')).read_text())
        assert registry['data']['attributes']['registered'] == s['datacite_registered']
        assert any(f['name'].endswith('.pdf') for f in s['files'])
        assert any(f['name'].endswith('lean-source.zip') for f in s['files'])
    assert len(sources) == 11
    assert any(r['id'] == 'rizzoli-21-68' for r in source_data['additional_sources'])
    chronology = json.loads((REV / 'chronology.json').read_text())['rows']
    assert {r['problem'] for r in chronology} == set(sources)
    for row in chronology:
        s = sources[row['problem']]
        assert row['datacite_registered'] == s['datacite_registered']
        assert row['zenodo_publication_date'] == s['publication_date']
    retrieval = json.loads((REV / 'retrieval-comparison.json').read_text())
    assert sha(PAPER / retrieval['input']) == retrieval['input_sha256']
    checks = json.loads((REV / 'checks.json').read_text())
    assert checks['status'] == 'PASS' and len(checks['commands']) == 2
    for row in checks['commands']:
        program = REV / Path(row['command'][-1]).name
        assert sha(program) == row['program_sha256']
        assert sha(REV / row['output']) == row['output_sha256']
        assert row['exit_code'] == 0
    assert (PAPER / 'appendices/v2-changes.tex').read_text() == render()
    assert r'\date{Version 2 --- 19 September 2026}' in v2_source(PAPER, 'main.tex').decode()
    assert PAPER / 'external-reviews/editors-reply1.md' not in public_review_files(PAPER)
    result = {'status': 'PASS', 'scope': 'V2 coverage, source and check bindings, version identity and preservation; not an automated theorem or priority verification.',
              'compared_entries': len(rows), 'doi_records': len(sources), 'unchanged_mathematical_sources': len(preserved),
              'representative_proofs_preserved': True, 'previous_pdf_preserved': True,
              'raw_editor_email_excluded_from_bundle': True}
    dest = REV / 'audit.json'
    if (PAPER / 'reviews/v3-2026-09-19/source-change.json').exists():
        result['unchanged_mathematical_sources'] = 49
        result['declared_v3_corrections'] = ['10.35 withdrawal; preserved v2 source checked separately']
        result['scope'] += ' V2 change excerpts and version date checked against the preserved v2 snapshot.'
        dest = PAPER / 'reviews/v3-2026-09-19/v2-preservation-audit.json'
    dest.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
