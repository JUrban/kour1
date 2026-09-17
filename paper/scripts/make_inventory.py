#!/usr/bin/env python3
"""Generate the deadline inventory and available-proof input list.

This does not change mathematical review status. Missing expositions remain
explicitly visible in working drafts, and are an error with --require-complete.
"""
import argparse
import json
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
SPECIAL = {
    "19.56": ("cand:19.56", None),
    "21.106": ("subsec:concise", None),
    "21.68": ("subsec:semiabelian", None),
    "20.108": ("subsec:holomorph", None),
    "21.121": ("cand:21.121", "21-121a"),
}

def tex(s):
    return "".join({
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }.get(c, c) for c in s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-complete", action="store_true")
    args = ap.parse_args()
    frozen = PAPER / "data/frozen-candidate-ledger.json"
    rows = json.loads(frozen.read_text())["candidates"]
    annotations = json.loads((PAPER / "data/review-annotations.json").read_text())["entries"]
    assert set(annotations) == {r["problem"] for r in rows}
    inventory = [r"""\section{The deadline candidate inventory}
\label{app:inventory}
This table preserves all 46 entries on the deadline ledger, including its
covered subparts. It is not a list of independently accepted new results.
Several entries share imported ingredients. The mathematical discussions
give the relevant scope and dependencies; the frozen ledger supplies the
original statement and evidence paths. The historical entry for 19.62
also groups 19.63 with it; the latter's square-closedness criterion was
already published before the experiment, as explained in
Section~\ref{cand:19.62}. This grouping contributes one ledger entry.
The additional review column records selected scope qualifications and
imported dependencies; an em dash means no additional note here, not
that the proof has no imports. Priority remains unestablished for all
46 candidates. These annotations supplement the historical descriptions.


\small
\begin{longtable}{@{}p{0.065\textwidth}p{0.065\textwidth}>{\raggedright\arraybackslash}p{0.36\textwidth}>{\raggedright\arraybackslash}p{0.30\textwidth}p{0.055\textwidth}@{}}
\toprule
No. & Parts & Deadline description & Scope / dependency note & Sec.\\
\midrule
\endfirsthead
\toprule
No. & Parts & Deadline description & Scope / dependency note & Sec.\\
\midrule
\endhead
\bottomrule
\endfoot
"""]
    proofs = [r"""\section{Further candidate arguments}
\label{app:candidates}
The following expositions develop the remaining deadline candidates.
The four examples proved in Section~\ref{sec:examples} are not repeated.
Statements below retain their mathematical force, while the experimental
classification and unresolved priority status remain those explained in
Sections~\ref{sec:methods} and~\ref{sec:discussion}.
"""]
    missing = []
    for row in rows:
        problem = row["problem"]
        label, stem = SPECIAL.get(problem, ("cand:" + problem, problem.replace(".", "-")))
        exists = stem is None or (PAPER / "appendices/candidates" / (stem + ".tex")).exists()
        scope = row["covered_subparts"].split(";")[0]
        loc = r"\ref{" + label + "}" if exists else r"\emph{Draft}"
        inventory.append(f'{tex(problem)} & {tex(scope)} & {tex(row["result"])} & {tex(annotations[problem]["review_note"]) or "---"} & {loc} \\\\\n')
        if stem is not None and exists:
            proofs.append(r"\input{appendices/candidates/" + stem + "}\n")
        if not exists:
            missing.append(problem)
    inventory.append("\\end{longtable}\n\\normalsize\n")
    inventory.append(r"""
\paragraph{Answers retained under prior-work status.}
The following entries in Appendix~\ref{app:prior} answer the printed
questions but remain outside the historical candidate count. They are
shown here to make that classification visible, not to increase 46.
\begin{center}\small
\begin{tabular}{@{}lp{0.74\textwidth}@{}}\toprule
Problem & Prior-work status\\\midrule
21.132 & Deduction from graded radical and Golod constructions.\\
21.42 & Deduction of self-similarity from the positive-grading theorem and Mathieu's lattice criterion.\\
20.33 & Effective universal-group construction from standard embeddings, with oracle bookkeeping; Mikaelian improves the generator bound.\\
\bottomrule\end{tabular}\end{center}
""")
    if missing:
        proofs.append("\n\\paragraph{Working-draft coverage.} Expositions still to be added: "
                      + ", ".join(missing) + ".\n")
    (PAPER / "appendices/inventory.tex").write_text("".join(inventory))
    (PAPER / "appendices/candidate-proofs.tex").write_text("".join(proofs))
    print(f"Inventory: {len(rows)} entries; {len(rows)-len(missing)} expositions present; "
          f"{len(missing)} remain.")
    if args.require_complete and missing:
        raise SystemExit("Incomplete candidate expositions: " + ", ".join(missing))

if __name__ == "__main__":
    main()
