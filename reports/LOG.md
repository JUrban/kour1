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

At 2026-09-10T23:00:47.099415+00:00, completed a fourth candidate resolution,21.68.
The group B semidirect (E semidirect A4) has order2592 and an explicit
semi-abelian chain. Its degree8 irreducible character is nonmonomial by
an index2 obstruction in Q8 semidirect C3. GAP's complete monomiality
test returns false. Independent Python verifies all9216 base products,
576 quaternion representation products,9216 coset action products,and
2592 exact induced-character values with norm1. Proof and internal audit
are complete; novelty search and outside review remain. The order96 base
and its SL2(3) subgroup are explicitly credited to Kida's published paper.

The final19.20 block also completed:2328 groups at128,15 abelian controls,
zero equality hits,and50 reverse inequalities. Total through255 is7011
nontrivial groups,493 abelian controls,6518 nonabelian groups,and54 reverse
inequalities. Every DONE marker and absence of errors was checked.
No nonabelian equality counterexample was found.

At 2026-09-10T23:20:06.835849+00:00, completed a fifth candidate resolution,16.87(a),(b).
The variety of class-two groups with commutators of exponent dividing p
is nonabelian and nonperiodic, while its free group of rank r has test
rank r. The central endomorphism g -> g c^f(g), with f chosen by an
integer nullspace, supplies the lower bound for every proposed smaller
test set. Exact generator-substitution checks passed for1,156 target
sets,2,398 fixed elements,and3,468 homomorphism/substitution checks.
The printed page was visually checked; a first literature audit found
no prior resolution. Outside review and further novelty work remain.

The19.20 order256 search was launched at23:05:27UTC across16workers,
covering all56,092 group IDs and retaining every exact pair of counts.
A short partition control matched the previously certified order64
counts and abelian skip. All16 command lines were revalidated at this
checkpoint; 4360 groups counted, no errors or equality hits.
Full metadata and snapshot are recorded separately from the live logs.

At 2026-09-10T23:36:22.213466+00:00, proved closed counting formulas for exponent-p extraspecial
groups times elementary abelian p-groups, p odd. Five small GAP models
matched both totals and all 29 subgroup types. The full order-2187
model then completed with 66,734 conjugacy classes and 134,414 actual
subgroups: End=8,241,952,876,767,369 and PIso=2,607,970,224,105,603.
All 13 multiplicities and automorphism orders match, giving a certified
odd-order reverse inequality. This remains adjacent to the equality
question in 19.20. None of the 60 formula cases gave equality.

A Lie-algebra reduction for 21.42 led to a complete positive-grading
argument for three-generator class-three algebras. The literature search
then located exactly that theorem in Dekimpe--Igodt--Pouseele (2003),
explicitly restated in Dekimpe--Deré (2014/2016). Mathieu's Proposition 6
(2021) supplies self-similarity for each original Malcev lattice. Thus
a negative answer follows from existing results. The full inference and
our grading rediscovery are retained, separately from the five new
candidates. Other triage on21.41,21.133 and countable width is recorded.

Only the16 order256 workers remain active, all revalidated. At this
snapshot they have counted 8446 groups, with no errors and no
equality hits. The48-hour goal remains active; no external contacts
or Git pushes have been made.

At 2026-09-10T23:51:14.219915+00:00, completed a sixth candidate resolution,10.35.
The two-generator group <U(1),diag(2i,2)> is torsion-free and
virtually Z^3. Every map to GL_2(Q), even with torsion image, kills
U(2), by an elementary two-dimensional centralizer-algebra lemma.
The exact fixed-degree statement was visually checked on PDF page40.
All246016 bounded integer matrix pairs and exact normal-form controls
passed. A faithful GL_3(Q) representation confirms the importance of
the fixed degree. No prior resolution was found in targeted searches;
novelty and outside review remain outstanding.

GAP4.16.1 was also rechecked at the relocated path. 16 live GAP workers with command lines and range-specific stdout files revalidated; 12657 counts, 0 equality hits, 0 reversals, no errors at snapshot.
The48-hour goal remains active. No external messages or pushes.

