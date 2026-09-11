# Later Issue20 triage and literature boundaries

## 20.51--52

The primary paper by Buckley and MacHale,
[Conjugate deficiency in finite groups](https://www.irishmathsoc.org/bull71/Buckley.pdf),
Irish Math. Soc. Bulletin71(2013),13--19, was read in full.
Its Lemma9 and bound(4) already give the order bound used in our20.52
experiment. Its Problem5 supplies groups with |G|-k(G)=2^j for
4<=j<=12, hence covers every m<=256 in the Notebook via odd-order
abelian direct factors. Our m<=64 screen therefore duplicates a known
existence range. In particular order1161 already supplies m=64;
failure of the fixed-point-free C3 kernel construction at order385
is not a negative example.

For20.51, the same paper's Problem7 reports a number-theoretic
search for odd class counts below10,000,001 using groups of order pq.
We have not independently replayed that range. Small searches here
would repeat earlier work. Neither general question is resolved.

## 20.115

Malle--Navarro--Tiep,
[Zeros of characters and orders of elements in finite groups](https://arxiv.org/abs/2605.04513v1),
6 May2026, addresses exactly20.115, with denominator chi(1), rather
than19.108's stronger p-group denominator chi(1)^2. It does not claim
a complete proof: Theorem B is a reduction to nearly simple groups,
and Theorems C,D cover substantial subclasses. The abstract explicitly
lists remaining difficulties involving character extensions. The
introduction and theorem statements were read, together with the start
of the reduction proof; the full reduction and Lie-type arguments
were not audited. Do not list20.115 as solved on the basis of this paper.

## 20.108

Tsang's exceptional SmallGroup(605,5) led to the new explicit
order-four-coset construction in `20.108-proof.md`, which resolves
(a),(b) as a candidate and gives a general family with unbounded
coset orders. The full holomorph is proved and independently checked.
Part(c) is already affirmative by Caranti--Tsang2023, recorded separately
in `20.108c-known-consequence.md`. This is the strongest
lead from this portion of the triage.

## Other scope cautions

- **20.91:** Sela, [Diophantine Geometry over Groups X](https://arxiv.org/abs/1012.0044),
  Theorem8.1 explicitly proves that a free product of stable groups is
  stable. The introduction and the start of Section8 were read; the long
  proof was not audited. This covers PSL2(Z)=C2*C3 but does not by itself
  settle SL2(Z)=C4*_C2 C6 or arbitrary virtually free groups. Neither
  stability under arbitrary finite extensions nor definability of an
  arbitrary finite-index subgroup has been established here. No answer
  to any of the three printed subquestions was obtained.
- **20.100:** The exact source and its bounded cyclic searches are now
  recorded in `20.100-reduction.md`. The new route proves every torsion-free
  case and reduces the general fixed-n question to finite abelian groups.
  Complete finite relation certificates for n=4,5 pass a separate integer
  presentation checker; n=6 and7 are still being processed.
- Stability in20.91 is model-theoretic stability. Search results about
  permutation stability, stable cylinders or Morse subgroups are
  unrelated and cannot settle the question.
- The20.59 virtual-retract question concerns every finitely generated
  subgroup. Later results about virtual retracts of cyclic subgroups
  alone are insufficient.
- The arbitrary-normalizer quotient in20.108 is not determined merely
  by exhibiting a permutation outside Aut(G). The full Hol(G) must
  be controlled, as done in the candidate proof.
