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

The introduction foregrounds the mathematical outcomes. The independent
review account begins on page 3 and the representative proofs on page 6.
The inventory, further proofs grouped by subject, partials and prior-work
deductions are in main-text Sections 5–8. Detailed configuration, accounting,
chronology and study design are in appendices. The bibliography follows the
main discussion. The four verbatim correspondence documents remain at the
end, preceded by the historical change record and editorial provenance.

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
- A second reader-focused pass checked emphasis, repetition, grouping and
  navigation. Visual inspection covered 41 rendered pages across the
  document. Details and actual short execution logs are retained under
  `polish-2026-09-17/`.

The existing source checks and exact 14.72 algebra check from the first
review revision remain under `revision-2026-09-17/`. The public filtered
snapshot and the unavailable 1.27 GB 20.100 certificate are documented as
before; no large file was added or deposited. Final source archives include
these completed receipts. Their member manifests and bindings to the
successfully checked typesetting and ancillary inputs are checked again
after packaging. No submission, external upload or Git push is included.
