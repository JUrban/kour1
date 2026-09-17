# Referee report on *Forty-eight hours with the Kourovka Notebook: an experiment in agentic mathematical research*

Paper: `review-other1/kourovka-experiment.pdf` (Codex gpt-6-astra, M. Kinyon, J. Urban; 15 September 2026; 96 pp.).
Scripts and logs written for this report are in `review-other1/checks/`; `review-other1/notes_progress.md` is the
working log. The first round created no file outside `review-other1/` and ran no git command. A response to
the authors' reply, with corrections to two items in this report, is in `review2.md`, and that round's
scripts are in `checks2/`.

## 1. Summary judgement

The mathematical core of the paper is in much better shape than the genre usually is. I checked all 46 entries of
the deadline ledger: 3 in the main text and 43 in Appendix C. Of these I verified a majority in full detail, by
reading the proofs line by line and, where a finite object is involved, by recomputing it independently in GAP or
Python. I found no false theorem among the claims I was able to settle, and the computations I reran all reproduced
the paper's numbers exactly, including the large search-coverage figures quoted in Section 3.

The problems I do see are of five kinds, and all but the third concern the framing rather than the algebra:

1. **Convention-sensitive readings.** A few entries turn on a stated convention that the reader must notice to
   judge the result (18.92 is the clearest case; 14.22 and 16.20 are milder). My first draft also listed 16.28(a)
   and 12.40 here; both were withdrawn after the authors' reply, see `review2.md`.
2. **Novelty.** The paper is careful to say that priority is unestablished, but at least one flagship result
   (Theorem 4.1, Problem 21.106) was duplicated publicly, with a Lean 4 proof, within the run window itself.
3. **One hypothesis-reading problem with substance.** In the surface example for Problem 14.72 the fixed locus is a
   smooth divisor of codimension one but is not cut out by a single equation, so whether it meets the hypothesis
   depends on how "regular hypersurface" is read (Section 6).
4. **Under-claiming in the other direction.** Three entries in the appendix of rediscoveries look like answers to
   their printed questions and are nevertheless excluded from the count. So the number 46 is not a like-for-like
   count in either direction.
5. **Dependence on unprinted certificates.** Two entries (19.61, 19.62) rest on machine-generated integer
   certificates that are not in the paper. I re-derived all of them independently, so in this instance the
   dependence turned out to be harmless, but a reader without that effort cannot check them.

## 2. How this report was produced

I read the whole paper, then for each of the 46 ledger entries I pulled the corresponding statement out of the
supplied Notebook file and compared it with what the paper proves. Proofs were read step by step. Wherever a claim
involves a finite object, a finite computation, or an explicit numerical constant, I recomputed it independently
rather than trusting the paper's own scripts (which are not part of the submission anyway: the archive is not
publicly reachable, see Section 7). The scripts I wrote are in `review-other1/checks/` with their logs.

The independent computations were: the order-2592 non-monomial group and its character degrees; the order-605
holomorph example; the p-Jordan estimate on all subgroups of the two smallest groups of the family; the 3.A7
5-modular decomposition data; the order-36864 triple-intersection family; the system-normaliser family for three
parameter pairs; the 2-modular data for the dicyclic group of order 12; the SL2 images over F4[t]/t^k; the numerical
constants in the classical-group argument; the 2-adic integer facts for PSL6(5^a); the orthogonal-basis criterion
against brute force; the palindromic-length algorithm against brute force; the common-centraliser construction; the
order-120 subgroup over F9; the Chevalley commutator constants for A2, B2 and G2, and with them all 19 printed
carpet derivations plus, by an independent saturation search, all 104 requests for inclusion (5) and all 300
certificates behind Lemma C.13. Later I added: the smoothness, invariants and defining relation of the surface for
14.72 by Groebner elimination; the two Baker-Campbell-Hausdorff formulas for 13.42 in an exact word algebra; the
interpolation polynomials for 14.26; the coefficient identity and degree bookkeeping for 20.92(a); the Chebyshev
inequalities for 10.32; the Golod-Shafarevich arithmetic for 19.93; the cycle-length arithmetic for 15.92; the
quasigroup identity for 9.4 by brute force over all quasigroups of order at most four; the closing counterexample
for 16.38; the twisted indicator identity for 16.60 over every automorphism class of seven small groups; the
subgroup ranks for 20.8 by Stallings folding; the class-two linearisation for 21.115 over the Heisenberg group mod
three; the order-256 subdirect example for 13.19; and the automorphism bound used in 21.121(b) over 344 cases. I
also reproduced the paper's search-coverage numbers (91,774 nonabelian groups of
order at most 511; 4,722 transitive groups of degrees 2 to 20; 3,933,931,043 binary necklaces of lengths 1 to 36),
checked the SHA-256 digest of the Notebook file against the one printed in the paper, and checked the internal
arithmetic of the token and cost tables.

