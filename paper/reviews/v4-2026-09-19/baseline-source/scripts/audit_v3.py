#!/usr/bin/env python3
"""Check the v3 correction, statement-audit evidence and preserved history."""
import hashlib
import json
from pathlib import Path
import re
from public_review_files import public_review_files
from render_v3_changes import render

PAPER = Path(__file__).resolve().parents[1]
REV = PAPER / 'reviews/v3-2026-09-19'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads((REV / 'baseline.json').read_text())
    assert sha(PAPER / baseline['pdf']['path']) == baseline['pdf']['sha256']
    bindings = {r['path']: r['sha256'] for r in baseline['sources']}
    for path, digest in bindings.items():
        assert sha(REV / 'baseline-source' / path) == digest, path
    correction = json.loads((REV / 'source-change.json').read_text())
    assert correction['path'] == 'sections/candidates/10-35.tex'
    assert correction['before_sha256'] == bindings[correction['path']]
    assert sha(PAPER / correction['path']) == correction['after_sha256']
    old = (REV / 'baseline-source' / correction['path']).read_text()
    new = (PAPER / correction['path']).read_text()
    # The lemma and its proof, including the field hypothesis, remain verbatim.
    pattern = r'\\begin\{lemma\}.*?\\end\{proof\}'
    assert re.search(pattern, old, re.S)[0] == re.search(pattern, new, re.S)[0]
    construction = old[old.index('Consider\n'):old.index(r'\begin{lemma}')]
    assert construction in new
    assert 'This disproves the required residual property.' not in new
    assert r'\GL_n(\overline{\Q})' in new and 'is withdrawn' in new
    unchanged = [name for name in bindings
                 if re.match(r'sections/(candidates|partials|prior)/', name)
                 and name != correction['path']]
    assert len(unchanged) == 49
    for name in unchanged + ['sections/representative.tex']:
        assert sha(PAPER / name) == bindings[name], name
    for name in bindings:
        if name.startswith('appendices/correspondence/'):
            assert sha(PAPER / name) == bindings[name], name

    frozen = json.loads((PAPER / 'data/frozen-candidate-ledger.json').read_text())['candidates']
    current = json.loads((PAPER / 'data/current-assessment.json').read_text())
    assert current['historical_candidates'] == len(frozen) == 46
    assert current['withdrawn_candidates'] == ['10.35']
    assert current['remaining_candidates'] == 45
    annotations = json.loads((PAPER / 'data/review-annotations.json').read_text())['entries']
    assert annotations['10.35']['current_status'] == 'withdrawn_wrong_problem'
    inventory = (PAPER / 'sections/inventory.tex').read_text()
    row = next(line for line in inventory.splitlines() if line.startswith('10.35 &'))
    assert 'WITHDRAWN' in row and 'Q(i)' in row
    assert '45 other candidates' in inventory

    audit = json.loads((REV / 'statement-audit.json').read_text())
    locations = json.loads((REV / 'statement-locations.json').read_text())
    assert audit['notebook'] == baseline['notebook']
    assert len(audit['entries']) == len(locations) == 46
    assert {r['problem'] for r in audit['entries']} == {r['problem'] for r in frozen}
    by_id = {r['problem']: r for r in locations}
    for r in audit['entries']:
        assert r['visual_statement_read'] and r['comparison']
        assert (PAPER / r['manuscript_path']).is_file()
        assert r['source_crops'] == by_id[r['problem']]['source_crops']
        assert r['covered_parts'] == by_id[r['problem']]['covered_parts']
        expected = 'withdrawn_wrong_problem' if r['problem'] == '10.35' else 'no_additional_statement_mismatch_identified'
        assert r['assessment'] == expected
        for c in r['source_crops']:
            assert c['pdf_page'] > 0 and len(c['bbox_points']) == 4
            assert sha(PAPER / c['render_path']) == c['sha256']
    originals = json.loads((REV / 'original-records.json').read_text())
    for row in originals:
        assert sha(REV / row['copy']) == row['sha256']
    assert (PAPER / 'appendices/v3-changes.tex').read_text() == render()
    assert r'\date{Version 3 --- 19 September 2026}' in (PAPER / 'main.tex').read_text()
    for name in ['editors-reply1.md', 'editors-reply2.md']:
        assert PAPER / 'external-reviews' / name not in public_review_files(PAPER)
    result = {
        'status': 'PASS',
        'scope': 'Correction coverage, counts, image/source bindings and preservation. The manual statement readings are recorded evidence, not machine-certified semantics or proof correctness.',
        'historical_candidates': 46, 'withdrawn_claims': ['10.35'],
        'remaining_candidates': 45, 'statement_records': 46,
        'unchanged_separate_mathematical_sources': 49,
        'corrected_source': correction['path'],
        'original_matrix_lemma_and_construction_preserved': True,
        'representative_proofs_and_verbatim_correspondence_preserved': True,
        'v2_pdf_and_source_baseline_preserved': True,
    }
    (REV / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
