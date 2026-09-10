# Current status

Updated: 2026-09-10 21:18 UTC.

- Active phase: candidate-solution audit, exact searches, and broader problem triage.
- Candidate complete solutions: 1, Problem 21.106 (negative), pending external review and further novelty checks. Complete self-contained proof in `research/21.106-proof.md`.
- Externally reviewed new solutions: 0.
- Mathematical experiments running: character-table search for 21.113(a), and degree-multiset collision search for 21.59(a)/21.135. See `state/jobs.json` for the last observed PIDs and tool sessions; verify live processes before relying on them.
- GAP 4.16.1 works. SmallGrp, TransGrp, and CTblLib load successfully; S4 is identified as SmallGroup(24,12). Use `bin/gap` for reproducible launches.
- Input PDF already includes many solutions from 2026. A further paper dated 29 August 2026 may address entries not yet updated in the supplied file.

Problem 21.106: the proposed formula defines exactly the two central generators in H(Z), while the generated subgroup is infinite cyclic. Residual finiteness follows directly by coordinate reduction. Exact arithmetic and direct finite-quotient formula checks passed; these are sanity checks, not the proof of the infinite theorem.

Completed computational result: all 4,722 transitive groups of degrees 2–20 satisfy 21.99 (4,631 checked by the orbital/class method, 91 rank-two cases by the derangement theorem). Independent full element enumeration agrees with the method for all 86 groups of degrees 2–8. This is bounded evidence only.

The problem index now contains 1,308 main-body entries, including all 150 Issue 21 entries. Editorial stars and later literature must be checked manually. The literature screen excludes recent claimed resolutions of 20.21 and the decidability part of 21.32, in addition to the 2026 multi-problem papers. An elementary pullback proof for 21.32 was found independently and retained as a rediscovery.

Next actions, in order:

1. Revalidate running character-table jobs and inspect any hits. Distinguish duplicate table names from nonisomorphic groups.
2. Finish the character-table computation; if (a) has no counterexample, test projective-character decomposition for 21.113(b).
3. Develop exact searches for 21.26 and involution graphs in 21.52–53; inspect their recent literature first.
4. Investigate 18.43: positive-word trace-equivalence search beyond the published length-20 range, with an exact polynomial certificate required for any hit. The primary paper *Decision problems, complexity, traces, and representations* reports no SL3-equivalent pairs through length 20.
5. Continue surveying older problems and audit the Golod-specific requirement of 21.132 before treating a direct-product observation as a resolution.

Deadline remains 2026-09-12 20:56:46 UTC. The overall goal is active; only about 22 minutes of the 48-hour opportunity have elapsed.
