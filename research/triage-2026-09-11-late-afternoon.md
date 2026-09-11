# Further scope checks, 11 September 2026

These are unresolved leads and prior-scope checks, not additional
complete candidates. The portfolio currently has 28 candidates.
The completed results from this pass are recorded separately:
8.78 (periodic locally nilpotent prior case), 9.55 (prior negative),
9.47 (candidate27), and 9.45 (candidate28).

## 9.70: the base-two formulation is equivalent

Let H=G_alpha and m be the maximum rank of H on one of its
transitive constituents. For every such constituent Delta,

    rank(H on Delta) <= |Delta| <= |H|.

Thus m<=|H|. If |H|<=m, equality holds throughout for a constituent
attaining m. Its size is |H|, so H acts faithfully and regularly
there, and {alpha,beta} is a base for any beta in that constituent.
Conversely, a base {alpha,beta} gives a regular H-orbit of size |H|;
its constituent rank is |H|, hence m=|H|. The regular primitive
case H=1 also satisfies the order condition and has a base of size
at most two.

Consequently the version on Cameron's personal page, "bounded rank
or a base of size 2", has the same force as the Notebook's version.
It is **not** a weaker replacement. The present page, dated
13 May 2026, still lists this conjecture among those to be settled:
https://cameroncounts.github.io/web/problems/cameronconjs.html
The earlier Queen Mary copy is dated23February2009. Both relevant
entries were read; no inference from the old date alone is made.

A different statement, saying that the *induced permutation group*
on a nontrivial orbit is regular, allows a kernel and is weaker.
That distinction is the subject of9.69, whose negative result by
Spiga2022 is already starred in the Notebook.

The primary source at https://ir.cwi.nl/pub/13079/13079D.pdf is
**not** the1981 Bulletin survey. It is the1975 revised edition of
*Combinatorics, Part3: Combinatorial group theory*, Mathematical
Centre Tracts57, edited by Hall and van Lint. The chapter
P.J.Cameron, *Suborbits in transitive permutation groups*, starts
on p.98. The relevant passage on pp.120--121, Section5(4), was
read. It discusses the weaker regular-constituent formulation and
the stronger equality formulation; it also states the subrank-three
classification (rank at most3, Frobenius stabilizer3, or the degree16
rank4 affine example). This is prior material, not a new result.
The full proceedings were not read.

No counterexample family or general rank bound was obtained here.
Subrank is the maximum **rank of a constituent**, not the maximum
subdegree. Sims-type bounds in the latter parameter cannot be
substituted without an additional argument.

## 10.8: joint multiplication is the missing condition

Schneider--Thom, *On Folner sets in topological groups*, Compositio
Math.154(2018),1333--1361, gives an algebraic embedding g -> delta_g
in RG and uses the UEB topology coming from the right uniformity.
The exact warning immediately following it on p.1338 is decisive:
convolution is jointly continuous precisely when G is SIN, by
Pachl--Steprans2017; it is always separately continuous. Thus this
does not prove that arbitrary G embeds into a topological ring.
The article is available at https://d-nb.info/1252834527/34 .
Reading scope: introduction, selected Section2 UEB setup and
Proposition2.1 statement, Section3 opening through Lemma3.1 and its
proof, and the relevant references. No full-paper audit.

The cited original is J.Pachl and J.Steprans, *Continuity of
convolution on SIN groups*, Canadian Math. Bull.60(2017),845--854.
Its original proof was not read in this pass. In particular, failure
of this one topology for a non-SIN group is not a proof that the
group cannot embed into *any* topological ring.

J.Dobrowolski, *Topologies induced by group actions*, arXiv:
1412.0447v1,1December2014, published Topology Appl.189(2015),136--146,
describes finest compatible group/ring topologies and gives actions
with no compatible Hausdorff group topology. Proposition2.8 treats
the action of Homeo([0,1]) on the direct sum H([0,1]) of copies of
any nontrivial group H. The proof telescopes finite sums of point
generators and forces two distinct generators to be inseparable.
https://arxiv.org/abs/1412.0447
Reading scope: introduction and Remark0.1, Theorem1.2 statement and
proof opening, selected ring-topology argument, definition of H(X),
and Proposition2.8 with proof. Other model-theoretic sections and
the full ring-topology construction were not audited.

