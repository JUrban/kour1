# Literature status and provenance

Last checked 2026-09-10. A search finding no solution is evidence only of the scope searched, not a proof of novelty. Downloaded reading copies are in ignored `references/cache/`; permanent reports cite their public sources.

## Newly audited older problems

- **13.19:** The supplied PDF page 67 was visually checked. Gorchakov's
  *Quotients of subdirect products of groups* (2009),
  https://doi.org/10.1007/s11202-009-0070-z , poses the same conjecture on
  Russian page 801; full source read at https://emis.de/ft/10761 .
  Kearnes--Mayr--Ruskuc, *Solvable quotients of subdirect products of perfect
  groups are nilpotent* (2018), https://doi.org/10.1112/blms.12196 , has a
  finite characteristic-2 construction implying a negative answer. Sections
  3--4 and 6 were read in the institutional author manuscript dated
  23 July 2018, https://research-repository.st-andrews.ac.uk/bitstream/10023/15796/1/Perfect10.pdf .
  The exact implication is recorded in `research/13.19-review.md` and is
  explicitly our inference; the paper need not name the Notebook problem.
  Our smaller independent counterexample is excluded from the novelty count.
- **12.69:** Visually checked page 63. Both norm and trace interpretations
  admit an elementary counterexample, including to the asserted uncountable
  analogue. No primary correction has been found. See the formulation audit.
- **19.20:** Cameron, *Endomorphisms and partial isomorphisms* (2025),
  https://doi.org/10.1007/s00233-025-10514-5 . Full two-page source read from
  https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/31654/Cameron_2025_SF_Endomorphisms-and-partial-isomorphisms_CC.pdf?sequence=1 .
  The nonabelian strict inequality is reported through order 63; our search
  reproduces that range and extends to 255.

## Notebook baseline

Official page: https://kourovkanotebookorg.wordpress.com/ . Latest posted update as observed: 1 September 2026, https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf . The user PDF was created 1 September 2026 and includes the corresponding recently solved entries. It remains the authoritative statement source for this task.

## Recent papers excluded from new-solution counts

- **21.115:** Benjamin Sambale, *On the complement of a union of cosets*,
  https://arxiv.org/abs/2609.09052v1 , submitted 8 September 2026. All six
  pages read; the finite-group argument checked. It resolves the problem
  in full. Our special-case work is excluded; the prepared search was
  archived before a group search began. See `research/21.115-literature-audit.md`.
- W. van Doorn, E. Judin, P. Monticone, D. Morrison, *On Some Problems from the Kourovka Notebook*, https://arxiv.org/abs/2607.17477 . Eight previously published resolutions; the supplied PDF already cites this work for several entries. Exact older problem identifiers still need extraction before surveying those issues.
- V. Ionin, A. Semidetnov, *On Some More Problems from the Kourovka Notebook*, https://arxiv.org/abs/2608.29219v1 . Downloaded and inspected the introduction and numbered questions. Addresses Notebook 14.85, 19.94, 16.11, 17.47, and 17.32, plus three questions from other sources. These are excluded from our novelty shortlist. This is a claimed-resolution screen, not an independent audit of that paper's proofs.
- I. Chinyere, *On the non-existence of finite groups with certain normal subgroups*, https://arxiv.org/abs/2601.01080 . Claims a negative resolution of 20.21. Excluded from new targets; abstract checked, proof not yet audited.
- S. Kalithasan, V. Z. Thomas, *On the decidability of the integrability of finite groups*, https://arxiv.org/abs/2602.18829v1 . Proves decidability, the principal part of 21.32. Downloaded and inspected main theorem. Our independently found pullback proof is retained as a rediscovery, not a new resolution.

## Problem 21.106

Primary sources checked:

- Conte–Petschick, https://arxiv.org/abs/2505.01411v1 , *Conciseness of first-order formulae*. Question 1 asks the exact question in 21.106. Theorem 1.2 establishes the existential case for torsion-free locally class-2 nilpotent groups. The published version is https://doi.org/10.1007/s00605-025-02127-5 with an accessible deposited copy at https://d-nb.info/1387927140/34 .
- Ciobanu–Conte, https://arxiv.org/abs/2605.06023v1 , *Concise formulae in groups of non-positive curvature*. Introduction still treats the general question as open and gives positive special cases.
- The supplied PDF, page 183, visually checked: no additional restrictions on the formula; question unstarred.

The deposited published Conte–Petschick version was also inspected: Question 1 remains unchanged, and its existential result is numbered Theorem 1.1 there (Theorem 1.2 in arXiv v1).

## Other candidate triage

- 21.89: OEIS A046668, https://oeis.org/A046668/internal , reports that a next term, if any, exceeds 2,000,000 (Kotesovec, 2018). Do not repeat a naive small-n search. Primary reference: Heffernan–MacHale, *The genesis of a conjecture in number theory*, https://doi.org/10.33232/BIMS.0093.39.41 .
- 21.99: P. Mueller, *On transitive sets of derangements in primitive groups*, https://doi.org/10.1007/s00013-026-02240-3 , resolves the stronger old 8.75 negatively using a degree-4,064,256 action of 3D4(2). Primitive groups of degree below 8192 were checked for that stronger question. Our small-degree search is mostly about imprimitive actions and validating the orbital implementation, not covering an unexplored primitive range.
- 21.113: G. Robinson, *A generalized character related to the local structure and representation theory of a finite group*, https://arxiv.org/abs/2505.03976 , poses the class-function conjecture and proves several special cases. Downloaded for detailed inspection.