At 2026-09-11T00:04:28.615824+00:00, completed a seventh candidate,16.28(a).
A closed trace-one class in SL_2 has nonclosed square, with -I a
missing limit point. Appending a central point at a transcendental
scalar coordinate produces a closed set for which every power n>=2
retains that nonclosed square in a distinct closed fiber. The base
field is an algebraic closure of F_5(t), allowed by the printed
statement. The example also embeds in SL_4. The part(b) conclusion
already follows from Guralnick--Malle--Tiep2013Lemma2.3(b), so that
part is a known-result consequence, excluded from new coverage.
The proof, assumptions, internal audit, and exact GAP/Python
certificates are recorded. Novelty and outside review remain.

16 live workers revalidated by command line and range-specific stdout; 15191 counts, 0 equality hits, 4 reverse inequalities; all log-format, uniqueness, range, and error checks passed.
The first four reverse inequalities in the order256 range occur at
IDs53042--53045. These are not equality hits or complete answers to
19.20. A reusable read-only process/log snapshot script now records
actual count comparisons and validates unique IDs and ranges.
The48-hour goal remains active; no external contacts or pushes.

At 2026-09-11T00:21:58.405270+00:00, completed an eighth candidate resolution,17.34.
The augmentation-ideal module I/(U(L)h+I^(c+1)) separates any Lie
subalgebra by a cocycle whose semidirect target remains of class <=c.
Malcev completion and BCH give the stated dominion result for arbitrary
divisible subgroups, with no rank bound. Thirteen exact tensor-algebra
presentations verify kernels, actions, cocycles and lower central series;
4,000 rational BCH homomorphism identities also pass. The construction
was checked against nonideal and nonhomogeneous subalgebras.

Shakhova2015 explicitly solved c<=2 as a partial answer to17.34; that
prior result is credited and the new candidate scope is all c. Budkin2018
concerns arbitrary subquasivarieties, a stronger target restriction.
Bergman's all-Lie-algebra PBW theorem was compared. Reid's related full
text remains unread after retrieval failures; no result from it is used.
Modern primary accounts of the Malcev/BCH facts were read. Further
novelty checking and outside review remain.

GAP4.16.1 is working at the supplied relocated path. All16 order256
workers were revalidated; 19,168 exact counts,0 equality hits,25 reverse
inequalities,all log checks PASS. The48-hour goal remains active.
No external messages or Git pushes have been made.

At 2026-09-11T00:29:35.647930+00:00, reclassified17.34 as a known-result consequence.
The broader search for filtered nilpotent Lie amalgamation found
d’Elbée--Müller--Ramsey--Siniora, arXiv:2310.17595v3, Theorem4.35.
Their free amalgam is explicitly strong (Definition4.14) and retains
the given class over an arbitrary field. Applying it to two copies of
L over h with induced filtrations, then using compactness and BCH,
gives the full Notebook answer. The precise implication is documented.
The prior brief provisional count of8 is corrected to7. Our PBW module
proof remains as independently developed work, with all13 controls PASS,
but carries no new-resolution or proof-method priority claim.
The related5September2026 successor paper was also found; the earlier
theorem already suffices. This illustrates why broader novelty audits
remain necessary for every candidate.

The order256 search snapshot at00:26:52UTC has20,555counts,0equality
hits,62reverse inequalities,16liveworkers,allchecksPASS.
The48-hour goal remains active, with no external communications or pushes.

At 2026-09-11T00:47:45.470414+00:00, completed an eighth candidate resolution,14.22.
The coefficient-support argument over Q uses a torsion-free amalgam
to separate a radical commutator from every finite normal isolated
closure. A second example over the nonabelian linear group Q * Z
includes a direct SL_2(Q(t)) embedding and a polynomial proof of
irreducibility. The groups are infinitely generated, which the printed
statement allows; no claim for a finitely generated variant is made.
The primary definitions were checked, all exact controls pass, and a
separate internal audit records the remaining novelty uncertainty.
This is a new eighth candidate, distinct from the earlier excluded17.34.

GAP4.16.1 was rechecked at /project/bin/gap, including |S4|=24. An
initial shell-generated smoke-test string had an embedded-newline
syntax error; the corrected literal heredoc passed. No research job
was affected. The48-hour goal remains active. No external messages
or Git pushes have been made.

