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

## 2026-09-10, 21:18–21:21 UTC

The improved 21.113(a) search completed: 2,750 ordinary tables, 9,850 table/prime pairs, no skips and no counterexample. Started the (b) projectivity screen using Brauer/projective duality; for every available modular table it reconstructs the ordinary character multiplicities through the decomposition matrix as a separate consistency check. The A5 characteristic-2 smoke check gives PIM multiplicities [1,0,0,1].

The degree-multiset screen also completed: 106 collisions involving almost-simple tables, all between entries marked almost simple. Preliminary name inspection shows mostly alternative table names or embeddings of the same familiar groups. The primed orthogonal/unitary tables merit a metadata check. No collision is currently counted as a counterexample.

## 2026-09-10, 21:21–21:42 UTC

Validated C++ positive-necklace enumeration and exact modular trace fingerprints for 18.43 against independent Python enumeration and matrix products: 1,602 evaluations in dimensions 2 and 3, lengths 1–12, all passed. The symbolic checker recovers a known GL2 identity and distinguishes the same pair in GL3. Searches at lengths 1–35 completed without collision; length 36 enumerated 1,908,881,900 necklaces and is sorting. At peak planning, six single-threaded workers needed at most about 62 GB of array storage. Last observed usage was one C++ worker at about 30 GB plus the GAP jobs.

Wrote the elementary equivalence of the GL3 and SL3 subquestions via exponent sums and scalar normalization. The negative computation remains limited to positive words.

Built and completed the first involution-class graph search for 21.52–53. During the write-up, detected that normalizing the inner permutation action is only a necessary condition for inducing the required group automorphism. Preserved the initial log, strengthened the test to construct and validate an actual automorphism on all class elements, and repeated the range. The strengthened run finished 27 group entries, 28 classes, one explicit size-cutoff skip, zero hits for either problem.

Checked the primed orthogonal and unitary degree-collision metadata. These encode alternate tables/fusion maps, not new abstract groups. No nonisomorphic collision established.

Developed a second complete candidate solution, for 21.132: an at most four-generated infinite residually p-finite Golod group with centre C_p for every prime p. The substantive step is a homogeneous annihilator quotient followed by a triangular nil-algebra extension with zero centre. Wrote the full argument and a requirement-by-requirement internal audit. Verified the statement visually on PDF page 187. Read the graded Golod construction in Ershov's survey and the cited Sereda–Sozutov 2006 centreless quotient theorem. Their theorem uses a different radical quotient and does not assert residual finiteness for that quotient. Novelty remains under audit; no outside review has occurred.

The 21.113(b) projectivity job continues with no observed hit. Every available Brauer-table case includes a decomposition-matrix reconstruction check. All work remains local, and the overall 48-hour research goal remains active.

At 2026-09-10T21:43:21.559809+00:00, the length-36 trace run was confirmed complete: 1,908,881,900 necklaces, zero collisions, 602.801 seconds. All lengths 1–36 together cover 3,933,931,043 necklaces. Validated the completion markers and zero-collision status for every retained log and wrote `results/18.43-summary.json`. The only remaining live computation is the projective-character GAP job.

## 2026-09-10, 21:44–22:04 UTC

The previous goal turn was concrete progress: a second candidate proof, complete
trace searches, and committed artifacts. Revalidated the live GAP process before
continuing. The projectivity search subsequently completed all 2,750 table entries:
7,573 available modular cases, 2,277 unavailable Brauer cases, zero hits, and all
decomposition-matrix reconstruction checks passed.

Read the Lisi–Sabatini Sylow-intersection paper. Its two-prime result means most
small examples are already covered theoretically. Designed an exact profile
computation using inclusion-minimal element-set intersections and an exact union
bound valid for every choice of Sylows. Initial orders 2–255 gave 4,188 checked
groups, all passing the bound. Independent direct enumeration agreed for 211
groups and 1,333 conjugator sets through order 60. Launched seven computational
blocks for orders 256–2000 with at least three prime factors; six completed.
Completed blocks total 63,122 groups including the initial run. The remaining
job is advancing through the 241,004 groups of order 1920. No hit or fallback
case has appeared so far. No agents were delegated.

Read the 2013 Timofeenko source cited by 21.132, correcting its DOI to
10.1515/dma-2013-0034. Its main construction concerns infinite subgroups of Golod
groups; no finite-nontrivial-centre example was found. The candidate retains a
homogeneous nil-algebra realization meeting the source convention.

