# Review guide: 46 complete solution candidates

Checkpoint: 12 September 2026, 19:00 UTC. Research remains active until
20:56:46 UTC. This guide indexes proposed complete answers and complete
answers to separately asked subparts. It is not a claim of 46 accepted
new solutions. All 46 await independent outside review, and priority
has not been established. Multiple answered parts of one problem count
as one candidate here; duplicate question 19.63 is not counted separately.

The exact indexed Notebook statement, covered subparts, principal files,
and evidence entry points for every row are retained in the
[machine-readable ledger](../research/complete-candidate-ledger.json).
The supplied [PDF](../docs/21tkt.pdf) remains authoritative. The handoff
audit compares the ledger to the existing statement index; it does not
constitute a new visual reading of all 46 PDF statements.

For a short initial review, the explicit finite constructions for
21.68, 20.108(a,b), 20.122(a–c), and 17.39 have direct group descriptions
and separate computational controls. The proofs for infinite groups,
topology, and asymptotic formulas must be assessed at their full stated
scope; finite controls do not prove their infinite assertions.

## Inventory integrity and its limits

The [inventory audit](../results/candidate-handoff-integrity.json) passed
with actual process exit 0 and empty stderr. It checked **1,870 historical
hash bindings**, reading **1,252 distinct files** totaling **328,556,704
bytes**. There were no missing linked files or historical digest
mismatches. All inspected source and evidence files are now in the Git
index for the local handoff commit.

Twenty-nine candidates have historical hash manifests at the selected
entry points. The remaining seventeen have earlier control logs or
verification records. Their linked files are included in the current
snapshot, but this does not retrospectively create a historical frozen
manifest or a missing process record. The per-candidate distinction is
explicit in the audit JSON.

The initial inventory audit failed because nineteen matching cached
source files had not been added to Git. Their existing bytes were added,
without changing any expected digest. The initial audit, logs, and actual
exit 1 remain archived; the second invocation passed with the same
ledger and auditor. See the [handoff report](review-handoff-report.md).
No mathematical search or certificate verifier was rerun during this
inventory audit, and its PASS result is not mathematical acceptance.

## Candidate entry points

"All" in the parts column records the current complete-candidate claim;
it does not replace the original statement. Read the proof's convention
and hypothesis discussion, especially where the Notebook terminology
admits multiple readings. Earlier proofs remain available where a later
proof supersedes them.

