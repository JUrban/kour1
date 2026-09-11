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
