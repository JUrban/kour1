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
