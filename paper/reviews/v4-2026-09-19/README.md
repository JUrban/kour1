# Version 4: two editions with shared mathematical sources

[Mathematical edition](../../kourovka-mathematics.pdf) ·
[Full account](../../kourovka-experiment.pdf) ·
[Preserved v3](../../versions/kourovka-experiment-2026-09-19-v3.pdf)

The editor requested a presentation centred on results and proofs, with
problem authors credited. Version 4 provides that presentation alongside
the full experimental account. Both entry points use the same proof files,
question metadata, bibliography, attribution notes and author footnotes.
The mathematical edition orders the 45 remaining candidate entries by
Notebook number and includes the substantive partial and prior-work
arguments. The full account retains all historical and experimental material.

The 10.35 application stays withdrawn. The general centralizer fact needed
by 20.90 is a shared lemma; no proof depends on including the withdrawn
exposition. Both editions disclose the correction and preserve the limits
of the review evidence. Counts and novelty status are unchanged.

[data/problem-statements.json](../../data/problem-statements.json) stores
69 concise question restatements and original-author credits. Codex checked
the rendered Notebook excerpts, including the field bars, subparts,
quantifiers and authors. These records include partial results, prior-work
entries, the withdrawn question and the repeated 19.83/20.89 question; they
are not a claim of 69 answers. The original sources are 46 rendered crops
from v3 and 23 additional crops in [statement-crops/](statement-crops/),
with page coordinates and image hashes in
[statement-locations.json](statement-locations.json). The supplied Notebook
is pinned by SHA-256 in the metadata. The source images support checking
the restatements; hash checks do not certify their mathematical meaning.

The extra images were rendered with Poppler at 216 dpi. For a recorded
rectangle (x0,y0,x1,y1), use x/y equal to floor(3*x0), floor(3*y0), and W/H
equal to ceil(3*(x1-x0)), ceil(3*(y1-y0)). The image page is selected by
`pdftoppm -f` and `-l`, with `-singlefile -png`. Text extraction located
the rectangles; the notation and names were read from the images.

[baseline.json](baseline.json) binds the v3 commit, PDF and 124 source
files. [changes.json](changes.json) records three literal before/after
pairs. [source-preservation.json](source-preservation.json) records the
before/after source hashes and the permitted editorial operations. The
preservation audit compares 61 original proof/attribution files
and three extracted representative arguments with their v3 text, after
undoing only the specified editorial operations. It also checks that both
editions include the same 45 candidate proof inputs and the same partial
and prior-work files. Only the Heisenberg chronology paragraph and the
bounded-search subsection have edition-dependent selection within proof
files. No mathematical argument is hidden by those switches.

```sh
python3 paper/scripts/build_paper.py --require-complete
python3 paper/scripts/audit_manuscript.py
python3 paper/scripts/audit_v4.py
python3 paper/scripts/package_paper.py
python3 paper/scripts/validate_source_bundle.py
```

The build defaults to both editions; `--edition full` and
`--edition mathematics` select one. Historical audits use the preserved
sources of their own versions. Their current compatibility receipts are
stored here rather than overwriting earlier dated records. The v4 checks
cover the actual current sources, including shared-source coverage and
rendered question counts. The portable validation rebuilds both editions
outside Git and compares their PDF texts with the working builds.

`reports/FINAL_REPORT.md` remains the frozen deadline report. Its useful
inventory structure is reflected in the current mathematical index without
copying its superseded 10.35 claim or review status. All three editor emails
remain local and outside the source archives. The paper does not turn the
editor's cursory observations into specialist approval or a priority finding.
