#!/usr/bin/env python3
"""Render v3 changes against the hash-bound complete v2 source snapshot."""
import argparse
import hashlib
import json
from pathlib import Path
from make_inventory import tex
from revision_sources import v3_source

PAPER = Path(__file__).resolve().parents[1]
REV = PAPER / 'reviews/v3-2026-09-19'


def render():
    rows = json.loads((REV / 'changes.json').read_text())
    out = [r'''\subsection{Version 3: withdrawal of 10.35 and statement fidelity}
\label{sec:v3-changes}
These changes follow Khukhro's correction of 19 September 2026.
The before/after pairs bind the complete v2 source at local commit
\artifact{deeecb6} to this version. The earlier revision records above
remain tied to their own preserved versions. The v2 PDF is retained as
\artifact{paper/versions/kourovka-experiment-2026-09-19-v2.pdf}.
''']
    for row in rows:
        raw = (REV / 'baseline-source' / row['before_path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['baseline_sha256']
        assert row['before'] in raw.decode(), row['title']
        assert row['after'] in v3_source(PAPER, row['after_path']).decode(), row['title']
        out.append('\\paragraph{' + tex(row['title']) + '}\n')
        for key, label in [('before', 'Version 2'), ('after', 'Version 3')]:
            out.append('\\noindent\\textbf{' + label + '.}\n\\begin{quote}\\small\n'
                       + row[key] + '\n\\end{quote}\n')
        out.append(tex(row['reason']) + '\n')
    out.append(r'''
\paragraph{Further changes and evidence.}
The 10.35 heading and opening now mark the withdrawal before presenting
the rational-field observation. Its original lemma and construction are
unchanged. The inventory marks the historical row as withdrawn; the
discussion and both comparison appendices distinguish the current
45 candidates from the deadline count of 46. The frozen research ledger
and usage records are unchanged. Appendix~\ref{app:statement-correction}
explains the error and reports the visual audit of all 46 candidate
statements. The per-entry record and rendered source excerpts are in
\artifact{paper/reviews/v3-2026-09-19/}. The raw editor email is not reproduced.
''')
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = render()
    path = PAPER / 'appendices/v3-changes.tex'
    if args.check:
        assert path.read_text() == result, 'stale v3 change record'
    else:
        path.write_text(result)
    print('PASS: five v3 before/after pairs bound to the preserved v2 sources.')


if __name__ == '__main__':
    main()
