# Review handoff checkpoint report

12 September 2026, after the 19:00 UTC inventory check. Research remains
active until 20:56:46 UTC. This checkpoint is not the final deadline report.

## Deliverables

The [review guide](REVIEW_GUIDE.md) gives entry points for all 46 current
complete candidates. The [ledger](../research/complete-candidate-ledger.json)
records each problem number, exactly claimed subparts, original indexed
statement, principal proof files, review or source-scope files, and evidence
entry points. The count is of candidates by problem, not of individual
subparts. Outside reviews remain zero; priority remains unestablished.

The [inventory auditor](../scripts/audit_candidate_handoff.py) checks
statement-index agreement, file existence, Git-index inclusion, and the
actual expected digests from the selected historical manifests. It uses
streaming reads and caches shared files, so repeated bindings do not cause
repeated full-file reads. It does not execute the mathematical verifiers.

## Observed results and correction

The initial invocation ran from 18:59:56.548721 to 18:59:59.310951 UTC,
with actual exit 1 and empty stderr. Its result was:

- 46 candidates, with every selected entry-point path present;
- 1,870 historical bindings, all matching;
- 1,252 distinct files, totaling 328,556,704 bytes;
- 19 existing cached source files absent from the Git index.

Those nineteen files totaled 12,666,011 bytes. They were added explicitly
with `git add -f`, retaining their exact existing bytes. Their paths are
listed in the [initial observation](../results/candidate-handoff-integrity-initial.json).
No historical digest was changed, and no missing file was regenerated.
The initial failure concerns archival completeness, not a failed
mathematical computation.

The second invocation used the same ledger and auditor. It ran from
19:00:46.529640 to 19:00:49.317226 UTC, with actual exit 0 and empty
stderr. It checked the same 1,870 bindings and 1,252 files, with no
missing, untracked, or mismatching paths. Its exact observations and
process record are retained in
[the final inventory](../results/candidate-handoff-integrity.json) and
[its process record](../results/candidate-handoff-integrity-process.json).
Both original stdout/stderr streams are archived for each invocation.

The auditor SHA256 was
`199d8cef860d9f08ac7bce1ba8f10dbdc2cd59e599ad3f586a25ed323373a4ab`.
The successful stdout SHA256 was
`ce1c7df296f70d884a816d9f235fa1e285a983caa919ce3d694ae1f372a596bd`.
These are integrity observations, not evidence of a formal proof.

Twenty-nine candidate entry points have historical hash manifests.
Seventeen instead use earlier control logs or verification records.
The inventory snapshots their current tracked files but does not assert
historical hash or process evidence that was never recorded. Individual
proofs and internal reviews continue to govern the exact interpretation
of the finite computations and imported results.

## Additional mathematical reading in this turn

The principal arguments for three candidates were read again with their
critical transitions in view:

- **17.39:** the biprime Sylow-system definition really gives every
  conjugate of C_G(t); the graph equations bound arbitrary intersections,
  not just the displayed successful sequence. The Frattini calculation
  is separate from the negative answer and agrees with the cited positive
  theorem's excluded hypothesis.
- **14.26:** the coefficient ideal is stable under the derivation; the
  Lagrange functionals descend and distinguish every required diagonal
  power. The inserted delta-image filtration is a central series, and
  the final maps preserve precisely the finite multiplication tables
  required for quasivariety membership. No homomorphism from the entire
  wreath product into a single nilpotent group is assumed.
- **15.76(b):** coefficient multiplication retains its noncommutative
  order; only units in the cyclic Laurent subring are used. The Magnus
  kernel identifies the word in the correct derived quotient, and the
  final objectwise isomorphisms satisfy naturality in the full category.

No new mathematical gap was identified in these readings. They are
additional readings by the same research agent, not independent outside
reviews, and are not presented as a fresh full audit of all 46 proofs.

## Remaining work

The deadline has not been reached. Continue discovery and source checking,
and update the final report with the actual deadline outcome. The general
positive-characteristic case of 20.89 remains unresolved. The same is true
of the other partial and bounded-search targets excluded from the ledger.
The handoff packet preserves this checkpoint without freezing the mutable
portfolio or claiming that the research objective is already complete.
