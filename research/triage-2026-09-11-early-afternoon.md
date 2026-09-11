# Early-afternoon source and formulation triage, 11 September 2026

These entries record limits on promising shortcuts. They are not new
complete solutions. All work remains local; the six long-running
20.100 n=7 GAP verification partitions are preserved.

## 16.94: the full infinite-dimensional linear group

Dennis–Vaserstein, *Commutators in linear groups*, K-Theory 2 (1989),
761–767, DOI 10.1007/BF00538432, was located through
[primary institutional metadata](https://pure.psu.edu/en/publications/commutators-in-linear-groups/)
and [Vaserstein's publication list](https://personal.science.psu.edu/lxv1/publications.html).
The abstract mentions a bound with N=2 and applications to infinite
linear groups. The full paper was not obtained. In particular, neither
the inequality convention nor its precise linear-group scope was
verified. This does not establish width one in the printed GL(V).

De Seguins Pazzis, *Products of involutions of an infinite-dimensional
vector space*, [arXiv:1808.02224](https://arxiv.org/abs/1808.02224),
DOI 10.4153/S0008414X19000579: the initial theorem statements and
Section 1.3's bilateral-shift definitions and discussion were read.
The paper works over fields. It states as open whether every
automorphism is a product of two elementary automorphisms and explains
why that would imply the commutator assertion in uncountable dimension.
The decomposition proofs were not audited. A sum of additive
commutators in an endomorphism ring is a different problem.

A block shift makes alpha direct-sum identity a commutator, but does
not give a commutator decomposition of arbitrary alpha on the original
space. Also, closure of basis supports under alpha and alpha inverse
does not justify a decomposition into countable invariant summands:
reverse incidences of supports can be uncountable. No full result is
claimed from either idea.

## 16.88–16.93 and nearby word questions

Countability alone does not rule out the precise Cayley boundedness
property in 16.88: do not replace it by a stronger uncountable-cofinality
or Bergman-property definition. See the earlier late-evening triage.
The BMN-variety results located for automorphism groups of infinite
free nilpotent groups do not automatically cover all free groups.
Likewise, first-order interpretation results for infinite-rank free
groups do not settle finite-rank 16.93. No new result was imported.

The compact cases of 16.68 and 16.69(b) are recorded separately as
prior consequences of Thom. Noncompact PSL2 trace statements require
attention to signs and the quotient by the center. They do not settle
16.69(a) here.

## 17.31: finite versus torsion abelianization

The primary abstract of Linnell,
[*Left Ordered Amenable and Locally Indicable Groups*](https://doi.org/10.1112/S0024610799007462),
J. London Math. Soc. 60 (1999), 133–142, was read. Secondary full-text
snippets identify an Example 5.1 with torsion abelianization. That
example's construction was not obtained from a primary full text and
was not audited. Torsion does not mean finite. Local indicability rules
out nontrivial finitely generated examples with finite abelianization;
the supplied 17.31 does not assume finite generation. No general
answer is claimed.

## 17.57–17.61: residue-class permutations

Kohl's [publication list](https://stefan-kohl.github.io/publications_kohl.html),
the [RCWA manual](https://stefan-kohl.github.io/rcwa/doc/chap3.html),
and the introductory discussion of
[*The Collatz conjecture in a group theoretic context*](https://stefan-kohl.github.io/preprints/collatzgroups.pdf)
were consulted. The two-adic group is Thompson's V. The paper expressly
distinguishes the more complicated case of multiple allowed primes.
No general finite-presentation theorem was located or imported.

The installed RCWA data include an epimorphism from a finitely
presented group onto CT_{2,3}(Z). This is not an injectivity certificate
or a presentation of CT_{2,3}(Z). A residue-class table cannot be
identified without proof with a usual prefix-replacement table on a
single rooted tree when multiple primes occur. No search was launched.

## 17.85: a missing restriction in the literal formulation

The supplied printed page 113 was visually checked. If arbitrary
varieties are allowed, the variety of all groups has relatively free
objects equal to ordinary free groups. Their integral homology is
Z in degree zero, free abelian in degree one, and zero in higher
degrees. It therefore satisfies the hypothesis and is nonabelian.
This elementary exception suggests a missing restriction to proper
varieties. No substantive new solution is counted from the omission,
and the proper-variety question remains untouched.

## 17.87: successful prior-theorem route

The universal central extension of a finitely generated perfect group
is finitely generated and superperfect. Apply this to Nekrashevych's
simple group of intermediate growth. Zheng's Lemma 3.1 allows arbitrary
FC-central kernels and preserves subexponential growth. The resulting
group has intermediate growth and zero Schur multiplier. All exact
deductions, including a direct central-kernel growth proof, are in
`17.87-prior-result.md`; the logical audit is in `17.87-review.md`.
This short combination of prior ingredients is excluded from possible
new priority, consistently with the treatment of Problem 19.9.

Other scanned Issue 17 entries remain unresolved here. In particular,
finite Engel-group experiments do not supply a non-Engel infinite
example, and a faithful representation in a larger matrix degree does
not meet the rank-two SL2(C) requirement of 17.107.

## 17.48, 17.115, 17.117 and 17.124

Sela's Theorem 8.1 gives the exact affirmative prior answer to 17.48;
the noncanonical reduction in Theorem 6.3 was not shown effective.
17.117 remains unresolved here. See `17.48-18.56-prior-results.md`.

Samuel Poss, *The Frattini Subgroup of Locally Free Groups*, Math.
Z. 141 (1975), 199–204, was located in primary bibliographic metadata
at https://eudml.org/doc/172167. The full text was not obtained.
Its title alone does not answer 17.115; nonabelianity is essential
because the additive group Q is locally cyclic and has no maximal
subgroups. No implication from the unread paper was imported.

The exact September 2026 prior claim for 17.124 was encountered again;
it is already recorded in `17.124-prior-claim.md`. No duplicate result
or new reading of its formalization is counted.

## 18.35: separation, discrimination and surjectivity

The publisher-indexed Proposition 36 and Theorem 37 of the
2014 paper, *The Relatively Free Groups F(Nc meet A2) Satisfy
Noncentral Commutative Transitivity*,
https://doi.org/10.1155/2014/379030, were read, including their local
proof discussion. Theorem 37 addresses finitely generated metabelian
groups and discrimination by homomorphisms. The supplied 18.35 has
no finite-generation hypothesis and requires surjective maps onto
the rank-two free metabelian group. These differences have not been
removed. The full paper and the definitions earlier in that paper
were not audited; no conclusion for 18.35 is claimed.

## 18.48: existing residue-class permutation coverage

Bardakov–Iskra, https://arxiv.org/abs/2409.13341v1, states the exact
possible orders 1,2,3,4,6,12 for products of two horizontal class
transpositions. Only the primary abstract was read. It explicitly
describes this as a partial answer, not a general resolution.

Kohl's primary https://stefan-kohl.github.io/preprints/cycles.pdf
was read through the definitions, intersection classification, and
selected displayed table rows. The installed RCWA examples and data
already cover the ten known nontrivial finite orders through 60,
along with infinite order. CHANGES.md records a 2025 correction to
one database entry, from order 12 to 60. These data were inspected,
not recomputed. No extra search was launched. The general 18.48
remains unresolved here.

## 18.56, 18.78 and 18.83

Wilkens 2017 explicitly settles 18.56; see the separate prior-result
note. There is no reason to duplicate the older small-group search.

Passman's cached *Character Theory and Group Rings*, Section 2,
definitions and Lemmas 2.1–2.7 with their proofs were read. A simple
twisted algebra need not be central simple over the initial field.
The Galois-conjugacy issue in the characteristic-zero case remains
unresolved. No general answer to 18.78 was established.

For 18.83, countability does not supply an automatic answer by citing
the stronger uncountable-cofinality version of the Bergman property.
Poor–Rinot's primary paper https://papers.assafrinot.com/paper60.pdf
and 2025 slides https://www.dmg.tuwien.ac.at/fb8/2025_slides/Poor.pdf
were consulted at the indexed introduction/definition level only.
The absence of countable n-Shelah groups is a uniform-bound statement,
not a solution of the question allowing the bound to depend on an
infinite generating set. No new theorem is claimed.

## 19.1–19.5: substantial older literature found

Allenby 2000, Theorem 4, is an exact prior root-amalgam counterexample
to 19.4(a),(b) and 19.5. The full deduction and a direct lower-bound
check are in `19.4-19.5-prior-results.md`. The six-page source was read;
the original 1999 upper-bound proof has since been read and its
local argument examined, with earlier dependencies partly unaudited.

Azarian 2011, Sections 1–5 and the relevant reference entries, were
read. The survey reproduces the root-amalgam theorem and also lists
the same assertions among its questions. It further points to known
lower-near-Frattini results for the knot groups in 19.1 and several
cases of 19.3. Follow-up reading and exact deductions now appear in
`19.1-19.3-prior-results.md` and its audit. They cover the standard
nontrivial knot constructions and 19.3(a),(b),(c),(e),(f), with proper
amalgam and degeneracy conventions explicitly stated. These are prior
results, not additions to the 24-candidate count.

For the literal 19.2, a finite normal subgroup H is always contained
in lambda(G): adjoining it changes a subgroup's index by at most
|H|. Also G cannot nearly split over finite H with the printed
conditions [G:N]=infinity and [G:HN]<infinity, since [HN:N]<=|H|.
Thus, whenever psi(G) exists, both sides of the proposed equivalence
are false. For arbitrary groups psi(G) need not exist; the question's
use of this notation needs qualification. The same index obstruction
makes the hypothesis of 19.3(g) impossible. These are formulation
observations, excluded from new-result counting.

## 19.6(a): an exact prior assertion; (b) still unresolved here

Allenby 2005, Section 4, page 1004, item (7), explicitly states
mu(A *_H B)<=H when A and B are nilpotent groups, with no finite
generation assumption. This is exactly the proper-amalgam assertion
in 19.6(a). Its reference is Allenby–Tang 1978, Theorem 5.1, for
the ordinary Frattini result; the section says the same proofs or
easy adaptations give the upper near-Frattini versions. The whole
seven-page 2005 paper was read, but the cited 1978 proof and the
adaptation for this particular item have not been independently
audited. Record an exact prior assertion, not a new proof or candidate.

The same paper's Section 5(3) still lists the residually finite case
with H satisfying an identity, matching 19.6(b), as a remaining
conjecture. Its Section 4 proves several stronger-hypothesis cases,
which must not be silently substituted for the unrestricted question.

Allenby 2008, J. Group Theory 11, 415–420, DOI
10.1515/JGT.2008.024: the primary journal issue's indexed abstract
states that countable H suffices for both upper near-Frattini and
ordinary Frattini containment. Full text was not obtained. This
is a useful boundary on remaining searches, but is not used in the
written 19.3(e) deduction, which instead uses the checked 2005
corollary and Hall's theorem. The primary issue credits Allenby
alone; third-party search metadata incorrectly or ambiguously adds
Wilson, so it is not used for authorship.