Searches on 10 September 2026 included combinations of `21.106`, `Kourovka`, `Petschick`, `concise formula`, `first-order conciseness`, and `Heisenberg`. No primary-source solution was located. A secondary problem directory also labels it open, but is not used to establish mathematical status.

The Heisenberg construction in `research/21.106-proof.md` was developed during this session before reading the detailed Conte–Petschick proofs. Its use of alternating quantifiers is compatible with their positive results. No external submission, message, or priority claim has been made.

## Problem 21.132

The exact statement was visually checked on supplied PDF page 187. A complete
candidate construction is now in `research/21.132-proof.md`.

- M. Ershov, *Golod–Shafarevich groups: a survey*, https://arxiv.org/abs/1206.0490 .
  Downloaded and read Theorems 2.1 and 2.4, including the countable-field homogeneous
  nil-algebra construction. This supports the starting algebra; subsequent
  annihilator and triangular-algebra arguments are given in our proof.
- V. A. Sereda, A. I. Sozutov, *Associative Nil-Algebras and Golod Groups*,
  https://doi.org/10.1007/s10469-006-0012-9 . Read the Russian original, especially
  Theorem 1 and its proof, from https://m.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=eng&paperid=144&what=fullt .
  They obtain a centreless Golod quotient via the Levitzki radical. The theorem
  does not assert residual finiteness of this quotient. No such assertion is
  assumed in our proof.
- The associated short note, https://doi.org/10.1007/s11006-006-0121-8 , was located
  but its full text has not yet been inspected. One download endpoint returned 403;
  the mobile Math-Net endpoint successfully supplied the longer paper above.
- The 2013 Timofeenko paper cited in the question is *Finite systems of generators
  of infinite subgroups of the Golod group*, DOI 10.1515/dma-2013-0034 (the extra
  zero is confirmed by the primary archive). Downloaded the full Russian original
  from https://m.mathnet.ru/php/getFT.phtml?jrnid=dm&option_lang=eng&paperid=1252&what=fullt .
  Read the introductory discussion of centre and grading and the construction
  statements in Sections 2–3. It recalls known infinite and trivial centres,
  then constructs infinite finitely generated subgroups inside Golod groups.
  No finite-nontrivial-centre construction was located. Its Golod realization
  uses homogeneous nil-algebra quotients, which our construction also provides.

Searches for the exact problem number, Golod groups with finite centre, and
nil-algebra annihilator/residual-finiteness constructions found no explicit
resolution. This is not a proof of novelty; in particular older homogeneous
radical results or an elementary consequence of a known centreless example may
already give the requested construction.

## Problem 18.43

Read Section 4.3 of Lawton–Louder–McReynolds, *Decision problems, complexity,
traces, and representations*, Groups Geom. Dyn. 11 (2017), 165–188,
https://doi.org/10.4171/GGD/393 , accessible at
https://ems.press/content/serial-article-files/29814?nt=1 . Its length-20 computation
is mentioned in the discussion of positive trace-equivalent pairs; implementation
details are insufficient to infer broader coverage. Our reported scope is
explicitly positive words only. Their displayed dimension-two example also serves
as an independent known-identity control for the code.

## Problem 21.26

Read Conjecture A, Theorems 1.1, 1.4, 1.5 and relevant proof passages in
Lisi–Sabatini, *Sylow subgroups for distinct primes and intersection of nilpotent
subgroups*, https://arxiv.org/abs/2505.21222 . This already settles groups with at
most two prime divisors, metanilpotent odd-order groups, and sufficiently large
symmetric and alternating groups. The last two-prime-order groups are therefore
excluded from the extended computational search.

The abstract of Burness–Huang, *On the intersections of nilpotent subgroups in
simple groups*, https://arxiv.org/abs/2508.03479 , claims a proof for every
non-alternating simple group. The revised Lisi–Sabatini source also cites it.
No simple-group result from our searches will be counted as new without checking
this work.

## Problem 21.121(a)

The exact definition and both subquestions were visually checked on PDF page
185. A new candidate negative answer to (a) is written in
`research/21.121a-proof.md`, with an all-subgroup estimate and exact finite controls.
No claim for (b) is made.

Searches for `p-Jordan exponent`, `p-Jordan infimum`, `Jordan exponent attained`,
`21.121 Jordan`, `Shramov Jordan exponent 2026`, and combinations of simplex
codes with quaternion groups and the Jordan property located no primary-source
resolution. A secondary directory labels the question open, but is not used to
establish novelty. The construction is original to this session as far as our
current literature search shows; outside review and broader checking remain.

The 19.20 follow-up found a counterexample to Cameron's stronger
nonabelian inequality: E32-plus x C2 has End=6,074,368 and
PIso=3,277,312. This is kept separate from the original equality question.
Searches combining the paper title, partial isomorphisms, extraspecial,
order64, counterexample, and the exact counts located no earlier example.
The scope of these searches does not establish priority. The author's
publication list confirms the final citation as Semigroup Forum111 (2025),
538--539; the full primary paper had already been read.
