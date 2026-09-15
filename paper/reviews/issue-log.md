# Manuscript review and correction log

This log concerns the later paper-writing phase. It does not rewrite
the frozen experiment or represent same-agent review as outside review.
The mathematical and source review has completed two reading passes.
Build and packaging checks are recorded separately from proof review.

| ID | Finding | Action and evidence | Status |
|---|---|---|---|
| E001 | The HTML header advertises 34,102 events, but many event bodies are absent. | The structural parser and an independent tag count agree on 4,439 exported event elements. Report both counts with distinct meanings. | Resolved for measurements. |
| E002 | Summing cumulative or repeated Last counters would inflate usage. | Retain 3,616 token observations; use the final monotone cumulative counters. Record 96 identical successive cumulative snapshots. | Resolved for measurements. |
| E003 | The initial analyzer assumed every Last record was itemized as input plus output. Its first run failed that assertion (tool observation `2d10f2`, actual exit 1). | Examination found 80 positive Last totals with all component counters zero. Preserve these records explicitly, do not assign an undocumented meaning to them, and use the internally consistent cumulative counters. The corrected generation passed (`711107`, actual exit 0). | Resolved; interpretation remains explicitly limited. |
| E004 | The historical model and reasoning setting are absent from the provided export. | The user supplied `gpt-6-astra xhigh` on 14 September. Cite this as human-supplied metadata, distinct from export-derived facts. | Resolved by attributed metadata. |
| E005 | A configured GitHub remote does not prove public artifact availability. | Anonymous API requests for the repository and the two observed revisions returned HTTP 404. Record the address and local snapshot without claiming public access or equality with the remote HEAD. | Resolved by limiting the availability claim; publication metadata may be updated by the author. |
| E006 | The root README still names an older candidate count. | Use the final ledger and closeout report as the deadline outcome; retain the README as a historical document. No claim is based on its obsolete total. | Resolved by source precedence. |
| E007 | Commit count can include administrative work after the research deadline. | Derive the count from the frozen history: 198 commits in the 48-hour window, followed by the closeout commit 16 seconds after its end. | Resolved for measurements. |
| E008 | BibTeX lowercased an unprotected mathematical macro in the Budkin title, stopping compilation. | Protect the mathematical title text and use the standard mathbb macro. The subsequent complete build exited zero. | Resolved. |
| E009 | The new 15.65 count-polynomial display used split with an extra alignment column. | Replace those displays with aligned. The 85-page build exited zero with no overfull boxes. | Resolved. |
| E010 | A characteristic-subgroup relation was initially typed with TeX's primitive char command. | Replace it by an explicit mathematical relation before the successful build. | Resolved. |
| E011 | The historical grouping of 19.62/19.63 could imply a new square-closedness result. | Introduction, inventory generator, and exposition now credit Nuzhin's prior all-type theorem; the 46-entry historical ledger is preserved. | Resolved; attribution reread in the final pass. |
| E012 | The final prior-results addition uses a real-number macro absent from the preamble. | Added the macro; the 93-page full-content build exited zero, PDF SHA256 088d44ddd6a822c14932fae12a8f362f49d3aa66a1a1cf87a99f335bc4620cae. | Resolved. |
| E013 | The new 2015 Shakhova entry had incorrect initials. | The primary MathNet record identifies S. A. Shakhova; corrected the entry. The earlier dominions entry already had the correct initials. | Resolved. |
| E014 | The FNP memoir was entered as a book with both volume and number but no publisher, producing BibTeX warnings. | Use its journal-series entry, preserving volume 176, number 830, year and DOI. The subsequent full build exited zero; bibliography wrapping is ragged right. | Resolved. |
| E015 | First visual inspection of the chronology figure found crowding between the upper tick labels and lower title. | Increase panel spacing and omit redundant upper x tick labels; both panels share the lower time scale. The regenerated 1400-pixel preview has clear spacing. | Resolved by visual recheck. |
| E016 | The supplementary local-finiteness paragraph in 9.4 used F2 even when the original finite generating group might have odd order. | Use the same Fp selected by Cauchy's theorem in the main proof. The shift, one-generator construction, and addition term work for every prime. The principal finite-identity obstruction was unaffected. | Resolved mathematically; included in subsequent build. |
| E017 | The 19.62 exposition omitted explicit credit for the previously solved types and characteristics. | Added Nuzhin 2023, Section 3, including the simply laced consequence of its quoted triple inclusion and the stated good-characteristic cases. The finite argument makes no novelty claim for those cases. | Resolved by rereading the exact prior inclusions and criterion. |
| E018 | Initial membership conditions in the carpet derivation tables sometimes shared a line with the table. | Insert a paragraph break in the renderer so all 19 tables follow their initial conditions consistently. | Resolved; all 19 tables visually rechecked in the final PDF. |

The analyzer has two deliberately different checks on the supplied data:
HTMLParser extraction is compared with literal-tag counts and an independent
parse of the final cumulative usage section; message-class counts are also
compared with the text export. These checks establish properties of the
exports. They do not recover missing tool events, prove the renderer's
accounting against invoices, or validate any mathematical argument.

## Revision, 15 September 2026

E001--E018 above record the original manuscript phase. The full JSONL,
supplied subsequently, changes the available evidence without changing the
frozen mathematical results.

| ID | Finding | Action and evidence | Status |
|---|---|---|---|
| E019 | The new full session includes manuscript preparation after the research closeout. | Divide by research deadline and the recorded new manuscript goal; assign requests by their own timestamps. Preserve the old HTML as a closeout projection. | Resolved; exact aggregate reconciliation. |
| E020 | The supplied ccusage row omits compactions, while the raw request ledger includes them. | Match all 84 compaction response IDs; their usage exactly equals the difference of the two ledgers in every component. The supplied $901.42 matches full ordinary usage; flat reconstruction including compactions is $969.78, with $910.61 assigned to research. | Resolved; not represented as actual billing. |
| E021 | The HTML-only model and tool-history caveats are obsolete for the fuller evidence. | All 139 turn contexts corroborate gpt-6-astra/xhigh. Count unique completed operations, without summing outer wrappers or mirrored records. | Resolved; remote implementation/resource limits remain explicit. |
| E022 | Request and notification timestamps can fall on opposite sides of the deadline. | A 90,535-token request recorded at 20:56:42.957 is notified at 20:56:49.929. Use request times and document the boundary example. | Resolved. |
| E023 | Author placeholders and the human-only authorship statement conflict with the supplied author list. | Credit Codex gpt-6-astra (OpenAI), Michael Kinyon (Denver), Josef Urban (AI4REASON; Gothenburg), and state their respective execution and conception/oversight roles. | Resolved in title, PDF metadata, text and source packaging. |
| E024 | The related-work account overemphasized recent industrial systems, then became too long in revision. | Read the requested primary sources; retain two brief paragraphs on MPTPChallenge motivation, MaLARea and nearby approaches, including TacticToe, DreamCoder and Alien Coding. Remove the extended historical discussion and redundant citations following user steering. | Resolved; detailed reading retained in source-checks.md. |
| E025 | Three-panel figure preview showed adjacent long vertical labels touching. | Shorten axis labels to Commits, Families and Observations; retain exact count definitions in caption and narrative. | Corrected; final rendered figure reviewed with the PDF. |
