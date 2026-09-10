# Current status

Updated: 2026-09-10 21:04 UTC.

- Active phase: candidate-solution audit, literature triage, and problem indexing.
- Candidate complete solutions: 1, Problem 21.106 (negative), pending external review and further novelty checks. Complete self-contained proof in `research/21.106-proof.md`.
- Externally reviewed new solutions: 0.
- Mathematical experiments running: none.
- GAP 4.16.1 works. SmallGrp, TransGrp, and CTblLib load successfully; S4 is identified as SmallGroup(24,12). Use `bin/gap` for reproducible launches.
- Input PDF already includes many solutions from 2026. A further paper dated 29 August 2026 may address entries not yet updated in the supplied file.

Problem 21.106: the proposed formula defines exactly the two central generators in H(Z), while the generated subgroup is infinite cyclic. Residual finiteness follows directly by coordinate reduction. Exact arithmetic and direct finite-quotient formula checks passed; these are sanity checks, not the proof of the infinite theorem.

Next actions: finish literature/version audit of 21.106, index statements, and start a portfolio of exact finite-group searches (including 21.26, 21.99, and 21.113) while surveying older problems.
