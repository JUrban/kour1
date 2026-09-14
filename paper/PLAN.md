# ArXiv manuscript plan

Requested on 14 September 2026: write a substantial paper about the 48-hour
Kourovka Notebook experiment, including its setting, technology, actual
trajectory, mathematical results, rediscoveries and alternative proofs,
partial results, outlook and recommendations; review and revise until the
review has no unresolved findings. This plan preserves that full scope.

## Evidence boundary

The experimental archive is frozen at commit
`cff2c37b9bf6b737e8ad5f7ead12291a551b5201`. Manuscript work is a later phase
on branch `paper/arxiv-experiment`. Do not change frozen proofs, historical
manifests, or research results to improve the apparent experiment.
Manuscript corrections and reclassifications belong under `paper/` and
must distinguish the deadline ledger from the current assessment.

The supplied HTML/text exports in `session/` are post-experiment evidence.
Determine what they actually retain. In particular, the advertised event
count is not the number of exported DOM events, cumulative token counters
must not be summed, and absence of exported tool/analysis events is not
evidence that no tools or analysis occurred. Raw private session files
will remain separate; the paper will include a reproducible aggregate
analysis with input digests and precise limitations.

## Deliverables

1. A readable research paper in LaTeX with a compiled PDF and a portable
   source bundle suitable for an eventual arXiv upload by the human author.
   No upload, submission, or Git push is part of this task.
2. An evidence-based experimental narrative: prompt and selection policy,
   software and resource setting, continuation and external memory,
   chronology, computations, checks, failures, corrections, and outcome.
3. Mathematical content: precise accounts of all 46 deadline candidates,
   detailed proofs and counterexamples, substantial partial results, and
   selected rediscoveries or alternative deductions from prior work.
   Long appendices are acceptable; do not reduce this to a numerical
   success-rate report or a collection of unsupported theorem summaries.
4. A clear separation between proof validity, exact computational checks,
   source coverage, priority, and outside acceptance. No unreviewed
   candidate count is described as a count of accepted new theorems.
5. Reproducible session/Git statistics, figures where they clarify the
   experiment, an artifact map, and a verified bibliography.
6. Discussion of limitations, dependence among claims, selection bias,
   possible training-data overlap, absence of a baseline, verification
   costs, and concrete recommendations for a follow-up experiment.
7. A recorded review process covering mathematics, empirical claims,
   attribution, clarity, typesetting, references, and reproducibility;
   successive fixes followed by a final full review with no unresolved
   findings. This is not a promise that future referees will find no error.

## Work sequence

- Establish a source inventory and exact export parser; distinguish
  measured, documented, inferred, and unavailable experimental metadata.
- Build the LaTeX structure, bibliography, generated inventory tables,
  and deterministic build/source-bundle commands.
- Write the main narrative and representative complete proofs in proper
  mathematical notation, supported by the actual artifacts.
- Audit and develop the remaining result appendices, including shared
  imported dependencies and the distinction between rediscovery and
  merely locating a prior result. Record any changed claim status.
- Review each result against the original Notebook statement and its
  load-bearing mathematics, not just an existing PASS log.
- Recheck sources and manuscript statistics; inspect rendered pages;
  revise all findings and repeat a full manuscript review.
- Compile and validate the final PDF and standalone source bundle;
  perform a requirement-by-requirement completion audit and commit locally.

## Publication metadata

Author names and affiliations remain pending. The user confirmed the
historical model and reasoning setting as gpt-6-astra xhigh; this is
attributed metadata, not a measurement from the export. The Git remote names
`https://github.com/JUrban/kour1.git`; public availability and the precise
archival revision must be checked before describing it as published.
The supplied session identifies Codex 0.153.4 but no model ID
has been found in that export. Do not substitute the current model or
current configuration for the historical run.

## Review discipline

Maintain a per-result review ledger and a manuscript issue log. For every
load-bearing assertion, identify the proof, exact computation, source,
or measurement that supports it. If an assertion cannot be justified,
repair it or explicitly revise its status and explain the effect on the
paper. Preserve the historical 46-entry outcome independently of that
later assessment. Imported theorems may be cited normally, but an exact
source statement must support the application.
