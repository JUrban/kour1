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
    comparisons = json.loads((PAPER / "reviews/v2-2026-09-19/comparison.json").read_text())["entries"]
    attribution = {r["ledger_problem"]: r["note_path"].removesuffix(".tex") for r in comparisons}
    assert set(annotations) == {r["problem"] for r in rows}
    inventory = [r"""\section{The mathematical portfolio: scope and index}
\label{app:inventory}
The table preserves the descriptions and claimed subparts of all 46
deadline candidates. \textbf{The claim for 10.35 is withdrawn in version~3},
leaving 45 other candidates; its row is retained as a historical record,
with the correction marked in the review column. The external assessment
is described in Section~\ref{sec:external-review}; the additional column
highlights scope qualifications and shared ingredients. The arguments
are grouped by subject in Section~\ref{app:candidates}. The historical entry for 19.62
also groups 19.63 with it; the latter's square-closedness criterion was
already published before the experiment, as explained in
Section~\ref{cand:19.62}. This grouping contributes one ledger entry.
An em dash in the review column means no additional note here, not that
the proof has no imported ingredients. The count records deadline coverage;
the independent review does not by itself establish discovery priority.
Version~2 adds individual attribution notes for eleven entries, compared
in Appendix~\ref{app:contemporary-comparison}. The other entries have not
thereby been established as new. For 16.9, qualitative computability is
a prior consequence; the displayed construction gives the explicit
reflection-length reduction and polynomial operation bound.


\small
\begin{longtable}{@{}p{0.065\textwidth}p{0.065\textwidth}>{\raggedright\arraybackslash}p{0.35\textwidth}>{\raggedright\arraybackslash}p{0.30\textwidth}p{0.065\textwidth}@{}}
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
    proofs = [r"""\section{Further mathematical arguments}
\label{app:candidates}
The following 42 expositions are organized by subject: 41 further candidate
arguments and the rational-field observation whose application to 10.35
is withdrawn. That entry is explicitly marked and retained for the record.
The four representative proofs in Section~\ref{sec:examples} are not
repeated. Each entry states the relevant scope and imported ingredients;
Section~\ref{app:inventory} provides the complete problem index.
"""]
    groups = json.loads((PAPER / "data/portfolio-groups.json").read_text())
    grouped = [p for group in groups for p in group["problems"]]
    further = {r["problem"] for r in rows if SPECIAL.get(r["problem"], (None, "proof"))[1] is not None}
    assert len(grouped) == len(set(grouped)) == 42
    assert set(grouped) == further
    missing = []
    for row in rows:
        problem = row["problem"]
        label, stem = SPECIAL.get(problem, ("cand:" + problem, problem.replace(".", "-")))
        exists = stem is None or (PAPER / "sections/candidates" / (stem + ".tex")).exists()
        scope = row["covered_subparts"].split(";")[0]
        loc = r"\ref{" + label + "}" if exists else r"\emph{Draft}"
        inventory.append(f'{tex(problem)} & {tex(scope)} & {tex(row["result"])} & {tex(annotations[problem]["review_note"]) or "---"} & {loc} \\\\\n')
        if not exists:
            missing.append(problem)
    inventory.append("\\end{longtable}\n\\normalsize\n")
    inventory.append(r"""
\paragraph{Answers retained under prior-work status.}
The following entries in Section~\ref{app:prior} answer the printed
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
    for group in groups:
        proofs.append("\n\\subsection{" + tex(group["title"]) + "}\n" +
                      "\\label{portfolio:" + group["label"] + "}\n" +
                      tex(group["introduction"]) + "\n")
        # Preserve each exposition's source heading while giving it the
        # appropriate depth inside the thematic subsection.
        proofs.append("\\begingroup\n\\let\\subsection\\subsubsection\n")
        for problem in group["problems"]:
            _, stem = SPECIAL.get(problem, (None, problem.replace(".", "-")))
            if (PAPER / "sections/candidates" / (stem + ".tex")).is_file():
                proofs.append(r"\input{sections/candidates/" + stem + "}\n")
                if problem in attribution:
                    proofs.append(r"\input{" + attribution[problem] + "}\n")
        proofs.append("\\endgroup\n")
    if missing:
        proofs.append("\n\\paragraph{Working-draft coverage.} Expositions still to be added: "
                      + ", ".join(missing) + ".\n")
    (PAPER / "sections/inventory.tex").write_text("".join(inventory))
    (PAPER / "sections/candidate-proofs.tex").write_text("".join(proofs))
    print(f"Inventory: {len(rows)} entries; {len(rows)-len(missing)} expositions present; "
          f"{len(missing)} remain.")
    if args.require_complete and missing:
        raise SystemExit("Incomplete candidate expositions: " + ", ".join(missing))

if __name__ == "__main__":
    main()
