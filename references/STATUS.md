# Literature status and provenance

Last checked 2026-09-10. A search finding no solution is evidence only of the scope searched, not a proof of novelty. Downloaded reading copies are in ignored `references/cache/`; permanent reports cite their public sources.

## Notebook baseline

Official page: https://kourovkanotebookorg.wordpress.com/ . Latest posted update as observed: 1 September 2026, https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf . The user PDF was created 1 September 2026 and includes the corresponding recently solved entries. It remains the authoritative statement source for this task.

## Recent papers excluded from new-solution counts

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