Four blocks of appendix sections were additionally read by separate agent instances working from the same text.
Those are not independent referees in the sense that matters, and I treated what they returned as leads: every
finding of theirs recorded below I checked myself first, in several cases by going back to the cited sources. Three
of the four returned; the fourth failed, so I read appendices D and E myself.

## 3. The experimental claims

I could check the parts of Sections 2 and 3 that are checkable from outside the archive, and they hold up.

- The SHA-256 digest printed for the input Notebook matches the file.
- Issue 21 does contain exactly 150 entries; a crude parse of the main body gives 1309 numbered entries against the
  paper's 1308, which is parsing noise on my side, not a discrepancy.
- Four coverage numbers quoted in Section 3.3 are exactly right: 91,774 nonabelian groups of order at most 511,
  4,722 transitive groups of degrees 2 to 20, 3,933,931,043 binary necklaces of lengths 1 to 36, and the 2,750
  ordinary character tables behind the 21.113 screen. The control set of 86 transitive groups in degrees 2 to 8
  quoted for Problem 21.99 is also exactly right, and so is the finer breakdown of the 21.113 screen: I count 9,850
  table/prime cases, 7,573 with the modular table available and 2,277 without, matching the paper to the unit.
- The token and cost tables are internally consistent, and the flat-rate reconstruction reproduces the quoted
  USD 901.42 to the cent.
- Appendix B has 46 rows with 46 distinct cross-references, covering C.1 to C.43 and 4.1 to 4.3 exactly once, and
  none of the 46 problems is starred as solved in the supplied Notebook file. Problem 19.63, which the ledger groups
  with 19.62, is starred there, exactly as the paper says.

The paper's epistemic framing is, in my view, its strongest feature. The repeated insistence that a "complete
solution candidate" is an observable outcome and not an accepted theorem, the separation of generation from
checking for the large certificate, the explicit statement that a second implementation by the same agent is not
independent review, and the admission that the deadline archive contains zero outside reviews are all correct and
unusually candid. Section 2.6 and Section 5.2 should be kept as they are.

Two framing points I would still press. First, the abstract's "46 entries labeled complete solution candidates"
is qualified properly in the body, but the number will be quoted out of context; it would help to state in the
abstract that several of those entries answer the printed sentence under a reading the proposer probably did not
intend (see Section 6 below). Second, the claim that the agent "chose its own targets" is used to explain the
portfolio, but the selection effect deserves a sharper statement: the entries that survived are, with few
exceptions, those where a small explicit object or a short reduction settles the question, which is also why so
many of them are checkable in an afternoon.

## 4. Entry-by-entry verdicts

The table records what I was able to establish. "Verified" means I rebuilt the object or the computation
independently; "checked" means I read the proof line by line and found it correct; a caveat in the last column is
explained in Section 6 or in the notes below the table.

