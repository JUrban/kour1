# Version 2 completion audit — 19 September 2026

The authorized eleven-entry comparison and explicit v2 revision are complete
on `paper/v2`, based on local commit `5fcdfdf`. The current PDF is
`paper/kourovka-experiment.pdf`: 138 pages, 812,877 bytes,
SHA-256 `ea8cdaf50bc1a6bcfc35e08e329f06aea2c79d2c57bddccc01cc70c139627d01`.

## Comparison and attribution

- Read all eleven Jayadevan papers, the separate Rizzoli 21.68 note, and
  the Dahmani–Guirardel and Brandenbursky–Gal–Kędra–Marcinkowski sources
  relevant to 16.9. Source versions and checksums are pinned in `sources.json`.
- `comparison.json` records the result, method, reading scope and assessment
  of every entry. Appendix N presents the comparison on pages 136–138.
- The abstract, introduction, review account and inventory identify the
  comparison. All eleven affected proofs have individual attribution notes.
  Both Rizzoli and Jayadevan are credited for 21.68; Zhang–Li credit remains.
- The 46-entry count retains its historical deadline meaning. The revision
  assigns no discovery priority and does not infer novelty of the other 35.
  It explicitly credits older computability and recurrence results for 16.9.
- Local proof-file commits, Zenodo date fields and DOI registration are
  distinguished. The printed chronology agrees with `chronology.json`.
  The retrieval-index search is reported with its limited scope.
- Specialist confirmation is attributed to Khukhro's report about alternative
  solutions of 21.68, 16.28(a) and 15.89. No broader human endorsement is claimed.

## Executed and visual checks

`checks.json` binds two successful executions: the GAP reconstruction of
PSL2(11), subgroups and projective characters for 4.55; and exact polynomial
identities for 15.89, 18.76 and 21.106. The 18.76 comparison supplies an
explicit characteristic-zero isomorphism that negates the additive kernel.

The manuscript audit passes with 46 candidate entries, 87 live TeX files,
118 labels, 115 cited works and 123 bibliography entries. The successful
build is bound by `../build-receipt.json` and `../structure-audit.json`.
There are no unresolved references, multiply defined labels or overfull boxes.

Both source archives were extracted outside the repository. Their manifests
passed, all ten portable commands exited zero, and the standalone cached
TeX build produced identical PDF text. Inventory regeneration, both change
records, source preservation, the v2 comparison and exact identities, and
all four ancillary carpet checks passed. See `../portable-validation.json`.
The final repack includes that receipt and this audit; its manifests and
tested input hashes are checked again without repeating unchanged executions.

Rendered pages 1, 2, 7, 11, 113, 114 and 136–138 were visually inspected.
The version date, reviewer credit, funding links, contents, proof attribution,
change excerpts, comparison table, formulas and chronology are legible and
fit within the page margins. The renderings remain in the ignored build cache.

## Preservation and limits

All 50 separate mathematical source files match the pre-v2 hashes. The
representative-proof source differs only by two attribution-note inputs.
The frozen deadline ledger, usage data, four verbatim review appendices and
eighteen earlier before/after pairs are preserved. Five additional literal
v2 pairs are bound to preserved source excerpts. The complete pre-v2 PDF
is retained in `versions/kourovka-experiment-2026-09-17-v1.pdf`.

The alternative Lean archives were downloaded and checksum-verified but
not built. Mathematical reading and targeted calculations do not constitute
kernel verification, a full replay of historical computations, or a priority
determination. The Fable appendix retains its dated 17 September scope.

The raw editor email is unchanged and excluded from both bundles. Large
certificates, raw session files and unrelated research outputs are not added.
The repository and paper landing pages identify v2 and link its review record.
No Git push, external upload, email or submission was performed.
