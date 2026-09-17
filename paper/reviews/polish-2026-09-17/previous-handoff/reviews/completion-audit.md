# Completion audit: external-review revision, 17 September 2026

Completed on `paper/review-revision`, branched from local manuscript commit
`8a59409`. The reviewed PDF remains at
`versions/kourovka-experiment-2026-09-15.pdf`; the current PDF is
`kourovka-experiment.pdf`. Previous handoff receipts are preserved under
`revision-2026-09-17/previous-handoff/`.

The revised paper has 125 pages, 100 cited works, all 46 historical candidate
expositions (four main examples and 42 further expositions), a change
appendix and four verbatim correspondence appendices. The 18 exact
before/after pairs are checked against baseline sources whose hashes bind
them to the reviewed version. Withdrawn objections and retained scope are
listed separately. The raw original report, first reply, follow-up and
partial update remain byte-identical to the supplied versions. Pandoc
conversion preserves their word streams; inline-code spaces are retained.

The mathematical strengthening is the globally principal reduced fixed
divisor in 14.72 after localization at x^2+1. Its explicit proof is in the
paper. `check_14_72_principal.py` passed exact Groebner and polynomial
checks over Q(i), including the fixed ideal, invariance of the localization
and survival of the quotient node. This supplements the geometric proof.
The 16.28 and 19.56 proof source files are unchanged, as are the frozen
candidate ledger and all prior usage/accounting outputs.

Validation completed:

- Tectonic 0.17.0 build: exit zero, no undefined references, duplicate labels,
  overfull boxes or TeX/BibTeX warnings. The structure audit binds the PDF
  and 69 TeX source files, with 104 unique labels and 24 original ancillary
  files. `build-receipt.json` identifies every typesetting input, including
  the correspondence sources and manifest.
- Both archives extracted outside the checkout; all member manifests
  matched. Inventory regeneration was byte-identical. The cached standalone
  TeX build produced identical extracted PDF text. The full bundle's
  before/after validation also passed outside Git.
- All four ancillary commands passed from the extracted arXiv source:
  rank-two coverage (104 targets), square completion (300 targets), the
  G2 integer constants (120 matrix identities, 156 rule entries), and the
  formerly missing G2 monomial input (2,712 requests, 62,835 nodes).
  Negative/corruption controls included in the checkers passed. All
  original input hashes remained unchanged after execution.
- GAP 4.16.1 / CTblLib 1.3.11 character-table input check passed.
- The retrieval parser regenerated identical outputs from the identified
  540,278,152-byte JSONL: 1,324 structured web observations. It exports
  no reasoning, compaction, system/developer or shell-command bodies.
- Visual inspection covered 42 rendered pages: title and contents; main
  example/discussion pages; the inventory; 14.72; reproduction; the entire
  change appendix and correspondence; and the end of the bibliography.
  Long code fragments, hashes, table columns and the new equations fit.
- Python syntax checks and `git diff --check` passed.

The public filtered research snapshot and original unfiltered one share
all 4,146 retained blob IDs. Selected public files and the baseline PDF
were byte-compared. The sole omitted research blob at that snapshot is
the 1,271,256,410-byte 20.100 certificate. Neither this revision nor the
public logs supply a full independent replay of it. No large-file deposit
was made, and the entire reviewer script collection was not rerun.

Machine-readable receipts are adjacent to this audit; revision-specific
source checks, actual short execution outputs, artifact provenance and
baseline bindings are under `revision-2026-09-17/`. Portable validation
binds the mathematical/typesetting inputs rather than recursively hashing
its own later documentation. Final archive manifests include the completed
receipts and are checked again after packaging. No submission, upload or
Git push is part of this handoff.