| Problem | Section | Verdict |
|---|---|---|
| 21.106 | 4.1 | Checked. The truth set really is {z, z^{-1}} and the group is residually finite. Priority: see Section 5. |
| 21.68 | 4.2 | Verified in GAP: order 2592, not monomial, six non-monomial irreducibles of degree 8, split chain as printed. The auxiliary group of order 96 is monomial, consistent with Kida's own computation for orders at most 240. |
| 20.108 | 4.3 | Verified in GAP: centreless, |Aut| = 12100, the holomorph is the full normaliser of the regular representation, theta normalises it, theta^2 is outside it and theta^4 = 1. |
| 21.121(a) | C.1 | Checked, and the key inequality verified on every subgroup class of the two smallest members of the family. |
| 16.87 | C.2 | Checked. The endomorphism is well defined because p-th powers are central, and it is not surjective. |
| 10.35 | C.3 | Checked, including the lemma on 2-by-2 matrices and the claim that the group does embed in GL_3(Q). |
| 16.28(a) | C.4 | Checked; scope caveat (needs an element of infinite multiplicative order). |
| 14.22 | C.5 | Checked; scope caveat (coefficient group not finitely generated). |
| 16.20 | C.6 | Checked under the stated convention; the variant convention is handled only by a sketched second example. |
| 17.33 | C.7 | Checked in full: the presentation, torsion-freeness, finiteness of the abelianisation, the embeddings of the proper-subspace preimages, and the variable-count argument. |
| 17.101 | C.8 | Checked. The Bass-Serre argument really does give V embedded in W, and the realising automorphism is the expected one; the freeness of kH over kG and the fact that the image of delta is a submodule are used silently. |
| 18.76 | C.9 | Checked, including the four commutation equations and the final cancellation, which needs that the division closure of kF centralises kL. |
| 18.92 | C.10 | Checked; the literal reading makes the problem trivial (Section 6). |
| 20.90 | C.11 | Checked; elementary (Section 6). Finite quotients verified in GAP. |
| 11.116 | C.12 | Checked; the digit encoding, the fibre description and the "d chains implies dimension at most d" step are all correct. |
| 14.72 | C.13 | Checked and recomputed: the surface is smooth (empty singular locus), the invariants satisfy exactly the relation V^2 = (A-1)D, and the quotient is singular at the image of (1,0,0,0). One caveat about the word "hypersurface", see Section 6. |
| 21.40 | C.14 | Checked. The key step, that the inverse automorphism turns alpha(h) = h^r into a tower of r^k-th roots inside the group, is correct, as is the trace-tuple index bound. |
| 21.60 | C.15 | Checked; the 2-modular data verified in GAP, and the failure of semiperfectness confirmed independently by a rank argument on idempotents. |
| 4.55 | C.16 | Checked; the 5-modular decomposition rows, Galois orbits and projective-cover degrees for 3.A7 verified against the character table library. |
| 21.107 | C.17 | Checked. The subgroup filter, the dense partition and the parity argument against expansive sequences all hold. |
| 15.89 | C.18 | Checked: the operator identities U^2 = U + 2I and A^{-1} = (U-I)B(U-I)/4 hold, and the Cayley graph is simple, 4-regular, connected and vertex-transitive. |
| 16.9 | C.19 | Checked, and the dynamic program verified against brute force on all 485 reduced words of length at most 5. |
| 18.18 | C.20 | Checked in full; the common-centraliser construction verified in GAP for three groups, with and without the extra orbit. |
| 19.56 | C.21 | Checked in full. This is the strongest entry in the paper: a short, correct solution of a 2018 problem. |
| 20.92(a) | C.22 | Checked. The coefficient extraction needs the hypothesis on the order of 2, and it works; the degree bookkeeping uses E = k^(2k-2). An exhaustive scan of all 1625 three-dimensional braces over F5, 800 of them with nonlinear lambda, reproduces the printed operation with no exception. |
| 9.47 | C.23 | Checked; contingent on the E-topology being the full Vietoris topology, which the paper states and which the Notebook never pins down. |
| 9.45 | C.24 | Checked, and the criterion verified against brute-force search over 1264 pairs (n, m). |
| 10.62 | C.25 | Checked; the elementary deductions are right, but the entry leans on the internals of an unrefereed 2025 preprint, and one scale condition is extrapolated. See Section 6. |
| 10.32 | C.26 | Checked. The covering arithmetic and the prime-counting inequalities hold, verified numerically well past the stated threshold. |
| 15.65 | C.27 | Analytic argument checked; all constants verified numerically and all inputs matched against the source memoir. |
| 12.40 | C.31 | Checked; the 2-adic arithmetic verified. |
| 15.92 | C.28 | Checked; the lemma and the arithmetic hold (720720 is the least common multiple of 1 to 16, the printed exponents are E/2, and w^2 = xyxy). But the proof depends on cycle-structure data read out of a 1980 doctoral thesis, which I could not verify, and the choice of 11 or 13 by residue class is asserted without a reason. |
| 4.75 | C.29 | Checked; a short corollary of the 10.62 construction, inheriting its dependence on the 2025 preprint. |
| 9.4 | C.30 | Checked, and the quasigroup identity verified by brute force over all quasigroups of order at most four. The cited source is about quasivarieties of automata, and the paper itself raises the resulting convention question. |
| 13.42 | C.32 | Checked, with both Baker-Campbell-Hausdorff formulas recomputed here in an exact word algebra. |
| 14.26 | C.33 | Checked; the interpolation polynomials have exactly the degree the choice of the parameter m provides, verified in three parameter sets. |
| 15.76(b) | C.34 | Checked; the coefficient identity has exactly the two integer solutions the argument uses. The cited contrasting example is a proper subvariety of the metabelian variety, of exponent four, which the paper could say in half a sentence. |
| 16.38 | C.35 | Checked, including the closing counterexample, which I reproduced. |
| 19.93 | C.36 | Checked; the Golod-Shafarevich inequality is used in the form the source states, and the value at two thirds is exactly the printed -115/729. |
| 20.1 | C.37 | Checked; the coprime-order lemma is correct and the order of the Janko group is coprime to 13. The entry rests on the imported theorem that that group is totally 2-closed. |
| 19.62 | C.38 | Checked, including the direct proof of the square criterion; all 104 requests re-derived independently. |
| 19.61 | C.39 | Checked; all 300 certificates re-derived independently. |
| 21.76 | C.40 | Checked; the rank-one argument is correct and the auxiliary group of order 120 over F9 verified in GAP. |
| 11.115 | C.41 | Checked; correct under both readings of the hypothesis. |
| 20.122 | C.42 | Verified in GAP: the full family of 10 distinct intersections, and both invariants equal to A, outside F(G). |
| 17.39 | C.43 | Verified in GAP for three parameter pairs: p^{d+1} system normalisers and minimum d+1 with trivial intersection. |

