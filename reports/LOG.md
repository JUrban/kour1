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

At 2026-09-11T02:22:25.751324+00:00, completed the eleventh candidate resolution,17.101.
A multiple HNN extension and an induced-module quotient extend any set
of isomorphisms between subrepresentations. The Bass–Serre tree and a
finite-support leaf argument prove injectivity of the original module.
Countable iteration gives a homogeneous extension without changing the
coefficient ring, valid even over commutative rings with non-split module
inclusions. The exact question and the ordinary-induction obstacle were
confirmed in Aladova--Gvaramia--Plotkin2012, Definition5.8/Problem5.11.
Python tree and module controls pass, as do independent GAP Laurent
controls after correcting a finite-field versus polynomial zero mismatch
in the verifier. Internal audit written; novelty and outside review
remain pending. The48-hour goal remains active, with local commits only.

## 2026-09-11, 02:26--02:44 UTC

Completed two exact character-library screens. For17.100, all2,750
ordinary tables were considered,215 simple entries supplied12,606
eligible pairs, and none vanished. A different simplicity criterion
agrees on all2,750 tables; eight actual-group tables supplied72 direct
controls, all PASS. Most library cases follow already from the elementary
nonvanishing of odd-degree characters on2-elements; the limited reach
of the remaining320 nonabelian-simple pairs is explicit.

For18.20, all33,810,661 unequal-degree pairs in2,750 tables were checked
without a counterexample. Independent enumeration of every class
partition on ten actual groups agrees on129 pairs, including16 positive
controls. The exact two-ratio reduction and an orthogonality identity
are written. A summary parser initially missed GAP-wrapped lines;
whitespace normalization fixed the parser, and all completion and
count-consistency checks now PASS. The mathematical searches were
unchanged. No general resolution is inferred from either screen.

Wrote a common-centralizer reduction proving the first nonenumerability
assertion in18.18, under the cofinite meaning of almost all. The assertion
about the complement remains unresolved. No novelty claim is made.

Located Jayadevan's9 September2026 exact prior claim for17.124 and
Jones--Keller2020 Theorem1.2 explicitly resolving18.44. Reading scope
and exclusions are recorded. No Lean audit or full proof verification
of those papers is claimed; no18.44 orbit search was launched.

Order256 snapshot 2026-09-11T02:44:56.521555+00:00: 40,693 groups,
0 equality hits, 85 reverse inequalities,
12 live GAP workers and 4 completed ranges, all checks PASS.
The count of complete candidate resolutions remains11, all awaiting
outside review and further novelty checks. The48-hour goal remains
active; no external messages or Git pushes.

## 2026-09-11T02:59:43.105493+00:00 — Twelfth candidate: 18.76

Constructed a nonsplit extension of D_add by F2 x F2 over a countable
division closure of its group algebra. The explicit iterated semidirect
product proves existence, and the four lift equations prove nonsplitting
in every characteristic. Primary division-ring hypotheses audited.
All five exact group-ring control batches and all 27 GAP matrix controls
pass. Proof and internal audit committed; novelty and outside review
remain open. Order256 search snapshot: 42,348 counted, zero equalities,
85 reversals, 12 live and four complete ranges, all log checks PASS.

## 2026-09-11T03:04:53.609296+00:00 — Thirteenth candidate: both parts of 18.92

A family of formations indexed by finite prime sets plus all primes
has only its bottom compact, hence is not algebraic. A five-member
family indexed by selected prime sets gives N5. The exact internal-join
convention was checked visually in the Notebook and in a primary
formation-theory source. All32 finite subfamilies and65 modular-law
cases checked, with the one intended failure and1,296 positive Boolean
controls. Complete proofs and internal audit; novelty and outside
review remain open.

## 2026-09-11T03:31:49.898392+00:00 — Completed18.114 screen and diagnosed library cache error

All2,468 soluble IRREDSOL entries through dimension6 processed;2,421
have order prime to5. Allseven equality cases are cyclic, and none of
the2,352 noncyclic cases attains equality. All57 independent affine
permutation controls and37 commuting-pair controls pass. The indexed
PrimitivePcGroup constructor reuses guardian data across incompatible
complements; the second of two reproducible calls returns order800
instead of1200. Initial runs are retained as invalid diagnostics. Every
counted run uses the matrices directly and asserts the affine order.
The completed-log parser validates counts and all completion markers.
A preliminary commentary mental total was incorrect; the authoritative
parser totals are2,468 processed and2,421 eligible.

New19.9 arguments are being written and audited separately.
Order256 snapshot: 45,851 counts,0 equalities,
87 reversals,10 live and6 completed ranges; allPASS.

## 2026-09-11T03:34:52.160784+00:00 — Complete derived answers to both parts of19.9

Part(a) is negative for Sp(10,Z): its tensor square is its universal
central extension, identified with Deligne's non-residually-finite
topological-cover pullback. A short perfect-lift lemma proves finite
generation before Malcev's theorem is applied.

Part(b) is affirmative for all n>=4. The diagonal Z factor splits
explicitly, and a rational Clifford representation detects the C2
Hopf kernel of the exterior square. Combined with the faithful braid
representation this gives degree1+n(n-1)/2+2^n over Q(q,t). All exact
rational controls and26 independent spin-matrix cases pass. The first
GAP check was stopped at expensive n=7 characteristic-zero group-order
recognition; its18-case prefix is preserved as incomplete. The final
26-case bounded scope completed with160 distant commutator checks.

Both are short prior-theorem consequences, retained separately from
new-priority claims, consistently with previous rediscoveries. No
exact earlier published tensor-square answer was located in the limited
search; this does not establish novelty. The working candidate count
remains13, all pending outside review and further literature work.

## 2026-09-11T04:02:07.259346+00:00 — 19.108 first possible order and a general orbit lemma

Confirmed GAP4.16.1 remains available. Wilde2013 already covers all odd groups through p^9 and characters through degree p^3, so no duplicate small-group screen was launched. The exact C27-square action search finishes with571 subgroup classes and1,596 regular orbits, zero failures. Independent integer reconstruction and174,312 exact Fourier sums agree; nine actual affine groups give197 matching character values and eight known p=2 violating elements. The initial assertion stop due to the documented permissive size option is retained and excluded.

The computed invariance led to a proof for every odd prime: an orbit of size p^4 in (Z/p^3)^2 is invariant under p^2 translations. Combined with Wilde's prior theorems this proves the support-order bound for groups of order p^10 with an abelian normal subgroup of size at least p^6, including nonsplit extensions. The full problem and novelty remain open; complete-candidate count stays13.

Order256 snapshot: 48,699 counts,0 equalities,89 reversals,8 live,8 complete ranges; all log checks PASS.

## 2026-09-11T04:22:34.989960+00:00 — Complete derived answers to20.8 and20.11

For20.8, the n=3 Lei--Zhang construction gives H of rank3 in F2 and a fixed subgroup K of rank4. The independent core-image argument checks every proper intermediate subgroup, including infinitely generated ones; it does not assume every overgroup is a principal quotient. All five vertex partitions, the subgroup ranks and457 GAP word controls pass.

For20.11, Jaikin-Zapirain's prior corollaries give pairwise minimum-rank intersection and join closure. The infinitely generated bottom is handled by first taking the finitely generated intersection. Chain unions and a fully stated descending Schreier-graph limit give greatest and least members for arbitrary ambient rank. Full proofs and a shared internal review are written. Both entries are prior-work consequences and excluded from the13-candidate new-priority count.

GAP4.16.1 is available. Order256 snapshot at04:21:21UTC:49,939 counts,0 equalities,102 reversals,8 live and8 complete ranges; all checks PASS.

## 2026-09-11T04:26:43.795312+00:00 — Complete derived affirmative answer to20.33

Enumerate all oracle-X finite-generator presentations, take their countable free product, and apply an explicit three-generator HNN construction preserving the X-c.e. relator stream. The HNN associated subgroup isomorphism is certified by a retraction to a rank-two free group, and every generator is eliminated by a fixed computable word. Direct embedding in this universal group proves one direction with one factor and zero extra relators; normal-closure proof enumeration proves the full converse. Mikaelian's prior two-generator theorem provides another route. The Notebook page152 was visually checked. This is a standard-construction consequence, excluded from the13 possible-new-priority entries.

Started an exhaustive20.52 odd-order search through1727: an elementary bound |G|<=27m makes this a complete decision range for m<=64. No conclusion pending output and independent verification. Also started a bounded20.30 character-table screen.

## 2026-09-11T04:39:52.383506+00:00 — Fourteenth complete candidate:20.108(a),(b)

Tsang's2025 theorem leaves SmallGroup(605,5) as one of two specific exceptions. For G=F_11^2:C5 with eigenvalues3,9, the full automorphism group acts trivially on C5, and the full holomorph has an explicit coordinate form. The permutation theta(x,y,k)=(y,3^(-k)x,2k) normalizes it and has an order4 coset. The elementary proof resolves(a) and(b) affirmatively; part(c) remains unresolved.

GAP independently identifies the group, centre and regularity, matches holomorph order7,320,500 to automorphism order12,100, verifies all normalizer generators and checks index4. Python checks all13,200 invertible matrices against four quotient units, all605 points for seven generators and8,000 further parameter choices. The deliberately omitted multiplier fails, as expected. A higher-dimensional family gives unbounded even coset orders; four parameter sets with orders4,6,12,16 pass5,939 affine-basis checks. Full proof and internal review written. Limited searches found no earlier explicit certificate, but novelty and outside review remain pending. Candidate count is now14.

At04:36:28UTC the order256 search has50,952 counts,0 equalities,124 reversals,8 live and8 completed ranges; all checks PASS.

## 2026-09-11T04:47:34.468983+00:00 — Complete20.30/52 checks and prior answer to20.108(c)

The20.30 screen completed on all2,750 ordinary tables:340 eligible perfect centreless entries and zero failures. Independent explicit conjugacy-orbit enumeration agrees with all nine actual-group class lists and eligibility checks. The20.52 search completed on2,845 groups of all odd orders through1727, including1,719 nonabelian groups. Every m<=64 occurs; all86 independent actual-group counts agree with the recorded IDs. The summary parser validates all rows and completion markers; one wrapped Monster-table line required a whitespace correction in the parser. No search output or mathematical result changed.

Buckley--MacHale2013 was read in full: their results already cover every m<=256 and include the order bound. The20.52 work is therefore bounded verification only. Malle--Navarro--Tiep2026 was checked for scope and supplies a reduction and partial results for20.115, not a full solution.

A further primary-source check settles the earlier uncertainty on20.108(c): Caranti--Tsang2023 Theorem1.1 explicitly gives GL4(3) inside T(G) for a group of order3^10, so5 divides |T(G)| although it does not divide6. This is prior work and does not change the14-candidate count. The separate centreless construction for(a),(b) remains a possible-new-priority candidate. The primary theorem and corollary were read, but the full p-group construction was not independently audited.

At04:46:20UTC the order256 search has51,632 counts,0 equalities,143 reversals,8 live and8 completed ranges; all log checks PASS.

## 2026-09-11T05:09:01.073246+00:00 — Fifteenth complete candidate:20.90

The closure of two explicit determinant-one matrices over F4[[t]] is an
infinite profinite CA-group with quotient A5. An exact polynomial leading
term proves infinitude. Two short matrix words give all elementary
generators modulo t, and explicit commutators prove the quotient perfect.
The centralizer argument uses the field F4((t)): nonidentity determinant-one
matrices are nonscalar, and their matrix centralizers are commutative.
The general constant-subgroup construction realizes every PSL2(2^m),m>=2,
as a finite quotient of a finitely generated infinite profinite CA-group.

A separate four-generator construction SL2(Z2[omega])/{I,-I} gives a compact
2-adic analytic example. Nonzero trace gives abelian projective centralizers;
at zero trace a determinant argument forces nonidentity unipotent reduction,
so the strict centralizer and its possible sign extension are pro-2.
Both constructions answer one Notebook entry, not two.

Python independently checks all252 nonscalar F4 matrix centralizers,
all59 nontrivial normal closures,256 polynomial powers and the240-element
mod-t-squared image. GAP checks the finite group, all59 centralizers,
generator words, perfectness and128 polynomial powers. The mod-t-squared
image is deliberately verified not to be CN: quotient centralizers need
not lift. A separate companion check covers all65,536 matrices over O/4O,
all3,840 determinant-one matrices and all240 trace-zero cases. All final
controls PASS. An initial mixed-domain GAP polynomial assertion stop was
corrected by putting every entry in the polynomial domain; its incomplete
finite prefix is retained and excluded from completed evidence.

The characteristic-two CA fact is explicitly prior work, credited to
Fine--Gaglione--Rosenberger--Spellman2015/2016. The2019 CA and2020 CN
sources still pose the profinite existence questions. Limited searches
found no explicit earlier application, but priority is not established;
the short argument especially needs outside review. Complete candidate
count is15, with zero externally reviewed new solutions.

GAP4.16.1 remains available. At05:09:01UTC the order256 search has53,054
counts,0 equalities,179 reversals,6 verified live workers and10 completed
ranges; all log checks PASS. No external messages or pushes were made.

## 2026-09-11T05:34:26.163888+00:00 — Structural reduction and certified new fixed-n cases of20.100

Proved the assertion for arbitrary torsion-free groups using positive
lengths on commensurable cyclic subgroups; unique roots and commutativity
are unnecessary. The full fixed-n problem reduces to finite abelian
groups. A graph of selected two-variable relations then shows any failure
has a finite abelian counterexample of order at most p_n*n^(n-1), where
p_n is the first prime greater than n+1. Thus each fixed-n assertion is
decidable by a finite computation.

The Python certificate generator refutes all potential collision patterns
at n=4 and5. An independent GAP checker uses integer presentation matrices
and localized Smith-normal-form membership, verifies the transformations
and unimodularity, and checks every child implication. The certificates
have227 and10,493 nodes, with1,056 and87,570 collision branches and a total
of430,298 verified relation implications. These are all-group fixed-n
proofs, with no group-order search cutoff. Sun2021's prior results are
n<=3 and torsion-free abelian groups, with higher-n bounded cyclic searches.
Novelty of the extensions remains unconfirmed; the full arbitrary-n
conjecture is unresolved, so complete-candidate count stays15.

The final n=6 certificate has265,104 nodes and3,245,190 branches; its
independent verification is running in GAP PID43528. The n=7 generator
is running in PID43634 with a10-million-state/two-hour bound. Both commands
and stdout destinations were revalidated. The authoritative summary is
`results/20.100-summary.json`; no inference of completion is made from
process intent or a partial log.

Independent exact controls pass on1,000 Klein bottle lists and400 mixed
Heisenberg/Klein bottle lists, checking69,760 assignments. Distinct roots
sharing a square are included. Allowing the excluded order5 yields the
expected C5 four-element counterexample; all24 assignments fail. The GAP
checker also rejects a deliberately false equality leaf.

20.91 remains unresolved: Sela's Theorem8.1 concerns free products, not
arbitrary finite extensions or finite amalgams. At05:34:26UTC the19.20
order256 search has54,018 counts,0 equalities,238 reverse inequalities,
3 verified live workers and13 completed ranges; all checks PASS.

## 2026-09-11T06:05:06Z — Independent all-group certificate for20.100 at n=6 passes

The GAP verifier has completed:265,104 nodes,48,758 forced-equality leaves,
3,245,190 branches and19,094,383 relation implications, with1,113,806 CPU
milliseconds. The saved summary rechecks the complete gzip, node count,
footer, compressed hash, uncompressed hash and final verifier counts.
The all-group cases n=4,5,6 are now certified; the full arbitrary-n problem
remains open, and complete-problem candidate count remains15.

The n=7 generator is still live (PID43634, command and stdout checked),
with5,790,000 states at observation and its original10-million-state and
two-hour bounds. No incomplete certificate is counted or staged.
The19.20 order256 snapshot has54,559 counts,0 equalities,307 reversals,
3 verified live workers and13 completed ranges; all log checks pass.

## 2026-09-11T06:14:41Z — Candidate affirmative resolution of11.116

A digit-place reversal gives a fixed bijection C_(p^infinity)->N_0 under
which every coset of every subgroup is an interval. Distinct-prime primary
factors turn all cosets in D into boxes. The fibers of every H<=G in the
[G:D] fixed cosets are empty or cosets of H intersect D. Endpoint inclusion
therefore embeds the whole subgroup lattice in2r[G:D] chains; explicit
coordinate-priority linear orders realize its order. Finite groups are
handled separately. The proof covers nonsplit extensions and infinite H.

The source statement was visually checked. Shevrin2012's entire eight-page
survey confirms the definition, exact order-dimension convention, and the
prior necessity theorem, while stating our sufficiency assertion as open.
Limited later searches found no resolution; novelty remains unconfirmed.
The proof and a separate internal audit are written. Complete candidate
count is now16; externally reviewed new solutions remain0.

Python passes2,056 finite coset encodings and40,000 exact quasicyclic coset
comparisons, including whole-group cosets, with negative controls for
ordinary numerical order and repeated-prime diagonal subgroups. GAP passes
all792 subgroups,2,176 fibers and242,344 ordered pairs across six actual
groups, including generalized quaternion, mixed-prime and nonabelian
quotient cases. It checks both coordinate inclusion and the intersection
of the constructed linear orders. No failed initial run occurred.

The20.100 n=7 generator remains live at7,250,000 states with its original
10-million-state/two-hour bound; n=4,5,6 remain fully verified. The19.20
order256 snapshot has54,746 counts,0 equalities,327 reversals,3 verified
live workers and13 completed ranges. No pushes or external messages.

