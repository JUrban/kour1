# Candidate portfolio

Updated 2026-09-10 21:41 UTC. This is a research triage list, not an assertion that every unstarred entry is still open.

| Problem | Current route | Status and next discriminator |
|---|---|---|
| 21.106 | Define a central generator up to inversion in H(Z) using first-order centralizer conditions. | Candidate complete negative solution committed; published-source version confirms question remains posed. Audit and refine manuscript. |
| 21.113(a) | Recover Psi from fibers of the p'-part map using character-table power maps; decompose exactly into irreducibles. | Complete: 2,750 ordinary tables, 9,850 table/prime cases, zero skips, zero counterexamples. Bounded evidence only. |
| 21.113(b) | Test the same class function against projective indecomposable characters when decomposition matrices exist. | Running on available Brauer tables; reconstruct ordinary coefficients to check duality calculations. |
| 21.99 | Test all orbital relations using conjugacy-class representatives whose fixed-point count differs from one. | Complete: all 4,722 transitive groups of degrees 2–20 satisfy it. Full-element validation on 86 groups of degrees 2–8 agrees. |
| 21.26 | Intersect conjugates of the allowed-conjugator sets for the Sylow subgroups. | Design exact inclusion-minimal intersection predicate; do not replace inclusion-minimal by minimum cardinality without proof. |
| 21.89 | Search n with p(n) dividing n!, using recurrence and smoothness/divisibility certificates. | Deprioritized: OEIS reports exhaustive checking through two million. Small searches would duplicate known work. |
| 21.52–53 | Automorphism groups of involution class graphs, comparing order colors and selected colors. | Complete initial range: 27 group entries, 28 classes, one size-cutoff skip, no counterexample. Actual extension to group automorphisms checked. |
| 21.59(a), 21.135 | Compare multisets of ordinary character degrees with multiplicity. | Complete table screen: 106 collisions, all between entries marked almost simple. Mostly apparent duplicates; no actual counterexample established. |
| 21.132 | Homogeneous annihilator quotient, triangular nil algebra, then adjoining a one-dimensional zero algebra. | Second complete candidate: at most four generators, infinite residually p-finite Golod group with centre C_p for every p. Proof and internal audit written; novelty and outside review pending. |
| 18.43 | Exact modular trace fingerprints of positive binary necklaces, with symbolic certification for collisions. | Lengths 1–35 complete, no collision; length 36 sorting 1,908,881,900 necklaces. Independent small checks passed. |
| 21.130 | Rainbow Hamiltonian cycles in the sum coloring of odd abelian groups. | Finite subset search possible, but avoid highly symmetric cases already checked in literature. |

The index contains 1,308 main-body problem entries, including all 150 Issue 21 entries. Exactly 104 headings are starred, but partial solution markers also occur within unstarred entries. Older issues remain to be surveyed systematically. The separate solved archive is intentionally excluded from the index.

## Exact reduction for 21.113(a)

Let exp(G)=p^a e with gcd(p,e)=1 and choose m congruent to 0 modulo p^a and 1 modulo e. Then g^m is the p'-part of g. For a p-regular x, the fiber {g:g^m=x} is precisely {xy:y is a p-element of C_G(x)}: one implication follows from the commuting p/p' decomposition, and the other from uniqueness of that decomposition. Therefore fiber size is Psi(x). Fibers over p-singular elements are empty.

For conjugacy classes K_i, power-map indices f(i), and class sizes s_i, one obtains

    Psi(K_j) = sum_{i: f(i)=j} s_i / s_j.

The computation uses the exact table inner product; all coefficients must be nonnegative integers for Psi to be a character. Ambiguous table data are explicitly skipped and logged, not guessed.

Optimization: m=p^a suffices as well. It sends the p'-part of g to its m-th power, which permutes p'-elements. The unique p'-root of x generates the same cyclic subgroup as x and has the same centralizer, so the fiber still has size Psi(x). The initial run using a Chinese remainder exponent was stopped after about six CPU minutes with no 100-table checkpoint; a prime-power implementation with per-table logging replaces it. The exact slow operation in the initial run was not isolated.

## Exact reduction for 21.99

Fix alpha=1 and label the orbits of G_alpha. Choose t_gamma taking gamma to alpha. For a class representative c, the orbital containing (gamma,gamma^c) has label equal to the G_alpha-orbit of (gamma^c)^t_gamma. Conversely, if this is the orbital of (alpha,beta), a conjugate of c takes alpha to beta. Fixed-point count is constant on conjugacy classes.

Thus the conjecture holds for a given permutation group exactly when representatives c with fixed-point count different from one cover every off-diagonal orbital via these pairs. Testing one conjugacy-class representative and all gamma is complete, without enumerating the group.