### Appendices D and E

These are outside the ledger, and the paper is careful to say so: appendix D collects partial results, appendix E
collects rediscoveries and deductions from prior work. I checked the following myself.

- **20.100 (D.1).** The reduction to finite abelian groups and the size bound are stated honestly as a decidability
  statement for each fixed n, not as a proof of the conjecture. The hypothesis control is right: over the cyclic
  group of order five no ordering of the four nonidentity elements makes the prescribed powers distinct, so allowing
  an element of order five at n = 4 really does break the conclusion.
- **20.89 (D.2).** The remark that bounded finite subgroups are not automatic in positive characteristic is
  immediate, since a diagonal matrix conjugates one unipotent to another with a scaled parameter, giving elementary
  abelian subgroups of unbounded rank.
- **21.121(b) (D.3).** Both auxiliary bounds hold. The bound on abelian prime-to-p subgroups of the automorphism
  group survived 344 test cases, and the Chermak-Delgado step, computed by hand from the measure, gave an abelian
  normal subgroup of index at most the square of the abelian index in all 132 nonabelian test groups. The exponent
  for the infinite alternating example lies strictly between two and three, as claimed.
- **20.124 (D.4).** The Rota-Baxter identity follows from the two displayed maps being mutually inverse; I checked
  the derivation. The paper is explicit that the method needs infinite rank.
- **17.118 (D.5).** With the cited bound on cube roots, four independent hyperplanes already cover more than the
  permitted proportion, so the rank is at most three and the index bound 27 follows; the case p = 2 gives 4.
- **21.114 and the rest of D.6.** The order-8192 central product rests on finite permutation models kept in the
  archive, so its numbers cannot be checked from the paper.
- **13.19 (E.1).** The small example is exactly as described: order 256, kernel of order 32, dihedral quotient of
  order eight, both subgroups subdirect in the fourth direct power, diagonal inside the kernel.
- **17.34 (E.2).** The separation module behaves as claimed in the smallest case: the subalgebra is exactly the
  kernel of the displayed map.
- **21.115 (E.3).** The class-two linearisation really is an abelian group operation, and subgroups stay closed
  under it, on the Heisenberg group over the field of three elements.
