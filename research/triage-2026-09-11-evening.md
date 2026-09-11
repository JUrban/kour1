# Evening triage: Issues10--12

Started 2026-09-11 after the10.32 packet. No new complete candidate
has yet emerged from the following routes; the total remains30.

## 10.71: centralizers in automorphism groups

Andrew--Martino, *Centralisers of linear growth automorphisms of free
groups*, arXiv2205.12865, published Math.Proc.Cambridge Philos.Soc.
177(2)(2024),219--240, proves type VF for centralizers of linearly
growing outer automorphisms. The primary abstract and Theorem1.2
excerpt were read, not the whole proof:
https://arxiv.org/abs/2205.12865
https://doi.org/10.1017/S0305004124000203

Mutanguha's *Limit trees for free group automorphisms: universality*
explicitly says in its concluding discussion that finite generation
of arbitrary centralizers is thought open:
https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/limit-trees-for-free-group-automorphisms-universality/06F37D39C53E12E83CC7346A49CEC720
Only that primary passage was consulted. These are special cases or
context, not a solution for arbitrary elements or finite sets in Aut(F_n).

## 11.5: coefficient qualification

The literal arbitrary-ring assertion is false, already with G infinite
cyclic and a rank-two projective module induced from the classical
nonprincipal ideal (2,1+sqrt(-5)). Projectivity has an explicit2-by-2
idempotent certificate; evaluation at z=1 and an exterior power prove
nonfreeness. See `11.5-coefficient-obstruction.md`. This is retained as
a formulation issue and adds no new-priority candidate.

## 11.8: multiplicities must be preserved

A primary author-uploaded introduction to *On groups with the same
character degrees as almost simple groups with socle Mathieu groups*
reports Navarro and Navarro--Rizo counterexamples for the SET of
degrees, without multiplicities:
https://www.researchgate.net/publication/283889601_On_groups_with_the_same_character_degrees_as_almost_simple_groups_with_socle_Mathieu_groups
The original Navarro papers and full uploaded paper were not read.
This statement does not settle the Notebook's multiset requirement.
An older Nguyen survey says even the degree-set version was unknown;
its publication chronology cannot be used as a current status assertion.

## 11.19: basic commutators as relators

Moravec--Morse's primary paper *Basic commutators as relations: a
computational perspective* gives an alternative computational proof
for weight five, including arbitrary rank:
https://users.fmf.uni-lj.si/moravec/Papers/mmpaper.pdf .
Only its abstract and introduction were read. It is a prior result,
consistent with the Notebook's comment, not a general solution.

An older Jackson--Gaglione--Spellman author-uploaded manuscript dated
18 October2001 studies the range of weights n through2n-4, and a
Manitoba thesis speculates about a negative weight-six example. Neither
is a proof of the proposed weight-six failure. No new presentation
verification has been run here. The equality of the associated graded
Lie ideals alone would not prove normal generation in the group.

## Other distinctions preserved

- **11.16/11.17:** The finite maps x -> [x,y] give eventual periods and
  depths, so exact finite tests are possible. The quoted small-depth
  and PSL2 results do not give uniform control for all finite groups.
- **11.23:** The e-automorphism condition quantifies over all pairs of
  invariant subgroups, not just normal quotients or the fixed subgroup.
  In an abelian group kernels of powers of phi-1 give a direct route;
  those kernels need not be subgroups in the nonabelian setting.
- **11.49:** The located Artinian-module results impose FC-hypercentral
  or additional socle-action conditions, not arbitrary soluble finite
  rank. No blanket countability claim follows from a countable ring.
- **11.113:** Lie-ring solvability from a regular automorphism does
  not automatically bound group derived length via the lower-central
  associated Lie ring. Fitting-height bounds also do not suffice.
- **11.61/11.63:** No density theorem or torsion-normal-closure subgroup
  theorem with the exact requested hypotheses was found in this screen.

All status searches are bounded discovery checks. No absence of a
search hit is interpreted as proof of novelty or continued openness.

## Issue13 follow-up,18:50 UTC

- **13.31:** Recent primary abstracts confirm active work on the greedy
  base-size problem. Del Valle--Roney-Dougal, arXiv:2503.23964,
  proves the conjecture for primitive symmetric/alternating groups
  apart from one class of possible exceptions. Huang--Roney-Dougal,
  arXiv:2605.16032 (15 May2026), proves it for diagonal-type groups.
  Del Valle, arXiv:2408.14139, proves equality of greedy and minimum
  base sizes for all almost simple primitive groups with sporadic
  socle. Only the primary abstracts and publisher introduction excerpts
  were read; no proof audit or full resolution is claimed.
- **13.53:** Sozutov--Alexandrova2017 already proves that every g works
  for an infinite locally graded p-group. The finite-quotient argument
  is checked in `13.53-prior-partial.md`. The unrestricted problem
  remains unresolved here.
- **13.57:** Coprime centralizer lifting followed by a fixed-point-free
  automorphism theorem applies only when p does not divide |G|. It
  cannot settle the p-group case. Existing bounds depending on the
  number or rank of fixed points also do not give a bound in terms
  of p alone when the fixed subgroup is merely required to be central.

The earlier detailed Issue13 exclusions in
`older-triage-2026-09-11.md` still apply, notably to13.3,13.14--15,
13.17,13.30,13.51 and13.54. Repeating those incomplete routes does
not produce additional candidates.
