# Current status

Updated: 2026-09-10T21:42:35Z.

- Active phase: proof audit, exact searches, and broader problem triage.
- Complete candidate solutions: **2**, Problems **21.106** (negative) and **21.132** (construction for every prime). Both await outside review and further novelty checks.
- Externally reviewed new solutions: 0.
- Running computations: 21.113(b) projective-character search and the length-36 positive trace-word search for 18.43. Revalidate handles in `state/jobs.json` before relying on liveness.
- GAP 4.16.1 and SmallGrp, TransGrp, CTblLib, Digraphs 1.15.0, and GRAPE work. `bin/gap` is the reproducible launcher.

## Candidate proofs

**21.106:** A parameter-free formula defines exactly the two central generators in the integral Heisenberg group, a residually finite group. Its value set is finite but generates an infinite subgroup. The self-contained proof and internal audit are in `research/21.106-proof.md` and `research/21.106-review.md`. Exact arithmetic and finite-quotient sanity checks passed; the infinite claim rests on the proof.

**21.132:** Starting from a graded Golod nil algebra, remove the homogeneous ideal of elements annihilated by a sufficiently high algebra power. A triangular extension has zero centre and preserves a grading with finite-dimensional pieces. Its three-generated adjoint subgroup is infinite, centreless, and residually a finite p-group. Adjoining a one-dimensional zero algebra gives a four-generated Golod group with centre C_p. Proof: `research/21.132-proof.md`; audit: `research/21.132-review.md`. The exact Notebook statement permits the final direct factor. The older centreless construction has been compared; broader novelty work remains.

## Completed bounded searches

- **21.99:** All 4,722 transitive groups of degrees 2–20 satisfy the conjecture: 4,631 orbital checks and 91 rank-two cases. Independent full-element verification agrees for all 86 groups of degrees 2–8.
- **21.113(a):** 2,750 ordinary character tables, 9,850 table/prime cases, no skips or counterexample. Part (b) continues, checking all available Brauer tables and reconstruction through decomposition matrices.
- **21.59(a)/21.135:** 106 degree-multiset collisions among 2,750 tables, all between entries marked almost simple. Primed orthogonal/unitary entries were checked and are alternative table/fusion data. No nonisomorphic counterexample established. See `research/degree-collision-audit.md`.
- **21.52–53:** 27 group entries, 28 involution classes, one explicit size-cutoff skip, no counterexample. The strengthened run verifies actual group automorphisms on every involution, correcting an insufficient normalizer-only test. See `research/21.52-53-results.md`.
- **18.43:** Positive words of lengths 1–35 have no collisions under two exact GL3 evaluations. Length 36 has enumerated 1,908,881,900 necklaces and is sorting. Independent Python checks cover enumeration and arithmetic through length 12 and recover a known GL2 identity. Any collision requires exact symbolic certification. GL3 and SL3 versions are equivalent by exponent sums and scalar normalization; this reduction is recorded in `research/18.43-plan.md`.

The index contains 1,308 main-body problem entries, all 150 Issue 21 entries. Editorial stars and later literature must be checked manually. Recent claimed resolutions of 20.21 and decidability in 21.32 are excluded from new-solution counts. Our alternate 21.32 argument is retained as a rediscovery.

## Next work

1. Revalidate running jobs and certify any hits.
2. Continue novelty and mathematical audits of both complete candidate constructions; inspect the 2013 Timofeenko source for 21.132.
3. Develop the exact simultaneous Sylow-intersection search for 21.26.
4. Expand beyond the initial involution graph range and continue surveying older problems.

Deadline: **2026-09-12 20:56:46 UTC**. The 48-hour goal remains active. No external messages, submissions, or Git pushes have been made.