## 2026-09-11T06:22:29Z — Larger-certificate continuation and verification controls

Added exact certificate-prefix resumption. Prefixes of113 nodes at n=4 and
5,000 nodes at n=5 reproduce the independently verified complete files
byte for byte. An actual bounded stop at n=4 with46 completed nodes also
resumes to the same proof. New bounded runs explicitly report incomplete
status and omit the root footer. The current n=7 process still uses its
original loaded code and has not been restarted or modified.

Added a GAP checker that partitions nodes and stores component states with
a fixed presentation cache. Three parts at n=4 and5 reproduce every count
from the original verifier. The runner checks common hashes, every part's
completion, disjoint coverage and aggregate counts before writing VERIFIED.
A n=4 integration check passes. A deliberately false cross-part implication
is rejected by the root's part; the valid leaf's part passes locally,
confirming that a local PASS_SHARD is insufficient. Six planned workers
have8GiB workspace ceilings each, within the overall resource budget.

The n=7 generator was still live at8,510,000 visited states. No additional
fixed-n result is claimed. Candidate count remains16 from11.116 and the
earlier entries. See research/20.100-computation.md for continuation details.

## 2026-09-11T06:25:22Z — Checkpoint

Sixteen complete candidates are documented; latest11.116 and all-group
20.100 n=6 evidence are committed. The n=7 generator's actual command and
stdout remain verified, with8,880,000 visited states and its original
10-million-state bound. If it reaches the bound, reuse the completed prefix
as documented rather than discard its completed proof nodes. The new
partitioned checker has passed its controls but has not yet run at n=7.
The19.20 order256 search has55,003 counts,0 equalities,345 reversals,
3 verified live workers and13 completed ranges; all log checks pass.
Older unsuccessful leads and scope pitfalls are saved in
research/older-triage-2026-09-11.md. The48-hour goal remains active.

## 2026-09-11T06:48:58Z — Resumed n=7 and older-problem findings

The original n=7 generator stopped at its explicit 10-million-state bound.
Its closed gzip was fully read, with 9,999,993 complete consecutive nodes
and no root footer; hash and stop evidence are preserved in the bounded
summary. The original file and log were renamed, then a new process resumed
that prefix with a 30-million-state / 7,200-second bound. It has completed
loading and reached 10.78 million states. No n=7 proof is claimed.

For 12.56, graph counting and the classical Droms/Laurence rigidity theorem
prove F(n)=n^(Theta(n)), with explicit bounds on log F(n). A derivation and
separate internal review are saved. This is a quantitative partial answer;
priority is not established and it does not increase the candidate count.
For 13.12, Carette's exact prior Theorem 6.3 answers the whole question
affirmatively. Its proof and scope were checked and the exclusion recorded.

GAP 4.16.1 is revalidated. A first version-print invocation had a shell
printf escaping error, corrected using a literal heredoc; no research
calculation was affected. The order-256 search has 55,320 counts, no equality
hits, 357 reversals, two verified live workers and 14 completed ranges.
All live-log checks pass. Sixteen complete candidates remain pending review.
The goal remains active, with no pushes or external communications.

## 2026-09-11T07:04:42Z — Candidate counterexample to 14.72

Found an explicit smooth irreducible affine surface with cyclic action of
order four over C. The three equations give two line-bundle charts over
y^2=x^3-x. The full fixed scheme is a smooth affine line and an effective
Cartier divisor. The global invariant ring is proved, in all degrees, to
be C[a,v,d]/(v^2-(a-1)d), with an ordinary quadratic singularity at (1,0,0).
Its preimage is a two-point orbit with a proper order-two stabilizer. This
answers the printed global cyclic question negatively; it does not address
a prime-order or local-action restriction not present in that statement.
The codimension-one/hypersurface convention is explicit in proof and audit.

Python verifies five exact identities, 1,661 invariant monomials and 850
reverse normal-basis images. Independent GAP controls pass over five fields:
2,955 smooth surface points, 817 orbits, 101 full fixed points and 11,497
orbit-pair checks. Quotient gradients identify the single node in each
field. No failed run occurred. The finite controls supplement the proof.
Relevant 2013 prime-order literature is credited with exact reading scope;
novelty and outside review remain pending. Complete candidate count is 17.

The n=7 generator remains live at 13.15 million states; no n=7 proof is
claimed. Order-256 search: 55,483 counts, zero equalities, 357 reversals,
one verified live worker and 15 completed ranges. All log checks pass.
No external communications or pushes; the 48-hour goal remains active.

## 2026-09-11T07:08:17Z — Checkpoint and verification resource measurement

The 17th candidate, 14.72, is committed with its explicit global invariant
ring, internal review and independent finite-field controls. Added an
explicit no-localization-torsion sentence to the invariant-ring proof.
Unsuccessful 12th--15th Issue leads and their scope pitfalls are saved.

A resource-only GAP probe retains one million n=7 state objects, measuring
205,051,944 reachable bytes after 52.5 CPU seconds. This is not proof
verification and excludes the checker workspaces and runtime overhead.
The extrapolation and limits are documented before the planned larger
independent check. The bounded incomplete gzip stays preserved locally;
only its hash/stop evidence is committed, not an active or final proof.

The n=7 generator is verified live at 13.68 million visited states.
The order-256 search has 55,523 counts, no equalities, 357 reversals,
one verified live worker and 15 completed ranges. All log checks pass.
The 48-hour goal remains active; about 37 hours 48 minutes remain.

## 2026-09-11T07:53:51.331519+00:00 — Candidate affirmative solution to 21.40 and reporter integration

A self-contained argument proves that a subgroup of GL(n,Q) with finitely
many automorphism orbits has a normal torsion-free nilpotent subgroup of
class at most n-1 and index at most (2n+1)^(n^2). The key steps are actual
root towers from an abstract automorphism, bounded-degree algebraic
integers forcing root-of-unity eigenvalues, and the trace-pairing radical
in the rational span of the group. An explicit finite-module argument
proves the ideal bound R^n=0 without a finite-generation assumption on G.
The exact question was visually checked on page 173. Related primary
papers were inspected with their hypothesis and reading limits recorded;
novelty and outside review remain pending. Candidate count is now 18.

Python passes 72 rational Jordan root identities and 24 finite-order root
identities. Both Python and GAP compute the trace radicals in triangular
algebras through degree six and in the actual infinite finite-orbit
example A5 times Q, whose algebra has dimension 18, radical dimension 1,
and finite quotient of order 60. GAP independently checks Aut(A5), 546
trace pairings and 25 additional Jordan root identities. Negative controls
exclude the stronger whole-group-solubility and generator-only trace claims.

The 20.100 reporter now recognizes partitioned independent checks and
requires complete coverage plus validated aggregate evidence. All 19
status/corruption controls pass. One initially failing negative control
exposed a partial duplicate PASS_SHARD marker; the runner and reporter
now reject it. A fresh n=4 three-part integration run and a direct replay
through the reporter pass with 227 nodes and 3,953 relation implications.
This infrastructure is committed separately as b810372 and proves no
additional fixed-n case.

The last search snapshot has n=7 at 19.66 million visited states, still
generating, and 55,944 order-256 groups checked for 19.20, with zero
equality hits and 357 reverse inequalities. Actual commands and stdout
remain verified. Prior 7.31 was resolved affirmatively by Li--Zhu2024;
its theorem and Section 3 proof were read and the exclusion recorded.
No pushes or external communications. The 48-hour goal remains active.

## 2026-09-11T08:10:16.295646+00:00 — Candidate counterexample to 21.60 and completed 19.20 range

For G=C3 semidirect C4 with inversion action at p=2, every simple
F2G-module is a reduction of a simple QG-module. Thus every module class,
not just the projective indecomposables, satisfies the positive condition
printed in21.60. Nevertheless Z_(2)G maps onto a rational division
quaternion order O with J(O)=2O and O/2O=M2(F2). The nontrivial matrix
idempotents cannot lift. The resulting negative proof is self-contained,
with a positive norm proving division and an explicit rational simple lift.

This also conflicts with Proposition3.3 in the source preprint. Its
claimed general Ext^1 reduction isomorphism fails already for two trivial
C2-lattices over Z_(2); the source display was visually checked and the
obstruction documented. This is a mathematical discrepancy explicitly
addressed in the review, not an unexamined use of a conflicting theorem.
Exact prior searches found no matching resolution, but novelty remains
unconfirmed. Complete candidate count is now19, all pending outside review.

Both initial verification runs pass. Python checks6,561 norm/inverse
examples, all144 group products, all256 products of the reduced quaternion
algebra and all4,096 modular group-algebra elements. GAP independently
constructs SmallGroup(12,1), its quotient and matrix modules, all52
idempotents, radical powers7,2,1,0 and both four-dimensional projective
indecomposables. No broad character-table scan was needed.

All16 order256 workers for19.20 have completed. The final audit matches
every omitted ID with the22 abelian groups independently constructed from
partitions of8. There are56,070 nonabelian counts, zero equalities and357
reversals at order256. Together with the earlier range, this is62,588
nonabelian groups through256, with zero equalities and411 reversals. The
completion evidence and all log hashes are committed as16e2886. This
remains bounded evidence, not a general resolution.

The n=7 generator for20.100 remains active at21.73million visited states
in the08:02 snapshot. No n=7 proof is claimed. No pushes or external
communications; the48-hour goal remains active.

## 2026-09-11T08:19:48.826056+00:00 — New bounded search and prior-work checkpoint

Nineteen complete candidates are committed, including the new21.40
and21.60 proofs and their audits. The19.20 order256 computation is
fully aggregated, and all remaining controller logs/state are preserved.
A new eight-worker search covers the29,700 catalogue groups of orders
257–511 in356 disjoint jobs, using the unchanged exact counting kernel.
Each worker has a4GiB workspace cap. The33-hour limit leaves time before
the overall deadline; incomplete jobs cannot produce a complete summary.
At08:19 UTC,249 jobs are complete,4,160 nonabelian groups counted,
457 abelian IDs skipped, and no equality or reversal found. All log,
source-hash and process-identity checks pass. Completed logs are committed;
active logs remain local and are not treated as final evidence.

The n=7 generator for20.100 has reached24.16million states at08:19 UTC,
remaining under its30million-state /7,200-second continuation bound.
It is still generating. If the bound is reached, preserve the closed
incomplete prefix and resume as documented; no unchecked n=7 result
may be promoted to a proof.

A6September2026 preprint gives the exact prior affirmative claim for
11.124. Its full proof was read, and the earlier recovery lead is now
excluded from new priority. No outside communications or pushes.
About36hours37minutes remain in the active48-hour goal.

## 2026-09-11T08:48:07.659647+00:00 — Twentieth candidate and preserved search checkpoint

Problem4.55 has a complete candidate negative proof for G=3.A7,p=5.
Four modular multiplicities satisfy a+d=b+c. Rational descent after
multiplication by168 gives projectives on four different rays; equal
reductions give a rank55,440 isomorphism with incompatible indecomposable
refinements. This addresses uniqueness itself and allows arbitrary Schur
indices. The actual group, ordinary table, twelve faithful modular
irreducibles and fourteen decomposition rows were independently checked
by GAP. Python independently verifies the field arithmetic, order7560
matrix group, absolute irreducibility, and all28,561 bounded multiplicity
vectors. Both final controls pass. The first Python run rejected invalid
JSON formatting before any mathematical check; the export was corrected.
Proof, review, scripts and matrix evidence are retained. Novelty and
outside review remain pending.

The n=7 generator for20.100 stopped at its explicit time bound, leaving
26,317,076 closed nodes. After its exit, the second incomplete prefix was
preserved and fully read with consecutive IDs and hashes verified. A
new one-CPU continuation started at08:40 UTC with60-million-state and
18,000-second bounds. It remains incomplete and is loading the prefix.
The old prefix remains intact; no partial certificate is a proof.

The19.20 extension has completed292 of356 jobs at08:46 UTC, with13,922
nonabelian counts,505 abelian skips, zero equalities and four reversals.
All eight live workers and all logs pass the provenance checks. The
4.55 table screen is exploratory and still incomplete; the proved
example was audited separately. No pushes or outside communications.
About36hours10minutes remain in the active48-hour goal.

## 2026-09-11T09:15:45.657904+00:00 — Countable topology counterexample and completed table screen

Problem 21.107 now has a complete candidate negative proof and internal
audit. A free ultrafilter supplies the standard coordinate-subgroup
topology on a countable Boolean group. Support cardinality gives an
explicit countable dense partition; the finite-fiber maximum-support
map and one ultrafilter choice rule out every expansive sequence. The
argument also works in exponent three. No selective ultrafilter, CH,
or numerical verification is used. Printed page 183 was visually
checked, and the standard Mathias topology was identified in a primary
publisher reprint. Novelty remains unestablished. Candidate count: 21;
externally reviewed new solutions: 0.

The 4.55 screen stopped at the trivial table because FactorsInt(1)
returns [1]. The error was corrected, its completed first 2,600-table
range preserved, and the final 150 tables independently rerun. The
aggregate covers 2,750 table names and 7,573 available modular cases,
with 840 rationality flags and 265 parity flags. These are exploratory
constraints, not new counterexamples. Both GAP processes exited; logs,
hashes, and a reproducible aggregation checker are retained.

The n=7 search for 20.100 finished loading its 26,317,076-node
incomplete prefix after 1,562 seconds and resumed generation. At09:14
UTC it has reached27.3million visited states, using about17GiB. The
19.20 extension has completed310 of356 jobs and counted18,939
nonabelian groups, with zero equality hits and four reversals. All
process/log checks pass; both searches remain incomplete. The main
remaining running workload uses nine CPUs, within the resource limits.

A relevant August prior claim for21.123 is documented with its
formulation caveats and unaudited main proof. Pro-p identity and
strongly regular graph scope corrections are saved in the triage log.
All changes remain local; no pushes or external communications. The
48-hour goal remains active until2026-09-12 20:56:46 UTC.

## 2026-09-11T09:50:04.026747+00:00 — Three prior-theorem deductions and live search checkpoint

Published theorems imply an affirmative answer to5.15 and negative answers
to12.11 and13.39(f) in nonabelian rank. The exact deductions are written,
with Notebook pages15,58,69 visually checked, source hashes retained,
and imported-proof reading limits stated. The fourth-power equation,
not the square equation, supplies the rational-group tree obstruction.
An exact August2026 prior claim for11.46(a) is recorded without claiming
audited tensor computations. A2022 matrix regularity theorem removes
more8.3 parameter ranges from useful search. New-candidate count stays21.

At09:47 UTC the19.20 extension has334 of356 completed jobs,24,850
nonabelian counts,507 abelian skips, zero equality hits, and four reversals.
Eight verified workers remain live. The20.100 n=7 generator has reached
31.78million visited states at about18.4GiB RSS. It has no completed proof
certificate yet. Both process/log checks pass, and the workload remains
within the nine-CPU main-work budget. Completed logs are checkpointed
locally; live and incomplete certificates remain explicitly unproved.

No push or outside communication. The48-hour research goal remains active
until2026-09-12 20:56:46 UTC.

## 2026-09-11T10:13:21.687327+00:00 — Completed integral-centre screens and square-obstruction analysis

For14.2, all2,750 named tables and16,146,897 rational-character pairs
were screened;682 integral swaps are all monomial. The single-block
extension covers249 mixed-degree conductor blocks and21,646 degree-changing
permutations, with no integral maps. Both processes exited zero. Independent
full-matrix inversion controls and503 actual class-product checks pass.
The complete ordered manifest, totals, scripts and raw-log hashes are
audited. These restricted exclusions do not solve the general problem.

For14.3, the exact obstruction is q(u)=u(u*)^-1 modulo squares of Z(G).
A real-character condition and an odd-conjugacy-class square-root condition
are proved. The latter gives finite nilpotent groups as a positive subclass,
without a novelty assertion. The primary2018 RS-property paper proves the
weaker norm exact sequence; its Theorem13 proof was fully read, and it is
not misclassified as the requested factorization. The table screen remains
in progress. The complete-candidate count stays21.

At10:12 UTC,19.20 has348/356 completed jobs,28,081 nonabelian counts,
511 abelian skips, zero equality hits and33 reversals; eight workers remain
verified live. The20.100 n=7 generator has35.16million visited states and
about19.5GiB RSS, with no complete certificate. Both provenance audits pass.
All work stays local; no push or outside communication. Goal deadline
remains2026-09-12 20:56:46 UTC.

## 2026-09-11T10:35:54.108802+00:00 — Central-unit criteria and fixed-rank versus uniform distinctions

The14.3 combined criteria are complete on all2,750 named tables.
Real characters exclude all central nonsquares in2,739 names; all13
survivors in11 names fail the odd-class square-root test.19 actual-group
controls,187 independent Frobenius--Schur indicators, and84 central
nonsquare checks pass. The parity proof also gives every finite group
with a normal Sylow2-subgroup. General14.3 remains unresolved.

The fixed-rank answer to14.15 is infinity by two published theorems;
the exact deduction and a quasimorphism lower bound are retained.
For14.24, the prior14.23 family has a conjugate of norm two and an
exact minimal conjugator norm r in rank2r-1. This disproves a rank-uniform
bound, while leaving the fixed-rank question unresolved. All11,172
GAP generator equations and38 fixed-lattice controls pass. Attribution
and quantifiers are explicit; the complete new-candidate count stays21.

