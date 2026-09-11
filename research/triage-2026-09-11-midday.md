# Midday research leads and limits,11September2026

These notes preserve exploratory findings. They add no complete candidate
beyond the separately proved negative answer to15.89.

## 19.20: coprime products of groups already counted

For finite groups X,Y of coprime orders, both the number of endomorphisms
and the number of partial isomorphisms are multiplicative under X x Y.
Indeed every subgroup of X x Y splits into the product of its projections:
appropriate integer powers of an element isolate either coordinate,
by coprimality. A homomorphism between subgroups likewise splits, since
every map from a subgroup of one factor into the other is trivial.
The same splitting applies to automorphisms and isomorphisms. Summing
the number of isomorphisms over all domain and image subgroups therefore
gives the product of the two partial-isomorphism counts.

It follows that coprime groups with reciprocal, nonunit ratios
|End(X)|/|PIso(X)| would produce a nonabelian equality example.
`scripts/search_19_20_coprime_products.py` searches the explicit COUNTS
records in the retained completed logs, checking duplicate agreement and
recording the exact input hashes. This is a reuse of previously computed
counts, not a new enumeration of endomorphisms. Earlier logs did not
retain every per-group count, so its scope is smaller than the completed
91,774-nonabelian-group coverage through511. The separate JSON report
states the available-record coverage and any reciprocal coprime pairs.
The completed run covers85,260 recorded groups,70,983 distinct nonunit
ratios and417 reverse inequalities; no reciprocal coprime pair occurs.
No result for arbitrary factors or for products of three or more factors
is inferred.

## 14.97: a prior factorization construction covers only special ranges

Bernhard Amberg's primary chapter *Some Results and Problems about
Factorized Groups*, in *Infinite Groups1994*, is available in a
[publisher preview](https://api.pageplace.de/preview/DT0400.9783110810387_A34803000/preview-9783110810387_A34803000.pdf).
Its introduction, Section2.3 including Theorem2.4 and its context, and
Section3.1 including Theorem3.1 and its context were read. The full
construction proofs were not audited; the Sysak reference list entry
lies beyond the available preview.

Theorem2.4, credited to Sysak, supplies a locally finite-soluble
factorization G=A A^alpha with a nontrivial elementary abelian q-part
and prescribed prime divisors of A. Its stated specializations already
give p-subgroup factors when q=2 and2^n-1 is a Mersenne prime p, and
when q=3,n=2,p=2. These do not settle the question for all distinct
primes p,q. No new construction was established here.

## 15.11: do not transfer regular p-group restrictions to arbitrary groups

Marta Morigi's primary1998 thesis summary, in Bollettino UMI,
[pages51--54](https://www.bdim.eu/item?fmt=pdf&id=BUMI_1998_8_1A_1S_51_0),
has an indexed final-page account of power-automorphism examples.
Only the primary indexed page excerpt was read in this pass, not the
whole thesis or its proofs. It records arbitrary elementary abelian
ranks for every p and examples with larger exponent. Consequently an
assertion that the power-automorphism group of every odd-order finite
p-group is cyclic would be false. A construction for every prescribed
finite abelian p-group was not obtained.

Wall's1975 [Secretive prime-power groups of large rank](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5E144BCDC648B804566E0BEAD77B3489/S000497270002400Xa.pdf/secretive_primepower_groups_of_large_rank.pdf)
is a possible construction lead. Only its primary abstract and initial
indexed statement were read, not its proof. An attempted extension of
norm constructions from F_p to Z/p^e was not completed.

## 15.9 and15.22: failed shortcuts

- Bardakov--Mikhailov's [2006 primary preprint](https://archive.mpim-bonn.mpg.de/id/eprint/1235/1/preprint_2006_146.pdf)
  discusses nonlinearity for IA automorphism groups. Its abstract and
  indexed questions were read, not the full proof. The basis-conjugating
  subgroup is a different group; the IA result was not transferred to it.
- For finitary barely transitive groups, perfectness does not contradict
  local finiteness or local p-finiteness. Pinnock's
  [primary lecture notes](https://chrispinnock.com/assets/2015/01/fpg.pdf)
  have indexed statements that the derived subgroup of an infinite
  transitive finitary group is transitive and perfect. Only indexed
  primary excerpts were checked here. A proposed exclusion using
  hyperabelianity would need additional hypotheses; no negative answer
  to15.22 was established.

The productive next step from the graph discussion was the explicit
four-neighbour C3*C2 construction in `15.89-proof.md`, with its
finite-sum inverse. That proof is separate from the uncompleted leads
above and uses none of their unproved conjectural steps.
