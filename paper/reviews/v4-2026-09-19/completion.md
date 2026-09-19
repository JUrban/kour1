# Version 4 completion record

Prepared on `paper/v4` from `5ee9816c07a3f90abc958a49ddfe80a030b05541`,
19 September 2026. The editor requested a mathematical presentation with
results, proofs and the original problem authors. This revision implements
that presentation alongside the full experimental account.

## Deliverables

- `paper/kourovka-mathematics.pdf`: 92 pages; current index on pages 2–4,
  45 candidate arguments in Notebook order, substantive partial results,
  prior-work deductions, contemporary attribution and mathematical supplements.
- `paper/kourovka-experiment.pdf`: 150 pages; full account with the same
  question and proof sources, all four verbatim review documents, and the
  experimental and revision history. Appendix G records three literal v4
  changes; Appendix P explains the two editions.
- Small `main.tex` and `mathematics.tex` wrappers select the presentation
  through `document.tex`. The bibliography, author footnotes, mathematical
  statements, proofs and attribution notes are shared.
- Both PDFs, two standalone TeX archives and one shared source ZIP are
  generated under `paper/dist/`. The landing pages link both PDFs.
- The complete v3 PDF and 124 source files are preserved and hash-bound.
  Historical research reports, ledgers and review correspondence retain
  their original content.

The mathematical edition omits the withdrawn 10.35 application and discloses
the correction. Its dependent matrix-centralizer fact is stated separately
and proved over an arbitrary field; 20.90 cites that shared lemma. Counts
remain 46 historical candidates, one withdrawal and 45 remaining candidates.

## Source and statement checks

`audit_v4.py` passed. It compares 61 existing proof/attribution files and
three extracted representative arguments against v3, undoing only the
listed editorial operations. `source-preservation.json` records their
before/after hashes and those operations. It also checks that both editions
include the same 45 current candidate proof inputs and the same substantive
partial and prior-work arguments. The two switches within proof files
select a chronology paragraph and bounded unsuccessful searches; they
remove no mathematical premise from the mathematical edition.

All 69 question-and-author records were checked against rendered Notebook
excerpts: 46 crops preserved from v3 and 23 additional crops. The metadata
include the withdrawn question, partial and prior-work questions, the
repeated 19.83/20.89 question and the already solved 19.63 criterion. They
do not represent 69 solutions. Restatements are concise, not verbatim
transcriptions. Source coordinates and image hashes are recorded.

Both editions pass source/PDF binding, reference, bibliography and actual
rendered-question coverage checks. The full build renders 69 question
blocks and the mathematical build 68, including the repeated 21.121 block
for its separate (a) and (b) treatments. Both TeX logs have no undefined
references, duplicate labels or overfull boxes.

## Build, portable and layout checks

`build_paper.py --require-complete` and `audit_manuscript.py` passed for both
editions. The final PDF hashes are:

| Edition | SHA-256 |
| --- | --- |
| Full | `7850aefc307c46aa24174e1e1b86e7308a734e381b4f2f4816fc628d92fe64d9` |
| Mathematical | `eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7` |

`validate_source_bundle.py` passed at 12:48:57 UTC. It extracted all three
archives outside Git, checked their manifests, and ran 14 commands: source
generation and preservation checks, historical revision checks, v2 exact
identities, both standalone TeX builds, and all four ancillary carpet
checkers. Both standalone PDF texts equal their working-build texts.
The 24 original ancillary files and 19 printed derivations are preserved.

Codex inspected rendered pages of both editions, including their title
pages and acknowledgments, the mathematical index, proof/question blocks,
the 10.35 correction, the extracted centralizer reference, attribution,
partial-result boundaries, prior-work authors and the new appendices.
The layout pass corrected spacing after shared reference macros and made
the 21.121 scope references work in both appearances of the question.
Final-build pages checked after those fixes include full pages 30, 45,
75 and 125, and mathematical pages 27, 31, 37, 45, 49, 60, 67, 72 and 77.
Earlier layout samples also covered full pages 1, 3, 5, 11, 27, 124,
149 and 150, and mathematical pages 1–4, 20, 27, 48, 54, 62, 71, 91 and 92.

The completion record and updated validation receipt are added to the
final shared ZIP after validation. No TeX, proof, checker or ancillary input
changes in that final packaging step; its manifests are checked again.

## Limits and repository scope

These checks establish source preservation, shared coverage and portable
typesetting; they are not a new verification of every mathematical proof,
a novelty finding or specialist approval. The alternative Lean projects
and large historical computations were not rerun. The omitted 20.100
certificate remains absent from the public bundles, with that limitation
stated in both editions.

All three raw editor emails remain local and excluded from every source
archive. No unrelated research output, raw session or large certificate
is added. Master and `paper/v3` remain at the base commit. The revision is
committed locally on `paper/v4`; no push, email or external submission is made.