The19.20 extension is down to two live jobs, with354/356
completed and29,173 nonabelian counts at10:34 UTC. No equality
hit has appeared. All514 abelian IDs were reconstructed independently
from partitions of prime exponents; the final full-coverage checker is
prepared but must await the last two jobs. The20.100 n=7 generator
continues with no completed certificate. All actions remain local,
with no push or outside communication. The48-hour goal remains active.

## 2026-09-11T10:39:27.384522+00:00 — Final audit handoff for19.20

At10:38 UTC,355/356 jobs are complete. The remaining job has counted
through order384 ID20167; ID20168 is still running and the last abelian
ID has not yet been logged. There are29,185 nonabelian counts,513 skips,
zero equalities and58 reversals. No complete through511 claim is made.
A one-hour bounded watcher will run the independent skipped-ID audit
and the disjoint-range aggregation when the final job exits successfully.
It writes local results only; review and Git commit remain separate.
The n=7 generator has38.42million states at10:35 UTC and no footer.

The14.24 deduction also makes the asymmetry explicit: its reverse
minimal conjugator norm is two, while the forward minimum is r. The
proof and updated hash are retained. Main ongoing computations now use
two CPUs, plus the negligible audit watcher, within the resource limits.

## 2026-09-11T10:41:00.060326+00:00 — Completed19.20 coverage through511

The last job finished while the audit watcher was being launched.
All356 jobs and the controller exited successfully. The watcher ran
both final audits immediately and exited zero at10:39:27 UTC.
All29,700 extension IDs are covered exactly; all514 abelian skips match
the independent classification-based reconstruction. The extension
has29,186 nonabelian counts, zero equalities, and58 reversals.

The three disjoint completed ranges therefore cover every one of the
91,774 nonabelian groups through order511: zero equality cases and
469 reverse inequalities. All source-summary hashes agree. This does
not solve the arbitrary finite-group equality question. The final
logs, state and audits are now retained locally.

The20.100 n=7 generator remains the only main running computation,
with39,160,000 visited states at10:40 UTC and no completed proof
certificate. The21 complete new candidates still await outside review
and further novelty checks. No pushes or outside communications.
The research deadline remains2026-09-12 20:56:46 UTC.

## 2026-09-11T10:52:35.636471+00:00 — GAP recheck and prior answer to14.59

Confirmed the user-provided GAP4.16.1 installation through bin/gap.
The20.100 n=7 generator remains verified live, with40,540,000 states
at10:50 UTC and no complete certificate. The complete Tent2016 paper
was read and its construction checked against printed14.59: countable
sharp3-transitivity, torsion-free two-point stabilizers and no Klein
four subgroup give a negative answer. This is credited prior work and
the new-candidate count stays21. Beginning14.67 structural reduction
and a bounded exact search; no general resolution is claimed.
All work remains local, with no push or outside communication.

## 2026-09-11T11:07:14.465738+00:00 — Prime-class theorem and completed14.67 search

The14.67 search exited zero at10:57:59 UTC. Its independent catalogue
and final coverage audit pass:92,803 nontrivial groups through511,
58,967 prime-power cases covered theoretically,33,836 other IDs
processed, including721 centreless groups. All14,500 eligible classes
and29,989 overgroups pass. Independent direct controls exited zero:
147 groups,1,966 element classes,67,289 literal subgroup cases,
1,321 positive and645 negative predicate controls.

A complete partial theorem now proves14.67 whenever the minimum
nonidentity class size is prime, without a solubility hypothesis.
The proof uses a cyclic regular conjugacy action, an outer-automorphism
argument and a last-vector calculation in characteristic r. The exact
hypotheses and eleven logical checkpoints were audited. Moretó2023
already states a related soluble prime case in its primary abstract;
its full proof was unavailable, so no novelty or new complete candidate
is asserted. The complete new-candidate count remains21.

At11:06 UTC the20.100 n=7 generator remains verified live with
42,710,000 visited states and about21.8GiB peak RSS.
No n=7 proof or completed certificate is claimed. Next work should
prefer structural composite-class arguments or other unresolved entries
over repeating completed small catalogues. All artifacts and commits
remain local. The48-hour goal is active, ending2026-09-12 20:56:46 UTC.

## 2026-09-11T11:39:59.169233+00:00 — Completed n=7 generation and a limit of the14.3 tests

The20.100 generator exited zero with42,891,332 states,5,435,268 leaves
and786,577,344 edges. Full gzip preflight and a separate full reporter
read pass. The canonical summary now reports VERIFYING: six independent
GAP workers, started11:12:29 UTC, and no completed shard. The unchanged
mathematical checker is bound to the full certificate by both hashes.
Six14GiB workspace ceilings give84GiB combined, about90.2GB before
process overhead. The earlier generator and other main searches are
finished. A two-worker n=4 integration run exits zero with unchanged
mathematical counts; a seven-by-fourteen-GiB request is rejected before
artifacts. All19 prior adverse reporter controls pass. A new progress
snapshot checks live commands/stdout, hashes, partition state and RSS
without repeatedly decompressing the complete certificate. No n=7 proof
is counted until every worker and the aggregate pass.

For14.3, the central product of semidihedral16 with Dic3 identifies
their central involutions and gives SmallGroup(96,123). Its central
nonsquare passes both real-character and odd-class-root criteria,
so those criteria are jointly insufficient to force a central square.
Nevertheless a degree-four character with field Q(sqrt(-2)) forces
every central integral unit to be symmetric: its scalar and inverse
are algebraic integers, hence units in that imaginary quadratic field,
whose only units are plus or minus one. The group, character and
number-field arguments are written with a logical audit. Independent
GAP checks on the actual96-element group, including21 direct
Frobenius--Schur indicators, pass with actual exit0. This is a positive
example and a limitation of a method, not a new complete resolution.

The complete-candidate count remains21, with outside review and further
novelty checks pending. All artifacts and commits remain local. The
48-hour goal remains active through2026-09-12 20:56:46 UTC.

## 2026-09-11T11:52:42.047116+00:00 — Twenty-second candidate: a four-regular counterexample to15.89

On G=C3*C2, S={aba,aba^2,a^2ba,a^2ba^2} is an inverse-closed
four-element generating set with no identity or repetition. Its Cayley
graph is infinite, connected, simple and vertex-transitive. For right
translations U=R_a+R_a^2 and B=R_b, the adjacency is U B U, while
U^2=U+2I and B^2=I. Thus (U-I)B(U-I)/4 is an inverse on every
complex-valued function, since it is a sum of only nine translations.
Zero is therefore not an eigenvalue, answering the printed question
negatively. The supplied page94 was visually checked.

Python checks exact free-product convolution,1,500 local coordinate
identities and a removed-edge negative control. Independent GAP uses
integer projective matrices, both inverse products, and actual finite
Cayley graphs of orders12,60,168 with63,936 identity-matrix entries.
Both processes exited zero. The complete proof, internal audit, all
control artifacts and a hash-binding summarizer are retained.

The zig-zag product is credited to Reingold--Vadhan--Wigderson2002;
Definition3.1 and the matrix factorization were read directly. The
finite-factor invertibility discussion in Cavaleri--D Angeli--Donno2019
was also read and credited. Trofimov2024 examples8.4--8.5 were checked
again; they do not supply this complex vertex-transitive counterexample.
The primary abstract of the2025 follow-up was located, but its full
paper was not obtained. No general novelty claim follows from these
limited checks. The complete-candidate count is now22, all awaiting
outside review and further priority work. The earlier positive
dihedral subclass remains valid.

The20.100 n=7 verifier remains live in all six partitions. At11:47 UTC
each had checked250,000 nodes, collectively1.5million, with about3GB
combined actual RSS. No shard or n=7 proof has completed. The48-hour
goal remains active through2026-09-12 20:56:46 UTC. All work and Git
commits remain local, without pushes or outside communications.

## 2026-09-11T11:55:05.953010+00:00 — Retained exploratory scope and progress checkpoint

Recorded the limited primary-source readings and failed shortcuts for
14.97,15.11,15.9 and15.22 so future passes do not reuse unproved steps.
For19.20, proved coprime direct-product multiplicativity of both counts
and searched the85,260 explicitly recorded group counts for reciprocal
coprime ratios. There are70,983 distinct nonunit ratios,417 reverse
groups and no such pair. The input hashes and exact available-record
coverage are retained; this is not full enumeration of all products.

The latest20.100 snapshot at2026-09-11T11:55:05.900210+00:00 verifies all six
workers live with no completed shard. The complete-candidate count
remains22, with15.89 the latest addition. No pushes or outside
communications; the48-hour goal remains active.

## 2026-09-11T12:12:57.818053+00:00 — Twenty-third candidate: exact palindromic length for 16.9

The free basis embeds by x_i=s_i s_0 in the free product of n+1
involutions. Multiplying a palindrome by s_0 gives precisely a
reflection. Alternating the basis-inverting automorphism yields the
exact formula pl(w)=min(r(w),r(w s_0)). A self-contained noncrossing
pairing proof identifies reflection length with the fewest deleted
positions needed to leave an identity word. Interval dynamic programming
therefore computes the exact minimum in cubic time and quadratic
storage, and its traceback returns a minimum palindrome factorization.
The source statement on printed page 97 and every algebraic convention
were audited.

Python compares the pairing recurrence with all deletion subsets for
9,841 involution words, then checks all 36,558 reduced free words in the
stated rank/length ranges against the separate Frid two-palindrome
criterion. Known exact families and 100 longer random inputs bring the
witness count to 36,698. Independent GAP evaluates all witnesses in an
actual free group of rank 22, checks reduced palindrome factors and
products, and confirms the parity lower bounds. Both processes exit
zero. The separate summary checks exact exhaustive input coverage,
markers, counts and source/artifact hashes.

The reflection deletion principle is prior Dyer work, read as reproduced
in Lotz 2024 and credited. Its original AMS proof was unavailable;
our needed special case is proved directly. Frid 2025 discusses the
general algorithm question and supplies the two-factor comparison.
Further novelty checks and outside review are pending. The complete
candidate count is now 23; no externally reviewed new solution is
claimed. The six long-running 20.100 n=7 GAP partitions continue, with
no completed n=7 proof. All work and commits remain local. The active
48-hour goal ends 2026-09-12 20:56:46 UTC.

## 2026-09-11T12:22:32.934799+00:00 — Bounded exclusions for 16.46

All 19 listed finite targets completed, with 9288 conjugacy-reduced A,B pairs and 21648 cube-compatible triples, and no nontrivial homomorphism. The exact reduction uses the independence of C,D,E,F; it allows coinciding images. K has trivial abelianization, verified from its 22 relators. Independent Python literal permutations match every recorded count for A5,A6,A7 and perform 35,904 expanded-relator checks. Both processes exited zero; coverage and hash audits pass. Printed page 101 was visually checked. These are bounded exclusions only, with no new complete candidate or novelty claim. The complete count remains 23.

## 2026-09-11T12:33:35.539956+00:00 — Twenty-fourth candidate: both assertions of 18.18

Completed the previously missing complement reduction. An explicit fixed
first-order sentence reconstructs points from four mutually noncommuting
involutions and their incidence sets, and its finite models are exactly
S_n for n>=5. A trivial-common-centralizer axiom makes the reconstructed
action faithful; all transpositions then force the full symmetric group.
Separately, two permutations on H x {0,...,|H|-1} have common centralizer
exactly the left regular H. Padding with a larger symmetric orbit gives
that centralizer in every S_n after 2|H|^2+3. These are self-contained
lemmas, without a classification theorem.

For input phi, (not sigma) or (exists a,b not phi^C(a,b)) is cofinite
exactly when phi fails in some finite group. Together with the earlier
universal-centralizer reduction, Malcev non-enumerability proves both
assertions. The witness H is needed only in the correctness proof,
not in the effective sentence transformation. The interpretation of
almost all is explicitly cofinite up to isomorphism, not density.

GAP verifies six positive incidence cases, twelve negative involution
classes, and all 14 base plus 28 padded centralizers for groups of orders
through eight. Independent Python literal permutations, 3,624 group-table
associativity checks and exact point-image propagation agree. Both final
processes exit zero. Two earlier GAP control runs were stopped incomplete;
diagnostics exposed redundant negative-case enumeration, replaced by an
exact three-endpoint rejection. Their logs and source hashes are retained
and excluded from pass evidence. The final summarizer audits markers,
counts, independent agreement and artifact hashes.

The primary Malcev theorem and the limited classical permutation-theory
reading are recorded precisely. Further priority checking and independent
outside review remain pending. The complete candidate count is now 24.
The 20.100 n=7 independent verification continues; no n=7 theorem is
claimed. All work and commits remain local, with the 48-hour goal active
through 2026-09-12 20:56:46 UTC.

## 2026-09-11T12:46:39.767646+00:00 — Prior compact word-map consequences

Recorded exact negative deductions for the SO(3,R) case of 16.68 and
16.69(b) from Thom Corollary 3.3. The quaternion argument first proves
both exponent sums vanish; central positive scalars then cancel, and
the norm estimate forces real part at least 7/8 for every nonzero pair.
These are prior results, excluded from the 24 complete new candidates.
The supplied page, source reading limits and cached hashes are retained.
The two PSL2 cases and real trace question remain unresolved here.

At 12:44 UTC all six 20.100 n=7 GAP shards were verified live, with
3,670,000 nodes checked and about 6.04 million KiB combined RSS. No
shard had completed. Full-certificate hash binding still passes.
The 48-hour goal remains active; all work and commits remain local.

## 2026-09-11T13:03:32.629553+00:00 — Complete prior consequence for 17.87

Let P be the infinite simple finite-index derived subgroup of
Nekrashevych's explicit 2018 intermediate-growth group. Its universal
central extension U=Fprime/[F,R] is perfect and finitely generated.
A second universal extension, the central commutator argument and
universality prove H2(U,Z)=0. A direct block-counting proof shows that
central extensions with finitely generated total group preserve
subexponential growth even for infinitely generated kernels, a special
case of Zheng 2020. The quotient P excludes polynomial growth.

This settles the printed construction request as a short consequence
of prior ingredients; no new priority or outside review is claimed.
The complete new-candidate count remains 24. Source reading scopes,
exact hashes and a ten-point logical audit are retained. Early-afternoon triage
also records the full/stable linear-group distinction in 16.94, the
finite/torsion distinction in 17.31, RCWA presentation limits, and
the literal all-groups-variety exception to 17.85. No false general
conclusion is imported from those leads. The 48-hour goal continues
and the six 20.100 n=7 verification workers are preserved.

## 2026-09-11T13:24:27.614301+00:00 — Exact prior answers and the root-amalgam audit

Located and recorded Sela Theorem 8.1 for 17.48 and Wilkens's 2017
main theorem explicitly answering 18.56. The source reading scopes
are limited: no independent full audit of either long proof, and no
algorithmic inference from Sela's noncanonical reduction for 17.117.

An independently considered unbounded-root amalgam proved to be
Allenby's exact 2000 Theorem 4. For generators a_n with a_n^n=z,
lambda(G)=mu(G)=H=<z>, an infinite cyclic group. This gives prior
negative answers to 19.4(a),(b) and 19.5. A separate coset-exponent
argument checks the essential lower bound for arbitrary subgroups.
All six pages of Allenby were read, with its older upper-bound input
explicitly remaining an imported theorem. Azarian's 2011 survey both
reproduces this theorem and lists the later Notebook questions.

Printed pages 110,123,132 were visually checked; source and artifact
hashes, a ten-point audit, and further triage limits are retained.
No new complete candidate is added: the count remains 24, all pending
outside review and broader novelty checking. The 48-hour goal remains
active through 2026-09-12 20:56:46 UTC; work and commits remain local.

At 13:23 UTC all six 20.100 n=7 verification workers remain live,
with 4,970,000 nodes checked and 7,824,116 KiB combined resident
memory. No shard has finished; the certificate remains unproved.

## 2026-09-11T13:37:36.216447+00:00 — Near-Frattini source audit and further prior deductions

Recorded prior affirmative deductions for 19.3(a),(b),(c),(e),(f),
using Allenby 1999–2005, an explicit retraction argument, and Hall's
finite-index free-factor theorem. The free-factor argument covers
arbitrary free-group ranks. For standard nontrivial product/cable
knots in 19.1, cyclic upper bounds and a checked abelian pushout
identity give psi=1. Proper-amalgam and degenerate-knot conventions
are explicit. Two errors in unrelated 1994 proof arguments were
confirmed visually and excluded from the deductions.

Allenby 2005 Section 4(7) already states the exact nilpotent assertion
in 19.6(a); its specific older proof adaptation remains unaudited.
The general 19.3(d) and 19.6(b) cases remain unresolved here. The
original 1999 upper-bound dependency for the earlier root-amalgam
note has now been read; earlier ordinary-Frattini dependencies remain
partly unaudited. No additional candidate is counted: 24 remain,
all awaiting outside review and broader novelty checks.

At 13:32 UTC all six 20.100 n=7 verification workers were live,
with 5,320,000 nodes checked and 8,164,596 KiB combined RSS.
No shard had finished. All work and commits remain local; the
48-hour goal continues through 2026-09-12 20:56:46 UTC.


## 2026-09-11T13:59:10.577429+00:00 — Hall–Higman refutes the printed 21.55 normalization

For every p-element in GL(n,p^f), (x-I)^n=0, so its order divides
p^ceil(log_p(n)). Hall–Higman's non-Fermat odd-prime exponent
bound therefore gives m_n(7^f)<=ceil(log_7(n)), and the proposed
ratio has upper limit at most 1/log_2(7)<1. The coarser theorem
also rules out every p>=5. The printed base 2 was visually
confirmed. Exact source hypotheses and a ten-point logical audit
are recorded; the original long Hall–Higman proof is imported.
This is a prior-theorem consequence, excluded from the 24 possible
new resolutions, all still pending outside review and novelty work.