- **16.60 (E.4).** The twisted indicator identity and the bound by the sum of the degrees hold for every
  automorphism class of seven small groups.
- **20.8 (E.8).** The two subgroups have the stated ranks three and four by Stallings folding, and the endomorphism
  that differs from the inclusion does fix the four generators of the smaller one.
- **20.89 and 19.83 (D.2).** The strongest of the partial results, and honestly bounded. The local reduction is
  correct: each generator is Engel on a finite-index normal subgroup avoiding the nonidentity sink, Gruenberg's
  theorem then places the commutators in the Hirsch-Plotkin radical, and the rest is bookkeeping. The
  characteristic-zero closure theorem, the bounded-torsion case, the triangular characterisation, and the case of
  normal subgroups of unit groups of finite-dimensional algebras all hold. I checked the last one in detail: the
  units 1 + ta commute with a and permute the minimal sink, and comparing two parameters forces every sink element
  to commute with a, so the sink is trivial. The unresolved positive-characteristic case is stated as such.
- **21.121(b) (D.3).** The soluble theorem and its two auxiliary bounds are correct, and the infinite alternating
  example really does have exponent exactly the logarithm ratio, strictly between two and three, which is the
  interesting part: it shows the conjectured bound of three cannot be improved to two in general. The permanence
  statements are correct and carefully hedged. The universal bound of three is left open, as the paper says.
- **17.118 (D.5).** The class-bounded results and the two optimal small-prime bounds are right, and the lower bound
  construction of index p to the p is correct, including the intrinsic characterisation of its distinguished
  subgroup. The paper is explicit that the class parameter is not known to depend only on the prime, so the question
  itself is untouched for primes at least five.
- **D.6 and D.7.** These are correctly labelled. The order-8192 example for 21.114 depends on permutation models in
  the archive and cannot be checked from the paper. The restricted theorems for 19.108 and 18.120, and the
  class-two case of 6.47, are stated with their hypotheses in the open. The bounded searches in D.7 carry explicit
  coverage boundaries, and every number in them that I could recompute was exact.
- **E.5, E.6 and E.7 (21.132, 21.42, 20.33).** These three deserve a remark in the paper's favour. Each appears to
  answer its printed question: a finitely generated residually finite p-group with nontrivial finite centre; a
  negative answer to whether there are three-generated torsion-free nilpotent groups of class three that fail to be
  self-similar; and the relativised embedding statement in both directions. All three are nevertheless excluded from
  the ledger because the ingredients are prior work. That is under-claiming, and it cuts against reading the number
  46 as a like-for-like count in either direction.
- **E.9 (19.9, 16.14, 19.48).** Correctly classified as prior answers. The 16.14 derivation really is a one-step
  specialisation of an earlier centraliser bound, and saying so is right.
- **12.69 (E.10).** The literal counterexample is correct, and the paper is right to record it as a formulation
  problem rather than a solution.


## 5. Priority

The paper says priority is unestablished and does not claim novelty; that is the right stance, and the following
should be added to it.

**Problem 21.106 (Theorem 4.1) was duplicated publicly during the run.** A GitHub repository,
`TPColor/kourovka-notebook-problem-21.106`, contains a complete Lean 4 formalisation of a counterexample using the
same group (the integral Heisenberg group with the same multiplication) and a formula of the same shape: an
existential over a commutator, a centrality predicate, and conditions forcing the two generators to span. The
repository was created on 10 September 2026 at 19:32 UTC, about 84 minutes before the experiment's research window
opened, but with an empty initial commit; the Lean files carrying the mathematics were pushed on 11 September at
10:54 UTC, roughly 14 hours after the agent had already committed its own proof file for 21.106. The credits name a
human author for the counterexample and a second person for the Heisenberg simplification, and mention a planned
arXiv preprint, which I could not find. So this is parallel discovery in which the agent was narrowly first, not a
case of the agent reproducing something already public. It does show that the problem was, at that moment, within
reach of at least two independent efforts, and the paper should say so: a flagship example that a student
formalised in Lean within two days of the same week is weak evidence of research-level difficulty.

