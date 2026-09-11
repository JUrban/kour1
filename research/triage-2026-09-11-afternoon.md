# Afternoon source triage, 11 September 2026

These are source-scope records and unresolved leads, not new complete
resolutions. The 20.100 n=7 verification continues independently.

## 19.22: local isomorphism without compact generation

Groenhout–Reid–Willis, *Topologically Simple, Totally Disconnected,
Locally Compact Infinite Matrix Groups*, J. Lie Theory 30 (2020),
965–980, [primary PDF](https://jolt.centre-mersenne.org/item/10.5802/jolt.1146.pdf):
the first three pages, including Theorem 1.1 and its explanation,
were read through the web tool. The main construction was not audited.
The paper gives uncountably many local isomorphism types, but its
open normalizers of nontrivial abelian subgroups obstruct compact
generation in topologically simple local envelopes. Thus it does
not remove the compact-generation hypothesis of 19.22.
A 2025 generalization, DOI 10.5802/jolt.1380, was seen at the indexed
abstract level only; it supplies no general resolution here.

## 19.26: exact original formulation located

Dicks–Serra, *The Dicks–Ivanov problem and the Hamidoune problem*,
European J. Combin. 34 (2013), 1326–1330,
[DOI 10.1016/j.ejc.2013.05.015](https://doi.org/10.1016/j.ejc.2013.05.015):
primary abstract and author metadata were read; the full five pages
were not obtained. The original inequality agrees with the Notebook.
Hamidoune–Serra, [arXiv:0804.2593](https://arxiv.org/abs/0804.2593),
was read only at the primary-abstract level; the abelian Pollard-type
extension does not settle the nonabelian question. No search or
general deduction is reported.

## 19.30: already treated families

Foroudi Ghasemabadi–Iranmanesh–Ahanjideh, *A new characterization of
some families of finite simple groups*, Rend. Sem. Mat. Univ. Padova
137 (2017), 57–74,
[primary PDF](https://www.numdam.org/item/10.4171/RSMUP/137-3.pdf),
was located; only indexed introductory material was inspected.
The full proof was not read. It reports prior coverage for sporadic,
alternating, certain PSL2, and groups with three or four prime divisors.
The [2019 primary paper](https://imar.ro/journals/Mathematical_Reports/Pdfs/2019/4/3.pdf)
was inspected only at indexed introduction and main-theorem level:
its special PSL families with Mersenne-prime conditions are not all
simple groups. Khatami–Babai,
[DOI 10.21136/CMJ.2018.0355-16](https://doi.org/10.21136/CMJ.2018.0355-16),
was inspected at primary abstract/introduction level: its Suzuki and
F4 cases have additional primality assumptions. Zhang,
[arXiv:2401.00767](https://arxiv.org/abs/2401.00767), was read only
at abstract level. Its E8(p) families do not give a general answer.
No new finite computation was launched for these covered families.

## 19.33: published character-restriction searches are extensive

Rossi–Sambale, *Restrictions of characters in p-solvable groups*,
[arXiv:2106.04818v2](https://arxiv.org/abs/2106.04818v2), was cached.
The introduction, Theorem 1, Corollaries 2–4, Conjecture 5,
Lemma 6 and its proof, the proofs of Theorem 1 and Corollaries 2–3,
the beginning of the Corollary 4 proof, and the concluding
computational scope were read. The full classification discussion
was not audited.

Theorem 1 expresses restrictions in the p-solvable case as positive
sums of induced characters with a specified subgroup index.
Corollary 3 and its discussion credit an earlier arbitrary-group
result when the Sylow p-subgroup is abelian. Repeating cyclic-Sylow
searches would add no new case. The stronger positive-induction
assertion fails for PSU5(2), p=2; this is not a counterexample to
the Notebook's distinct-linear-constituent question. Conjecture 5
allows negative integral coefficients, so it cannot simply be used
as a positive-character decomposition.

The authors report GAP/4ti2 verification of the stronger assertion
through group order 2000, and no minimal counterexample among
perfect groups through one million; the weaker conjecture was
tested on simple groups through PSL3(13) and sporadics through Co3.
These are the source's computations, not runs audited or repeated
here. No new 19.33 counterexample is established.

## 19.34: residual finiteness and an extra intersection hypothesis

Gonçalves–Nasybullov,
[arXiv:1705.06842v1](https://arxiv.org/abs/1705.06842v1),
*On groups where the twisted conjugacy class of the unit element is
a subgroup*, DOI 10.1080/00927872.2018.1498873, was cached.
Read: introduction, Section 2 definitions and Lemmas 1–6,
Theorem 1 statement and initial proof, the closing Proposition 2
argument and Corollary 2, Section 4 Proposition 3 and full proof,
Problem 2, Theorem 2 and full proof, Corollary 3, and the concluding
Example 2 discussion, Problem 4 and final paragraph. The full
18-page paper and example constructions were not audited.

For the inner-automorphism condition the commutator-value subgroup
is normal, the condition passes to quotients, and the finite
quotients are nilpotent. Hence residual finiteness gives residual
nilpotence. This already covers finitely generated linear and
metabelian groups by their standard residual-finiteness theorems;
these are not new general cases. The paper's concluding Problem 4
is the exact general question in 19.34.

Theorem 2 requires a trivial intersection condition on every
sequence of nested commutator-value subgroups. Its conclusion
about a stabilized lower-central term cannot be invoked after
discarding that hypothesis. In particular, neither the fact that
each individual value subgroup is proper nor exclusion of simple
quotients proves residual nilpotence. No general answer is claimed.

## 19.42: the March 2026 finite-fiber theorem has specified scope

Bhattacharyya–Halder–Lazarovich–Mj, *Finiteness of Cannon–Thurston
fibers*, [arXiv:2603.22428v1](https://arxiv.org/abs/2603.22428v1),
was cached. Read: the complete introduction with Theorem A and
proof sketch; Section 2 definitions, Lemmas 2.1–2.3, Proposition
2.4 and proof, Definition 2.5 and Lemma 2.6; Section 3 Definition
3.1, Theorem 3.2, Definition 3.3, Lemma 3.4 and proof, Definition
3.5; the last paragraph of Theorem 5.8 and Question 5.9.
The main boundary-flow/bundle proof was not independently audited.

Theorem A gives uniform finite fibers for normal hyperbolic
subgroups of hyperbolic groups, suitable hyperbolic trees of spaces
with uniformly quasi-isometrically embedded edge maps, and certain
metric graph bundles. These hypotheses cannot be dropped to cover
an arbitrary hyperbolic subgroup for which a Cannon–Thurston map
exists. Question 5.9 still asks a general finite-fiber question.
Baker–Riley examples without a Cannon–Thurston map do not refute
19.42, which assumes one exists. No general resolution is claimed.

## 21.55–21.56

The printed normalization in 21.55 is refuted by the Hall–Higman
exponent theorem at p=7. This prior consequence has its own proof
and audit, `21.55-prior-result.md` and `21.55-review.md`.

Güloğlu–Ercan, *Fixing size and Fitting height*,
[arXiv:2606.07242v1](https://arxiv.org/html/2606.07242v1),
was read through the introduction's main theorem statements,
Definition 2.1, Proposition 2.2, Proposition 2.3 with its proof,
and the statement of Proposition 2.4. The later main proofs were
not read. The bounds with constants 2 and 1 require such additional
conditions as at most one shared prime and an invariant Hall
subgroup, or a regular-orbit assumption. The arbitrary nilpotent
action in 21.56 remains unresolved here.