Recorded detailed source reading scopes for 19.22, 19.26, 19.30,
19.33, 19.34, 19.42 and 21.56. The 2026 finite-fiber and fixing-size
papers retain additional hypotheses; no general answer is claimed.
Published character-restriction searches already cover substantial
small-group and simple-group ranges, so no redundant run was started.

At 13:53 UTC all six 20.100 n=7 GAP verification workers were live,
with 6,040,000 nodes checked and 9,214,196 KiB combined RSS.
No shard had completed. Work and commits remain local; the active
48-hour goal continues through 2026-09-12 20:56:46 UTC.


## 2026-09-11T14:31:10.119041+00:00 — Complete affirmative candidate for 19.56

The hyperfocal theorem supplies primary-input Sylow generation in a
perfect group. The order hypothesis then centralizes the Frattini
subgroup of a smallest nonsoluble example. In its minimal-simple
central quotient, explicit local matrix subgroups give a restricted
commutator mapping to an involution. Baer–Suzuki and an abelian cyclic
preimage produce a forbidden pair. No quotient inheritance or closure
of commutator values under powers is assumed. Fourteen logical audit
points and exact source-reading limits are recorded.

All 586 groups through order64 plus seven named cases were checked:
159,220 primary-input pairs and843 Sylow generation equalities pass.
The 24 matrix examples,17,472 Suzuki additive identities and three
central lifts pass. Seven independently constructed Python groups
agree exactly, with176,580 multiplication entries and twelve extra
prime-field controls. The initial trivial-group run failed despite
GAP returning OS status zero; its script/log/record are preserved and
excluded. The final clean run, completion markers, hashes and coverage
all pass.

Monakhov's soluble restricted theorem and ordinary-commutator theorem,
and Bastos–Monetta's unrestricted coprime theorem and local strategy,
are credited. None of the inspected statements directly gives the
Notebook's weaker hypothesis. The portfolio now has25 complete
candidates; outside review and further priority checking remain pending.

At14:21 UTC all six20.100 n=7 workers were live, with7,010,000 nodes
checked and10,343,156 KiB combined RSS. No shard had completed.
The 48-hour goal remains active through2026-09-12 20:56:46 UTC.


## 2026-09-11T14:37:19.259794+00:00 — Prior computable-coefficient obstruction for19.60

A classical Stoltenberg-Hansen–Tucker field F has decidable equality
and arithmetic but undecidable roots of unity. The computable
Euclidean PID F[t] therefore admits no free-generation algorithm
even for the one-matrix tuple diag(a,a^-1) in SL2. The effective
reduction, ten-point scope audit, exact source dependencies and
repair of an unneeded auxiliary source error are recorded. This
settles the literal unrestricted-computable-coefficient reading,
not the familiar integer or rational matrix-group problems. It is
a prior consequence and leaves25 possible-new candidates unchanged.
The12-page original CWI preprint was read in full; the final1980
typeset version was not obtained. All work remains local.


## 2026-09-11T14:48:13.116022+00:00 — Exponent qualification for 20.18 and source triage

