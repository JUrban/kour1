# Audit of three prior ProofForum answers

2026-09-12. The work adds no new complete candidate; the working
count remains44. There is no external human-review claim.

| Problem | Primary preprint | Internal outcome |
|---|---|---|
| 17.113 | PF:2026.000002 v1, August27 | Full affirmative construction is sound; independent finite controls pass. |
| 19.1 | PF:2026.000005 v1, August30 | Algebraic proof is sound and applies to all knot groups using the checked prior topological statements. |
| 19.9(a),(b) | PF:2026.000006 v1, September1 | Both prior answers are sound with uniformity of Deligne's obstruction and finite generation made explicit. |

Detailed mathematical reading scopes, supplied steps and limitations
are in `17.113-prior-result.md`, `19.1-proofforum-addendum.md` and
`19.9-proofforum-addendum.md`. The original local19.1 and19.9
proof files remain unchanged; the new addenda supersede their
earlier priority-search and knot-scope comments.

## Computation

The28 declared GAP cases returned actual exit0, empty stderr and
the terminal sentinel `PASS_17113_GAP cases=28`. The wrapper also
returned actual exit0 in tool chunk4682dd, session25039. They
include classes2 through7. Independent integer-coordinate controls
cover15 parameter pairs,507,074 projection products and15,000
associativity triples. Their actual return code is0 and output
is deterministic.

The earlier30-case GAP request was intentionally stopped during
p=11,n=5. It had completed28 passing rows but had no sentinel;
actual GAP and wrapper exit codes were1 (tool chunkf49772).
Its script, stdout, stderr and process record are preserved in
`results/17.113-stopped-run/`. It is not counted as a completed run.

`scripts/audit_proofforum_2_5_6.py` verifies the manifest hashes,
the source-download metadata, all saved process/log bindings,
the exact28-case coverage and every printed invariant. It also
checks the stopped prefix against the completed rows and reruns
the independent coordinate implementation with byte-identical
output. It does not repeat the already completed GAP calculation.

Reproduce the evidence audit:

    python3 scripts/audit_proofforum_2_5_6.py

To regenerate both finite-control logs deliberately:

    python3 scripts/run_17_113.py

Regeneration changes timestamp-bearing process records, requiring
an intentional manifest refresh. The frozen originals are retained
in the local Git commit. The audit observation outside the manifest
records its actual exit and output hashes, avoiding a self-reference.

## Sources and limits

All three primary PDFs and TeX files were downloaded successfully
with recorded SHA256 hashes. Every page of each preprint was read;
selected proof pages were visually checked. The relevant original
Notebook statement and symplectic rank bound were also viewed.
The exact topology statements were inspected in Agol,
Przytycki--Wise and the author-hosted Aschenbrenner--Friedl--Wilton
manuscript. Their deep proofs are imported and not machine-checked
by the arithmetic audit. Nor does the manifest validate mathematical
truth merely by validating file hashes.

For17.113, the full finite model, presentation, lower central series
and deficiency argument were checked directly. The other two
answers rely on the prior theorems identified in their addenda.
The public archive's AI-review labels are not used as proof evidence.
