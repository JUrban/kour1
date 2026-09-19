#!/usr/bin/env python3
"""Render and check the v2 change record against the preserved pre-v2 sources."""
import argparse
import hashlib
import json
from pathlib import Path
from make_inventory import tex

PAPER = Path(__file__).resolve().parents[1]
REV = PAPER / 'reviews/v2-2026-09-19'


def render():
    rows = json.loads((REV / 'changes.json').read_text())
    out = [r'''\subsection{Version 2: contemporary solutions and attribution}
\label{sec:v2-changes}
The following changes were made on 19 September after the editor
identified further contemporary solutions. They compare the complete
pre-v2 paper at local commit \artifact{5fcdfdf} with version~2.
The preserved PDF is
\artifact{paper/versions/kourovka-experiment-2026-09-17-v1.pdf}.
Source hashes and literal excerpts are bound in
\artifact{paper/reviews/v2-2026-09-19/}. Each pair identifies the old
statement and its replacement or the additional qualification.
''']
    for row in rows:
        old = (REV / 'baseline-source' / row['before_path']).read_bytes()
        assert hashlib.sha256(old).hexdigest() == row['baseline_sha256']
        assert row['before'] in old.decode(), row['title']
        assert row['after'] in (PAPER / row['after_path']).read_text(), row['title']
        out.append('\\paragraph{' + tex(row['title']) + '}\n')
        for key, label in [('before', 'Before'), ('after', 'Version 2')]:
            out.append('\\noindent\\textbf{' + label + '.}\n\\begin{quote}\\small\n'
                       + row[key] + '\n\\end{quote}\n')
        out.append(tex(row['reason']) + '\n')
    out.append(r'''
\paragraph{Individual attribution and evidence.}
Eleven new notes accompany the affected proofs. They credit the papers
listed in Appendix~\ref{app:contemporary-comparison}, including both
Rizzoli and Jayadevan for 21.68 and the retained Zhang--Li work for
21.106. The inventory identifies every overlap. The new appendix gives
the comparison, chronology and checks; the Fable appendix now explicitly
retains the historical meaning of our answer count in that comparison.
The original proof expositions, deadline ledger and four exchanged
review documents remain preserved. The v2 comparison and algebraic
identities are later work, separate from the deadline results and
Claude's original review. The raw editor email is not reproduced.
''')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    text = render()
    path = PAPER / 'appendices/v2-changes.tex'
    if args.check:
        assert path.read_text() == text, 'stale v2 change record'
    else:
        path.write_text(text)
    print('PASS: five v2 before/after excerpts bound to preserved sources.')


if __name__ == '__main__':
    main()
