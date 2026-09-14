# Manuscript completion audit — 14 September 2026

The requested writing and internal-review task is complete. The final
revised manuscript has no unresolved finding from this same-agent review.
This assessment is limited to the work described here; it does not imply
outside acceptance, formal verification, or exhaustive novelty search.

## Scope delivered

| Requested content | Location and evidence |
|---|---|
| Experiment, setting and technology | Sections 1--2 and Appendix A: original objective, selection policy, Codex/GAP setting, resources, persistence, retained-event limits, and token accounting. |
| How the run proceeded | Section 3: chronology figure from frozen CSVs, early corrections, literature-guided constructions, long 20.100 computation, late structural results, and deadline review. |
| Proofs and counterexamples | Section 4 contains three complete representative arguments; Appendix C supplies the other 43 deadline candidates. Appendix B preserves all 46 historical entries and subparts. |
| Partial results | Appendix D: 20.100, almost-Engel groups, p-Jordan bounds, Rota--Baxter construction, characteristic exponent subgroups, restricted character/derived-length results, and bounded exclusions. |
| Rediscoveries and alternative proofs | Appendix E: subdirect quotients, nilpotent Lie amalgamation, Fourier and tensor arguments, and further deductions from prior results, with priority and formulation limits. |
| Finite proof material | Appendix F prints 19 representative carpet derivations. Ancillary files supply all integer certificates and checkers for 19.61/19.62. |
| Outlook and recommendations | Section 5: selection bias, dependence among claims, absence of a baseline, possible training overlap, missing logs/resources, independent evaluation, selective formalization and review burden. |
| Reproduction and bibliography | Appendix G, 99 references, measurements, source/build scripts, portable archives, manifests and review records. |

## Mathematical and source review

Each of the 46 entries was read and rewritten, then read again against
its stated scope and load-bearing argument. The per-entry ledger gives
concrete final-pass notes; every entry retains zero outside reviews and
unestablished priority. The seven files containing the partial and
prior-result appendices were also read in full. Their original general
questions are not represented as solved by restricted results.

The last mathematical finding was the supplementary 9.4 example's use
of F2 when the generating finite group might have odd order. It now uses
the same Fp selected in the principal argument; the shift, generation and
addition construction were checked again for arbitrary p. The main
finite-identity obstruction did not change. The 19.108 partial's quotient
and induction reduction was expanded for clarity. These revised passages
were reread with no further finding.

The last attribution finding was missing explicit prior coverage for
19.62. The exposition now credits the earlier simply laced and specified
good-characteristic cases, as well as Nuzhin's prior all-type 19.63
criterion. Its integer derivations make no novelty claim for those
already covered cases. The added paragraph was checked against the exact
2023 theorem and triple-product inclusion.

Source-notes.md records the exact reading depth and imported statements.
In particular, the explicit Johnston--Rumynin conflict is restricted to
the read arXiv v2; the unavailable published text is not asserted to be
equivalent. Standard and deep imported results remain imports. A bounded
source search and same-agent proof reading cannot establish priority or
substitute for specialist refereeing.

## Recorded checks

All commands below actually completed with exit code zero.

| Check | Command / record | Result and scope |
|---|---|---|
| Measurements | python3 paper/scripts/analyze_experiment.py --check; final run completed at 16:58 UTC | Five generated files agree with the frozen repository and supplied exports; 4,439 exported events, 3,616 snapshots, 199 commits, 198 in the window. |
| Character input | /project/bin/gap --quitonbreak paper/scripts/check_character_input.g; observation 5b0eed | Exact 3.A7 modular rows, Frobenius pairs, ordinary Galois orbits and projective dimensions agree. This is not a fresh full MeatAxe reconstruction. |
| Final TeX build | python3 paper/scripts/build_paper.py --require-complete; 16:58:30 UTC | Tectonic 0.17.0; 94 pages; 610,531 bytes. Source hashes and PDF hash are bound in build-receipt.json. |
| Structural audit | python3 paper/scripts/audit_manuscript.py | 46 expositions, 63 TeX files, 78 unique labels, 99 cited bibliography entries, 23 intact original ancillary files and 19 printed derivations. No undefined references, duplicate labels or bibliography warnings; no overfull boxes. This checks structure and records, not proof validity. |
| Portable source | python3 paper/scripts/validate_source_bundle.py; 17:01:02 UTC | Both source archives extracted under /tmp outside /project. Manifests passed; inventory regenerated unchanged; cached standalone TeX compilation passed; extracted PDF text is identical. |
| Rank-two carpet proofs | python3 scripts/verify_19_62_rank_two.py, run from extracted anc/ | All 104 targets, representative/Weyl coverage, short derivations and 12 deliberate corruptions passed. |
| Square completion | python3 scripts/verify_19_61_square_completion.py, run from extracted anc/ | All 300 targets and 12 deliberate corruptions passed. |
| G2 structure constants | python3 scripts/check_19_62_g2_integer_constants.py, run from extracted anc/ | All 120 integer polynomial matrix identities passed. |

The portable-validation receipt binds the mathematical TeX inputs and
original ancillary manifest. Final packaging adds these review records
without changing the tested manuscript or certificate inputs. The final
archive manifests and dist/validation.json separately record integrity
of the actual handoff files.

The final PDF SHA-256 is:

ad804339ad686a1c85aa1fafb1d7519edf1fd010b8aaa91eac9e461efaee1146

## Visual review

All 94 pages of the final PDF were rendered and inspected in 16 contact
sheets, including the title and contents, chronology plot, inventory,
displayed proofs, all 19 carpet tables, reproduction table and bibliography.
The earlier figure-label crowding and inconsistent table placement are
fixed. No clipped, overlapping or missing content was found. The figure
occupies its own float page. The author line deliberately remains a
visible placeholder for missing human publication metadata.

## Remaining publication inputs and evidence limits

Human author names and affiliations must be supplied before submission.
Anonymous availability of the exact frozen Git snapshot is unverified;
the paper gives the configured address and exact local revision without
claiming public equivalence. These publication inputs do not conceal an
unfinished mathematical exposition or an unresolved finding in this
internal review.

Raw session exports, absent internal event bodies, audited invoices,
remote hardware and actual peak memory are not supplied by the source
bundle. Their absence and the difference between configured limits and
measured usage are explicit. The long historical n=7 verification and
other large searches were not all rerun during writing. Certificate
integrity, successful execution, theorem validity, priority and outside
acceptance remain separate claims throughout the manuscript.

Only paper/ was changed for manuscript preparation. The frozen research
revision is cff2c37b9bf6b737e8ad5f7ead12291a551b5201. No external upload,
submission, message or repository push was performed.
