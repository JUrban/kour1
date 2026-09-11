# Current status

Updated: 2026-09-11T10:13:21.687327+00:00.

- Active phase: proof audit, exact searches, and broader problem triage.
- Complete candidate resolutions: **21**: **21.106** (negative), **21.132** (construction for every prime), **21.121(a)** (infimum not attained at p=2), **21.68** (semi-abelian non-monomial group of order2592), **16.87(a),(b)** (nonabelian, nonperiodic variety with maximal test rank at every finite rank), **10.35** (torsion-free complex matrix group not residually rational in the same degree), **16.28(a)** (a closed set with every power greater than one nonclosed), **14.22** (failure of finite isolated-radical presentation over infinitely generated torsion-free linear coefficient groups), **16.20** (a finite modular nondistributive dominion lattice), **17.33** (infinite axiomatic rank of the Klein bottle quasivariety), **17.101** (every group representation has a homogeneous extension), **18.76** (a nonsplit additive division-ring extension), **18.92(a),(b)** (non-algebraic and non-modular complete lattices of formations), **20.108(a),(b)** (a centreless group of order605 whose multiple-holomorph quotient contains an element of order4), **20.90** (a two-generator infinite profinite CA-group mapping onto A5), **11.116** (finite subgroup-lattice dimension for the stated Chernikov groups), **14.72** (a smooth affine surface with a smooth fixed Cartier divisor but singular cyclic quotient), **21.40** (a normal nilpotent subgroup of finite index in every rational linear group with finitely many automorphism orbits), **21.60** (an order-twelve counterexample to the semiperfectness criterion), **4.55** (non-unique indecomposable projective decompositions over Z_(5)[3.A7]), and **21.107** (a countable resolvable group without an expansive sequence). All await outside review and further novelty checks.
- Externally reviewed new solutions: 0.
- Latest prior-result audit: 5.15 (affirmative), 12.11 (negative), and 13.39(f) (negative in rank at least two) follow from published theorems; detailed deductions are saved and excluded from new priority. An exact August prior claim for 11.46(a) and further known ranges for 8.3 are also recorded.
- The 21.26 search through order2000 and the 19.20 search through order256 are complete. Exact ID coverage and all completion records pass.
- **19.20 complete:** all62,588 nonabelian groups through order256, zero equality hits and411 reverse inequalities. The order256 extension covers56,070 nonabelian groups and has357 reversals; the22 omitted abelian IDs were independently reconstructed and matched exactly. The initial493 abelian equality controls remain retained. The arbitrary-group equality question is unresolved.
- **19.20 extension active:** orders257–511 have29,700 library groups. At10:12 UTC, eight verified GAP workers have completed348 of356 jobs, with28,081 nonabelian counts,511 abelian skips, zero equalities and33 reversals. All log checks pass. The run remains incomplete.
- **20.100 n=7 active:** the saved26,317,076-node prefix has loaded and generation has resumed. At10:12 UTC the generator has reached35,160,000 visited states, using about19.5GiB; no n=7 proof is claimed.
- **4.55 exploratory screen complete:** all2,750 installed table names and7,573 available modular cases are covered by two disjoint audited ranges. Flags remain exploratory; the separate3.A7 proof supplies the candidate resolution.
- GAP 4.16.1 and SmallGrp, TransGrp, CTblLib, Digraphs 1.15.0, and GRAPE work. `bin/gap` is the reproducible launcher.
- **14.2 restricted searches complete:** 16,146,897 rational pairs give682 integral swaps, all monomial;21,646 degree-changing permutations in249 individual conductor blocks give no integral maps. Independent matrix and actual-group controls pass. General question unresolved.

## Candidate proofs

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
of19,524,681 relation implications. The n=7 continuation stopped at its time bound with26,317,076 closed nodes, preserved and fully read as an incomplete gzip. A further continuation started at08:40 UTC with a60-million-state /18,000-second bound and is loading that prefix. The full arbitrary-n
conjecture and novelty remain open. See `research/20.100-reduction.md` and
`research/20.100-review.md`; complete-candidate count is20 from the separately resolved entries.

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

**15.89:** Proved the positive infinite-dihedral Cayley subclass by an exact Laurent-polynomial coefficient argument. All complex values occur as adjacency eigenvalues on unrestricted functions, for every finite inverse-closed generating set. The general vertex-transitive problem remains unresolved. Search and independent controls pass; no novelty claim is made. See `research/15.89-dihedral.md`.

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
2. Continue novelty and mathematical audits of all twenty-one candidate resolutions.
3. Investigate 19.20 equality beyond the completed range, using the verified reverse inequality as a structural lead.
4. Expand beyond the initial involution graph range and continue surveying older problems.

Deadline: **2026-09-12 20:56:46 UTC**. The 48-hour goal remains active. No external messages, submissions, or Git pushes have been made.
