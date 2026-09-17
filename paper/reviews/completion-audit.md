# Completion audit: reader-focused revision, 17 September 2026

Completed on `paper/review-revision`, following the first review revision
`f9e1956`. Both earlier PDFs remain under `versions/`; the current 127-page
PDF is `kourovka-experiment.pdf`. Previous handoff receipts are preserved
under `polish-2026-09-17/previous-handoff/`.

The opening page, abstract, early review section and contribution statement
now credit Anthropic's Claude Opus[1m] (`claude-opus-5[1m]`, xhigh reasoning,
via Claude Code). These settings were supplied by the organizer. The early
account explains the detailed independent checks and the exchange with Codex,
including confirmations, corrected objections and the 14.72 strengthening.

The introduction foregrounds the mathematical outcomes. In the final polish
following `6c8cbb4`, the full inventory moved to Section 2, beginning on page 4
immediately after the introduction. The independent review begins on page 7;
the representative proofs begin on page 9. Main-text Sections 5–8 contain the
proofs, partials and prior-work deductions. Kinyon's title-page footnote records
his AI4REASON research visit. Urban's title-page footnote credits ERC NextReason
(Grant Agreement No. 101200949) and hyperlinks the institute's sponsors at
https://ai4reason.eu/sponsors.html; the separate acknowledgement paragraph
before the references has been removed.
Detailed configuration, accounting,
chronology and study design are in appendices. The bibliography follows the
main discussion. The four verbatim correspondence documents remain at the
end, preceded by the historical change record and editorial provenance.

The subsequent opening polish removes the requested redundant abstract
sentence and explicitly states 46 entries or specified subparts, nine
partial-result questions, and rediscoveries/deductions. It brings the deadline
and requested local resource budget into the introduction and adds a brief
competition analogy. Counting conventions and checked sources are recorded
in `opening-polish-2026-09-17.md`; the inventory still begins on page 4.

Validation:

- The Tectonic 0.17.0 build passed without TeX/BibTeX warnings, undefined
  references or overfull boxes. The structure audit binds 72 TeX source
  files, 114 unique labels, 100 cited works, 46 candidate entries, 24
  original ancillary files and 19 printed carpet derivations.
- `audit_reader_revision.py` checks all 50 relocated mathematical source
  files against their f9e1956 hashes. The sole permitted textual change
  is Appendix -> Section in the 20.90 reference to 10.35. Every live TeX
  file is included exactly once. Frozen candidate and usage data match
  their recorded baseline hashes.
- The 18 historical before/after pairs are checked against preserved
  source copies of both versions. The original review documents and
  replies are unchanged; their rendering preserves the word streams.
- Both archives were extracted outside the repository. Member manifests,
  inventory regeneration, the historical change record and mathematical
  preservation audit passed. The cached standalone build produced
  identical extracted PDF text.
- All four ancillary commands passed from the extracted bundle: rank-two
  coverage, square completion, integer constants and the formerly missing
  G2 monomial certificate. The original proof-input hashes are unchanged.
  No new large-certificate replay or external model review was performed.
- The preceding second reader-focused pass checked emphasis, repetition,
  grouping and navigation, with 41 rendered pages inspected. Details and
  short execution logs for that pass remain under `polish-2026-09-17/`.
  The final polish inspected pages 1, 3, 4, 6, 7, 9, 79 and 110 for the
  title-page footnote, reading routes, inventory placement, renumbering,
  acknowledgement and editorial change record. The inventory source and
  all mathematical arguments are unchanged from `6c8cbb4`.
- The subsequent opening polish inspected pages 1–4, 82 and 110. Its nine
  partial-result groups match the selected table in the frozen final report;
  the five bounded-search questions match the manuscript. The new IMO
  reference was checked against the official regulations. Build and bundle
  receipts describe the current PDF and sources.
- The funding-footnote pass inspected pages 1 and 79. The full funding
  sentence occurs once, on page 1, attached to Urban's surname. `pdfinfo -url`
  confirms the page-1 annotation targets https://ai4reason.eu/sponsors.html.
  The separate acknowledgement paragraph is absent before the references.

The existing source checks and exact 14.72 algebra check from the first
review revision remain under `revision-2026-09-17/`. The public filtered
snapshot and the unavailable 1.27 GB 20.100 certificate are documented as
before; no large file was added or deposited. Final source archives include
these completed receipts. Their member manifests and bindings to the
successfully checked typesetting and ancillary inputs are checked again
after packaging. No submission, external upload or Git push is included.
