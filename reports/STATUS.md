# Current status

Updated: 2026-09-12T09:46:20.647939+00:00.636707+00:00.

- Active phase: proof audit, exact searches, and broader problem triage.
- Complete candidate resolutions: **44**: **21.106** (negative), **21.132** (construction for every prime), **21.121(a)** (infimum not attained at p=2), **21.68** (semi-abelian non-monomial group of order2592), **16.87(a),(b)** (nonabelian, nonperiodic variety with maximal test rank at every finite rank), **10.35** (torsion-free complex matrix group not residually rational in the same degree), **16.28(a)** (a closed set with every power greater than one nonclosed), **14.22** (failure of finite isolated-radical presentation over infinitely generated torsion-free linear coefficient groups), **16.20** (a finite modular nondistributive dominion lattice), **17.33** (infinite axiomatic rank of the Klein bottle quasivariety), **17.101** (every group representation has a homogeneous extension), **18.76** (a nonsplit additive division-ring extension), **18.92(a),(b)** (non-algebraic and non-modular complete lattices of formations), **20.108(a),(b)** (a centreless group of order605 whose multiple-holomorph quotient contains an element of order4), **20.90** (a two-generator infinite profinite CA-group mapping onto A5), **11.116** (finite subgroup-lattice dimension for the stated Chernikov groups), **14.72** (a smooth affine surface with a smooth fixed Cartier divisor but singular cyclic quotient), **21.40** (a normal nilpotent subgroup of finite index in every rational linear group with finitely many automorphism orbits), **21.60** (an order-twelve counterexample to the semiperfectness criterion), **4.55** (non-unique indecomposable projective decompositions over Z_(5)[3.A7]), **21.107** (a countable resolvable group without an expansive sequence), **15.89** (a four-regular infinite Cayley graph with invertible adjacency on all functions), **16.9** (an exact cubic-time algorithm returning a minimum palindrome factorization in every finite-rank free group), **18.18** (non-enumerability of both the cofinite finite-group theory and its complement), **19.56** (solubility from restricted coprime commutator orders), **20.92(a)** (the printed brace average is pre-Lie for a uniform sufficiently large prime), **9.47** (a height-four scattered compact space that cannot embed in any noncompact-subgroup E-space), **9.45** (an explicit coordinate divisibility criterion for orthogonal bases in every dimension), **10.62** (a three-generated perfect periodic group with a single involution class and odd pairwise products), **10.32** (an explicit logarithmic degree bound for symmetric-group power-word universality), **15.65** (nonrationality of all the stated classical cyclic and semisimple limits, also under the source's squarefree-characteristic-polynomial convention), **15.92** (continuum many nonisomorphic infinite alternating-residual quotients of every triangle group Delta(2,3,r), r>6), **4.75** (a periodic group with Sylow 2-subgroups of order two whose involutions are noncentral modulo its odd-order radical), **9.4** (no finite quasigroup generates the ordinary isotope variety of a nontrivial finite group), **12.40** (no finite bound on Brauer-degree p-parts in terms of the group-order p-part), **13.42** (a free nilpotent group with an unrestricted Z[t]-completion that is not locally nilpotent), **14.26** (closure of the torsion-free nilpotent quasivariety under restricted wreath products with Z), **15.76(b)** (innerness of every category automorphism for each full variety of groups of fixed derived length), **16.38** (periodicity of every subgroup contained in a product of two periodic subgroups of a soluble group), **19.93** (unbounded lower p-central factors in two-generator finite p-groups with no C_p wr C_p quotient), **20.1** (the insoluble totally 2-closed group J1 x C13 with Fitting subgroup C13), **19.62** (closedness of every derived elementary carpet over every commutative ring), **19.61** (every carpet closure is a carpet, with unchanged derived carpet), and **21.76** (irreducible closed noncompletable nets of every order in every odd characteristic). All await outside review and further novelty checks.
- Externally reviewed new solutions: 0.
- **21.76 full affirmative candidate:** the explicit net over k(x,y) has levels kx+y*k[x,y] at one opposite pair and y*k[x,y] elsewhere. A polynomial degree lemma and reduction modulo y prove closedness; x^3 rules out completion. A second example works over F9(t), with an explicitly certified group of order120. The 37-file replay passes all14,400 finite matrix products and36,432 polynomial words. The rank-one polynomial lemma is prior Koibaev2011 and is credited; outside review and priority remain pending. See `research/21.76-proof.md` and `research/21.76-report.md`.
- **15.46 structural consequence:** after omitting generators at one opposite-root pair, the remaining generators form a normal subgroup whose root intersections at that pair are exactly the derived levels. The proof uses the new 19.61/19.62 candidates; 1,127,612 finite pair controls and a 411-file replay pass. The full rank-one intersection remains unresolved, so this adds no complete candidate. See `research/15.46-omitted-pair-lemma.md` and `research/15.46-source-audit.md`.

- **19.62 full affirmative candidate, shortened proof:** the stronger inclusion A_p^2 B_-p inside B_p reduces to A2, B2 and G2. All 104 targets pass independent integer checking; 19 representative derivations are printed in full. The 291-file replay verifies the short certificates, 655 nodes, complete Weyl transport, root models and exact polynomial constants. Start with `research/19.62-rank-two-proof.md` and `research/19.62-rank-two-derivations.md`; the direct known-criterion proof is in `research/19.62-closedness-criterion.md`. The earlier 71,056-target proof remains frozen. Outside review and priority remain pending; 19.63 is not counted again.

- **19.62 earlier stages:** the finite screen verified 6,999 derived carpets from 193,805 originals; the universal G2 packet then verified 2,712 targets. Both are retained as audited stages superseded by the full theorem above.

- **19.61 full affirmative candidate:** adjoining opposite-root square terms preserves the derived carpet. All 300 universal targets and 3,191 integer derivation nodes pass; an explicit countable completion and the known closedness criterion prove that every carpet closure is a carpet, with the same derived carpet. The 395-file replay also checks all 193,805 saved finite controls. See `research/19.61-proof.md` and `research/19.61-report.md`. Outside review and priority remain pending.

- **19.61 earlier finite stages:** the C2 pilot, G2 prime-field pilot, four-ring extension, F9 search and Z/9 congruence-kernel calculation remain independently audited evidence. Their reports and all raw outputs are preserved; the full theorem above supersedes their bounded-only status.

- **21.102 partial:** adapting Olshanskii2026 gives log|F_n(G)|<=A n^c [G:N]^n for any nilpotent normal subgroup N of class c. With the prior nonabelian-monolithic quotient theorem this proves the desired integral limit for that quotient class. General case and partial-result priority unresolved; see `research/21.102-nilpotent-normal-bound.md`.
- **20.21 order1536 excluded:** the Sylow reduction leaves 18,028 of the 408,641,062 catalogue groups. All 26,760 pairs among 30,414 retained kernels are independently separated by table-derived invariants. The 67-file audit passes and every possible counterexample now has order at least 3,072. General question unresolved; see `research/20.21-order1536-report.md`.

- **20.21 order768 excluded:** all1,090,235 groups tested,606 with both quotients,2,368 pairs independently separated using2,878 kernel multiplication tables. The65-file audit passes. The prior minimality reduction now excludes every order below1536. General question unresolved; see `research/20.21-order768-report.md`.
- **20.21 bounded pilot:** all22,015 groups of orders12,24,48,96,192,384 have no matching C12/A4 kernel pair. The123 groups with both quotient types are retained;25 independent table controls and the14-file audit pass. General question unresolved; see `research/20.21-search-report.md`.
- **20.59 prior affirmative:** Minasyan2026 Theorem1.1 proves property(LR) for every virtually free group and explicitly answers the question. Statement image viewed and final proof read; embedding and reflection inputs imported. No new count; see `research/20.59-prior-result.md`.
- **20.3 prior negative consequence:** Gong--Yang--Zeng2026 Theorem5.3 gives closure number at least n for PSL_n(3), with odd n>=5. Source pp.21--22 were read and viewed; an elementary determinant proof is recorded. No new count; see `research/20.3-prior-consequence.md`.
- **20.1:** Coprime direct products preserve total 2-closure in all faithful actions. The published J1 theorem gives J1 x C13, with Fitting subgroup exactly C13. All177 GAP and independent Python action controls agree; the30-file replay audit passes. Complete affirmative candidate; see `research/20.1-proof.md` and `research/20.1-report.md`. Imported classification and unconfirmed priority are explicit.
- **19.77 prior affirmative:** Kapovich2026 Theorem A and Corollary1.2 state uniform generic small-cancellation stability, including sphere and ball models. Relevant statements and selected proofs were inspected; full paper remains imported. **20.21:** the located negative preprint was withdrawn for an error and is not a solution. See the separate source notes.
- **18.84 bounded screen:**78 character-table pairs and87 catalogue tests yield no counterexample;87 missing or class-capped entries remain. Exceptional order-three cases are inconclusive. Tables and embeddings are not independently reconstructed. See `research/18.84-report.md`; no candidate count.
- **19.93:** Three power relations exclude the wreath quotient, while filtered Golod--Shafarevich growth and an elementary normal-form count force unbounded lower p-central dimensions, already at (p,d)=(7,2). The 23-file audit replays21,714 norm checks and12 exact algebra truncations; seven GAP quotients reach order7^68. Complete negative candidate, with the whole-group quotient hypothesis explicit; see `research/19.93-proof.md` and `research/19.93-report.md`.
- **17.16 prior D5 consequence:** Paris--Soroko2026 Theorem1 and an explicit finite-index linearity argument settle type D5. General spherical types remain unresolved here; no new count. See `research/17.16-prior-d5.md`.
- **16.38:** A finite-orbit argument for cocycles and induction on derived length prove the full affirmative answer, without assuming AB is a subgroup. The 21-file audit replays 6,125 rational matrix cocycle/product pairs and 87,380 sign-action pairs. An infinite direct-sum example clarifies why individual elements of AB can still have infinite order. Complete candidate; see `research/16.38-proof.md` and `research/16.38-report.md`.
- **15.76(b):** An affine coefficient induction proves that every normalized associative word on the full variety S_d is xy or yx. An explicit reduction then makes every category automorphism inner, for all d>=1. The 42-file audit replays 2,430 bounded metabelian words, noncommutative controls over S3/S4, and 1,000 free-group naturality checks. Complete candidate; see `research/15.76-proof.md` and `research/15.76-report.md`.
- **20.72 prior affirmative:** Fernandes--Tsurkov2019 Theorem9.1 gives an outer quotient of order two for a metabelian exponent-four class-four subvariety. Intermediate calculations remain imported; no new count. See `research/20.72-prior-result.md`.
- **15.44(a) prior negative consequence:** The cubic-cone Segre ring, already in Hochster2007 pp.15–16, is the invariant ring of a reductive torus acting on a Cohen–Macaulay hypersurface. All printed filtration hypotheses are checked; an explicit parameter sequence and Hilbert series both prove failure. No new count; see `research/15.44-prior-counterexample.md`.
- **11.78 scope audit:** Disconnected generalized dihedral algebraic groups refute both literal parts. Frécon2013 already supplies substantial connected positive cases. The connected convention is unconfirmed; this scope obstruction adds no candidate. See `research/11.78-scope-audit.md`.
- **18.77 partial:** A prime-power ring Pfaffian argument proves character regularity, and simultaneous detection of p-e elements, for finite p-groups of class less than p. The class-two consequence is explicitly prior (Isaacs--Passman1968, Theorem1.5). The 32-file audit replays 22,063 initial parameter values, 578 forbidden-hyperplane sets, and a nontrivial Z/25 valuation control. General question and small-class priority unresolved; see `research/18.77-report.md`.
- **18.120 partial:** The abelian-normal-closure criterion proves all groups of class at most four, including overlapping factors. A completed GAP search covers 59,349 groups and 28,155 disjoint factorizations beyond class four, with no failure. Six independent table controls check 2,791 subgroups and 812,589,714 triples; the 37-file audit passes. General question unresolved; see `research/18.120-report.md`.
- **14.26:** A finite polynomial-algebra construction gives torsion-free nilpotent local models for every finite part of G wr Z, for G in Q(all torsion-free nilpotent groups). Budkin1999 explicitly confirms finite support. Dual interpolation proves the needed independence; a refined matrix central series proves nilpotence. Four exact algebras and a37-element Heisenberg wreath table pass, with319 relations and666 separations. The23-file replay audit passes. Complete affirmative candidate; see `research/14.26-proof.md` and `research/14.26-report.md`.

- **16.45 extension:** All2,435 groups of orders81,125,128,243,343,625 pass the sufficient normal-Frattini criterion. Eight added table controls reconstruct474 subgroups and check307,619,161 triples. The46-file audit replays both packets. Combined coverage is2,789 groups and1,153,563 subgroups; general problem unresolved. See `research/16.45-extension-report.md`.

- **16.45 pilot:** All354 p-groups in the prescribed orders through64 have a sufficient normal-Frattini certificate for b(G)=mu'(G). The screen covers45,105 subgroups;12 independent table controls reconstruct3,243 subgroups and explicit minimal bases. The26-file audit passes. Initial GAP syntax warnings and the rejected wrapper run are retained. General problem unresolved; see `research/16.45-report.md`.

- **16.14 prior deduction:** The centralizer bound in Sambale2014, Theorem1.3 proof, gives d(G)<=2d(Z(G)) under the exact central-involution hypothesis. The relevant author pages and a later restatement were read and viewed; the underlying MacWilliams theorem is not independently audited. Excluded from new candidates; see `research/16.14-prior-result.md`.

- **13.42:** The unrestricted Z[t]-completion of the free nilpotent rank-two class-three group is not locally nilpotent. An explicit torsion-free exponential group sends every [x^t,y,...,y] to the nonzero polynomial (T-1)^r in Q[Q]. All original conditional scalar axioms are proved. The 17-file replay audit passes, including a generic ten-coordinate truncated-algebra check and exact rational controls. Complete affirmative candidate; see `research/13.42-proof.md` and `research/13.42-report.md`.

- **14.89(b):** Jaikin-Zapirain2000 Corollary3.1 gives the exact prior affirmative answer. The complete seven-page DVI text was read; PDF conversion failed and no visual audit is claimed. Excluded from new candidates; see `research/14.89b-prior-result.md`.

- **12.40:** For every k>=3, an odd a gives G=PSL_6(5^a) with |G|_2=8192 and an irreducible 2-Brauer degree of 2-part exactly 2^k. Bray's projective-heart construction is credited; an elementary exponent lift proves unboundedness. All 510 lifting controls, eight exact orders, three actual GAP modules and 352,440 table degrees pass the 37-file audit. The initial trivial-table coverage failure is retained. Complete negative candidate; see `research/12.40-proof.md` and `research/12.40-report.md`.
- **7.58 prior consequence:** An explicit spanning-tree retraction gives the image test rho(b)=b t_q^-1 and reconstructs a preimage. McCool1987 already proves the associated conditional algorithm for this exact question. The self-contained proof and 82,134 finite membership controls are retained, without a new count; see `research/7.58-proof.md`.
- **6.47 partial:** A self-contained proof covers all class-two groups. Frozen pilot, extension and vector packets now cover 38 groups, 4,207 normalized operations, 178 associative outputs and 876,136,474 triples. All outputs belong to var(G). The vector method completes all twelve earlier timed-out cases; two operations on SmallGroup(64,34) require general isomorphisms, verified on 8,192 pairs. The earlier capped (24,3) case remains incomplete. The 131-file vector auditor also replays both earlier packets and 26 forced-cap regression controls. No new count; see `research/6.47-vector-report.md` and `research/6.47-class-two.md`.
- **5.25 prior negative:** Bludov--Kopytov--Rhemtulla2009 Example 3.1 explicitly constructs a totally orderable soluble group of derived length three with abelianization of exponent two. The relevant construction was read and a local sign discrepancy documented; omitted module calculations remain unaudited. Our metabelian positive argument is retained, but the proposed finite-extension step is false. No new count; see `research/5.25-prior-result.md`.
- **8.24 prior announcement:** Kopytov2013/2014 Theorem 1 states the finitely generated locally indicable finite-rank case. Both pages were read and viewed; full proofs and an arbitrary-group extension are not supplied there. No new count; see `research/8.24-prior-announcement.md`.
- **10.59 prior partial:** Di Bartolo--Ersoy--Falcone, arXiv:2604.01011v2 (June 2026), settles periodic residually finite p'-groups and excludes periodic Tarski monsters. The abstract metadata omits an essential p' hypothesis retained in the full text. All mathematical text read; no new count. See `research/10.59-prior-result.md`.
- **15.95 partial:** A coset-counting proof settles transitive p-groups with a regular normal subgroup, including nonabelian ones. General case and priority unresolved; see `research/15.95-regular-normal-case.md`.
- **11.115 partial:** The commutator inclusion is strict if N has finite index or contains a primitive element. The relation-module proof handles arbitrary free rank but not general N; see `research/11.115-partial.md`. No new count.
- **13.53 prior partial:** Sozutov--Alexandrova2017 covers every conjugating element in infinite locally graded p-groups; a short finite-quotient proof is retained. The unrestricted question remains unresolved here.
- **19.20 product follow-up:** No reciprocal count ratios among85,343 IDs with retained rows, so coprime products from this data yield no equality. See `research/19.20-coprime-products.md`; the original complete catalogue audit is unchanged.
- **12.9(b) prior affirmative consequence:** KMS Theorem62 gives finite generation of every abelian subgroup of a finitely presented tree-free group; the chain-union argument proves the requested maximal condition. Part(a) untouched, no new count; see `research/12.9b-prior-result.md`.
- **11.15 source audit:** Brandl1981 already disproves the simple commutator-power sequence for every odd p using SL(2,p^2). The all-group odd-prime problem remains unresolved here; see `research/11.15-source-audit.md`.
- **11.124 prior affirmative:** Tursunbaev, arXiv:2609.06755v1 (6 September 2026), Corollary1.2 settles the exact normality question. All mathematical proofs read and internally checked against the imported classical inputs; no new count. See `research/11.124-prior-result.md`.
- **11.18 bounded investigation:** GAP and ACE reproduce the known G(2,2)=1 and reach workspace limits in the other cases. A symbolic matrix screen through period10 finds no new characteristic-zero route; independent permutation replay resolves the source composition convention. No new count; see `research/11.18-exploration.md`.
- **11.5 coefficient qualification:** The literal arbitrary-ring version is false over Z[sqrt(-5)] with G infinite cyclic; explicit rank-two projective and determinant obstruction in `research/11.5-coefficient-obstruction.md`. Classical construction, no new count; restricted coefficient versions untouched.
- **9.55 prior negative:** Weiss' permutation-lattice criterion gives the requested p-adic integral-unit/group-automorphism factorization for every augmentation-preserving automorphism. The complete double-action deduction is in `research/9.55-prior-result.md`; original rigidity proof imported, no new count.
- **8.78 periodic locally nilpotent case:** A countable universal group is the restricted direct product of Maier's unique countable existentially closed locally finite p-groups. The extension and primary-decomposition arguments are proved explicitly. This prior consequence does not settle the locally soluble case and adds no new candidate; see `research/8.78-prior-result.md`.
- **7.27 affirmative prior consequence:** Fulman--Guralnick Theorem3.2 leaves only algebraic maximal-rank overgroups. A diagonal element whose n!-th power is regular forces every proper irreducible overgroup to permute coordinate blocks. For fixed n, almost every diagonal element works as q grows. No explicit threshold or new count; see `research/7.27-prior-result.md`.
- **4.56(b) prior cancellation consequence:** Equal classes in G(T) give equal projective Euler classes; Bass 1964 Theorem 9.3 then gives isomorphic kernels for n>dim(max(R)). Literal equality of submodules is distinguished, and part (a) is untouched. Excluded from the new count; see `research/4.56b-prior-result.md`.
- **20.112 bounded screen:** For F=N^3, all 8,339 groups of orders 648,1296,1944 pass the saturation implication. Twelve require full ambient/Frattini-quotient checks. General saturation remains unresolved; see `research/20.112-screen-report.md`.
- **20.80 prior affirmative theorem:** Lu, arXiv:2511.20171v1 (25 November 2025), Theorem A supplies the missing monomial P-character implication. Full short proof read and checked, with a reversed kernel sign corrected explicitly; excluded from the new count. See `research/20.80-prior-result.md`.
- **20.18 exponent qualification:** At p=2 a class-two group of exponent dividing 2^k has derived exponent dividing 2^(k-1), so the exact-derived-exponent reading is false. The divisibility-only reading is already asserted in Budkin 2020. Convention and source limits are explicit; no new count. See `research/20.18-exponent-obstruction.md`.
- **19.60 coefficient qualification:** A fixed computable Euclidean domain F[t] can have undecidable free generation even for one diagonal matrix in SL2, by Stoltenberg-Hansen–Tucker’s roots-of-unity theorem. This refutes the literal arbitrary-coefficient reading; it does not settle the Z or Q cases. Excluded from new priority; see `research/19.60-coefficient-obstruction.md`.
- **21.55 prior negative deduction:** Hall–Higman and the unipotent exponent bound give limsup m_n(7)/log_2(n)<=1/log_2(7)<1. The printed base 2 was visually checked. This complete classical-theorem consequence is excluded from the 26 new candidates; see `research/21.55-prior-result.md`.
- Latest near-Frattini follow-up: **19.3(a),(b),(c),(e),(f)** follow from Allenby 1999–2005 and Hall; **19.1(a),(b)** follow for the standard nontrivial knot constructions. Proper-amalgam and degenerate-knot conventions are explicit. **19.6(a)** is already asserted in Allenby 2005, with its specific earlier proof adaptation unaudited. All are excluded from the 26-candidate count; see `research/19.1-19.3-prior-results.md`.
- Latest prior-result audit: **19.4(a),(b)** and **19.5** are negative by Allenby 2000: the near Frattini subgroup of an unbounded root amalgam is its infinite cyclic amalgam. **17.48** and **18.56** have exact affirmative prior theorems of Sela and Wilkens. Reading scopes and exact deductions are recorded; none increases the 25-candidate count.
- Previous prior-result audit: **17.87** is affirmative by the universal central extension of a published perfect group of intermediate growth. The resulting group has zero Schur multiplier; the precise proof is in `research/17.87-prior-result.md`, excluded from the new count.
- Other recent prior deductions: the SO(3,R) case of **16.68** and **16.69(b)** are negative by Thom's almost-law theorem; **14.59** is negative by Tent's sharply 3-transitive construction. These and the earlier prior consequences remain excluded from possible new priority.
- The 21.26 search through order2000 and the 19.20 search through order511 are complete. Exact ID coverage and all completion records pass.
- **19.20 complete:** all91,774 nonabelian groups through order511, zero equality cases and469 reverse inequalities. All356 jobs in the latest extension completed;514 omitted abelian IDs were independently reconstructed and matched exactly. The initial493 abelian equality controls remain retained. The arbitrary-group equality question is unresolved.
- **20.100 n=7 verifying:** generation completed 42,891,332 nodes and 786,577,344 edges. At 07:38:35 UTC on 12 September, all six 14 GiB GAP workers are live, with 36,310,000 checked nodes, zero completed shards, and 50,824,436 KiB combined RSS. No n=7 proof is claimed until every shard and aggregate pass.
- **4.55 exploratory screen complete:** all2,750 installed table names and7,573 available modular cases are covered by two disjoint audited ranges. Flags remain exploratory; the separate3.A7 proof supplies the candidate resolution.
- GAP 4.16.1 and SmallGrp, TransGrp, CTblLib, Digraphs 1.15.0, and GRAPE work. `bin/gap` is the reproducible launcher.
- **14.2 restricted searches complete:** 16,146,897 rational pairs give682 integral swaps, all monomial;21,646 degree-changing permutations in249 individual conductor blocks give no integral maps. Independent matrix and actual-group controls pass. General question unresolved.
- **14.3 partial:** the two earlier criteria settle all2,750 table names, with actual-group controls passing. A separate order96 example proves those criteria jointly insufficient to force a central square. Its degree-four Q(sqrt(-2)) character nevertheless forces all central integral units symmetric. Normal Sylow2 case proved; general problem unresolved, no novelty claim.

**14.59:** Negative by Tent2016 Theorem2.1. The countable construction
has trivial three-point stabilizers and torsion-free two-point
stabilizers, and its absence of Klein four subgroups excludes the
proposed projective linear groups. Full source read and exact deduction
written; excluded from the new-candidate count.

**14.67:** Proved the prime minimal-class-size case for arbitrary finite
groups, with internal logical audit. The bounded search covers every
group through order511:721 centreless groups,14,500 eligible classes,
29,989 overgroups and zero counterexamples; the other cases have
nontrivial centre. Independent controls cover67,289 literal subgroup
cases. General question and novelty remain unresolved. See
`research/14.67-prime-class.md` and `research/14.67-review.md`.

## Candidate proofs

**9.4:** Thirty-fourth complete candidate: every n-element quasigroup satisfies the identity L_x^(n!)(y)=y, but a coordinate-shift isotope of a finite power of C2 violates it. The proof extends to every nontrivial finite group and to ordinary quasivariety and pseudovariety generation. An infinite monogenic isotope gives a separate local-finiteness obstruction. All 591 Latin squares through order four, 12 affine models, 93,252 quasigroup axioms and 2,396,744 Boolean identity checks pass; the 18-file auditor replays them. Gvaramiya1985 distinguishes ordinary quasigroups from three-sorted automata, and its relevant section was checked. That convention and priority remain explicit review concerns; see `research/9.4-proof.md` and `research/9.4-review.md`.

**4.75:** Thirty-third complete candidate, using the unchanged 10.62 existence result. Its exponent and order-four exclusion make every Sylow 2-subgroup C2. If an involution had central image modulo the odd-order radical, normal generation would make the quotient cyclic; perfectness and involution survival contradict this. The elementary deduction and 14-point audit are in `research/4.75-proof.md` and `research/4.75-review.md`. The 13-file auditor and the full frozen 27-file dependency audit pass. These two candidates share one geometric construction; priority and independent review remain pending.

**15.92:** Thirty-second complete candidate: a fixed word with uniformly bounded nonzero support in alternating quotients yields a marked limit with a finitary normal subgroup. A finite-quotient obstruction and recursive separating words produce continuum many distinct quotient kernels and isomorphism types. Conder's 1980 construction supplies a fixed 11- or 13-cycle word for every r>6. All 150 cycle-table cases and five independent reconstructed r=7 GAP actions pass; four general order calculations also pass, while the redundant fifth is deliberately stopped and preserved. A 70-file integrity audit binds the proof, sources, controls and failures. See `research/15.92-proof.md` and `research/15.92-review.md`. Priority and independent review remain pending.

**15.65, all stated classical families:** Thirty-first complete candidate, now extended to every cyclic and literal semisimple limit for full unitary, symplectic, and orthogonal groups, separately in both characteristics where needed. It also covers FNP's squarefree-characteristic-polynomial meaning of separable. A local zero raised to a nonconstant exponent has monodromy that single-valued analytic prefactors cannot cancel. Explicit alternating-series and zero-free bounds isolate the semisimple zero. The prime-power identity-theorem step rules out rational interpolation. All69 finite probability comparisons pass for23 GAP groups and563 classes; two exact series methods agree. Of160 published coefficient checks,159 match; the remaining table entry is inconsistent with the source's own exact relation and is documented. See `research/15.65-classical-proof.md` and `research/15.65-classical-review.md`. The original unitary cyclic packet stays frozen; novelty and outside review remain pending.

**10.32:** Thirtieth complete candidate: for nonzero r,s with at least one odd, the word x^r y^s is universal on S_n whenever n>=max(1126,16 log(rad(|rs|))). Every constant c>8 works beyond a suitable uniform threshold. A positive-genus cycle-product theorem handles odd targets after support reduction; the classical even-target cover and prime estimates finish the proof. All 6,143 actual witnesses and 49,144 root identities pass independent Python replay. See `research/10.32-proof.md` and `research/10.32-review.md`. Imported theorems are credited; priority and outside review remain pending.

**10.62:** Twenty-ninth complete candidate: a periodic quotient of C2*C2*C2 from Amelio's 2025 geometric theorem, with (abc)^p imposed in the first stage, gives an infinite perfect group of exponent 2p and no subgroup of order four. Its involutions form a single generating conjugacy class with all distinct pairwise products of order p. The scaling, direct-limit exclusion, and quotient-of-order-two obstruction are explicit. The 200 finite presentation abelianizations and 21,318 dihedral pair controls pass; these do not verify the imported geometric theorem. See `research/10.62-proof.md` and `research/10.62-review.md`. Outside review and novelty remain pending.

**9.45:** Twenty-eighth complete candidate: inspect at most four centered representatives per cyclic coset and keep exactly those whose normalized dual vector lies in the dual lattice. Every accepted line splits and distinct lines are automatically orthogonal, so counting gives the full criterion. The proof includes all rounding ties, exact O(mn) decision cost, and prime-power support restrictions. All 3,520 Python cases, 1,198 GAP basis equalities and 291,330 independent GAP box points pass. See `research/9.45-proof.md` and `research/9.45-review.md`. Prior two-dimensional results and general methods are credited; novelty and outside review remain pending.

**9.47:** Twenty-seventh complete candidate: compact families of closed noncompact subgroups have clopen selectors, while the explicit Dow--Watson height-four compact space does not. The Komarov--Protasov neighborhood lemma and counterexample obstruction are both proved in full with prior attribution. Conversely every compact space with a selector embeds using a discrete abelian group, with both Vietoris subbases checked. See `research/9.47-proof.md` and `research/9.47-review.md`. Novelty of the connection and outside review remain pending.

**20.92(a):** Twenty-sixth complete candidate: the exact base-2 average on the original additive space recovers its affine Lazard pre-Lie product whenever p>k and ord_p(2)>(k-1)k^(2k-2). A constructive polynomial inverse gives a dimension-only degree bound without strong nilpotence. The classical correspondence and prior averaging methods are credited. All 17,667 actual GAP affine-group elements, 303 inverse controls, three formal polynomial examples and 23,328 modular matrix entries are audited; expected small-prime discrepancies are retained. See `research/20.92a-proof.md` and `research/20.92a-review.md`. Outside review and comprehensive novelty checks pending.

**19.56:** Twenty-fifth complete candidate: the order inequality on restricted coprime commutators forces solubility, even when imposed only on primary outputs. The hyperfocal theorem gives the required Sylow generation; a smallest counterexample is a central extension of a minimal simple group, and an explicit local lift contradicts Baer–Suzuki. All 593 GAP cases, 843 Sylow equalities, 24 matrix examples, three central lifts, and independent Python controls pass. Close Monakhov and Bastos–Monetta results are credited. See `research/19.56-proof.md` and `research/19.56-review.md`; outside review and broader novelty checking pending.

**18.18:** Twenty-fourth complete candidate, under the cofinite isomorphism-type meaning of almost all. A fixed first-order sentence defines exactly S_n for n>=5 among finite groups; every finite H occurs as a two-element common centralizer in every S_n beyond 2|H|^2+3. Two effective reductions from Malcev finite-group validity prove that neither the cofinite theory nor its complement is computably enumerable. The sentence and centralizer lemmas are proved in full. Independent Python and actual GAP controls pass, including 14 base and 28 padded centralizers. See `research/18.18-proof.md` and `research/18.18-review.md`; outside review and further novelty checks pending.

**16.9:** Twenty-third complete candidate: encode the free group in the free product of one additional involution. Palindromic length is the minimum of two reflection lengths, each computed by noncrossing pairings. The proof gives O(L^3) word operations, O(L^2) storage and a shortest factorization. All 9,841 direct deletion controls, 36,558 exhaustive free-word and two-palindrome comparisons, and 36,698 independent GAP witness checks pass. Reflection deletion is credited to Dyer; the exact conversion and algorithm await broader novelty checks and outside review. See `research/16.9-proof.md` and `research/16.9-review.md`.

**15.89:** Twenty-second complete candidate: on G=C3*C2, the connection set {aba,aba^2,a^2ba,a^2ba^2} gives an infinite connected simple four-regular Cayley graph. Its adjacency operator U B U has inverse (U-I)B(U-I)/4 on all complex-valued functions, so zero is not an eigenvalue. Free-product Python and independent projective-matrix GAP checks pass, together with63,936 finite-matrix identity entries. The zig-zag construction is prior and credited; novelty of this consequence and outside review remain pending. See `research/15.89-proof.md` and `research/15.89-review.md`. The earlier positive dihedral subclass remains valid.

**21.107:** The countable group of finite subsets of N under symmetric
difference, with open subgroups consisting of the finite subsets of a
free ultrafilter member, has an explicit partition into countably many
dense sets. For any disjoint sequence of finite subsets of the group,
the finite-fiber maximum-support map gives an open subgroup missing
infinitely many terms. Thus no expansive sequence exists. The topology
is standard and credited; the proof uses only ZFC and also works for
the direct sum of copies of C3. See `research/21.107-proof.md` and its
internal audit. Novelty and outside review remain pending.

**4.55:** For G=3.A7 and p=5, the rationality condition on four modular projective multiplicities is a+d=b+c. Four distinct rays give projectives after multiplication by168 and rational descent; equal modular reductions give an isomorphism whose two sides have incompatible indecomposable refinements. The common rank is55,440. GAP independently reconstructs all12 faithful Brauer characters and14 decomposition rows from actual permutation modules; Python enumerates the7560-element matrix group and checks absolute irreducibility. See `research/4.55-proof.md` and `research/4.55-review.md`; novelty and outside review remain pending.

**21.60:** For G=C3 semidirect C4 with inversion action and p=2, both simple F2G-modules are reductions of simple rational modules. Thus every module class satisfies the proposed positive-combination condition. But Z_(2)G maps onto an order in a division quaternion algebra whose reduction is M2(F2), so nontrivial idempotents cannot lift and the ring is not semiperfect. All4,096 modular group-ring elements and52 idempotents are checked independently by Python and GAP; both projective indecomposables have dimension four. An invalid Ext-lifting step in the source proposition is explicitly audited. See `research/21.60-proof.md` and `research/21.60-review.md`; novelty and outside review remain pending.

**21.40:** Finitely many automorphism orbits give arbitrarily deep roots of a positive power of each element. A bounded-degree algebraic-integer argument forces every matrix eigenvalue to be a root of unity. The finite set of integer traces then gives a normal torsion-free nilpotent subgroup of class at most n-1 and index at most (2n+1)^(n^2). The proof is self-contained and covers infinitely generated groups. Exact Python and independent GAP controls pass, including the nonsoluble finite-orbit example A5 times Q. See `research/21.40-proof.md` and `research/21.40-review.md`; novelty and outside review remain pending.

**14.72:** An explicit smooth affine surface over C admits an order-four cyclic action whose entire fixed scheme is an affine line and a smooth Cartier divisor. Its invariant ring is exactly `C[a,v,d]/(v^2-(a-1)d)`, singular at `(1,0,0)`. The two points above that node have a proper order-two stabilizer, so they are outside the full fixed locus. Both affine charts and the all-degree invariant-ring computation are proved. Exact normal forms and independent GAP checks on 2,955 surface points and 817 orbits pass. See `research/14.72-proof.md` and `research/14.72-review.md`; novelty and outside review remain pending.

**11.116:** An explicit digit bijection turns every coset in a quasicyclic p-group into an integer interval. Subgroups of a product of quasicyclic groups at distinct primes split into primary factors, so their cosets become boxes. Every subgroup of a finite extension is encoded by its finitely many coset fibers. This gives order dimension at most2r[G:D], without a splitting assumption. All40,000 exact coset comparisons and242,344 actual GAP subgroup comparisons pass. Shevrin2012 states the converse as open and supplies the prior necessity direction. See `research/11.116-proof.md` and `research/11.116-review.md`; novelty and outside review remain pending.

**20.90:** The closure of two explicit matrices in SL2(F4[[t]]) is infinite, has abelian centralizers, and reduces onto A5. A separate four-generator example SL2(Z2[omega])/{I,-I} has centralizers which are abelian or pro-2. Both give the required non-prosoluble profinite CN-group. The matrix arguments are complete; independent GAP/Python checks pass, including252 algebra centralizers and all65,536 matrices over the mod-4 companion ring. The characteristic-two CA lemma is prior work, explicitly credited. See `research/20.90-proof.md`, `research/20.90-2adic-proof.md` and `research/20.90-review.md`; novelty and outside review remain pending.

**20.108(a),(b):** G=F_11^2 semidirect C5 with diagonal weights3,9 is centreless. Its full holomorph is determined explicitly, and theta(x,y,k)=(y,3^(-k)x,2k) normalizes it while theta^2 lies outside it. Hence T(G) contains C4. GAP identifies SmallGroup(605,5) and independently checks the full holomorph order; Python checks every invertible matrix and8,000 permutation cases. A general family gives unbounded element orders in these quotients, with5,939 additional basis checks. This was an explicit unresolved exception in Tsang's2025 paper. Part(c) is already affirmative by Caranti--Tsang2023; novelty of(a),(b) and outside review remain pending. See `research/20.108-proof.md` and `research/20.108-review.md`.

**21.106:** A parameter-free formula defines exactly the two central generators in the integral Heisenberg group, a residually finite group. Its value set is finite but generates an infinite subgroup. The self-contained proof and internal audit are in `research/21.106-proof.md` and `research/21.106-review.md`. Exact arithmetic and finite-quotient sanity checks passed; the infinite claim rests on the proof.

**21.132:** Starting from a graded Golod nil algebra, remove the homogeneous ideal of elements annihilated by a sufficiently high algebra power. A triangular extension has zero centre and preserves a grading with finite-dimensional pieces. Its three-generated adjoint subgroup is infinite, centreless, and residually a finite p-group. Adjoining a one-dimensional zero algebra gives a four-generated Golod group with centre C_p. Proof: `research/21.132-proof.md`; audit: `research/21.132-review.md`. The exact Notebook statement permits the final direct factor. The older centreless construction has been compared; broader novelty work remains.

**21.121(a):** A free product of central quotients of (Q_8 semidirect C_3) powers has 2-Jordan exponent log(24)/log(8), with no bound at the infimum. A binary simplex-code lemma controls every subgroup, giving a uniform bound for each larger exponent. Proof and audit: `research/21.121a-proof.md` and `research/21.121a-review.md`. Exact checks passed on all 11,781 subgroups of the second finite group, plus independent code and quaternion controls. Part (b) remains unresolved.

**21.68:** G=B semidirect K, where K=E semidirect A4 has order96 and contains H=Q8 semidirect C3 of index4. B is the three-dimensional F3 augmentation module on K/H. The explicit abelian extension chain makes G semi-abelian. A degree8 irreducible character would, if monomial, force an index2 subgroup in H, contradicting H_ab=C3. GAP and independent rational quaternion/cyclotomic computations pass. See `research/21.68-proof.md` and `research/21.68-review.md`.

**16.87(a),(b):** In the variety defined by central commutators of exponent dividing p, every relatively free group G_r has abelianization Z^r and central p-th powers of its generators. For any fewer than r selected elements, an epimorphism f:G_r -> Z vanishes on all of them. A suitable central c with f(c)>0 makes g -> g c^{f(g)} fix them exactly and fail to be onto. Thus test rank is r for every r, although the variety is nonabelian and contains Z. The proof is self-contained; exact substitution checks on 1,156 target sets passed. See `research/16.87-proof.md` and `research/16.87-review.md`.

**10.35:** The two-generator group generated by U(1) and diag(2i,2) is a torsion-free subgroup of GL_2(C), isomorphic to Z^2 semidirect Z with a quarter-turn action. In every rational two-dimensional representation the image of U(1) squares to the identity, by a two-dimensional centralizer-algebra argument. Thus U(2) is killed by every such representation. The elementary proof and internal audit are in `research/10.35-proof.md` and `research/10.35-review.md`; exact controls passed. The fixed degree in the printed question is essential, and novelty remains unconfirmed.

**16.28(a):** In SL_2 times G_m over an algebraic closure of F_5(t), take the union of the trace-one class at scalar coordinate one and the central point (I,t). Every power n>=2 has a closed scalar fiber equal to the nonclosed square of that class. Hence no such power is closed. The proof covers the exact printed field and subset assumptions and can also be placed in SL_4. GAP rational-function identities and independent finite matrix/word controls passed. Part (b) has a negative answer already implied by existing class-product results and is excluded from new coverage. See `research/16.28-proof.md` and `research/16.28-review.md`.

**14.22:** The rational coefficient group Q gives an irreducible one-variable line whose radical cannot be generated by any finite system as a normal isolated subgroup. Every finite system uses a cyclic coefficient subgroup C, and the torsion-free amalgam Q *_C (C x Z) separates a missing commutator with a rational root. A nonabelian version over Q * Z has an explicit faithful SL_2(Q(t)) representation and a polynomial specialization proof of irreducibility. Both coefficient groups are infinitely generated, permitted by the printed statement. Exact polynomial and normal-form controls pass; novelty and outside review remain pending. See `research/14.22-proof.md` and `research/14.22-review.md`.

**16.20:** A central quotient of SL_2(5) x SL_2(7) x SL_2(13), of order 44,029,440, gives an affirmative answer. Every normal subgroup R is the dominion of 1 for the quasivariety generated by A/R. Thus the entire family is the 15-element normal subgroup lattice, modular and containing a central M3. GAP independently constructed this group and checked the whole normal lattice. A seven-factor construction also realizes exactly M3 under the extra requirement A belongs to every target quasivariety. Its structural proof and exhaustive central-code controls pass. See `research/16.20-proof.md` and `research/16.20-review.md`; novelty and outside review remain pending.

**17.33:** For every n>=2, an explicit finitely presented torsion-free virtually abelian group Gamma_n has finite abelianization, so every map to the Klein bottle group K is trivial. Yet every subgroup generated by fewer than n elements embeds in a finite power of K. A finite presentation supplies a separating quasiidentity; therefore q(K) cannot have a basis with a bounded number of variables. The complete affine proof, internal audit, exact arithmetic controls, and independent GAP presentation checks pass. See `research/17.33-proof.md` and `research/17.33-review.md`. Novelty and outside review remain pending.

**17.101:** Every representation over any fixed commutative ring embeds in a homogeneous one. A multiple HNN group extends the group components of partial isomorphisms; a quotient of the induced module enforces their module components. A finite-support leaf argument on the Bass–Serre tree proves the original module survives. Iterating realizes all isomorphisms of finitely generated subrepresentations by inner pairs in the final union. The exact category and earlier stated obstruction were checked in the authors’ 2012 paper. Finite tree, cyclic-module, and independent GAP Laurent controls pass. See `research/17.101-proof.md` and `research/17.101-review.md`. Novelty and outside review remain pending.

**18.76:** A countable division ring containing k[F2 x F2] admits a nonsplit extension of its additive group by F2 x F2 with the prescribed multiplication action. Two explicit automorphisms build the extension; three commuting-lift equations force the fourth to assert 0=1. Exact finite-support group-ring controls in five characteristics and 27 independent GAP matrix models pass. The standard Mal'cev--Neumann input was checked in primary sources. See `research/18.76-proof.md` and `research/18.76-review.md`. Novelty and outside review remain pending.

**18.92(a),(b):** Let F_S be the formation of all finite groups whose prime divisors lie in S. Taking finite prime sets plus the set of all primes yields a complete lattice whose only compact element is its bottom. Five selected F_S give the non-modular pentagon N5. Both use internal joins in the chosen family, as explicitly defined in the Notebook and checked in a primary formation-theory source. All finite lattice controls pass; the infinite assertion has an explicit chain proof. See `research/18.92-proof.md` and `research/18.92-review.md`. Novelty and outside review remain pending.

## Completed bounded searches

- **20.30:** All2,750 CTblLib entries screened,340 perfect centreless entries, zero counterexamples. All nine actual-group conjugacy-orbit controls pass. General question unresolved; see `research/20.30-search.md`.
- **20.52:** All2,845 odd-order groups through1727 checked, including1,719 nonabelian groups. Every m<=64 occurs, with86 independent actual-group controls passing. This repeats a known existence range; Buckley--MacHale2013 already covers every m<=256. See `research/20.52-plan.md` and `research/20-later-triage.md`.

- **18.114:** All2,468 soluble irreducible library entries over F5 through dimension6 processed;2,421 eligible, including2,352 noncyclic. No noncyclic equality;57 independent affine controls and37 commuting-pair checks pass. The indexed affine-constructor cache bug was diagnosed; all initial invalid runs were excluded and replaced. See `research/18.114-plan.md`.

- **17.100:** All2,750 CTblLib tables screened;215 simple-table entries
  yield12,606 eligible character/class pairs, with no counterexample.
  All2,750 alternative simplicity checks and72 direct character checks
  on eight actual groups pass. See `research/17.100-search.md`.
- **18.20:** All33,810,661 unequal-degree pairs in2,750 ordinary tables
  checked, no counterexample. Exhaustive class-partition controls on
  ten actual groups agree on129 row pairs, including16 positive controls.
  See `research/18.20-search.md`.

- **16.95:** All invertible binary matrices through dimension6 covered modulo column permutations:28,082,408 unordered bases and50,718,594 cyclicity tests, no counterexample. All22,347 independent Krylov controls pass. Dixon2016 was explicitly withdrawn in2017; it does not resolve the problem. See `research/16.95-plan.md`.

- **16.14:** All58,760 groups of orders2,4,...,256 checked, with no counterexample. The rank bound holds in55,177; each of the other3,583 has an explicit noncentral involution. Every witness was replayed, and340 independent small controls pass. An elementary exponent-four subclass proof is in `research/16.14-exponent4.md`; the general question remains unresolved and no novelty claim is made.

- **21.99:** All 4,722 transitive groups of degrees 2–20 satisfy the conjecture: 4,631 orbital checks and 91 rank-two cases. Independent full-element verification agrees for all 86 groups of degrees 2–8.
- **21.113(a):** 2,750 ordinary character tables, 9,850 table/prime cases, no skips or counterexample. **21.113(b)** also completed: 7,573 available modular cases, 2,277 unavailable cases, no counterexample; all decomposition-matrix reconstruction checks passed.
- **21.59(a)/21.135:** 106 degree-multiset collisions among 2,750 tables, all between entries marked almost simple. Primed orthogonal/unitary entries were checked and are alternative table/fusion data. No nonisomorphic counterexample established. See `research/degree-collision-audit.md`.
- **21.52–53:** 27 group entries, 28 involution classes, one explicit size-cutoff skip, no counterexample. The strengthened run verifies actual group automorphisms on every involution, correcting an insufficient normalizer-only test. See `research/21.52-53-results.md`.
- **18.43:** All 3,933,931,043 positive necklaces of lengths 1–36 have distinct pairs of exact GL3 trace fingerprints within each length. No candidate identity found. Summary: `results/18.43-summary.json`. Independent Python checks cover enumeration and arithmetic through length 12 and recover a known GL2 identity. Any collision requires exact symbolic certification. GL3 and SL3 versions are equivalent by exponent sums and scalar normalization; this reduction is recorded in `research/18.43-plan.md`.

- **21.26:** All 309,429 checked groups satisfy the strict exact union bound. The full range through order 2000 is covered by these checks together with the known result for orders involving at most two primes. No fallback or counterexample occurred. Independent direct enumeration agrees for all 211 non-prime-power-order groups through order 60.

The index contains 1,308 main-body problem entries, all 150 Issue 21 entries. Editorial stars and later literature must be checked manually. Recent claimed resolutions of 20.21 and decidability in 21.32 are excluded from new-solution counts. Our alternate 21.32 argument is retained as a rediscovery.

## Verified result adjacent to 19.20

For G=(D8*D8) x C2 of order 64, |End(G)|=6,074,368 exceeds
|PIso(G)|=3,277,312. This disproves the stronger inequality asked in
Cameron's 2025 paper. The Notebook equality question remains unresolved.
A complete coordinate argument and independently verified finite counts
are in `research/19.20-stronger-counterexample.md`. The Python certificate
enumerates all 593 subgroups without GAP; a GAP central-product realization
gives the same totals. This is a separate partial result, not a complete
resolution of a Notebook problem.

The odd-order group E_(3,2) x C3^2 of order 2,187 also reverses the
stronger inequality: End = 8,241,952,876,767,369 and
PIso = 2,607,970,224,105,603. Closed formulas for odd-exponent extraspecial
groups with elementary abelian direct factors are proved in
`research/19.20-odd-extraspecial.md`. GAP independently counted all
134,414 subgroups of this example and matched every type multiplicity
and automorphism order. Five smaller controls also agree. None of the
60 evaluated parameter triples gives equality.

## Additional constructions and exclusions

**11.124:** Tursunbaev, arXiv2609.06755v1, submitted6September2026, gives an exact prior affirmative claim. The full preprint was read; imported classical inputs and outside review remain pending. Excluded from new priority; see `research/11.124-prior-claim.md`.

**7.31:** Li--Zhu2024 Theorem1.1 gives the affirmative answer, including
the full automorphism group. The exact statement and its Section3 proof
were read; the representation and classification inputs remain unaudited.
Excluded from new priority; see `research/7.31-known-resolution.md`.

**15.36:** Shakhova2018 explicitly states the exact negative answer: some
finite G have L(qG) of infinite axiomatic rank. The primary publisher
abstract and the printed question were checked; the full proof remains
unaudited. Excluded from new-result priority; see
`research/15.36-prior-claim.md`.

**12.56:** The classical rigidity theorem for right-angled Artin groups gives an elementary graph-counting lower bound, proving `F(n)=n^(Theta(n))` in the printed presentation-length convention. Explicitly, `(n/4)log n-(n/2)log log n-O(n) <= log F(n) <= n log n+O(n)`. This is a quantitative partial answer, with novelty unestablished and no additional complete candidate. See `research/12.56-growth-bounds.md` and `research/12.56-review.md`.

**13.12:** Carette Theorem 6.3 (2011, corrected preprint 2010) already proves that every hyperbolic group has finitely presented automorphism group. Exact theorem and its proof read; excluded from new priority. See `research/13.12-known-resolution.md`.

**20.100 partial results:** A positive-length argument proves the assertion
for every torsion-free group, without commutativity or unique roots. The
general conjecture at each fixed n reduces to finite abelian groups, with
counterexample order bounded by p_n*n^(n-1). Exact
finite certificates now prove the all-group cases n=4,5,6: independent GAP
Smith-normal-form checks verify227,10,493 and265,104 nodes, with a total
of19,524,681 relation implications. The earlier n=7 continuation stopped with26,317,076 closed nodes, preserved as an audited incomplete gzip. The08:40 UTC continuation has completed42,891,332 nodes and exited zero. Six independent GAP workers are checking the complete certificate; all must pass before n=7 is a proof. The full arbitrary-n
conjecture and novelty remain open. See `research/20.100-reduction.md` and
`research/20.100-review.md`; complete-candidate count is22 from the separately resolved entries.

**20.108(c):** Caranti--Tsang2023 Theorem1.1 already gives a group of order3^10 with GL4(3) inside T(G), hence prime divisor5 outside p(p-1)=6. Prior affirmative result, excluded from new priority; see `research/20.108c-known-consequence.md`. This corrects our earlier provisional status for(c).

**20.33:** Complete affirmative consequence of effective HNN embeddings. An explicit three-generator X-c.e.-presented universal group contains every finitely generated X-c.e.-presented group. Both directions, presentation elimination and the absence of any extra oracle are proved. Mikaelian's prior theorem improves the generator bound to two. Excluded from new priority; see `research/20.33-known-consequence.md` and `research/20.33-review.md`.

**20.8:** Complete negative deduction using Lei--Zhang's2026 three-generator equalizer construction. An explicit K<H<F has ranks4,3,2 and a nonidentity map H->F fixing K. All five vertex partitions of K's core graph prove that every proper intermediate subgroup has rank at least4. Independent Python and GAP rank/folding controls and457 word controls pass. Credited prior construction; excluded from thenew-priority count. See `research/20.8-known-consequence.md` and `research/20.8-11-review.md`.

**20.11:** All four assertions follow from Jaikin-Zapirain's subgroup-rigidity corollaries. Explicit chain-union and descending-intersection arguments cover infinitely generated F and arbitrary-rank H as permitted by the printed statement. Complete prior-theorem deductions, excluded from new priority. See `research/20.11-known-consequence.md` and the shared review.

**19.108 partial theorem:** For every odd prime p, the support-order divisibility holds for groups of order p^10 having an abelian normal subgroup of order at least p^6. An elementary orbit lemma proves the extension beyond Wilde's prior bounds; nonsplit extensions are included. The p=3 screen covers 571 subgroup classes and 1,596 regular orbits, with independent integer replay, 174,312 exact Fourier sums and nine actual character controls. The full question remains unresolved; no novelty claim or extra complete-candidate count. See `research/19.108-partial.md` and `research/19.108-review.md`.

**19.9(a),(b):** Complete deductions from prior theorems: Sp(10,Z) has a non-residually-finite universal central extension, so its finitely generated tensor square is nonlinear; every B_n tensor B_n, n>=4, embeds in GL_(1+n(n-1)/2+2^n)(Q(q,t)) using its Clifford-detected Hopf kernel. Exact rational controls and26 independent GAP spin-matrix cases pass. The deductions are retained as prior-theorem consequences and excluded from thenew-priority count; no earlier explicit tensor-square answer or novelty is asserted. See `research/19.9-proof.md` and `research/19.9-review.md`.


**18.111:** Frigerio--Sisto2023 Theorem1.2 gives the exact prior negative answer with a finitely generated example. Introductory statement and conventions read; full proof unaudited. See `research/18.111-known-resolution.md`; excluded from new-result priority.

**18.18:** A common-centralizer interpretation proves that the cofinite
theory of finite groups is not computably enumerable. The question
about its complement remains unresolved here. Partial result only,
with no novelty claim; see `research/18.18-partial.md`.

**17.124:** Jayadevan's9 September2026 preprint arXiv:2609.10281v1
claims the exact affirmative enumeration theorem. Theorem1.1 and early
sections read; remaining proof and Lean formalization unaudited.
Excluded from new-result priority; see `research/17.124-prior-claim.md`.

**18.44:** Jones--Keller2020 Theorem1.2 explicitly resolves the question
affirmatively. Primary introduction and theorem read; full proof
unaudited. Excluded from new-result priority; see
`research/18.44-known-resolution.md`.

**16.60:** The full affirmative answer is stated in Yerrapati--Dixit--Shukla, arXiv:2605.23195v1, Theorem3.1. A direct tensor-projection argument verifies the bound and repairs an unjustified scalar Cauchy--Schwarz step in the source. Excluded from new coverage; see `research/16.60-known-consequence.md` for exact reading scope.

**17.25(b):** Kim--Koberda, arXiv:1901.06375v4, Theorem1.4(1), already gives27/7 in the required interval. Excluded from new coverage; part(a) remains unresolved here. Full computational proof unaudited; see `research/17.25b-known-consequence.md`.



**11.46(a):** The August 2026 preprint https://arxiv.org/abs/2608.07275v1 claims a finite E-group of class three. Its primary abstract was read, but the full proof was not audited. Excluded from new-target priority; no independent verification is claimed.


**17.34:** A positive answer follows from the existing fixed-class strong amalgamation theorem of d’Elbée--Müller--Ramsey--Siniora, Theorem 4.35 of arXiv:2310.17595v3. Give the divisible subgroup the induced filtration, take a strong self-amalgam, and apply Malcev/BCH; compactness covers arbitrary rank. The full inference is in `research/17.34-known-consequence.md`. Our independently developed PBW module proof and its 13 exact controls are retained, but this problem is excluded from the new-candidate count. This corrects its brief provisional inclusion.

**21.42:** A negative answer follows from the existing positive-grading
theorem of Dekimpe--Igodt--Pouseele (2003) and Mathieu's self-similarity
criterion (2021). The necessary implications and a self-contained
rediscovery of the grading argument are documented in
`research/21.42-known-consequence.md`. This literature consequence is
kept separate from the complete candidate resolutions.


**21.115:** A September 8 preprint by Sambale resolves the coset-union
problem in full: https://arxiv.org/abs/2609.09052v1 . Its finite-group
argument has been checked. Our abelian and odd-derived class-two
arguments are retained as special-case rediscoveries; the prepared
finite search is archived. See `research/21.115-literature-audit.md`.

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
2. Continue novelty and mathematical audits of all forty-three candidate resolutions.
3. Investigate 19.20 equality beyond the completed range, using the verified reverse inequality as a structural lead.
4. Expand beyond the initial involution graph range and continue surveying older problems.

Deadline: **2026-09-12 20:56:46 UTC**. The 48-hour goal remains active. No external messages, submissions, or Git pushes have been made.
