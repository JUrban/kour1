# Current status

Updated: 2026-09-10 21:21 UTC.

- Active phase: candidate-solution audit, exact searches, and broader problem triage.
- Candidate complete solutions: 1, Problem 21.106 (negative), pending external review and further novelty checks. Complete self-contained proof in `research/21.106-proof.md`.
- Externally reviewed new solutions: 0.
- Mathematical experiments running: projective-character search for 21.113(b). See `state/jobs.json` for the last observed PID and tool session; verify live processes before relying on them.
- GAP 4.16.1 works. SmallGrp, TransGrp, and CTblLib load successfully; S4 is identified as SmallGroup(24,12). Use `bin/gap` for reproducible launches.
- Input PDF already includes many solutions from 2026. A further paper dated 29 August 2026 may address entries not yet updated in the supplied file.

Problem 21.106: the proposed formula defines exactly the two central generators in H(Z), while the generated subgroup is infinite cyclic. Residual finiteness follows directly by coordinate reduction. Exact arithmetic and direct finite-quotient formula checks passed; these are sanity checks, not the proof of the infinite theorem.

Completed computational result: all 4,722 transitive groups of degrees 2–20 satisfy 21.99 (4,631 checked by the orbital/class method, 91 rank-two cases by the derangement theorem). Independent full element enumeration agrees with the method for all 86 groups of degrees 2–8. This is bounded evidence only.

Completed character-table result: 21.113(a) has no counterexample among all 2,750 CTblLib ordinary tables and 9,850 table/prime pairs, with no skipped cases. This is bounded evidence, conditional on library data and the proved power-map reduction. The projectivity question (b) is now being tested on all available Brauer tables, with an independent decomposition-matrix reconstruction check in every case.

The degree-multiset screen finished all 2,750 tables and reported 106 collisions involving almost-simple tables. Every colliding entry is itself marked almost simple. The list predominantly consists of different names or embeddings of the same groups; no nonisomorphic pair has been established. Inspect the primed orthogonal/unitary table cases and metadata before closing this lead.

The problem index now contains 1,308 main-body entries, including all 150 Issue 21 entries. Editorial stars and later literature must be checked manually. The literature screen excludes recent claimed resolutions of 20.21 and the decidability part of 21.32, in addition to the 2026 multi-problem papers. An elementary pullback proof for 21.32 was found independently and retained as a rediscovery.

Next actions, in order:

1. Revalidate the running 21.113(b) job and inspect any hits.
2. Audit the 106 degree-multiset collisions, distinguishing duplicate table names from nonisomorphic groups; retain only meaningful leads.
3. Develop exact searches for 21.26 and involution graphs in 21.52–53; inspect their recent literature first.
4. Investigate 18.43: positive-word trace-equivalence search beyond the published length-20 range, with an exact polynomial certificate required for any hit. The primary paper *Decision problems, complexity, traces, and representations* reports no SL3-equivalent pairs through length 20.
5. Continue surveying older problems and audit the Golod-specific requirement of 21.132 before treating a direct-product observation as a resolution.

Deadline remains 2026-09-12 20:56:46 UTC. The overall goal is active; only about 25 minutes of the 48-hour opportunity have elapsed.