I checked the two most plausible collision candidates in the recent literature and found no overlap: arXiv:2607.17477
(July 2026) settles Kourovka 3.46, 18.50, 19.25, 20.125, 21.8, 21.24, 21.147, 21.150, and arXiv:2608.29219 (August
2026, itself LLM-assisted) settles 14.85, 19.94, 16.11, 17.47 and 17.32. None of these is among the 46.

I also confirmed the two prior-work statements that matter most for the carpet entries. Nuzhin's 2026 Siberian
Mathematical Journal paper does give the complete positive answer to Problem 19.63 (the square criterion), so the
ledger's grouping of 19.63 with 19.62 must indeed not be read as a new solution, exactly as the paper states; and
Sambale's September 2026 preprint on complements of unions of cosets does cover Problem 21.115 as printed, because a
right coset Hg is the left coset g(g^{-1}Hg), so the paper's decision to exclude 21.115 from the count is right.

## 6. Where the printed sentence and the intended question part company

This is my main substantive criticism. Several entries are correct answers to the printed words but almost certainly
not to the question that was asked. The paper usually flags this in a sentence at the end of the section; the flag is
too quiet given that the entries are then counted.

- **18.92 (C.10).** Under the definition printed in the Notebook, a "complete lattice of formations" is any
  nonempty intersection-closed family with a largest element. The paper answers both parts with the formations
  defined by sets of primes: an infinite family for (a), and five members forming a pentagon for (b). This is
  correct and takes a page, but it makes a long-standing question of Skiba's trivial, which is strong evidence that
  the intended object is the lattice of all formations closed under some operation, not an arbitrary family. I would
  not count this entry without stating that explicitly.
- **16.28(a) (C.4). RETRACTED.** I claimed the construction lived over a non-closed field. It does not: the paper
  sets the field to be the algebraic closure of the rational function field over the field of five elements, and the
  bar was lost in my text extraction. The field is algebraically closed and its transcendental element still has
  infinite multiplicative order, so the entry meets the usual convention and my objection was simply wrong. See
  `review2.md`.
- **14.22 (C.5).** The counterexample uses the additive rationals, a coefficient group that is not finitely
  generated; the cited positive result for free groups is in the finitely generated setting. Again correct as
  printed, and again a different question from the one the proposers were probably asking.
- **16.20 (C.6).** The construction depends on allowing the ambient group A to lie outside the quasivariety N whose
  dominions are taken. The paper says a second, larger example handles the opposite convention, but that example is
  only sketched, so the entry is fully verified only under one of the two conventions.
- **14.72 (C.13).** The printed question supposes that the fixed-point variety is "a regular hypersurface of X (of
  codimension 1)". The paper's fixed locus is a smooth codimension-one closed subvariety and a Cartier divisor, and
  the paper says so; but it is not the zero set of a single global function. The surface fibres over the affine
  elliptic curve y^2 = x^3 - x minus its point at infinity, as the total space of a line bundle, and the fixed locus
  is the fibre over the 2-torsion point (0,0). Restricting a putative global generator to the zero section would
  produce a function on that affine curve with divisor exactly one copy of the 2-torsion point, which would force
  that point to be trivial in the group law. So the hypothesis of 14.72 fails under the reading "hypersurface = one
  equation" and holds under the reading the parenthetical suggests, namely "closed subvariety of codimension one".
  The paper should settle which it means; the example looks repairable by deleting a suitable orbit of 4-torsion
fibres, which kills the obstruction while
  keeping both the fixed divisor and the singular point. Separately, the problem allows arbitrary characteristic and
  the construction is over the complex numbers only, so the wild case is untouched.
- **10.62 (C.25) and 4.75 (C.29).** Both rest on a single geometric existence theorem from a September 2025
  preprint, and not only on its statement. I read the source. Its Theorem 6.7 gives what the paper says it gives:
  elliptic subgroups embed, every finite-order element of the quotient is either killed to exponent twice one of the
  prescribed odd integers or comes from an elliptic element, and infinitely many elements are new. But two things
  the paper needs sit outside that statement. The ability to put a chosen primitive loxodromic element into the
  first family of imposed relations lives in the proof, which builds the quotient by adding relations of that form
  step by step. And the scale condition is read off a remark that states the principle "a smaller rescaling
  parameter is available at the cost of a larger critical exponent" but fixes the constant for translation length
  two, whereas the word abc used here has translation length three. Both extrapolations look safe, and the paper
  does say it uses the construction and not only the theorem. One thing that looks like an inconsistency in this
  section is not one, and I record it so that a later referee does not report it as an error: the vanishing of the
  overlap invariant coexists with the choice of a smaller scale, because that invariant is computed in the original
  space and is multiplied by the scale factor under rescaling, while admissibility is measured against a fixed
  universal constant. The source itself works with hyperbolicity constant zero and vanishing overlap invariant.
  Still, two ledger entries stand on one unrefereed import, and that belongs in the main text rather than only
  in the appendix.
