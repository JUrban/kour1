# Research log

## 2026-09-10, 20:56–20:59 UTC

Initial inspection found only the supplied PDF and an inaccessible GAP symlink. No existing research repository or computational jobs were present. Extracted the PDF text and confirmed Issue 21 (2026), 150 new problems, with an archive of solved earlier problems beginning at printed page 190. The main body also includes starred solved entries and partly solved entries; membership in the main body does not establish that a problem remains open.

User repaired the GAP installation during setup. Created local Git repository and a 48-hour research plan. No previous mathematical work to resume; previous interrupted turn provided source and environment evidence, but no new mathematical result.

Primary-source literature reconnaissance located the official September 2026 update and arXiv:2607.17477 and arXiv:2608.29219. These must be incorporated into candidate triage to prevent duplicate claims.

## 2026-09-10, 20:59–21:04 UTC

Validated the supplied GAP 4.16.1 and principal finite-group libraries. Committed the initial research setup as e25c134. Surveyed most new Issue 21 problems and identified 21.106 as a promising elementary model-theoretic counterexample target.

Developed a parameter-free formula using surjectivity of commutators onto the centre and a factorization by two centralizers. In the integral Heisenberg group these conditions force the two projected vectors to form a unimodular basis of Z^2; hence the formula defines exactly z and z^(-1). Wrote a self-contained candidate negative solution with residual-finiteness proof and quantifier audit. Verified the exact source statement visually on PDF page 183.

The Python checker independently expands commutators by multiplication/inversion, checks 15,625 integral pairs and finite-quotient reduction maps, and evaluates the formula in H(Z/nZ) for n=2,3,4,5 using actual commutator and centralizer sets. All checks passed. The finite tests support arithmetic and formula interpretation only; the infinite conclusion rests on the written proof.

Read the relevant primary papers: Conte–Petschick (2025) and Ciobanu–Conte (May 2026) still pose the general conciseness question; their positive theorems do not cover the alternating formula used here. Checking the published version and later literature remains part of the audit. No externally reviewed solution is claimed yet.

## 2026-09-10, 21:04–21:18 UTC

Committed the complete 21.106 candidate proof and arithmetic verifier as 0c02fbb. Checked the published Conte–Petschick version: the general question remains Question 1; its existential theorem has different numbering. Added a requirement-by-requirement internal audit of the candidate. No flaw located so far; outside review and an exhaustive novelty check have not occurred.

Built a reproducible main-body problem index (1,308 entries, all 150 Issue 21 problems). Surveyed substantial parts of Issues 17–21, maintaining a portfolio rather than committing to one search. Located primary-source claims already resolving 20.21 and decidability in 21.32; excluded them. Independently developed a pullback construction giving an explicit integral-order bound for 21.32 before locating the February 2026 paper, then correctly classified the result as a rediscovery.

Derived an exact power-map formula for Robinson's class function in 21.113(a). Initial search using a composite Chinese remainder exponent ran for about six CPU minutes with no 100-table checkpoint and was deliberately interrupted; retained its log. Replaced it with the equally valid pure-p-power fiber formula and per-table progress logging. The precise slow operation was not isolated, so the performance explanation remains a hypothesis. The revised job is progressing through CTblLib tables.

Derived a complete orbital/class-representative test for 21.99, avoiding enumeration of entire groups. It finished for all 4,722 transitive groups of degree 2–20 without counterexample. An independent direct-element verifier for all 86 groups of degree 2–8 agreed exactly. The source script subsequently received only a local-variable wrapper to remove GAP syntax warnings; the retained search output is from the initial equivalent code.

Launched a character-degree-multiset collision screen for 21.59(a) and 21.135. Initial almost-simple collisions look like alternate tables for familiar isomorphic subgroups; none has yet been accepted as a counterexample. An additional metadata-only GAP probe was deliberately stopped to avoid duplicating work.

Resource use at last inspection: two running GAP search processes, about one CPU core each, each using less than 250 MB resident memory. No software installation was needed after the user supplied GAP. No messages or results were sent externally. The overall research goal remains active.