Developed a third complete candidate resolution, for 21.121(a). For k>=1 take
the quotient of (Q8 semidirect C3)^(2^k-1) by the central binary simplex code,
then form the free product of those finite groups. A code-intersection lemma
bounds the central losses in every subgroup and yields a uniform 2-Jordan
bound at every exponent above log(24)/log(8). The actual finite factors show
that the bound fails at that infimum. Wrote the complete proof and an internal
audit, and visually checked the exact Notebook statement. Part (b) is not solved.

The GAP checker validates all 5 subgroup classes of the first factor and all
614 classes (11,781 actual subgroups) of the second factor. All inequalities and
normal-abelian-subgroup conditions passed. Independent Python code validates the
code lemma on 4,157 disjoint-support spaces and checks the quaternion identities.
An initial GAP function-name error was corrected before mathematical checks;
both the failed diagnostic log and the successful DONE log are retained.

Targeted novelty searches found no prior resolution of 21.121(a). All three
candidate resolutions still await outside review and further novelty checking.
The 48-hour goal remains active, with about 47 hours left at this checkpoint.

## 2026-09-10, 22:04 onward: older problems and a rediscovery

Revalidated GAP and the live Sylow search; it continues through order 1920
with no observed failure of the strict union bound. Surveyed older problems
and read the precise 13.19 statement in the PDF. Constructed Q <= D8^4
of order 256 and H normal of order 32, both subdirect, with quotient D8.
Wrote a complete elementary matrix proof. GAP verifies independently
generated Q and H and identifies them as SmallGroup(256,8935) and
SmallGroup(32,46). An independent literal binary-matrix enumeration checks
all 65,536 products/map identities and 8,192 conjugations. All pass.

The novelty audit found a decisive prior implication: Kearnes--Mayr--Ruskuc
(2018), Sections 3--4 and 6, constructs a nonabelian finite 2-group quotient
of two subdirect groups. Checked the institutional manuscript dated
23 July 2018 and wrote out why its quotient is a 2-group. Thus 13.19 is
excluded from the new-solution count, despite the small counterexample.
Also wrote a self-contained stronger realization: every finite p-group
is a quotient of two finite subdirect p-groups, via a truncated free
associative algebra and deleting blocks of variables. Its novelty is
unestablished. The candidate count remains three.

Problem 12.69 has a literal norm/trace counterexample which also contradicts
its claimed uncountable analogue. Recorded this formulation issue and
did not count it as a substantive new resolution of the intended problem.

Read Cameron's 2025 endomorphism/partial-isomorphism note. It reports the
strict inequality for nonabelian groups through order 63. Launched exact
subgroup/quotient-type counts through order 255 in five bounded workers.
The control block 2--63 completed with 318 groups (105 abelian), no equality
for a nonabelian group, and no reverse inequality. Its closest ratio is
763/734 for SmallGroup(32,49), suggesting extraspecial groups as a useful
family for structural analysis. Four larger blocks remain live. All work
is local; no agents, messages, submissions, or pushes.

At the next checkpoint the 64--127 run had found two groups with End>PIso:
SmallGroup(64,263) and (64,264). These do not settle the Notebook equality
question. Independently certified the second group as E32-plus x C2,
using a binary group law and a direct presentation-based endomorphism
count. A standalone Python checker enumerates all 374 quotient subspaces,
all 593 subgroups, quadratic isometry classes, and automorphism orders;
it computes End=6,074,368 and PIso=3,277,312. A separate GAP construction
via the central product D8*D8 followed by C2 agrees exactly. Wrote the
complete argument and the 17-type subgroup table. This refutes the
stronger question posed in Cameron's 2025 note, while 19.20 itself stays
open. No prior counterexample was found by the targeted search.

The three completed endomorphism-count blocks cover 2,112 groups of
orders 2--127 and 129--191. They give no nonabelian equality and the two
reverse inequalities above. Order128 and192--255 continue. The Sylow
job is still progressing toward completion. Goal remains active.

At 2026-09-10T22:31:56.858285+00:00, the last Sylow block was confirmed complete and its
runner session closed. It checked 246,307 groups with no fallback or hit.
The total is 309,429 checked groups; all satisfy the exact strict union
bound. Combined with the known two-prime theorem, every group through
order2000 is now covered. Only two endomorphism-count GAP workers remain.

At 2026-09-10T22:49:41.240858+00:00, archived 21.115 after locating Sambale's
8 September 2026 general resolution (arXiv:2609.09052v1). The finite proof
was checked. Our abelian Fourier and class-two arguments are retained as
special-case rediscoveries. The CP-SAT model passed 72 independent set
controls; 465 group coset files were exported, but no group solver search
was launched. OR-Tools 9.15.6755 installed locally with dependency versions
recorded. The 192--255 endomorphism block completed: 2571 groups,133 abelian,
zero equality hits,two reverse inequalities (coprime extensions of the
order64 examples). The order128 worker remains live.