| Problem / parts | Proposed result | Proof and review scope | Evidence entry points |
|---|---|---|---|
| 21.106 (all) | A parameter-free definable two-element set generating an infinite subgroup | [proof](../research/21.106-proof.md); [review / source scope](../research/21.106-review.md) | [21.106-verification.txt](../results/21.106-verification.txt) |
| 21.121 (a) | The p-Jordan infimum need not be attained | [proof](../research/21.121a-proof.md); [review / source scope](../research/21.121a-review.md) | [21.121a-controls.json](../results/21.121a-controls.json); [21.121a-subgroups.log](../results/21.121a-subgroups.log) |
| 21.68 (all) | A semi-abelian non-monomial group of order 2592 | [proof](../research/21.68-proof.md); [review / source scope](../research/21.68-review.md) | [21.68-independent-verification.json](../results/21.68-independent-verification.json); [21.68-gap-verification.log](../results/21.68-gap-verification.log) |
| 16.87 (a,b) | Maximal test rank at every finite rank in a nonabelian nonperiodic variety | [proof](../research/16.87-proof.md); [review / source scope](../research/16.87-review.md) | [16.87-verification.json](../results/16.87-verification.json) |
| 10.35 (all) | A torsion-free complex linear group not residually rational in the same degree | [proof](../research/10.35-proof.md); [review / source scope](../research/10.35-review.md) | [10.35-verification.json](../results/10.35-verification.json) |
| 16.28 (a) | A closed set whose every power greater than one is nonclosed | [proof](../research/16.28-proof.md); [review / source scope](../research/16.28-review.md) | [16.28-gap-validation.json](../results/16.28-gap-validation.json); [16.28-independent-verification.json](../results/16.28-independent-verification.json) |
| 14.22 (all) | Failure of the stated finite isolated-radical presentation | [proof](../research/14.22-proof.md); [review / source scope](../research/14.22-review.md) | [14.22-verification.json](../results/14.22-verification.json) |
| 16.20 (all) | A finite modular nondistributive dominion lattice | [proof](../research/16.20-proof.md); [review / source scope](../research/16.20-review.md) | [16.20-verification.json](../results/16.20-verification.json); [16.20-factor-verification.log](../results/16.20-factor-verification.log) |
| 17.33 (all) | Infinite axiomatic rank of the Klein bottle quasivariety | [proof](../research/17.33-proof.md); [review / source scope](../research/17.33-review.md) | [17.33-verification.json](../results/17.33-verification.json); [17.33-gap.log](../results/17.33-gap.log) |
| 17.101 (all) | Every group representation has a homogeneous extension | [proof](../research/17.101-proof.md); [review / source scope](../research/17.101-review.md) | [17.101-verification.json](../results/17.101-verification.json); [17.101-gap.log](../results/17.101-gap.log) |
| 18.76 (all) | A nonsplit additive division-ring extension | [proof](../research/18.76-proof.md); [review / source scope](../research/18.76-review.md) | [18.76-controls.json](../results/18.76-controls.json); [18.76-gap-controls.log](../results/18.76-gap-controls.log) |
| 18.92 (a,b) | Non-algebraic and non-modular complete lattices of formations | [proof](../research/18.92-proof.md); [review / source scope](../research/18.92-review.md) | [18.92-controls.json](../results/18.92-controls.json) |
| 20.108 (a,b) | A centerless group of order 605 with a multiple-holomorph quotient element of order four | [proof](../research/20.108-proof.md); [review / source scope](../research/20.108-review.md) | [20.108-python-controls.log](../results/20.108-python-controls.log); [20.108-gap-controls.log](../results/20.108-gap-controls.log); [20.108-family-controls.log](../results/20.108-family-controls.log) |
| 20.90 (all) | A two-generator infinite profinite CA-group mapping onto A5 | [proof](../research/20.90-2adic-proof.md); [proof 2](../research/20.90-proof.md); [review / source scope](../research/20.90-review.md) | [20.90-2adic-controls.log](../results/20.90-2adic-controls.log); [20.90-python-controls.log](../results/20.90-python-controls.log); [20.90-gap-controls.log](../results/20.90-gap-controls.log) |
| 11.116 (all) | Finite subgroup-lattice dimension for the specified Chernikov groups | [proof](../research/11.116-proof.md); [review / source scope](../research/11.116-review.md) | [11.116-controls-summary.json](../results/11.116-controls-summary.json) |
| 14.72 (all) | A smooth affine surface with a smooth fixed divisor and a singular cyclic quotient | [proof](../research/14.72-proof.md); [review / source scope](../research/14.72-review.md) | [14.72-controls-summary.json](../results/14.72-controls-summary.json) |
| 21.40 (all) | Virtual nilpotence of rational linear groups with finitely many automorphism orbits | [proof](../research/21.40-proof.md); [review / source scope](../research/21.40-review.md) | [21.40-python-controls.json](../results/21.40-python-controls.json); [21.40-gap-controls.log](../results/21.40-gap-controls.log) |
| 21.60 (all) | An order-twelve counterexample to the semiperfectness criterion | [proof](../research/21.60-proof.md); [review / source scope](../research/21.60-review.md) | [21.60-python-controls.json](../results/21.60-python-controls.json); [21.60-gap-controls.log](../results/21.60-gap-controls.log) |
| 4.55 (all) | Non-unique indecomposable projective decompositions over Z_(5)[3.A7] | [proof](../research/4.55-proof.md); [review / source scope](../research/4.55-review.md) | [4.55-python-controls.json](../results/4.55-python-controls.json); [4.55-gap-controls.log](../results/4.55-gap-controls.log) |
| 21.107 (all) | A countable resolvable group without an expansive sequence | [proof](../research/21.107-proof.md); [review / source scope](../research/21.107-review.md) | [21.107-provenance.json](../results/21.107-provenance.json) |
| 15.89 (all) | An infinite four-regular Cayley graph with invertible adjacency on all functions | [proof](../research/15.89-proof.md); [review / source scope](../research/15.89-review.md) | [15.89-free-product-summary.json](../results/15.89-free-product-summary.json) |
| 16.9 (all) | An exact cubic-time minimum-palindrome-factorization algorithm in free groups | [proof](../research/16.9-proof.md); [review / source scope](../research/16.9-review.md) | [16.9-summary.json](../results/16.9-summary.json) |
| 18.18 (all) | Non-enumerability of both the cofinite finite-group theory and its complement | [proof](../research/18.18-proof.md); [review / source scope](../research/18.18-review.md) | [18.18-summary.json](../results/18.18-summary.json) |
| 19.56 (all) | Solubility from the restricted coprime-commutator order condition | [proof](../research/19.56-proof.md); [review / source scope](../research/19.56-review.md) | [19.56-summary.json](../results/19.56-summary.json) |
| 20.92 (a) | The printed brace average is pre-Lie for every uniformly sufficiently large prime | [proof](../research/20.92a-proof.md); [review / source scope](../research/20.92a-review.md) | [20.92a-summary.json](../results/20.92a-summary.json) |
| 9.47 (all) | A height-four scattered compact space excluded from the stated E-spaces | [proof](../research/9.47-proof.md); [review / source scope](../research/9.47-review.md) | [9.47-summary.json](../results/9.47-summary.json) |
| 9.45 (all) | An explicit criterion for orthogonal bases in every dimension | [proof](../research/9.45-proof.md); [review / source scope](../research/9.45-review.md) | [9.45-summary.json](../results/9.45-summary.json) |
| 10.62 (all) | A three-generated perfect periodic group with one involution class and odd pairwise products | [proof](../research/10.62-proof.md); [review / source scope](../research/10.62-review.md) | [10.62-summary.json](../results/10.62-summary.json) |
| 10.32 (all) | An explicit logarithmic degree bound for symmetric-group power-word universality | [proof](../research/10.32-proof.md); [review / source scope](../research/10.32-review.md) | [10.32-summary.json](../results/10.32-summary.json) |
| 15.65 (all) | Nonrationality of the stated classical cyclic and semisimple limits | [proof](../research/15.65-classical-proof.md); [proof 2](../research/15.65-proof.md); [review / source scope](../research/15.65-classical-review.md); [additional review](../research/15.65-review.md) | [15.65-classical-summary.json](../results/15.65-classical-summary.json); [15.65-summary.json](../results/15.65-summary.json) |
| 15.92 (all) | Continuum many infinite alternating-residual quotients of every triangle group Delta(2,3,r), r>6 | [proof](../research/15.92-proof.md); [review / source scope](../research/15.92-review.md) | [15.92-summary.json](../results/15.92-summary.json) |
| 4.75 (all) | A periodic group with Sylow two-subgroups of order two and noncentral involutions modulo the odd-order radical | [proof](../research/4.75-proof.md); [review / source scope](../research/4.75-review.md) | [4.75-summary.json](../results/4.75-summary.json) |
| 9.4 (all) | No finite quasigroup generates the ordinary isotope variety of a nontrivial finite group | [proof](../research/9.4-proof.md); [review / source scope](../research/9.4-review.md) | [9.4-summary.json](../results/9.4-summary.json) |
| 12.40 (all) | Unbounded Brauer-degree p-parts with the group-order p-part fixed | [proof](../research/12.40-proof.md); [review / source scope](../research/12.40-review.md); [report](../research/12.40-report.md) | [12.40-summary.json](../results/12.40-summary.json) |
| 13.42 (all) | A free nilpotent group with a Z[t]-completion that is not locally nilpotent | [proof](../research/13.42-proof.md); [review / source scope](../research/13.42-review.md); [report](../research/13.42-report.md) | [13.42-summary.json](../results/13.42-summary.json) |
| 14.26 (all) | Closure of the torsion-free nilpotent quasivariety under restricted wreath products with Z | [proof](../research/14.26-proof.md); [review / source scope](../research/14.26-review.md); [report](../research/14.26-report.md) | [14.26-summary.json](../results/14.26-summary.json) |
| 15.76 (b) | Innerness of category automorphisms for full varieties of groups of fixed derived length | [proof](../research/15.76-proof.md); [review / source scope](../research/15.76-review.md); [report](../research/15.76-report.md) | [15.76-summary.json](../results/15.76-summary.json) |
| 16.38 (all) | Periodicity of subgroups contained in a product of periodic subgroups in a soluble group | [proof](../research/16.38-proof.md); [review / source scope](../research/16.38-review.md); [report](../research/16.38-report.md) | [16.38-summary.json](../results/16.38-summary.json) |
| 19.93 (all) | Unbounded lower p-central factors in the specified two-generator finite p-groups | [proof](../research/19.93-proof.md); [review / source scope](../research/19.93-review.md); [report](../research/19.93-report.md) | [19.93-summary.json](../results/19.93-summary.json) |
| 20.1 (all) | The insoluble totally two-closed group J1 times C13 with Fitting subgroup C13 | [proof](../research/20.1-proof.md); [review / source scope](../research/20.1-review.md); [report](../research/20.1-report.md) | [20.1-summary.json](../results/20.1-summary.json) |
| 19.62 (all; duplicate 19.63 not counted) | Every derived elementary carpet is closed | [proof](../research/19.62-rank-two-proof.md); [proof 2](../research/19.62-rank-two-derivations.md); [proof 3](../research/19.62-closedness-criterion.md); [review / source scope](../research/19.62-proof.md) | [19.62-rank-two-packet.json](../results/19.62-rank-two-packet.json) |
| 19.61 (all) | Every carpet closure is a carpet with unchanged derived carpet | [proof](../research/19.61-proof.md); [review / source scope](../research/19.61-report.md) | [19.61-square-completion-packet.json](../results/19.61-square-completion-packet.json) |
| 21.76 (all) | Irreducible closed noncompletable nets of every order in every odd characteristic | [proof](../research/21.76-proof.md); [review / source scope](../research/21.76-source-audit.md); [report](../research/21.76-report.md) | [21.76-packet.json](../results/21.76-packet.json) |
| 11.115 (all) | Proper-power normal closures with equal commutator subgroups | [proof](../research/11.115-proof.md); [review / source scope](../research/11.115-report.md) | [11.115-packet.json](../results/11.115-packet.json) |
| 20.122 (a,b,c) | Minimum-order intersections outside the Fitting subgroup in a soluble wreath group | [proof](../research/20.122-minimum-proof.md); [review / source scope](../research/20.122-minimum-source-audit.md); [report](../research/20.122-minimum-report.md) | [20.122-minimum-packet.json](../results/20.122-minimum-packet.json) |
| 17.39 (all) | Unbounded numbers of system normalizers, with fixed Frattini order three | [proof](../research/17.39-proof.md); [review / source scope](../research/17.39-source-audit.md); [report](../research/17.39-report.md) | [17.39-packet.json](../results/17.39-packet.json) |