This obstruction cannot automatically be transferred to10.8:
an arbitrary embedding of Homeo([0,1]) into ring units has not been
shown to contain a faithful copy of that particular permutation
module. Likewise, an operator representation with the strong
operator topology does not by itself supply jointly continuous
multiplication on the ambient operator ring. No solution is claimed.

The same embedding question appears as3.5 in the Dniester Notebook
(search-indexed statement only). Search also found older work on
extending ring and group topologies to group rings with local
boundedness/compactness hypotheses; those hypotheses were not
verified from the original papers, so no broader conclusion is used.

## 9.1: two meanings of potency

The Notebook allows torsion: for an element x of finite order,
only divisors of that order are prescribed. Antolin--Dicks--Linnell,
*Non-orientable surface-plus-one-relation groups*, arXiv:0810.2734v1,
Definition4.1, instead requires every nonidentity element to attain
every finite order at least2 in a finite image. That forces the
group to be torsion-free. Their history statement(H7), citing
Allenby1981 Theorem2.4, says free products preserve this stronger
notion. It does not settle the torsion-allowing Notebook question.
https://arxiv.org/abs/0810.2734

Reading scope: Section4 Definition4.1, Lemma4.2 and proof, and
history(H1)--(H7), including the power-series discussion. The full
paper and Allenby's original *Potency of cyclically pinched
one-relator groups*, Arch.Math.36(1981),204--210, were not read.
An indexed passage in Elisabeth Green's1990 thesis, p.89 Lemma5.8,
also distinguishes the known torsion-free case; the thesis was not
read in full. No new count.

## 8.4: finite nilpotent loops

Mayr's arXiv:2206.06136 abstract says Vaughan-Lee's order12 loop is
finitely based. Kompatscher--Mayr arXiv:2409.12484 gives finitely
based cases and supernilpotent reduct results, including the order-pq
setting. Only the primary abstracts were consulted. They do not
supply a finite nilpotent loop without a finite identity basis.
No example or general finite-basis theorem was established here.

## 9.65 and further stopped routes

- **9.65:** The question is locally soluble, not merely soluble.
  Search-indexed sources give the soluble periodic-factor theorem,
  but not the required locally soluble version. Amberg--Sysak,
  *Products of locally cyclic groups* (2021), Theorem1.3, treats
  products of periodic locally cyclic factors under permutability
  conditions: https://doi.org/10.1007/s00013-021-01593-1 . Its
  introduction/results and selected Lemma5.1 statement were read,
  not the full proof. No solution to arbitrary9.65 was obtained.
- **10.17--10.18:** The central quotient of an FC-group is residually
  finite by its actions on finite conjugacy classes. But "direct
  product" may mean restricted direct product in this context,
  distinct from the Notebook's Cartesian product terminology.
  Residual finiteness alone is not counted as resolving these.
- **10.46:** Over a field, a general rank-one transvection can be
  chosen to make the first commutator fix its direction; a second
  transvection with the same direction then has a unipotent
  commutator. Extending this argument to arbitrary rings, or
  insisting on elementary coordinate transvections, needs work.
  No formulation-dependent trivial or field-only argument is counted.
- **8.2:** A holomorph of a polycyclic normal subgroup need not give
  the desired linearity for all arbitrary extensions.
- **8.14(b):** Local innerness facts for existentially closed groups
  do not settle all requested cases without the exact Thomas source.
- **8.79:** The uncountability of Aut(Hall's universal locally finite
  group) does not by itself exclude some other countable complete
  locally finite group.
- **8.50:** For a cyclic module over a possibly non-Noetherian
  metabelian group algebra, ambient polynomial-growth arguments do
  not bound all submodule generator growth. A cyclic module over a
  commutative non-Noetherian ring can have a very large socle.
- **8.58--8.59,8.62:** Topological local pronilpotence cannot simply
  be substituted for algebraic local nilpotence.
- **9.38:** Closedness of a locally elliptic radical does not imply
  the requested closedness of every maximal compactly covered
  subgroup without a separate argument.
- **9.51--9.53:** No new word/conjugacy/isomorphism algorithm was
  found for the stated finitely presented soluble groups. Finite
  rank by itself does not imply the useful linearity properties.

These records prevent repeated false starts. None changes the
28-candidate total or the count of zero external reviews.
