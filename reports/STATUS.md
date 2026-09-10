# Current status

Updated: 2026-09-10T22:23:13.268158+00:00.

- Active phase: proof audit, exact searches, and broader problem triage.
- Complete candidate resolutions: **3**: **21.106** (negative), **21.132** (construction for every prime), and **21.121(a)** (infimum not attained at p=2). All await outside review and further novelty checks.
- Externally reviewed new solutions: 0.
- Running computations: 21.26 Sylow-intersection search for orders 1792–2000; currently processing order 1920. Revalidate handles in `state/jobs.json` before relying on liveness.
- Also running: 19.20 endomorphism/partial-isomorphism counts through order 255. The published range through 63 has been reproduced: 318 groups, including 105 abelian equality controls and 213 nonabelian strict inequalities. Four further blocks are running.
- GAP 4.16.1 and SmallGrp, TransGrp, CTblLib, Digraphs 1.15.0, and GRAPE work. `bin/gap` is the reproducible launcher.

## Candidate proofs

**21.106:** A parameter-free formula defines exactly the two central generators in the integral Heisenberg group, a residually finite group. Its value set is finite but generates an infinite subgroup. The self-contained proof and internal audit are in `research/21.106-proof.md` and `research/21.106-review.md`. Exact arithmetic and finite-quotient sanity checks passed; the infinite claim rests on the proof.

**21.132:** Starting from a graded Golod nil algebra, remove the homogeneous ideal of elements annihilated by a sufficiently high algebra power. A triangular extension has zero centre and preserves a grading with finite-dimensional pieces. Its three-generated adjoint subgroup is infinite, centreless, and residually a finite p-group. Adjoining a one-dimensional zero algebra gives a four-generated Golod group with centre C_p. Proof: `research/21.132-proof.md`; audit: `research/21.132-review.md`. The exact Notebook statement permits the final direct factor. The older centreless construction has been compared; broader novelty work remains.

**21.121(a):** A free product of central quotients of (Q_8 semidirect C_3) powers has 2-Jordan exponent log(24)/log(8), with no bound at the infimum. A binary simplex-code lemma controls every subgroup, giving a uniform bound for each larger exponent. Proof and audit: `research/21.121a-proof.md` and `research/21.121a-review.md`. Exact checks passed on all 11,781 subgroups of the second finite group, plus independent code and quaternion controls. Part (b) remains unresolved.

## Completed bounded searches

- **21.99:** All 4,722 transitive groups of degrees 2–20 satisfy the conjecture: 4,631 orbital checks and 91 rank-two cases. Independent full-element verification agrees for all 86 groups of degrees 2–8.
- **21.113(a):** 2,750 ordinary character tables, 9,850 table/prime cases, no skips or counterexample. **21.113(b)** also completed: 7,573 available modular cases, 2,277 unavailable cases, no counterexample; all decomposition-matrix reconstruction checks passed.
- **21.59(a)/21.135:** 106 degree-multiset collisions among 2,750 tables, all between entries marked almost simple. Primed orthogonal/unitary entries were checked and are alternative table/fusion data. No nonisomorphic counterexample established. See `research/degree-collision-audit.md`.
- **21.52–53:** 27 group entries, 28 involution classes, one explicit size-cutoff skip, no counterexample. The strengthened run verifies actual group automorphisms on every involution, correcting an insufficient normalizer-only test. See `research/21.52-53-results.md`.
- **18.43:** All 3,933,931,043 positive necklaces of lengths 1–36 have distinct pairs of exact GL3 trace fingerprints within each length. No candidate identity found. Summary: `results/18.43-summary.json`. Independent Python checks cover enumeration and arithmetic through length 12 and recover a known GL2 identity. Any collision requires exact symbolic certification. GL3 and SL3 versions are equivalent by exponent sums and scalar normalization; this reduction is recorded in `research/18.43-plan.md`.

- **21.26:** 63,122 groups in completed blocks, all satisfying the strict exact union bound. The full range through order 1791 is covered by these checks together with the known result for orders involving at most two primes. The final block 1792–2000 is running. Independent direct enumeration agrees for all 211 non-prime-power-order groups through order 60.

The index contains 1,308 main-body problem entries, all 150 Issue 21 entries. Editorial stars and later literature must be checked manually. Recent claimed resolutions of 20.21 and decidability in 21.32 are excluded from new-solution counts. Our alternate 21.32 argument is retained as a rediscovery.

## Additional constructions and exclusions

**13.19:** Found and verified an explicit negative example with Q of order 256,
H of order 32, and four dihedral factors of order 8. Both groups are subdirect
and Q/H is the irregular group D8. Independent matrix enumeration checked
all 65,536 products and quotient-map identities. The literature audit shows
that Kearnes--Mayr--Ruskuc (2018) already implies a negative answer, so this
is excluded from the new-solution count. See `research/13.19-proof.md` and
`research/13.19-review.md`. A separate self-contained realization of every
finite p-group as such a quotient is in `research/13.19-universality.md`.

**12.69:** The literal statement has an elementary norm/trace counterexample
which also contradicts its claimed uncountable analogue. A formulation
issue is recorded in `research/12.69-formulation-audit.md`; it is not counted
as a substantive new resolution of the intended problem.

## Next work

1. Revalidate running jobs and certify any hits.
2. Continue novelty and mathematical audits of all three candidate resolutions. The 2013 Timofeenko source has now been inspected.
3. Finish the remaining 21.26 range and inspect any case not settled by the union bound.
4. Expand beyond the initial involution graph range and continue surveying older problems.

Deadline: **2026-09-12 20:56:46 UTC**. The 48-hour goal remains active. No external messages, submissions, or Git pushes have been made.