## Results that are deliberately outside the count

The portfolio also contains substantial partial results and exact bounded
searches. They are not promoted to full resolutions by this inventory.
Examples include [20.89 / 19.83](../research/20.89-char0-proof.md),
[20.124 in infinite rank](../research/20.124-infinite-rank-proof.md),
[21.114](../research/21.114-report.md),
[17.118](../research/17.118-report.md), and
[21.99](../research/21.99-extension-report.md). The latest additional
20.89 case is [bounded finite-subgroup orders](../research/20.89-bounded-torsion-proof.md).
The full [portfolio](../research/PORTFOLIO.md) and
[status report](STATUS.md) describe the other partial results and searches.

Identified prior answers and prior-theorem consequences remain excluded.
In particular, 21.132, 21.115, 16.14, and 19.48 are not in this ledger.
A proof retained in the repository is not, by its presence alone, a new
candidate. The relevant source audits explain the reclassifications.

## Reproducing this inventory checkpoint

From the repository root, run:

```sh
python3 scripts/audit_candidate_handoff.py --output results/candidate-handoff-integrity-recheck.json
```

This verifies links and recorded hashes and writes a fresh observation.
It does not execute GAP, replay the mathematical certificate programs,
or check novelty. Individual evidence summaries and reports identify
those programs and their original execution records, including rejected
and deliberately stopped runs. Do not interpret a GAP exit code of zero
alone as successful verification; the individual runners also check
errors, completion markers, and the stated case coverage.

This checkpoint is part of the ongoing 48-hour task. The final report
will state the actual deadline outcome and any later changes to this
ledger. No repository push or outside communication is part of this
handoff.