Order256 snapshot 2026-09-11T00:47:45.332946+00:00: 24,693 groups, 0 equality hits, 80 reverse inequalities, 15 live workers, 1 completed range, all checks PASS.

At 2026-09-11 01:20 UTC, retained a proved positive subclass of 15.89:
every complex number is an adjacency eigenvalue for every connected
finite-valency Cayley graph of the infinite dihedral group. A binary
coefficient induction rules out a nonzero constant Laurent determinant.
The exact search checked 2,796,202 reflection polynomials; all 4,094
constant determinants were zero. Independent convolution and 7,000
neighbor-action controls passed. This is not a full Notebook solution
and has no novelty claim. Trofimov's 2024 paper was compared with
explicit reading limitations. A new August 2026 E-group preprint was
also located; 11.46(a) is excluded from new-target priority on that basis.

At 2026-09-11T01:22:03.231079+00:00, completed the ninth candidate resolution,16.20.
The finite perfect central-product construction makes every normal
subgroup a dominion. Its full dominion family is modular and has a
nondistributive central diamond. The smaller example has order
44,029,440 and exactly15 normal subgroups, independently constructed
and enumerated in GAP. A seven-factor variant also covers the stricter
convention requiring A in every target quasivariety, giving exactly M3.
All factor, binary-code, quotient-support, and lattice checks pass.
The printed page and primary definition were checked. Budkin2007's
conditional semidistributivity theorem was compared carefully; it does
not impose an extra condition on the Notebook question. No prior
resolution surfaced in the limited search. Internal audit is written;
novelty and external review remain pending.

Order256 snapshot 2026-09-11T01:20:27.451407+00:00: 30,421 groups,
0 equality hits, 82 reverse inequalities,
14 live workers and 2 completed ranges, all checks PASS.
The48-hour goal remains active. No external messages or pushes.

At 2026-09-11T01:28:19.632094+00:00, completed the16.14 search through order256.
All58,760 groups were covered:55,177 satisfy the rank bound, and
3,583 have explicit noncentral involutions excluding the hypothesis.
Every witness was independently reconstructed and tested;340 direct
small-group controls also pass. An elementary parity argument proves
the exponent-four subclass, including central direct factors. No
complete solution or novelty claim is made. The definitions in Kuhn
and Jezernik differ at p=2 and were checked before importing results.
No order512 search was launched. The portfolio remains nine complete
candidates pending novelty and outside review. The48-hour goal remains
active, and only local files and Git commits have been written.

Order256 snapshot 2026-09-11T01:28:53.922504+00:00: 31,819 counted, 0 equality hits, 82 reverse inequalities, 13 live workers, 3 completed ranges, all checks PASS.

At 2026-09-11T01:55:56.226842+00:00, completed the tenth candidate resolution,17.33.
The affine group Gamma_n has no nontrivial homomorphism to the Klein
bottle group K, but every subgroup on fewer than n generators embeds
in a finite power of K. Its explicit finite presentation gives a Horn
sentence separating it from q(K), proving no finite bound on the
variables of a quasiidentity basis can suffice. The printed statement
was visually checked. Python exact controls and an independent GAP
presentation computation passed, including SmallGroup(256,26974) as
the predicted finite quotient. The internal audit records every key
logical implication and the limited primary-literature review. Novelty
and outside review remain pending. Only local files and commits were
created; the48-hour goal remains active.

At 2026-09-11T01:57:45.521066+00:00, retained the completed16.95 binary search through
dimension6:28,082,408 unordered bases,50,718,594 permutation tests,
no counterexample. All22,347 independent all-vector Krylov controls
pass. This is bounded evidence, not a general solution. The prior
Dixon proof was withdrawn, as explicitly stated on its primary page.

Recorded exclusions16.60 (May2026 full affirmative claim, plus an
independent tensor proof repairing an unjustified source step) and
17.25(b) (Kim--Koberda Theorem1.4(1) at27/7). Their exact reading
limitations are explicit. The portfolio remains ten complete candidates.

Order256 snapshot 2026-09-11T02:06:12.707134+00:00: 36,335 counted, 0 equality hits, 84 reverse inequalities, 12 live workers, 4 completed ranges, all checks PASS. The goal remains active through2026-09-12 20:56:46 UTC.