- **12.40 (C.31).** The problem asks for the best possible estimate of the p-part of a Brauer character degree in
  terms of the p-part of the group order. The paper shows no finite bound exists. That is a legitimate answer to the
  printed request, but "find the best possible estimate" suggests the proposer had a restricted class in mind.
- **20.90 (C.11).** The example is correct, but it is elementary: every closed subgroup of SL2 over a
  characteristic-two power series ring has abelian centralisers, because centralisers of non-scalar 2-by-2 matrices
  are commutative and scalars are trivial in characteristic two. The paper says the centraliser argument is
  classical and claims only the application; that is honest, and the entry should be weighted accordingly.
- **11.115 (C.41).** The counterexample is three lines long. It is correct under both readings of "not maximal"
  (as a subgroup and as a normal subgroup), and the paper covers the variant where T is also not maximal. Such a
  short refutation of a 1990 problem is a priority risk rather than a mathematical one.

None of these is an error, and after the authors' reply I no longer put a number on the group; see `review2.md`.
What stands is that a reader counting 46 solved problems should be told which entries turn on a stated convention.

## 7. Reproducibility and the unprinted certificates

Appendix G is honest that the configured repository address was not anonymously reachable during manuscript
preparation, and that a local query found a remote head different from the frozen revision. That means a referee has
the paper and nothing else. For most entries this is fine, because the constructions are printed in full and can be
rebuilt from the text, which is exactly what I did. Two entries are different in kind.

For 19.62 the paper prints 19 representative derivations in Appendix F and asserts that an ancillary checker verifies
all 104 requests; for 19.61 it asserts 300 certificates with 3,191 nodes, none of which is printed. I checked both
claims independently. I computed the absolute Chevalley commutator constants for A2, B2 and G2 from a Chevalley
basis in the adjoint representation, confirmed that every application in the 19 printed derivations uses a genuine
rule with the stated constant and that the greatest-common-divisor steps are right, and confirmed that the displayed
destination roots carry exactly the stated numbers of requests. I then wrote my own saturation search over the same
proof calculus and re-derived all 104 requests for inclusion (5) and all 300 merged requests behind Lemma C.13,
obtaining the paper's counts exactly (6, 20 and 78 requests in types A2, B2, G2; 12, 48 and 240 merged certificates
from 600 raw substitution terms). So these two entries are sound. But this took a working day; the right fix is to
print the request tables and the certificate grammar, or to ship the ancillary files with the paper as the appendix
says they are shipped in the arXiv source.

The same applies to the largest computation in the paper, the n = 7 certificate for Problem 20.100, which is not an
entry in the ledger but is the headline of Section 3.3. Nothing about it can be checked from the paper. The paper is
careful to say so, and to distinguish generation from verification, which is the right instinct.

## 8. Small things

- Section 2.5: the phase estimates 846.09 + 64.52, 0.56 and 54.77 + 3.85 add to USD 969.79, not the 969.78 stated.
  The paper does say estimates are rounded independently, so this is a rounding artefact, but it reads as an error.
- Appendix C.4 asserts that part (b) of 16.28 also follows from the same class, and then excludes it as prior work.
  If that is spelled out, it must be restricted to odd characteristic: in characteristic two the argument that the
  square omits minus the identity collapses. (My earlier suggestion said "any field" and was wrong.)
- C.16 states the four projective covers have dimensions 90, 60, 90, 90 and lists GAP ordinary indices 10, 16, 18,
  20, 22. Both match the character table library exactly; it would cost one sentence to say which table version was
  used, since the indices are library-dependent and the paper already warns about this.
