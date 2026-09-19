# Manuscript status

Version 4, dated **19 September 2026**, is prepared on `paper/v4`, based
on `5ee9816`. It provides a [mathematical edition](kourovka-mathematics.pdf)
and a [full research-and-review account](kourovka-experiment.pdf).
The v3 PDF is preserved in `versions/kourovka-experiment-2026-09-19-v3.pdf`;
its source baseline is under `reviews/v4-2026-09-19/baseline-source/`.

Both editions use the same statements, proofs, bibliography, attribution
notes and author footnotes. `main.tex` and `mathematics.tex` are small
wrappers around `document.tex`; the edition switch selects introductions,
indexes and experimental material. The mathematical edition presents the
45 remaining candidate arguments in problem-number order, then partial
results and prior-work deductions. It retains the carpet derivations and
a short explanation of computational proof inputs.

**10.35 remains withdrawn.** The example embeds over Q(i), an allowed
target for the original problem over the algebraic numbers. The full
account retains the rational-field observation and withdrawal history;
the mathematical edition discloses the withdrawal and omits the failed
application. The general matrix-centralizer fact used by 20.90 is now a
shared lemma with a proof valid over every field.

The current count remains **46 historical candidates, one withdrawal,
45 remaining candidates**. No new correctness, novelty, formal-verification
or human-endorsement claim accompanies the editorial revision.
The 69 shared question records include the withdrawn question, partial
and prior-work entries, the repeated almost Engel question and the known
19.63 criterion. They are not 69 claimed solutions. Their concise
restatements and author credits were checked against rendered Notebook
pages; 46 earlier crops are reused and 23 additional crops are recorded.

Source checks compare the current text of 61 proof and attribution files
and three extracted representative arguments with v3, allowing only
explicit metadata, heading, reference and edition-selection changes.
The mathematical text is preserved; the new standalone centralizer lemma
states and explains the fact already used in v3. Old review reports,
source baselines, literal change pairs and `reports/FINAL_REPORT.md` retain
their historical content. Appendix G adds three literal v3/v4 changes;
Appendix P explains the two editions.

The full account retains the preliminary Fable comparison (Appendix M),
the eleven-entry contemporary comparison (Appendix N), the 10.35 correction
(Appendix O), and all four verbatim review documents. Contemporary
attribution also accompanies the proofs in the mathematical edition.
The alternative Lean projects and omitted large historical computations
have not been rerun.

Build and structure receipts cover each edition separately. Portable
validation checks two standalone TeX archives and the shared source ZIP,
including both PDF text comparisons and all four ancillary proof programs.
The detailed completion evidence is recorded in
`reviews/v4-2026-09-19/completion.md`.

All three raw editor emails remain local and excluded from source bundles.
No large certificate, raw session or unrelated output is added. Master and
v3 remain unchanged; no remote push, email or external submission is made.