The class-two collection identity proves exp(G') divides 2^(k-1)
whenever exp(G) divides 2^k. The printed universal exact-derived-
exponent request therefore fails at p=2. The other convention makes
the derived condition redundant and is already asserted in Budkin
2020; only its primary abstract was read. A sharp unitriangular
example, ten-point logical audit and PDF image are retained. This
formulation qualification leaves 25 possible-new candidates unchanged.

Recorded further source limits for 20.19 and older leads. In particular,
a lattice in a product of trees does not automatically supply the
free or hyperbolic group required in 20.19. The active 48-hour goal
continues, with no outside communications or pushes.


## 2026-09-11T14:57:31.983735+00:00 — Exact prior P-character result and source boundaries

Lu 2025 Theorem A answers the remaining direction of 20.80. Its
five-page preprint was read, and the short proof was checked with
an explicit correction to a reversed kernel sign. This is prior
work, leaving the 25 possible-new candidates unchanged. Recorded
why the weaker Frobenius-ratio inequality and selected maximal
abelian-normal-subgroup bounds do not settle 20.86 or 20.75–76.

At 14:55 UTC the six 20.100 n=7 workers were all live, having
checked 8,150,000 nodes with combined RSS 12,153,076 KiB. No shard
had completed, and no n=7 proof is claimed. Work remains local.


## 2026-09-11T15:22:40.102887+00:00 — Candidate 26: uniform large-prime brace average

Completed a proof of 20.92(a): classical affine matrix Lazard gives
a pre-Lie product on the original additive space, and k residual
corrections give a polynomial inverse for the exponential translation
map. Its dimension-only degree bound lets the printed base-2 average
extract precisely the linear term, without strong nilpotence.
Trappeniers' correspondence, correction and Fourier techniques are
explicitly credited; part (b) is not counted again.

The 20-point internal audit and controls pass: 17,667 actual affine
group elements, 303 inverse inputs, three formal polynomial examples
and 23,328 literal modular entries. Non-right-nilpotent examples and
small-prime averaging discrepancies are retained. An initial
associative-control indexing error was caught, repaired, and its
failed evidence preserved. All 25 packet files are hash-bound.
There are now 26 complete candidates, none externally reviewed;
comprehensive novelty verification remains pending.

At 15:16 UTC all six n=7 GAP verifiers were live at 8,880,000 nodes
and combined RSS 13,228,276 KiB. No shard had completed. Work remains
local, with no pushes or outside communications.


## 2026-09-11T15:43:18.558188+00:00 — Cancellation consequence and a saturation screen

Recorded 4.56(b)'s module-isomorphism conclusion as a consequence of
Bass 1964 Theorem9.3. Local projectivity, the Euler-class homomorphism,
and arbitrary free-cover kernel ranks are proved explicitly; the
printed literal-equality issue and unresolved part(a) are separated.
This is prior machinery, keeping the complete-candidate count at26.

For 20.112, read the entire 11-page source preprint and tested F=N^3
on all8,339 groups of orders648,1296,1944. No saturation failure
occurred;12 cases required both normalizer-chain computations. Actual
exit0, clean log, coverage rows and final sentinel are hash-audited.
These computations remain exploratory, and the general question is
unresolved. Existing n=7 workers continue; no communications or pushes.


## 2026-09-11T15:58:42.804608+00:00 — Diagonal elements and maximal-rank overgroups

Completed an affirmative deduction for7.27 using Fulman--Guralnick
Theorem3.2. The selected diagonal element has regular n!-th power;
this places the algebraic split torus in every remaining connected
overgroup. Type-A root groups then give coordinate blocks. The
argument treats all proper irreducible subgroups simultaneously and
works in every characteristic with n fixed and q sufficiently large.

The author manuscript was checked against the initial arXiv copy;
source scopes, algebraic versus finite torus distinctions, centre
issues, descent and an internal audit are explicit. This is recorded
as a complete consequence of prior machinery, leaving26 possible-new
candidates and zero outside reviews. No computation is asserted to
prove the asymptotic theorem. Long n=7 verifiers continue locally.


## 2026-09-11T16:20:57.114239+00:00 — Countable universal periodic locally nilpotent group

Completed the last named case of8.78 from Maier1981: each countable
locally finite p-group embeds in its unique countable existentially
closed extension type, and the restricted product over primes is
universal and remains countable periodic locally nilpotent. The
extension schedule and primary decomposition are proved explicitly.
Leinen1986 pages191--194 and the exact theorem on page192 were
checked, with the latter visually checked. Maier's original proof
is an imported input and was not read. Locally soluble8.78 remains
unresolved; possible-new count stays26, outside reviews0.

The six n=7 GAP workers remain live. At16:18 UTC they reported
10,970,000 nodes collectively and15,625,460KiB combined RSS; no shard
was yet complete. The certificate hash continues to match.


## 2026-09-11T16:25:00.070845+00:00 — Integral p-adic factorization for9.55

Recorded a complete negative consequence of Weiss1988 Theorem2.
The double-action lattice is free over its normal left G factor,
and its invariants are the rank-one trivial quotient module. Weiss
supplies a permuted integral basis; a trace argument makes that
basis one regular G-orbit and its chosen vector an integral unit.
Both composition orders are checked explicitly. Centrality is not
needed. The exact criterion was read in BKL2020 Remark1.8 and
visually verified; Scott1990 was read in full for attribution.
Original Weiss and Roggenkamp--Scott proofs were not independently
read. This is prior work, keeping26 possible-new candidates.


## 2026-09-11T16:36:08.630092+00:00 — Candidate27: scattered compact obstruction for9.47

The original Protasov1986 Lemma2 supplies the missing containment
neighborhood fact. After reading its antecedent in Komarov--Protasov
1981, expanded the compact-family proof in full: an assumed failure
creates an infinite closed discrete family inside a compact space.
Thus every compact family of noncompact subgroups has a clopen
selector. Dow--Watson1990 supplies a height-four compact without one;
its full topology, almost-disjoint coding, derived sets and diagonal
contradiction are now written explicitly. The counterexample itself
is prior and credited; the connection to9.47 is a possible-new
application pending novelty checks. The positive direction is also
proved using a discrete abelian group and both Vietoris subbases.

Twenty-seven audit points and exact source reading scopes are
recorded. No finite computation is substituted for this uncountable
topological proof. There are27 complete candidates and0 outside
reviews. At16:34:59 UTC all six n=7 verifiers remained live, with
11,500,000 nodes checked and16,316,148KiB combined RSS. Local work
and local commits only; no communication or push.


## 2026-09-11T17:06:25.266932+00:00 — Candidate28: coordinate criterion for9.45

Every orthogonal rank-one summand is represented by a centered cyclic
coset vector, with at most two half-coordinate ties. Membership of
its normalized dual vector is exactly two integer-divisibility tests.
All passing lines are automatically perpendicular; n passing lines
therefore give a lattice basis. The resulting coordinate-only test
takes O(mn) arithmetic work for denominator m. The full proof and
28-point internal audit are written. Bardakov's prior n=2 answer,
CGG's normalized-dual method and classical decomposition context are
credited. Historical priority and outside review remain pending.

Independent exact searches agree on3,520 cases (599 positive). GAP
checks1,198 HNF basis equalities and independently examines291,330
box points in274 cases. The incorrect handwritten m=6 residue was
corrected after both searches rejected it; the failed log is retained.
A first GAP run with unbound-global warnings was rejected despite its
sentinel and exit0; the corrected local-variable run is clean and0.

At17:02:42 UTC the six n=7 certificate workers remained live with
12,400,000 total checked nodes and17,640,692KiB combined RSS. No
shard was complete. Work and commits remain local only.


## 2026-09-11T17:15:50.515703+00:00 — Later triage and definition checks

Recorded unresolved9.1,8.4,9.65 and neighboring routes in
`research/triage-2026-09-11-late-afternoon.md`. Corrected two
potentially misleading research notes: Cameron's base-two version
of9.70 is equivalent to the Notebook stabilizer-order alternative;
the weaker condition concerns a regular induced constituent with
a possible kernel. The downloaded source is the1975 proceedings
chapter, not the1981 Bulletin survey. Cameron's current page dated
May2026 still lists the base-two conjecture.

For10.8, Schneider--Thom2018 explicitly warns that the natural UEB
group-ring multiplication is jointly continuous exactly for SIN
groups. Dobrowolski2015 supplies a non-Hausdorff action obstruction,
but no reduction from an arbitrary ring embedding to that particular
permutation module was obtained. No additional result is counted.


## 2026-09-11T17:34:57.076226+00:00 — Problem 10.62 periodic candidate

Recorded the twenty-ninth candidate: apply Amelio's 2025 Theorem 6.7 to
C2*C2*C2, rescale so abc is selected in the first quotient, and impose its
p-th power. Every finite stage is tame. A finite multiplication-table
lifting lemma excludes order-four subgroups in the limit, so every product
of distinct involutions has odd order p. The odd triple relation eliminates
the remaining quotient of order two and makes the group perfect.

The source v2 and the exact Notebook page were visually checked. The
geometric theorem is imported; the application has a 26-point internal
audit. A positive-delta overlap calculation avoids a zero-hyperbolicity
strict-inequality convention. GAP checks 200 presentation abelianizations,
eight literal C2 assignments and21,318 dihedral pairs, actual exit0 and a
clean completion sentinel. No finite calculation is claimed to certify the
infinite quotient theorem. Novelty and outside review remain pending.

At17:24:47 UTC the six n=7 workers remained verified live, with13,020,000
total checked nodes and18,475,764KiB combined RSS; no shard was complete.
The earlier index-two obstruction in the Amelio--Andre--Tent framework was
avoided by using Amelio's newer theorem, not silently assumed absent.


## 2026-09-11T17:48:51.651117+00:00 — 10.32 conditional cycle-product route

Recorded the remaining mixed-parity exponent case and an explicit unproved
class-product lemma. All3,621 exact coefficients for15 eligible (n,q)
pairs through degree25 are positive on odd classes. A5 is independently
covered by two elements of order dividing3, correcting a printed auxiliary
claim in Malcolm2017 Remark2.6 (visually checked). The logarithmic
consequence with c>8 is conditional on the class-product lemma;10.32
is not counted. Plan, bounded transcript and actual clean exit0 retained.


## 2026-09-11T18:09:17.393481+00:00 — Problem 10.32 logarithmic candidate

Recorded the thirtieth complete candidate: n>=max(1126,16 log m),
and asymptotically every c>8, suffices for x^r y^s on S_n when at least
one exponent is odd. The positive-genus three-partition theorem applies
after restricting to max(support size,2q) points; transpositions use
cycle merging. The even-target cover, signed modular roots, explicit
prime estimates and all quantifiers are checked in a25-point audit.

GAP finds6,143 actual factorization witnesses at seven eligible pairs
through degree25; independent Python replay verifies every target type,
all49,144 root identities and six exact rational margins. An undefined
GAP function caused the first rejected run. The next run completed
mathematically but emitted line continuations incompatible with JSON;
its raw evidence is retained. The final stream export is valid and all
checks pass, with clean actual exit0. No finite computation is presented
as proof of the unbounded statement or the imported source theorems.

At18:05:18 UTC all six n=7 workers were live with14,360,000 checked
nodes and20,175,092KiB combined RSS, zero completed shards. Candidate
priority and outside review remain pending; all work remains local.


## 2026-09-11T18:16:45.760594+00:00 — Coefficient obstruction and evening triage

The literal11.5 assertion fails over Z[sqrt(-5)], with G infinite cyclic.
An explicit idempotent presents the nonprincipal ideal used in a rank-two
projective module; evaluation at z=1 and the determinant line prove
nonfreeness. The printed coefficient assumption was visually checked.
This classical coefficient obstruction is not added to the30 candidates.

Recorded bounded source checks and obstacles for10.71,11.8,11.19,
11.23,11.49,11.61,11.63 and11.113 in the evening triage note.
No special-case centralizer theorem, degree set without multiplicities,
or associated-graded Lie argument is mistaken for the general target.


## 2026-09-11T18:33:44.400837+00:00 — Problem 11.18 bounded exploration archived

No resolution is claimed. The four coset enumerations and four ACE runs
reproduce only the known G(2,2)=1; other final outcomes are workspace
limits. The exact canonical-matrix screen reaches period10 and finds
only the known tenth-root factor at periods5,10. All final process
records have actual clean exit0 and completion sentinels. Earlier failed
runs remain retained and excluded. Independent Python replay matches
24 permutation orbits and corrects the opposite composition convention
in the source examples. The53-file hash audit passes.

At18:33:11 UTC all six n=7 workers were live with15,170,000 checked
nodes and21,534,964KiB combined RSS; zero completed shards.
All work remains local; complete candidate count30, outside reviews0.


## 2026-09-11T18:36:29.466370+00:00 — Problem 11.124 prior result checked

Tursunbaev's September6 preprint settles the exact normality question
for arbitrary-rank free groups. All mathematical proofs were read;
the key rational-module and final cancellation pages were visually
checked. The original classical dependencies remain imported. The
result is excluded from the30-candidate count. Neither derived-subgroup
inclusion nor the different11.115 question follows automatically.

## 2026-09-11T19:01:28.279431+00:00 — Prior-result boundaries and structural follow-ups

Committed the12.9(b) chain-condition deduction and11.15 Brandl source
audit as aa28c7f. The further13.53 source packet includes a checked
finite-quotient proof of the known locally graded p-group case.
The11.115 relation-module criterion proves the finite-index and
primitive-element cases, with the general missing step explicit.
A read-only19.20 ratio search finds no reciprocal pair among85,343
retained IDs; exact fractions, duplicate checks and all input hashes
are recorded. No new complete candidate; the count remains30.

The18:49 UTC n=7 snapshot verifies all six workers live and records
15,600,000 checked nodes. No shard has completed and no n=7 proof
is claimed. All large certificates and live logs remain preserved.


## 2026-09-11T19:29:02.509591+00:00 — Candidate 31: unitary cyclic limit is not rational

Problem15.65 has a complete negative candidate for its unitary cyclic
component. The first product in FNP2005 Theorem2.1.9 is holomorphic
near t=1/q=0. Removing the degree-one self-conjugate factor leaves a
nonzero holomorphic product throughout |t|<3/4. The omitted factor
has a zero of its base at alpha=(1-sqrt(5))/2 with exponent alpha,
which gives a nonintegral local power and rules out rationality. The
identity theorem justifies passing from prime-power values to the germ.
No assertion about irrationality of individual probabilities is made.

Exact logarithmic series calculations agree through degree80 and match
the published first13 coefficients. Independent GAP enumeration checks
14 full unitary groups and426 conjugacy classes against the finite
generating formula; minimal-polynomial and power-matrix-rank tests
agree throughout. Both processes exit0, logs are clean, and sentinels
are present. The15-file audit binds proof, review, inputs and controls.
The source's different definition of separable is recorded explicitly;
the cyclic result does not depend on correcting the Notebook.

Earlier Issue14/15 scope checks and the19.20 duplicate-screen crosslink
were committed as c9499f0. At19:16 UTC all six n=7 workers remained
live with16,270,000 checked nodes; no complete shard or n=7 proof.
All work remains local, the48-hour goal remains active, and outside
review and further priority checks remain required for all31 candidates.


## 2026-09-11T19:52:25.821478+00:00 — Extend candidate31 to every classical component of15.65

The analytic obstruction now covers all full U, Sp, O odd, and O+/-
cyclic and semisimple limits, including both fixed characteristic
parities. It also treats squarefree characteristic polynomial, resolving
the source/Notebook definition discrepancy in either convention. The
cyclic zero is the same quadratic root as before. For semisimple limits,
explicit alternating-series bounds isolate a zero of the reciprocal
unitary-order series in(-3/5,-1/2). A zero-free disc for all higher
factors and a separate positive degree-one linear-group factor prevent
cancellation. Nonconstant-exponent monodromy handles prefactor zeros
and the integral-exponent values in the regular semisimple case.

Twenty-three GAP groups give563 paired class tests and69 exact finite
probability comparisons. The final GAP and outer Python runs exit0,
with clean completion sentinels. The first GAP run's obsolete-API
messages and the initial Python table assertion failure are preserved.
Independent binomial and logarithmic series agree through degree12.
159 of160 published coefficients match; the odd symplectic SS t^9
entry-195 conflicts with the exact product and the source's orthogonal
row and ratio identity, all of which give-193. This is a documented
source discrepancy, not a discarded failed check or a proof premise.

The original15-file unitary packet remains frozen. The extension has
a separate proof, review, source images, controls, and hash auditor.
No new candidate number is added:31 now covers the whole question.
Priority and independent review remain pending. At19:50 UTC all six
n=7 workers remain live, with17,150,000 verified nodes and24,160,500KiB
combined RSS. No shard is complete and no n=7 proof is claimed.


## 2026-09-11T20:20:11.627590+00:00 — A separating-kernel route for15.92

A general bounded-support criterion now has an internal proof: a fixed
nontrivial word of uniformly bounded support in alternating quotients of
unbounded degree forces continuum many nonisomorphic quotients residually
finite alternating. The argument uses a marked limit, a finitary normal
closure, elementary finite-subgroup averaging, and recursive kernel
witnesses. It does not infer normal-kernel independence from the number
of maximal subgroups. The conditional periodic-chain route is retained.

Conder's1980 Oxford thesis has just been obtained and its Chapter5 may
supply a fixed11- or13-cycle word for every triangle parameter. Source
auditing is in progress; no new complete candidate is counted yet. The
20:12 UTC certificate snapshot verifies six live workers and17,790,000
checked nodes, with no completed shard. All work remains local.


## 2026-09-11T20:45:33.228798+00:00 — Two restricted deductions and late Issue 15 boundaries

The regular-normal-subgroup case of 15.95 has a direct proof by counting
fixed-point elements in each coset of the regular subgroup. No existence
of such a normal subgroup is established for the general question.
The June 2026 Di Bartolo--Ersoy--Falcone paper settles the periodic
residually finite case of 10.59. Its full proof is audited, with a direct
replacement for the power-automorphism step in its Tarski exclusion.
The metadata omission of the essential p-prime hypothesis is retained
as a source-boundary warning. Nine hashes bind the source and deduction.
Neither result increases the 31-candidate count. The 15.92 mathematical
packet is drafted; its fifth independent GAP diagram control is still
running. Nearby pro-p identity and splitting-automorphism scope limits
are added to the triage record. No outside communication or push.


## 2026-09-11T20:51:56.892063+00:00 — Candidate 32: every triangle parameter in 15.92

Conder's 1980 thesis supplies the exact finite-image condition: in each
parameter class, one fixed ordinary triangle word maps to a single
11- or 13-cycle in alternating quotients of unbounded degree. The
bounded-support criterion and separating-kernel proof therefore give
continuum many nonisomorphic infinite quotients residually finite
alternating, in the strong epimorphic sense, for every r>6.

All 150 table-and-join controls pass. Independent geometric reconstruction
of the r=7 diagrams gives five exact alternating images of degrees
78, 120, 162, 246 and 456, certified by primitivity, an 11-cycle, even
parity and Jordan's theorem. The final GAP and outer processes exit 0
with clean sentinels. Four general group-order calculations also pass;
the redundant degree-456 order calculation was stopped after its
independent primitivity certificate succeeded. Its actual GAP exit is 1,
as is its outer exit. The initial orientation failure and the first
auditor's incorrect expectation of raw signal status -15 are retained.
The corrected 70-file integrity auditor passes with actual exit 0.

The complete-candidate count is now 32. No priority certification or
independent outside review is claimed. The 20:48 UTC n=7 snapshot shows
six live workers and 18,610,000 checked nodes; no shard is complete.
The 48-hour goal remains active and all work remains local.


## 2026-09-11T21:07:44.340931+00:00 — Candidate 33: central images of involutions in 4.75

The unchanged 10.62 construction also supplies a negative answer to
4.75. Every 2-subgroup has exponent two and cannot contain a Klein
four subgroup, so every Sylow 2-subgroup is C2. Normal generation by
each involution and perfectness exclude its central image in every
quotient where it survives, in particular modulo the odd-order radical.
The elementary deduction has a 14-point internal audit. The exact
Notebook page and Durakov's earlier restricted theorem were visually
checked; all mathematical text in that five-page prior paper was read.
No involution-centralizer hypothesis is asserted and 15.54 is not settled.

The 13-file packet auditor passes with actual exit 0 and invokes the
unchanged 27-file 10.62 auditor successfully. The candidates share that
geometric dependency, including its imported estimates and outside-review
limitations. The complete-candidate count is 33, with priority pending.
At 2026-09-11T21:04:14.334975+00:00, all six n=7 workers are live, with
18,990,000 checked nodes and 26,880,756 KiB combined RSS.
No shard is complete. All work remains local and the 48-hour goal is active.


## 2026-09-11T21:32:11.597332+00:00 — 6.47 pilot frozen; 5.25 metabelian partial

The exact binary word-function pilot covers five finite groups: all 289
normalized functions and 522,952 associativity triples. Each group has
only its original and opposite multiplication. SmallGroup(24,3) exceeds
the cap with 8,192 normalized functions and is explicitly omitted. Six
actual GAP processes and the outer runner exit 0; the initial NumPy-path
failure is retained with actual exit 1. The 52-file auditor replays all
exported tables and passes with actual exit 0.

A self-contained class-two identity-transfer proof is recorded. Cooper's
1974 conjecture and class-three classification were checked against the
full paper and rendered pages; the S3 computation is explicitly a
rediscovery of Płonka2013. The class-three-to-five extension remains live
and is not included in this frozen packet. Completed additional class-three
operations checked so far have explicit power-map isomorphisms; order-27
abelian outputs satisfy the variety conclusion. Neither partial result
increases the 33-candidate count.

Problem5.25 is affirmative for metabelian bi-orderable groups, by finite
order of conjugation on the derived subgroup. The reduction for higher
derived length is recorded as unproved. All six n=7 certificate verifiers
remain in progress. No external communications or pushes.


## 2026-09-11T21:44:27.267851+00:00 — Explicit 7.58 retraction criterion; prior boundary checked

A spanning-tree change of free edge basis gives an explicit retraction
onto the embedded kernel and the image test rho(b)=b t_q^-1. The proof
includes arbitrary rank and variety, the exact embedding kernel, a
preimage formula, the abelian flow reduction, and source-convention
conversion. The literature audit found that McCool1987 explicitly
discusses 7.58 and gives the associated conditional algorithm using
the same free-factor structure. The result is excluded from new
coverage. All ten source pages were read; p.140 was visually checked.

Independent path-continuity checks cover 82,080 bounded free-edge cases,
and the complete 54-element nonabelian-base model checks against the
generated image. All controls and the 17-file replay auditor pass with
actual exit 0. Candidate count remains 33. The last n=7 snapshot at
21:37:54 UTC has 19,750,000 checked nodes, six live workers, zero
completed shards, and 28,108,020 KiB combined RSS.

The full raw-data whitespace check in the preceding 6.47 commit
reported GAP's retained trailing spaces; the authored research, scripts
and reports pass the separate whitespace check. No raw output was
altered to silence that diagnostic. All work remains local.


## 2026-09-11T21:59:08.441959+00:00 — Candidate 34: finite translation obstruction for 9.4

Every finite quasigroup satisfies a factorial identity for its left
translations. Coordinate-shift isotopes of finite elementary abelian
groups violate any proposed bound. This gives a complete negative
candidate under ordinary variety generation, and also for quasivarieties
and pseudovarieties. A separate infinite monogenic example verifies
the local-finiteness obstruction. The trivial generating group is
explicitly excluded.

The 20-point internal review checks the quantifiers, isotopy direction,
division signs, finite-family extension and generation conventions.
Gvaramiya1985 Section 3 was read, including its separate ordinary
quasigroup and three-sorted theorems; pp.326 and 328 were visually
checked. The relevant 2016 definitions were also checked. No exact
prior answer was found in the limited search; novelty is not asserted.

Controls and the 18-file replay auditor both exit 0. They cover all
591 Latin squares of orders 1--4, 12 affine models, 93,252 axiom checks,
2,396,744 Boolean identity checks and ten finite separating witnesses.
The candidate count is 34, all awaiting outside review. The latest
n=7 snapshot at 21:52:32 UTC has 20,130,000 checked nodes, six live
workers and zero completed shards. The 6.47 order-64 bounded jobs
remain active; timeouts are retained. All work remains local.


## 2026-09-11T22:07:50.352443+00:00 — 5.25 exact prior counterexample located

The 2009 Bludov--Kopytov--Rhemtulla paper explicitly answers 5.25.
Its Example 3.1 gives a totally orderable group of derived length three
with exponent-two abelianization. The relevant construction and order
argument were read; omitted module consistency checks remain unaudited.
A local sign discrepancy in formula (17) was detected visually and
reconciled with formula (11) and the subsequent square formula.

The earlier metabelian positive proof is retained. The contemplated
finite-extension lemma is false: a finitely generated nonmetabelian
subgroup of the example has a metabelian normal subgroup of finite
index. This is a corrected research direction, not a new candidate.
Kopytov2013/2014 also announces the finite-generation case relevant
to 8.24, without a full proof in the two-page note. Candidate count
remains 34. The 6.47 bounded extension and n=7 verifiers continue.


## 2026-09-11T22:13:36.543949+00:00 — 6.47 extension complete: 21 cases, 12 explicit timeouts

The prescribed 33-job extension completed with actual outer exit 0
and its completion sentinel. All 21 completed GAP processes have
actual exit 0, clean logs and sentinels. SmallGroup(32,9), (32,11),
and all ten selected order-64 cases time out with actual exit -9.
They carry no associativity conclusion. The 21 complete cases cover
622 normalized operations and 18,926,930 triples. Of 88 associative
outputs, 86 have explicit power-map isomorphisms and two are abelian
with the same exponent; all therefore belong to the original variety.

The 158-file auditor replays these controls and both intermediate
classification snapshots, and reruns the unchanged 52-file pilot
auditor. It passes with actual exit 0. Combined completed coverage
is 26 groups, 911 normalized functions, 98 associative outputs and
19,449,882 triples. No general answer or new candidate is claimed.
A separate vector enumeration is being considered to avoid the
large direct-product bottleneck; frozen inputs and logs are preserved.

The n=7 snapshot at 22:08:08 UTC has 20,550,000 checked nodes, six
live workers, zero completed shards and 28,860,148 KiB combined RSS.
Candidate count remains 34. All work is local.


## 2026-09-11T22:27:41.510153+00:00 — 6.47 coordinate method completes all twelve timeouts

The new normal-closure orbit algorithm matches full word-vector sets and all
associative tables from the 26 frozen GAP cases. Scalar predecessor and closure
checks certify the new searches; forced cutoffs remain explicitly incomplete.
The twelve formerly timed-out cases contribute 3,296 functions, 80 associative
operations and 856,686,592 triples. All 80 outputs are isomorphic to their source
groups: 78 via power maps and two via independently verified general permutations
on SmallGroup(64,34). All actual exits are zero and GAP logs have clean sentinels.
The 131-file vector auditor, including both prior packet auditors, passes with
actual exit zero. Combined coverage is 38 groups, 4,207 functions and 178
associative outputs. No general solution or candidate increment is claimed.

The 22:23:25 UTC n=7 snapshot has 20,920,000 checked nodes, six live workers,
zero completed shards and 29,329,140 KiB combined RSS. Candidate count remains
34. Original timeout records and all earlier frozen packets are preserved.


## 2026-09-11T22:56:27.950961+00:00 — 12.40: no bound with fixed Sylow order

Candidate 35 gives irreducible 2-Brauer degrees with arbitrary exact
2-part 2^k, k>=3, in PSL_6(5^a), a odd, while every group-order
2-part is 8192. The projective-heart irreducibility is prior work
credited to Bray2007. Its precise hypotheses and argument were read
and the relevant pages viewed. The arithmetic lifting proof uses
only powers of five and does not invoke primes in progressions.

The 37-file auditor passes with actual exit zero. It replays 510
lifts, eight exact integer group orders and degrees, 16,383 root
candidates, 32,766 exponent candidates, and all 352,440 table degrees.
Three actual projective GAP modules have the expected absolutely
irreducible factors. The original 2,750-name table screen has 7,573
available and 2,277 unavailable tables, and passes with actual exit
zero. The first independent coverage audit failed on the rowless
trivial Alt(2); its script, failure log and transparently reconstructed
process record are retained. GAP metadata output continuations are
retained and decoded explicitly. No mathematical result was edited.

The latest n=7 snapshot, 22:43:04 UTC, has 21,390,000 checked nodes,
six live workers, zero completed shards and 30,202,612 KiB combined
RSS. The table screen and module checks ran sequentially under the
existing 4-GiB ceiling. Late-evening source triage records why the
16.90 BMN-generation and 5.36 uniform-rank steps remain unavailable.
All 35 candidates await outside review and further priority checks.
No external communications or pushes have occurred.


## 2026-09-11T23:24:29.106557+00:00 — 13.42: non-locally-nilpotent tensor completion

Candidate 36 constructs an explicit Z[t]-group from the rational rank-two
class-three BCH group and the additive group algebra Q[Q]. A conjugation-
equivariant function is additive on commuting pairs because the first
three Lie coordinates of commuting elements are proportional. This gives
a scalar action factoring through t^2, while the scalar ring Z[t] itself
is an integral domain and the ordinary target group is torsion-free.
Every original A-group axiom is proved, including cross-commutation in
the conditional product law. The universal completion contains a fixed
pair whose r-fold commutator maps to (T-1)^r for all r.

The 17-file audit has actual exit zero and replays the controls: ten
generic coordinate variables, 15 truncated words, 81 scalar monomials,
75 exact model elements, 525 commuting pairs, 5,250 conditional-product
checks, and 64 nonzero commutators. Original source Definitions 1 and 2
and universal existence are the specialized prior input; their exact
pages and the Notebook question were read and viewed. Limited searches
found recent restricted class-two work but no exact prior construction.
Independent review and novelty remain pending.

The separate 14.89(b) investigation located the exact prior answer in
Jaikin-Zapirain2000 Corollary3.1. The complete DVI text was read; failed
PDF conversion is disclosed and its invalid output excluded. This is
not a candidate increment. The 23:23:15 UTC n=7 snapshot records
22,390,000 checked nodes, six live workers, zero completed shards and
31,422,196 KiB combined RSS. No new GAP worker was needed for 13.42.
All work remains local; no communications or pushes have occurred.


## 2026-09-11T23:38:20.105488+00:00 — 16.45 pilot and 16.14 prior deduction

The 354-group p-group pilot for16.45 has a sufficient normal-Frattini
certificate in every case. Its30,755 subgroup classes represent45,105
subgroups. Independent multiplication-table controls reconstruct3,243
subgroups in12 groups, verify1,146,659 associativity triples and produce
explicit minimal bases. The26-file closed audit exits zero. The initial
GAP process exited zero but emitted five unbound-global warnings; its
wrapper correctly exited one. That full run is preserved. Declaring
local variables produces a clean rerun with byte-identical data.
Nonfaithful actions are included, as required by the exact convention.
The general question is unresolved.

Source triage located the centralizer bound inside Sambale2014's
Theorem1.3 proof, explicitly restated by Halasi--Podoski--Pyber--Szabo.
Putting E=Omega_1(G)<=Z(G) gives C_G(E)=G and d(E)=d(Z(G)), hence
precisely the16.14 inequality. The relevant PDF pages were viewed.
The underlying MacWilliams theorem remains an imported, unaudited
premise; this is a prior deduction and not a new candidate.

The 23:38:19 UTC n=7 snapshot has22,790,000 checked nodes,
six live workers, no completed shards and32,705,268 KiB
combined RSS. Candidate count stays36. All work remains local.


## 2026-09-12T00:04:36.855408+00:00 — candidate37:14.26

A polynomial interpolation construction proves closure of Q(all torsion-free
nilpotent groups) under restricted wreath products with Z. Budkin1999
p258 explicitly confirms finite support. Nearby copies commute in a
finite rational algebra, while dual polynomials separate their powers.
Superdiagonal scaling and a refined central series give torsion-free
nilpotent local models. A finite-table lemma passes to arbitrary bases
in the quasivariety. Jennings1955 Theorem5.2 is the sole imported
group theorem, with its exact use and reading scope documented.

Four exact algebras pass110 derivation-stability checks,246 dual
annihilations,47 separation values and the matrix/shift controls.
An independently implemented Heisenberg wreath ball has37 elements,
319 internal relations and666 distinct pairs, all preserved. Both
child processes, runner and23-file replay audit actually exit zero.
The earlier working draft and rejected index-grading idea are retained.
No gap was identified internally; outside review and novelty remain
pending. Complete candidate count is37.

The n=7 snapshot at00:03:53 has23,550,000 checked nodes, six live
workers and no completed shards. The16.45 extension remains live;
its last progress reports2,300 groups and no missing sufficient
certificate. No n=7 or general16.45 conclusion is claimed.


## 2026-09-12T00:13:15.857612+00:00 — 16.45 extension frozen

All2,435 groups in the six prescribed new orders have a normal-Frattini
maximum-rank witness. The1613.97-second GAP run and outer runner
actually exited zero with a clean sentinel. The extension covers
619,438 subgroup classes and1,108,458 subgroups;1,010 groups have
no abelian maximum-rank witness. Eight independently reconstructed
tables verify474 subgroups and307,619,161 associativity triples.
The46-file audit replays all20 pilot/extension table controls and
passes. Combined coverage is2,789 groups and1,153,563 subgroups.
The general question remains unresolved and the candidate count37.


## 2026-09-12T00:32:18.499610+00:00 — 18.120 partial and bounded search frozen

The elementary abelian-normal-closure criterion settles class at most four,
even with overlapping factors. The pilot and order-256 extension cover
59,349 groups: 58,946 by the theorem and 403 by subgroup enumeration.
All 28,155 tested disjoint factorizations in higher class pass. Six table
controls reconstruct 2,791 subgroups and verify 812,589,714 associativity
triples. All child processes, runners and the 37-file replay audit actually
exit zero with clean completion evidence. Root-partition exploration
through UT_6 adds no obstruction. General problem and priority of the
elementary partial remain unresolved; complete candidate count stays 37.

The n=7 snapshot at 00:27:52 has 24,190,000 checked nodes, six live
workers and no completed shard. No n=7 conclusion is claimed.


## 2026-09-12T00:46:05.091615+00:00 — 18.77 small-class partial frozen

A Pfaffian/interpolation proof over Z/p^k establishes that largest-degree
characters separate every finite p-group of class less than p when e<p.
A homogeneous-polynomial strengthening detects any p-e nonidentity
elements simultaneously. The all-class-two consequence is prior by
Isaacs--Passman1968, Theorem1.5; its original pages were read and viewed.
The finite Kirillov theorem is an explicit imported input with scope
recorded. The 32-file audit replays 22,063 initial parameter values,
5,772 further values and 578 forbidden-hyperplane sets, plus the Z/25
divided-Pfaffian control. All actual processes and audit exit zero.
No general answer or priority claim; complete candidate count stays37.

The 00:40:06 n=7 snapshot has24,570,000 checked nodes, six live
workers and no completed shard. Its certificate still has no proof status.


## 2026-09-12T00:56:50.044835+00:00 — 11.78 scope and prior results

The disconnected groups Ga^n semidirect C2 give elementary counterexamples
to both printed parts. A full argument and a six-file source binding are
retained. Frecon2013 supplies prior positive connected cases; its exact
hypotheses were read and pages 5,72,73 viewed, but its long proof is imported.
The intended connectedness convention remains unconfirmed. No new count.

At 00:56:12 the n=7 verifier has 24,970,000 checked nodes, six live workers,
zero completed shards and 35,031,796 KiB combined RSS.


## 2026-09-12T01:02:50.398583+00:00 — 15.44(a) prior negative consequence

The classical cubic-cone Segre ring is realized as the invariant ring of
a one-dimensional torus acting on a Cohen–Macaulay hypersurface. The
monomial weight basis supplies the exact induced-module filtration. An
explicit three-element homogeneous parameter sequence is not regular;
the Hilbert numerator 1+3t+3t^2-t^3 independently confirms failure.
Hochster2007 pp.15–16 already give the ring and obstruction; those pages
and the graded Cohen–Macaulay criterion on p.12 were read and viewed.
Eight files are hash-bound. No new priority or candidate increment.


## 2026-09-12T01:25:07.149693+00:00 — 15.76(b) complete candidate frozen

The Magnus affine model and cyclic Laurent-unit specializations prove
normalized associative-word rigidity for every full solvable variety
S_d. The explicit category reduction and naturality formula prove all
automorphisms inner, including the full metabelian case. The 42-file
audit actually exits zero and replays 2,430 reduced words, 800 affine
coefficient checks, 800 boundary identities, 28,080 usual/opposite
associativity checks, two deeper perturbation witnesses, 289 Laurent
pairs, and 1,000 free-group homomorphism controls. A packet-generation
quoting error and its missing-manifest follow-up are retained. No gap
identified internally; independent review and priority remain pending.
Complete candidate count is 38.

The exact prior affirmative theorem for 20.72 is recorded separately,
with the 2019 source calculation limits explicit and no new count.
The n=7 snapshot at 01:22:17 has 25,760,000 checked nodes, six live
workers, zero completed shards, and 36,067,572 KiB combined RSS.


## 2026-09-12T01:36:34.801711+00:00 — 16.38 complete candidate frozen

A cocycle of a locally finite group into a torsion-free abelian group
cannot contain both t and 2t in its image for nonzero t: finite
averaging and an invariant inner product give the obstruction.
Two periodic factors yield just such a cocycle on their common
quotient image. Derived-length induction proves that every subgroup
contained in their set product is periodic in a soluble ambient group.
The original page and related source pages were viewed. The 21-file
audit actually exits zero, replaying 6,125 matrix cocycle/product pairs
and 87,380 sign-action pairs, with a finite-torsion mutation retained.
An infinite finite-support example excludes an incorrect global
coboundary assumption and the stronger false elementwise conclusion.
No internal gap found; independent review and priority remain pending.
Complete candidate count is 39.


## 2026-09-12 01:47 UTC — Artin D5 source deduction and triage

Paris--Soroko2026 Theorem1 gives the D5 case of 17.16. Exponent sum
is 40 on the central generator, so the centre quotient is virtually
a linear subgroup of the original group; induction of a faithful
representation handles both finite extensions. Pages1--4 were read
and2--3 viewed. Six source/note hashes replayed successfully. Original
classification and linearity inputs remain imported. No new count.
The recent almost-simple maximal-subgroup paper does not settle17.91;
a scope note retains the elementary normal/core-free cases.
Latest n7 snapshot:26,190,000 checked nodes; six live workers, no
completed shards,36,629,236KiB combined RSS.


## 2026-09-12T02:16:38.564425+00:00 — 19.93 complete negative candidate frozen

For every prime p>=7, the relations x^p=y^p=(xy)^p=1 exclude
a C_p wr C_p quotient. Finite truncations of their complete algebra
give exactly two-generator finite p-groups. Filtered Golod--Shafarevich
growth contradicts the partition-product bound implied by uniformly
bounded lower p-central factors. The original hypothesis is on the
whole group, not all its sections. Ershov pp.9--10 were read and viewed.
The 23-file audit actually exits0, replaying21,714 wreath norm checks
and12 exact algebra truncations. Seven GAP triangle quotients reach
order7^68 with final factor dimension28. Initial scope warnings and
the rejected wrapper run remain archived. Nineteen internal review
points found no gap; imported GS and unconfirmed priority are explicit.
Complete candidate count is40; externally accepted count remains0.
Latest n7 snapshot at02:07:13:27,040,000 checked nodes, six live workers,
zero completed shards,37,787,380KiB RSS.


## 2026-09-12T02:19:03.919320+00:00 — 18.84 screen archived; 18.65 source scope

The corrected14-test pilot,12-test exceptional follow-up and87-test
catalogue over78 table identifiers all complete with actual exit0.
No ambient positive certificate appeared; every catalogue prime set
has an involution obstruction. There are87 missing/class-capped entries
and possible duplicate isomorphism types under different identifiers.
The conclusions remain conditional on character-table and extension
metadata. Initial display and scope-warning logs are retained.
The source/packet archive hash and sentinel check passes; no new count.
Guralnick--Malle's2014 author version was distinguished from its2013
submission date; p.2 was viewed. Theorem1.2 has a stronger closure
hypothesis than18.65, and the stated Ree reduction is not independently
proved in this packet. The general conjecture remains unresolved.


## 2026-09-12T02:35:25.922808+00:00 — prior stability theorem and withdrawn claim

Kapovich's18 August2026 preprint gives19.77 via Theorem A and
Corollary1.2, including freely reduced sphere and ball sampling.
The statement pages3--4 were viewed; selected overlap and transfer
proofs were read, with the rest explicitly not fully audited. No new count.
The initially found negative20.21 claim is officially withdrawn on
7 January2026 for an error in Section3.4. Current metadata and the
explicit old version are archived; no result from it is used.
The source hashes pass. Latest n7 snapshot at02:30:25 has
27,630,000 checked nodes, six live workers, zero completed shards,
38,955,764KiB RSS. A new coprime-product route to20.1 is under audit.


## 2026-09-12T02:49:02.995526+00:00 — 20.1 affirmative candidate frozen

The two factor-orbit partitions give an injective action of the2-closure
on the two quotient sets. Coprime orders ensure singleton intersections
and faithful quotient actions, so total2-closure of the factors forces
the product to be totally2-closed. The published J1 theorem now gives
J1 x C13, of order2,282,280 and Fitting subgroup exactlyC13. The original
question has no indecomposability restriction. All177 GAP controls agree
with independent exhaustive Python orbital-colour enumeration, including
48 enlarged negative cases and two explicit hypothesis mutations. The
30-file auditor actually exits0. Two initial GAP API failures remain
archived. Nineteen internal review points found no gap; the J1 theorem
is imported and priority remains unconfirmed. Complete candidate count
is41, independently accepted count0. Latest n7 snapshot at02:43:33 has
28,050,000 checked nodes, six live workers, zero completed shards and
39,574,260KiB RSS.


## 2026-09-12T02:51:49.063174+00:00 — 20.3 prior negative consequence

The determinant adjustment obstruction gives k(PSL_n(3))>=n for
odd n>=5. This exact local matching statement already appears in
Gong--Yang--Zeng2026 Theorem5.3, although the paper emphasizes20.2.
The full relevant proof was read and pp.21--22 viewed. A source
archive with six hashes passes. The elementary specialization is
recorded, with standard simple-group facts explicit and no new count.
The STATUS timestamp formatting artifact was also corrected.


## 2026-09-12T03:02:52.221527+00:00 — virtual retractions prior result; kernel search begun

Minasyan's20 March2026 v2 Theorem1.1 gives the exact affirmative
answer to20.59. The introduction and final proof were read, with
the first page viewed; deeper inputs remain imported. Four archive
hashes pass, with no new count. A separate bounded20.21 GAP pilot
now searches orders12,24,48,96,192,384 without using the withdrawn
claim or the unaudited minimality reduction. Up to192 there are25
groups with both quotient types and no matching kernel type.


## 2026-09-12T03:14:00.519443+00:00 — 20.21 pilot frozen

All22,015 catalogue groups in the six selected orders12,24,48,96,192,384
were tested;1,241 admit C12 and123 have both quotient types. All kernel
identifier pairs differ. The25 independent multiplication-table controls
reconstruct43 normal subgroups of index12 and certify six nonisomorphic
kernel pairs. A16-element coordinate mutation shows that isomorphic
kernels with C4/V4 quotients alone are possible. The14-file audit exits0
and replays all controls. This is bounded evidence only; no minimality
reduction or withdrawn result is used, and the candidate count stays41.


## 2026-09-12T03:24:20.451366+00:00 — 20.21 reduction audited and order768 launched

Recovered the publisher PDF, read the full Conder--Maslova proposition
and proof, and viewed printed pp.287–288. The prior minimality argument
is complete; a typo in the irrelevant automorphism statement is recorded.
It converts the pilot into exclusion of all orders below768. The first
two-shard control failed on a GAP range endpoint; the wrapper returned1
despite child exit0. Failed scripts and outputs are preserved. The fixed
retry exits0 and exactly reproduces all order96 rows and counts. Eight
1GiB GAP workers now search1,090,235 groups of order768, in addition to
six14GiB certificate verifiers:14 compute processes,92GiB workspace
ceiling, substantially smaller actual RSS. A24-file launch/source manifest
passes; no order768 result is claimed while the processes run.


## 2026-09-12T03:30:17.749704+00:00 — 21.102 source and nilpotent-normal bound

Olshanskii2606.04577v3 still asks the exact general existence and
integrality questions. All group arguments in Sections1–3 and the group
examples/questions were read; pp.1 and6 viewed. The coordinate partition
argument extends from abelian to nilpotent normal N: boundedly many
quotient lifts generate a bounded group K, whose conjugates of the
remaining generators generate a nilpotent kernel of polynomial logarithmic
size. This yields log|F_n(G)|<=A n^c [G:N]^n and an integral limit when
G/N has a nonabelian monolith. The partial proof and six source hashes
are archived; general21.102 and priority remain unresolved. A broader
early-morning triage note records unproved leads and rejected shortcuts.


## 2026-09-12T03:33:03.146802+00:00 — exact nilpotency filter speeds20.21 extension

The first32 order768 catalogue entries are nilpotent. The slow job was
intentionally stopped, with all outputs preserved and no result claimed.
The replacement skips nilpotent groups, which cannot have A4 quotients,
after incrementing the unchanged C12-eligibility counter. Its two-shard
order96 control exits0 and matches all frozen rows. Eight1GiB replacement
workers are live under the order768-fast prefix; the old workers were
terminated and waited for by their controller. The source and launch
manifest passes. The n7 snapshot at03:30:38 records29,340,000 checked
nodes, six live verifiers, zero completed shards and41,322,228KiB RSS.


## 2026-09-12T03:57:20.412630+00:00 — 19.61 five-ring C2 packet frozen

Exact root matrices generate every commutator implication and enumerate
all17,609 valid carpets over five rings. GAP finds3,048 enlargements and
no failure of the carpet conditions. The independent matrix checker
enumerates134,213 states across1,288 cases, including104 enlargements;
an eight-element mutation rejects a false example whose initial data
is not a carpet. All five searches and controls exit0. The36-file audit
regenerates every input and replays the controls; its initial integer-vs-
JSON-string histogram-key failure is retained and its corrected run
exits0. No new complete count. The previous20.21 restart commit retains
eight raw CR-only logs; diff-check flagged only those preserved bytes,
and the source/document check with those raw logs excluded passed.


## 2026-09-12T04:03:03.249723+00:00 — order768 exclusion fully audited

All eight fast search children and their controller exit0:1,090,235
groups tested,11,562 C12-eligible,606 with both quotients, no matching
kernel pair. Every one of the2,878 kernels was exported as a64-element
multiplication table. Independent checks separate2,341 pairs by element
orders and27 by abelianization exponent, covering all2,368 pairs. The
2,267 distinct tables require594,280,448 associativity triples. The first
control invocation preceded compression completion and failed visibly;
its log is retained, and the unchanged checker passes after actual
compressor completion. The65-file auditor replays the pilot and all
kernel controls and exits0. The audited prior minimality reduction
gives a lower bound1536 for any counterexample. General20.21 remains
open and the complete count remains41.


## 2026-09-12T04:20:28.456435+00:00 — G2 prime-field carpet packet audited

All 174 G2(F2) and 217 G2(F3) carpets are already closed. Integral
adjoint divided powers, 2,744 Jacobi triples, and every commutator
factor are checked before enumerating all 4,096 assignments per field.
The F3 orbit spans only seven dimensions; no full-span assertion is
used. Direct matrix enumeration checks all 390 nontrivial-to-certify
cases (126,998 states), with the full F3 assignment handled by definition.
All seven processes exit zero. The 26-file auditor reconstructs both
inputs and replays all controls, also exiting zero (cdbff9). This is
a bounded negative result; complete candidate count remains 41.


## 2026-09-12T04:21:05.657787+00:00 — order-1536 structural interval launched

Both quotient types force normal Sylow 2 and nonnormal Sylow 3. The
SmallGroups source partitions 408,641,062 groups, leaving exactly the
18,028 indices 408526598 through 408544625. Eight boundary groups have
the expected actual Sylow-normality flags, with exit zero (726ff3).
The separate interval runner reproduces every order-96 pilot row and
all counts, exiting zero (f8d101). Four 1 GiB workers now search the
complete relevant interval and assert the flags for every group. No
order-1536 result is claimed. The n7 snapshot at 04:19:58 UTC records
30,810,000 checked nodes, six live workers, no completed shard, and
43,897,588 KiB combined RSS.

The staged whitespace check flagged only the verbatim GAP metadata
log and verbatim decompressed library source. Those bytes are retained
for hash reproducibility; the source/document check excludes those two
external evidence files. No executable or authored-document error was
reported.


## 2026-09-12T04:29:04.441358+00:00 — G2 four-element ring extension prepared

A binary-implication closure enumerator reproduces all 18,000 frozen
C2/G2 prime-field pilot carpets exactly (exit zero fea384). The four
new rings have 10,479, 59,921, 47,345 and 17,955 carpets, respectively
F4, dual numbers, split ring, and Z/4. Preparation exits zero (df8382);
all ring operations and commutator factors are exact. Explicit fourteen-
vector witnesses establish faithful orbit actions of degrees 4095,
4032, 3969 and 4032. The preparation auditor reproduces every new input
byte for byte and replays the old exhaustive controls (exit zero 420c47).
Four 1 GiB searches are running; their observed ambient orders all match
the validation formulas. No completed four-ring result is claimed.


## 2026-09-12T04:42:48.967642+00:00 — order-1536 search finished; kernel audit underway

All four interval workers and their controller exit zero (5f82ee).
The 18,028 groups include 5,006 with both quotient types, 30,414 kernels
and 26,760 pairs, with no isomorphic pair. The diagnostic covers 1,102
kernel types and 7,057 distinct type pairs: 6,972 differ in order counts,
51 first differ in abelianization exponent and 34 in its full type.
No additional invariant is needed at this diagnostic stage. Four exports
are now producing every actual 128-element kernel table. A native
associativity checker agrees with Python on all 19,699 binary/ternary
tables and on large cyclic tables and mutations, with exit zero. The
audited lower bound remains 1,536 until all actual-table checks pass.

The staged whitespace check reports only the compiler version command
output ending with a blank line. That raw evidence is preserved; the
authored source/document check excludes the compiler log.


## 2026-09-12T04:48:37.332696+00:00 — G2 four-ring packet frozen

All 135,700 carpets over F4, dual numbers, the split ring, and Z/4
have carpet closures, with 12,492 strict enlargements. The four GAP
children and controller exit zero (3340fb). Direct matrix controls
verify 2,214 cases, including 146 enlargements and 142,492 states, and
recheck all four spanning witnesses by ring Gaussian elimination
(exit zero bbf858). The final 38-file auditor reproduces every input
and matrix control and exits zero (47447f). No new complete candidate.
The n7 snapshot at 04:43:09 UTC has 31,420,000 checked nodes, six live
workers, no completed shard, and 43,897,588 KiB combined RSS.


## 2026-09-12T04:51:17.628626+00:00 — G2(F9) prepared with faithful projective action

Exact preparation finds 40,105 carpets and a complete 66,430-point
projective orbit; it exits zero (7754fb). All root matrices preserve
the computed seven-dimensional invariant module. Steinberg Section 3
constructs the adjoint group by these divided powers, and Theorem 5
makes it simple over F9. An explicit root moves the line of the second
basis vector, so the projective orbit action is faithful. Construction
and theorem pages were visually checked; the full earlier Chevalley
theory remains imported. The 18-file launch manifest passes. A fresh
preparation replay is running; the serial search has the expected
ambient order 22,594,320,403,200. A separate four-shard control is
being tested before splitting this larger search.


## 2026-09-12T04:52:47.685938+00:00 — validated four-shard F9 search replaces serial pilot

The new generic shard loop reproduces all 2,515 C2(F4) carpets and
every one of the 576 frozen enlargement rows. All four control children
and their controller exit zero (6f6d4f). The F9 serial pilot is stopped
with SIGTERM after its ambient-order check; its actual exit is 1
(6a1ed1), and the original log and partial changes are retained. No
result is inferred from it. Four 2 GiB F9 workers now cover disjoint
congruence classes of all 40,105 carpet indices. Together with six
14 GiB n7 workers and four 512 MiB kernel exporters, GAP workspace
ceilings total 94 GiB. The separate Python preparation replay uses
small additional memory; actual process RSS remains much lower.


## 2026-09-12T05:01:54.057785+00:00 — F9 preparation replay passes; all order-1536 kernels exported

The F9 preparation auditor reproduces all 40,105 inputs and the
66,430-point orbit exactly, excluding only elapsed time (exit zero
8bf876). Its four search workers continue. The order-1536 kernel export
controller and all four GAP children also exit zero (17e16f), exporting
all 30,414 actual kernel tables for 5,006 groups. Each completed shard
was compressed only after its GAP exit was observed; the independent
table audit is now running against the completed compressed files.


## 2026-09-12T07:45:59.274348+00:00 — order-1536 exclusion audited, lower bound 3072

The independent checker validates 30,414 kernel occurrences, with
23,096 distinct full tables and 48,435,822,592 associativity triples
(exit zero 466d97). It separates 26,118 pairs by element orders, 434
by abelianization exponent and 208 by abelianization element orders,
covering all 26,760 pairs. The 67-file packet auditor checks all source
and prior-packet bindings and replays all native controls and actual
kernel calculations, exiting zero (925efb). Together with the audited
minimality reduction this excludes every possible order below 3,072.
The compressed archives total 304,007,641 bytes; uncompressed files
remain local. General 20.21 is unresolved and the complete count is 41.
The n7 snapshot at 07:38:35 UTC records 36,310,000 checked nodes, all
six workers live, none complete, and 50,824,436 KiB combined RSS.


## 2026-09-12T07:58:47.418791+00:00 — G2(F9) packet audited

The four search children and controller exit zero (e05d94), covering all
40,105 carpets with 4,032 enlargements and no failed carpet closure.
Independent 14-dimensional matrix enumeration checks 1,114 cases, 99
enlargements and 110,305 states (77b49c). The 62-file final auditor
verifies all launch bindings and replays these controls, exiting zero
(37bc0c). Its preparation was already reproduced exactly (8bf876).
The simple-group faithfulness argument and exact source reading scope
are retained. General 19.61 remains open; complete candidate count 41.


## 2026-09-12T08:05:07.548175+00:00 — G2(Z/9) exact kernel packet audited

All 531,441 assignments yield 20,047 valid carpets, each already closed.
The lifted prime-field calculation enumerates 109,693 matrix states and
696,168 edge discrepancies. Explicit invariance and coset stability prove
the computed congruence kernels are complete; the proof audit clarifies
the discrepancy orientation. Independent Python multiplication checks
219 groups, 64,648 states and 3,421 actual kernel states (cb9c51).
The final auditor fully reproduces the input, kernels and search, and
repeats all native and matrix controls, exiting zero (81213d). General
19.61 remains open; complete count 41. The 08:00:05 UTC n7 snapshot
records 36,950,000 checked nodes, all six workers live and 52,348,660 KiB RSS.


## 2026-09-12T08:17:21.673533+00:00 — derived-carpet finite screen audited

The saved 19.61 inputs give 6,999 distinct derived carpets from 193,805
original carpets across twelve type/ring cases. Every derived carpet is
closed and passes the square-condition check. The first audit exits one
(f2ba65) because the old C2 observation has a different schema. Its log
is preserved; explicit handling of that schema gives a successful full
replay (be9423). The 62-file packet binds every prior completion.
A separate symbolic inclusion experiment finds derivations for all 2,712
G2 targets (fe3a87); this is preliminary until explicit certificates and
integer constants are independently checked. No complete count change.


## 2026-09-12T08:25:50.093065+00:00 — universal G2 derived-carpet inclusion certified

The C++ search emits 2,712 explicit integer derivations, all independently
verified by Python: 62,835 nodes, largest proof 70 nodes, four corruptions
rejected (32e71b). A separate Z[t,u] polynomial-matrix calculation verifies
all 120 commutator identities and 156 constants exactly (1e98eb). The final
packet audit replays both checks and exits zero (d954a1). Together with
Nuzhin 2023 Theorem 1 this gives a candidate for every commutative ring
in type G2. The full 19.62 count is not increased. The failed certificate
compiler warning (5a96ea) and corrected zero exit (f530db) are retained.


## 2026-09-12T08:49:47.494250+00:00 — all-type derived-carpet theorem audited; candidate 42

Every square-expansion target lies in a root subsystem of rank at most
four. Explicit certificates cover all eleven irreducible types of ranks
two through four: 71,056 targets and 974,165 integer derivation nodes.
The other ten types add 68,344 targets to the frozen G2 packet. All 75
search children and their controller exit zero (72e364); independent
ordinary-integer checking passes (6d2cd1). Exact polynomial identities
verify the commutator constants over Z, so the result is ring-independent.
The known square closedness criterion is also proved directly, using
a diagonal conformal symplectic matrix to handle every symplectic rank
without division by two. Integral controls pass 2,592 cases (f91c62).
The full 255-file source/coverage/preparation/certificate auditor exits
zero (0b0e7a), with all 44 deliberate corruptions rejected. This gives
a complete affirmative candidate for 19.62 and raises the count to 42;
priority and outside review are pending. The already known 19.63 criterion
is explicitly credited and adds no separate count. General 19.61 remains
unresolved. At 08:43:54 UTC the six n7 workers have checked 38,210,000
of 42,891,332 nodes, with no completed shard and 53,912,308 KiB RSS.


## 2026-09-12T09:01:25.670743+00:00 — stronger rank-two proof of 19.62, with nineteen printed derivations

The stronger inclusion A_p^2 B_-p inside B_p reduces each target to
three variables in a rank-two subsystem. All 104 targets in A2, B2 and
G2 pass (0712e7). The initial runner named a nonexistent binary and
exited one before starting any child (1da763); its record is preserved.
Independent ordinary-integer checks verify 763 original nodes (462962).
Removing redundant gcd edges gives 655 nodes, at most nine per proof;
19 representatives are written out completely (4aaf70). Determinant
solutions enumerate every root equation without an exponent cutoff.
The Weyl groups of orders 6, 8 and 12 preserve every absolute rule and
transport all targets to the displayed ones; both certificate versions
pass (b2ac3a). The 291-file audit replays integral root models, polynomial
constants, target generation, proof shortening and the printed appendix,
then checks every certificate, exiting zero (54242a). This is the
preferred review route for candidate 19.62; the earlier full proof is
preserved unchanged. Candidate count stays 42. The stronger theorem also
gives 2 A_p A_p B_-p inside B_p by polarization. General 19.61 is still
unresolved, and whether this inclusion helps there is being examined.


## 2026-09-12T09:12:22.652251+00:00 — full affirmative candidate for 19.61; candidate 43

Adjoining one element a^2 b at root r preserves the original derived
carpet. The complete preparation expands both inputs of every ordered
commutator rule with that rule's original constant. The first-argument
pilot (2f54b3) is retained; the full version strengthens 36 G2 target
coefficients and passes all 300 targets (8687dc). An independent sparse
polynomial expansion covers 416 substitutions and 600 terms and checks
all 3,191 derivation nodes, rejecting twelve mutations. Iterating the
single adjoining operation and taking directed unions gives a weakly
supplemented carpet C with unchanged derived family B. The known square
criterion closes C. The actual root closure D lies between A and C,
so every commutator parameter for D lies in B inside A inside D.
This proves both that D is a carpet and that its derived carpet is B.
Independent finite completion agrees with every one of the 193,805 saved
carpets (2087f1): 38,632 completions enlarge, and 20,300 are strictly
larger than the actual group closure, illustrating why equality with C
must not be assumed. The 395-file final auditor replays all foundations,
preparation, certificates and finite controls, exiting zero (379a54).
The complete candidate count is 43, with priority and outside review
pending. At 09:06:11 UTC the six n7 workers have checked 38,980,000 of
42,891,332 nodes and use 54,732,532 KiB combined RSS; none is complete.


## 2026-09-12T09:24:05.636707+00:00 — omitted-pair consequence and 15.46 source audit

The complementary subgroup N_p generated by all roots except p,-p is
normal in E(A), and its root intersections at p,-p are exactly B_p and
B_-p. The proof isolates each derived commutator factor and completes
the carpet with those two levels fixed. It uses the completed 19.61 and
19.62 packets. All 1,127,612 finite omitted-pair controls agree with the
frozen actual group closures (bdf0b1). The 411-file replay exits zero
(902daa). This does not identify N_p's intersection with the entire
rank-one subgroup and therefore does not yet resolve 15.46. All seven
pages of Itarova--Koibaev2019 were read and printed p.28 viewed; their
result is a partial decomposition theorem with imported net lemmas.
The attempted 2015 download failed certificate verification and is not
imported. Candidate count remains 43.

## 2026-09-12 09:46 UTC — 21.76 complete candidate

The 37-file replay passed with actual exit0 (tool chunk5bfcf5), making
21.76 the44th complete candidate. The main construction works over
k(x,y) for every field k and all n>=3; the alternate F9(t) construction
uses an exact120-element finite group. Both proofs are self-contained.
The polynomial-pair lemma is prior Koibaev2011 and credited; its full
six-page source and two theorem/proof images were read. The2021 cited
characteristic-zero paper was read through the web but its direct
download returned403. Seven deliberately corrupted certificates fail;
36,432 polynomial words,5,196 matrix-unit controls and all14,400 finite
matrix products pass. The initial GAP warnings and rejected wrapper
are retained. No outside review or novelty confirmation is claimed.

At09:37:25 all six n7 verification workers remained live. The updated
progress file is retained; no full n7 conclusion is claimed.
A separate nonclosed-pair lift now looks promising for19.48; its plan
is written, but it is not yet counted.

## 2026-09-12 09:54 UTC — 19.48 prior answer and independent alternative

The F9 finite screen led to an explicit nine-factor word producing the
new upper parameter 2+j from levels F3 and (1+j)F3. Lifting with the
common ideal tF9[t] gives an irreducible nonclosed net of free rank-two
F3[t]-modules over the quadratic extension F9(t)/F3(t), in every order
n>=3. Both native GAP and independent prime-field matrices verify the
word; 3,024 R-module basis products also pass.

Priority search then found ProofForum PF:2026.000007 v1, uploaded on
September 1, with a different cubic example over Z. Its complete proof
was read and its proof page viewed. A separate integer-matrix check
confirms its unit, diagonal and conjugation identities. It is a preprint
with no confirmed human review; its direct short proof is sound under
this internal audit. The problem is therefore recorded as a prior
negative answer, with no increase from 44 new complete candidates.
The 33-file replay returned actual exit0 (tool chunk5affef).

The same public archive also advertises answers to 19.9, 19.1 and
17.113. Only their abstracts have been seen so far; no proof status is
assigned to those three papers before a separate audit.

## 2026-09-12T10:12:40.377728+00:00: three ProofForum prior-answer audits

Read the complete PDFs and TeX of PF:2026.000002,000005,000006, with selected page-image checks. The17.113 balanced metacyclic family is sound and already prior;28 declared GAP cases and15 independent coordinate cases pass, including507,074 projection products and15,000 associativity triples. The original30-case request was stopped during p=11,n=5 after28 passing rows; its actual exit1 and missing sentinel are retained, not called a completed run. Revised runner actual exit0: tool chunk4682dd.

The19.1 algebraic RFRS argument is sound; exact prior topological statements cover every knot group, removing the old convention limit. The same argument gives the largest finite normal subgroup for every finitely generated virtually RFRS group; this consequence is proved with no novelty claim. The19.9 preprint explicitly predates our deductions; its argument works after making the uniform2Z obstruction and finite generation explicit. The printed symplectic rank bound is >=4, visually confirmed despite faulty PDF text extraction. Original local proofs remain unchanged.

The52-file source/evidence audit returned actual exit0 with the terminal sentinel (tool chunk5d0576); hashes, saved GAP rows, stopped prefix and byte-identical coordinate replay pass. Candidate count remains44, outside human reviews0. All cited deep topological/homological proofs remain imported within the stated reading scopes.

n=7 snapshot at2026-09-12T10:09:36.749305+00:00: six workers live,0 completed shards,40,880,000 checked nodes, combined RSS57,409,780 KiB. Still no n=7 proof claim.

## 2026-09-12 10:37 UTC — 17.118 sharp partial bounds

Wrote a complete deletion-lemma proof of the class-dependent bound p^(c+1), where c is the class of the given exponent-p maximal subgroup. An explicit finite squarefree-word algebra example has a characteristic exponent-p subgroup of index exactly p^p and none of smaller index; the proof identifies that subgroup intrinsically and uses a cyclic permutation of p letters. This makes the class bound sharp at c=p-1. The optimal small-prime answers are4 and27; the latter upper bound imports Laffey1976, whose full short source was read with its classical dependencies explicitly left imported. The known2009 infinite counterexample does not settle the finite question.

All6,561 words and19,683 generator edges in the smaller3^8 example pass an independent convolution checker, together with every cube, cyclic image and five forced corruptions. Native GAP independently builds a faithful16-dimensional matrix group and verifies its isomorphism with the pilot quotient. The35-file source/evidence replay completed with actual exit0 and terminal sentinel (tool chunk c1aad5). General p>=5 and partial-result priority remain unresolved; new complete candidates44, outside reviews0.

At 2026-09-12T10:34:23.296460+00:00, the n=7 snapshot still has no complete aggregate proof status. Three workers have pass markers but their actual exit records await collection by the sequential controller; three workers remain live, combined RSS27,878,024KiB. No restart or full n=7 claim.

## 2026-09-12 10:57 UTC — 21.98 nilpotent case and two source audits

The missing general finite-generation/FC reduction for cyclically covered word values is exactly prior Cutolo--Nicotera2010 Lemma1.1. Its full author version was read, including the lower-central proof, and the lemma page viewed. A separate univariate polynomial path gives the finite-by-cyclic conclusion for every word in locally finite-by-nilpotent groups; torsion-free locally nilpotent groups give a cyclic verbal subgroup. Jennings1955 remains the explicit classical embedding import. No general central-verbal-subgroup extension or partial novelty is claimed.

The35-file evidence replay completed with actual exit0 and terminal sentinel (tool chunk40ace6). Native GAP and independent rational polynomial arithmetic agree;48 paths,384 integer evaluations and100 explicit distinct directions pass. The initial invalid GAP Int(boolean) run had GAP exit0 but stderr and no sentinel, and its wrapper correctly returned1; that rejected evidence is retained.

The complete Poss1975 PDF was finally obtained through its publisher DOI. All six pages were read and two viewed. It proves constant-embedding special cases and states one higher-rank case without proof, leaving17.115 unresolved. Both full questions remain open here. New complete candidates44, outside reviews0.

n=7 snapshot 2026-09-12T10:56:12.658249+00:00: 3 shard pass markers, live PIDs [77396, 77399, 77400], status VERIFYING. No full n=7 claim before the completed aggregate.

## 2026-09-12T11:17:45.887042+00:00: independent20.112 subgroup-chain audit

Confirmed GAP4.16.1 and the absence of installed groups at the queried larger orders2592,2916,3888,5184,5832,7776,10368; no search there is claimed. Rechecked the12 retained cases from the original8,339-group N^3 screen, plus3 distinct quotient models, by maximal-subgroup/core/Fitting-series search.

A separate Python checker reconstructs all15 groups from faithful permutations and verifies37,152 generator edges,25,380,864 products,30 complete Sylow-normalizer chains,61 maximal steps and137 nilpotent factors. Five different corruptions are rejected. The original catalogue/Frattini identifications remain GAP imports; direct positive membership of the original12 groups does not depend on the Frattini identifications.

The initial GAP run returned0 with a sentinel but six syntax warnings; its wrapper correctly returned1 and its exact evidence is retained. The corrected GAP runner returned0 (7d80d3), independent Python returned0 (140c43), and the full28-file audit plus exact dual replay returned0 (59a581). General20.112 remains unresolved. New complete candidates44, outside reviews0.

The report also records the elementary central-Frattini lifting case with no novelty claim. All original screen files and source hashes remain unchanged. The n=7 controller continues; at this update shard3 has ended, and workers0 and4 remain active. No aggregate proof claim.

## 2026-09-12: integral finiteness reductions for21.70--21.71

Recorded full conditional arguments: integral FP plus orientable field duality implies integral duality; finite generation of integral homology through the field-resolution bound forces equal Euler characteristics. Neither missing finiteness hypothesis is supplied by the original problems. A squarefree-denominator rank-one group and a factorial telescope isolate two invalid field-to-integral shortcuts.

The2025 Fisher--Italiano--Kielak source was read on pp.1--5 and23--29, including the limited low-dimensional integral conclusion. Kropholler2021 Sections1--6 were read; its FP_2 construction contains torsion of every prime order through its displayed stabilizers and cannot have finite cohomological dimension over any finite prime field. Two theorem-page images were checked. The10-file packet binds sources and proof notes only; no computational proof or new solution is claimed.

## 2026-09-12T12:01:15.229924+00:00: 21.100 coprime-action screen and independent characters

The pilot plus eight completed GAP shards cover15,623 actions on32,262 catalogue groups of class at least3, with313,685 invariant characters and66,172 nonlinear correspondents. All count and pointwise tests pass. The larger orders256 and2187 include all nontrivial cyclic prime-power coprime actions; the smaller orders81,243,729 include involutions. The full screen remains dependent on GAP catalogue, automorphism and character algorithms.

Thirteen independently certified actions cover orders2,3,4,5,7,8,13. A Python checker reconstructs faithful permutation models, induced character bases, exact cyclotomic restrictions and the correspondence:2,316 irreducibles,328 invariant characters,120 nonlinear correspondents with explicit zero witnesses,17,320,818 multiplication entries and22,599,799 linear-map edges. Five corruptions are rejected.

The initial exporter exposed repeated characters from IrrConlon and an order-dependent Irr cache effect on SmallGroup(729,268). Both failures and the successful seven-model stage are preserved. The final exporter deduplicates against a standard basis computed first; the independent character proof does not trust the Conlon output. The initial auditor also rejected an in-memory tuple versus JSON-list comparison; that rejected run is retained. Final thirteen-model GAP returned0 (8ac84d), Python returned0 (fb17e5), and the109-file audit with byte-for-byte export replay returned0 (61debf), with clean stderr and required markers.

Navarro2023 Section6 gives the prior question and the known linear-correspondent direction, which is credited. This is a bounded negative search with positive certificates, not a full solution. New complete candidates44, outside reviews0. No external messages or pushes.

The n=7 progress snapshot at 2026-09-12T12:00:30.498720+00:00 has five shard pass markers and one live worker (77400). The aggregate remains pending.

## 2026-09-12T12:29:21.787883+00:00: 21.99 degree47 with complete independent word certificates

The previous turn was progress: commit519fe8a completed the21.100 packet. Current work revalidated the live n=7 process and extended21.99 from the initial degree20 screen. A Sylow-subgroup proof covers every prime-power degree; eight completed GAP workers supply generator-word witnesses for all496,284 catalogue actions in the remaining degrees through47. No action is unresolved.

The independent proof evaluates18,404,612 witnesses,64,329,817 circuit products and2,484,321,676 point-composition entries. The485-group pilot passed (8a2046 and a37a2f). All eight producer exits were collected, and the controller returned0 (2e091f). The full raw verifier returned0 (dc4451); all archives verified losslessly (ef1090), and the independent archived proof returned0 (00762f). Five corruption types were rejected separately in each archive shard. The116-file audit with complete archive replay, exact pilot regeneration and matrix replay returned0 (cf3ae6), with empty stderr and the required marker.

The 1,076,716,159-byte raw certificates are preserved locally; the committed deterministic archives contain224,198,201 bytes and reproduce the producer hashes. Catalogue completeness remains imported, while every supplied action is checked only by permutation word evaluation. Prime-power degree32 is handled theoretically, not by a missing catalogue.

Recorded the semiregular-normal-subgroup lifting lemma, its nilpotent consequence and product reductions with priority unclaimed. All six pages of Muller2026 were read, with two pages viewed. An exact F8 control verifies the printed source identities and an explicit witness fixing two cosets at the stronger derangement question's obstructed pair. Full Steinberg-group identification is not independently claimed. A memory-limited Factorization probe is preserved and excluded. General21.99 remains unresolved; new complete candidates44, outside reviews0.

n=7 snapshot 2026-09-12T12:27:50.028020+00:00: five pass markers, one verified-live PID [77400], worker4 checkpoint 6900000 nodes. The aggregate is pending. No external messages or Git pushes.

## 2026-09-12T12:42:59.152402+00:00: 21.132 priority correction

The preceding goal turn was progress: commit24eb5ec completed the degree47 word certificates. This turn revisited the unresolved radical-homogeneity issue in the earlier21.132 audit. Hong et al.2018 Proposition A explicitly states the needed classical result, with nonunital rings allowed. Sereda--Sozutov2006 Section1 was reread and its two theorem pages viewed. The1982 original proof remains imported through the explicit2018 statement.

A complete written deduction shows that the graded Levitzki quotient has a two-generated infinite centreless residually p-finite adjoint subgroup. Adjoining a one-dimensional zero algebra gives an infinite three-generated Golod group with centre C_p, meeting the exact9.76 definition and21.132 wording. The elementary grading, centre, infinitude and finite-quotient steps are all proved. This is our deduction from prior published theorems; an explicit earlier publication of this final answer has not been located.

The requested result is therefore reclassified as a prior consequence and excluded from the new-candidate count, which changes44 to43. The original four-generator triangular proof is retained without a mathematical defect found. Historical log entries are unchanged. The earlier21.106 and21.107 arguments were also reread during this audit turn, with no new defect identified; neither has outside independent review. No finite computation is claimed to prove the infinite-algebra deduction.

The n=7 controller and worker4 remain active; no restart or aggregate proof claim. Sources, page images and proof notes are retained locally, with no external messages or Git pushes.

The15-file source-and-note integrity check returned actual exit0 with its terminal marker (tool chunk6f3d2d); this checks file hashes and status consistency, not the imported radical proof. The retained download record matches the author PDF. The n=7 snapshot at2026-09-12T12:42:09.261425+00:00 has worker4 at6,980,000 checked nodes, five pass markers, and only the first four actual exits collected.

## 2026-09-12T13:12:27.766471+00:00:21.114 central-product theorem and derived-length-three examples

The preceding goal turn was progress: commit2191f24 reclassified21.132. This turn reread the21.106 and15.89 arguments with no new defect found, then investigated the central-extension route to21.114. The completed pilot covers3,181 catalogue groups in orders64,81,128,243,729; its1,901 class-at-least3 cases contain177 weakly ab-maximal groups. All are metabelian. Among177 computed Schur covers, exactly the covers of(128,854) and(128,860) raise derived length to3.

Central quotients of these covers give512-element groups with cyclic central kernel4 and weakly ab-maximal quotient128. Independent permutation checks reconstruct both groups, every homomorphism product, their derived series, and all776 quotient subgroups. The512-element groups themselves have abelian subgroups of order64 versus abelianization16. A general central-product theorem over Z/p^k Z supplies order8192 weakly ab-maximal outputs with derived length3. A separate proposition proves that every central extension of these outputs still has derived length at most3, so iteration cannot establish unboundedness.

Pilot returned0(1a975c), covers0(5c95b3), exporter0(42039c), final independent checker0(fade7a), and native central-product construction0(97d798). All have empty stderr and required markers. The51-file audit with byte-identical model regeneration and independent/native replay returned actual exit0(e9b316), with clean stderr and its marker. Final independent totals:4,352 permutation edges,557,056 table entries,524,288 homomorphism products,4,035,842 commutator pairs and776 quotient subgroups, plus five rejected corruptions. General21.114 and partial-result priority remain unresolved; complete new candidates43, outside reviews0.

The n=7 controller completed its aggregate at2026-09-12T13:08:05.432891+00:00. All six recorded worker exits are0 and no worker or controller remains live. The aggregate covers42,891,332 nodes and5,447,182,055 relation implications. Polling historical tool session84653 returned143(3f76ac); its association with the completed controller is not independently established. This is preserved without claiming a zero controller exit from that handle. A fresh full reporter was started with actual child PID recorded in results/20.100-n7-final-report-live.json and tool session34383, to recheck the completed proof evidence. No workers were restarted.

The exact GAP JSON dumps retain their original line-wrapping whitespace so byte-identical model replay remains meaningful. Whitespace checks pass for scripts and proof/report sources; the raw dumps are retained verbatim. All51 packet bindings match the staged Git content.

## 2026-09-12 13:28 UTC — completed20.100 n=7 proof packet

The preceding goal turn was progress: commit83010dc proved the21.114 central-product theorem and derived-length-three partial examples. This turn confirmed GAP4.16.1 and finalized the completed20.100 verification. All six actual worker exits are zero. Their disjoint partition verifies42,891,332 nodes,5,435,268 equality leaves,786,577,344 collision cases and5,447,182,055 relation implications. The structural finite-abelian reduction therefore gives the assertion for every eligible group at n=7, including infinite nonabelian groups. The general-n question remains unresolved; complete candidates43, outside reviews0, priority unestablished.

The fresh full reporter returned actual zero with empty stderr at13:13:13 UTC; its receipt and exact output are preserved. A new strict C++ data parser then consumed all four complete archives. For n=7 it independently recovered all19,404,331,316 raw bytes and the recorded SHA256 in109.837 seconds, proving the archive contains only literal-data calls to the mathematical checker. Eleven malformed inputs were rejected. The data wrapper returned actual zero with its marker and empty stderr (tool chunk6f2033).

A separate final auditor consumes every worker log token and requires the exact commands, common hashes, all six actual exits, every checkpoint partition ID, terminal counts and aggregate. Nine additional corruptions are rejected, including missing/nonzero exits and a warning after PASS. This explicitly supplies an actual-exit check absent from the older full reporter's aggregate-reader function. No mathematical checker or original runner was changed, and no25-hour mathematical verification was repeated.

The62-file packet audit returned actual zero at13:28:22 UTC with empty stderr and its terminal marker (tool chunk0ca474). The1,271,256,410-byte complete archive, six full verifier logs, receipts, proof/review notes, scripts, controls and Sun source are included in the local commit. Earlier incomplete gzip prefixes remain preserved locally. The historical tool84653/exit143 association discrepancy is retained without claiming a zero controller exit from that handle. No external messages or pushes.

## 2026-09-12T14:00:49.754354+00:00: 11.115 proper-power counterexample

The preceding goal turn was progress: commit2cf0a75 completed the all-group n=7 partial proof of20.100. This turn found a full negative candidate for11.115. For X=F(a,b), N=<<a^m>> and T=ker(X->C_m), m>=2, normality of T and N permits the quotient X/[T,N]. In that quotient a^m commutes with both free generators, so its normal closure is central and [T,N]=[X,N]. Maps to C_m and Z prove N<T<X. The common subgroup is nontrivial and proper in N; m=4 also makes T nonmaximal. The printed page56 was viewed and all hypotheses were checked.

A self-contained proof identifies the common subgroup as <<[a^m,b]>> and X/[T,N] as F_m semidirect Z. Schreier free bases and both conjugation maps provide supplementary word controls. Native GAP returned actual0 with clean stderr (a22d4d), checking seven moduli and228 identities. Independent signed-word arithmetic returned actual0 (5938e0):91,847 exhaustive reduced words,7,000 longer samples,7,000 products,7,000 associativity triples and five rejected corruptions. The 25-file audit regenerated all seven GAP models byte for byte and replayed Python; actual exit0 at14:00:01 UTC with empty stderr (d61dba). The infinite-subgroup theorem rests on the mathematical proof, not these finite ranges.

The prior finite-index and primitive-element sufficient conditions remain valid and do not cover this example. Limited primary-source searches did not locate an explicit earlier answer, which does not establish novelty. New complete candidates increase43 to44; outside reviews remain0. The internal reading audit of9.4,13.42,4.75,10.62 and part of15.92 is separately recorded with its exact scope. No external messages or pushes.

## 2026-09-12T14:03:25.816368+00:00: preserve the stopped20.113 feasibility probe

Installed ANUPQ3.3.3 supports64-bit builds but retains int presentation/workspace indices and packed fields. Its lower exponent-p class agrees with ordinary class for exponent7, not automatically for exponent8. The bounded H(7,8) probe printed quotient log-orders4,9,25,70,214,654,1978,6238 without finishing the GAP result path. Its180-second wrapper terminated it and collected actual exit1; no completion marker or Schur multiplier was produced. The native pq child had ended before the bound, while the precise expensive GAP stage was not instrumented. There was no restart.

Vaughan-Lee arXiv:2111.11098v3 is cached with its download hash. Reading covered the abstract, introduction, statements on pages1–4 and Theorem1's short proof; the rest was not audited. Neither subpart is solved. Commit3a7915a preserved nine evidence files. The initial inline evidence audit rejected a list-versus-tuple comparison and failed before creating its packet; the following shell commands still committed those files. The error and its limited effect are recorded. The standalone corrected auditor returned actual0 (6cc555), verifying eleven bound files and requiring the probe's failed completion status. This audit does not rerun the stopped probe. Complete candidates remain44; outside reviews0. No external messages or pushes.

## 2026-09-12T14:31:10.626287+00:00: elementary class-two refinement and16.14 status reconciliation

The preceding goal turn was progress:65ab2ba completed11.115, and3a7915a/04912a8 preserved and audited the stopped20.113 probe. This turn revisited several unresolved free-group and graph-group leads without closing their gaps, recorded in research/triage-2026-09-12-1405.md. A new elementary square-map argument removes the exponent restriction from the previous class-two case of16.14 and proves the stronger d(G)+dim Z/(Z intersection Phi(G))<=2 rank(Z(G)). Products of quaternion and cyclic groups attain equality; applying the theorem to subgroups also bounds every section's generator number by2 rank(Z(G)).

The pre-final ledger check caught a stale portfolio row and later status entry:16.14 was already fully answered here as a consequence of Sambale's prior centralizer bound, recorded in commitf3c185b. The relevant source argument was reread and agrees with that deduction. The new elementary refinement is retained, but supplies no new solution. Canonical stale entries and the older plan/exponent-four scope are corrected. The MacWilliams input for the full prior result remains imported. Complete candidates44, outside reviews0.

Ten GAP models include exponent64 abelian data, quaternion direct factors, failures of the central-involution hypothesis, and an order256 exponent8 group with derived exponent4. Independent table arithmetic reconstructs84,097 table entries,291,200 generating associativity cases,401 square-map representative checks and4,483 polarization triples. All1,086,606 small quadratic maps satisfy the predicted zero-count restriction; an anisotropic cubic is rejected. Five model corruptions are rejected.

Four native setup runs failed despite child exit0; stderr and missing markers correctly rejected them. A prematurely started independent run failed on missing input. Every failed source/log/receipt and emitted prefix is preserved. The accepted native returned actual0 (99ff5b); the final independent checker, with its stale scope corrected, returned actual0(c43701). The earlier successful output with its stale scope is retained separately. The70-file audit regenerates all ten models byte for byte and repeats the independent proof; actual completion is recorded in results/16.14-class2-audit-process.json. These finite controls supplement the mathematical proof and do not establish the stronger refinement in higher class. No external messages or pushes.