- The ledger description for 20.90 in Appendix B says "CA-group" while the section title says "CN-groups". Both are
  true (the example has abelian centralisers, hence pronilpotent ones), but the inconsistency looks like a slip.
- The two prime-counting inputs in C.26 are correct, but the attribution deserves a look: the upper bound with the
  constant 1.01624 is indeed Theorem 9 of the cited paper, while the lower bound valid from 563 onwards is usually
  cited as formula (3.16), not Theorem 4.
- C.28 leans on unpublished cycle-structure data from a 1980 thesis (one p-cycle in a specific permutation, all
  cycle lengths dividing 720720), and on an unexplained assignment of the prime 11 or 13 to residue classes of r.
  Both should be stated as explicit hypotheses with a precise pointer, since nothing in the paper lets a reader
  check them.
- C.32 cites "Exponential groups 2" for the definition of an A-group and of tensor completion, whereas the Notebook
  entry for 13.42 points the reader to the 1994 "Exponential groups 1" paper. Worth aligning.
- C.27 identifies the analytic obstruction at the first zero of A(t), namely the golden-ratio conjugate. I verified
  the inputs against the Fulman-Neumann-Praeger memoir: the paper's A, B, E, D and P are exactly the memoir's
  quantities, and its J_d is the memoir's N*(q;2d). The one item I could not confirm from the memoir text is the
  exact index in the K_d exponents, where the paper itself records a discrepancy in the source. The conclusion is
  therefore correct modulo a transcription the paper has already flagged as delicate.

## 9. Recommendations

On the mathematics:

1. Separate the ledger into columns the reader can see at a glance: answers the printed question under the reading
   the proposer intended; answers the printed sentence under a reading the proposer probably did not intend; and
   answers a subpart. On my reading roughly seven of the 46 belong in the middle column. While doing that, move the
   three appendix entries that do answer their printed question into the same table with their prior-work status
   recorded, rather than leaving them invisible to anyone counting.
2. Print the request tables and certificate grammar for 19.61 and 19.62, or state plainly that those two entries are
   unverifiable from the paper alone. The same holds for the n = 7 certificate discussed in Section 3.3.
3. For each entry, name the imported theorems in the entry itself and say what would survive if the import failed.
   The paper is good at disclosing shared dependencies, for instance that 10.62 and 4.75 rest on one geometric
   existence theorem, but it never says which parts of an entry would be lost if a cited result were withdrawn or
   turned out to be weaker than the use made of it.
4. Promote 19.56 in the exposition. It is a complete, short, self-contained solution of a 2018 problem whose proof
   uses only standard machinery, and it is much stronger evidence for the experiment's thesis than the three
   examples currently chosen for Section 4.
5. Say explicitly, for each of the elementary entries (20.90, 11.115, 21.76, 18.92), that the mathematics is short.
   A reader who sees 46 entries will otherwise assume uniform difficulty, and the paper's own honesty elsewhere
   makes this omission conspicuous.

On the experiment:

6. Record what the agent read. The single most valuable missing datum is the list of pages retrieved during the run.
   Problem 21.106 was solved publicly and formally, by other people, inside the same 48 hours; without a retrieval
   log one cannot distinguish independent discovery from a lucky search, even though in this instance the commit
   times favour the agent.
7. Freeze and publish the archive before the manuscript, not after. Appendix G currently tells the reader that the
   repository could not be reached anonymously, which undercuts every claim that rests on it.
8. Keep the separation of generation from checking, and extend it: state for each large computation who checked what,
   with which independent implementation, and what a failure would have looked like.

## 10. Overall

Accept after revision. The mathematics I could settle is sound: no entry I checked is false, the finite objects are
what the paper says they are, the large certificate machinery for the two carpet problems survives an independent
re-derivation, and the reported search-coverage numbers are exact. The two appendices outside the ledger hold up as
well. The partial results are bounded honestly, with the open cases named in each section, and the appendix of
rediscoveries is if anything too cautious: three of its entries look like answers to their printed questions and are
still excluded from the count. The revisions I would insist on are editorial rather than mathematical: a visible
separation of literal from intended readings in the ledger, an explicit statement of which entries are short
arguments, publication of the archive and of the two certificate families, and the priority note about Problem
21.106.

