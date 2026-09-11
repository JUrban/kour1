# Kourovka Notebook research

Objective: solve as many previously unsolved problems in `docs/21tkt.pdf` as possible during a 48-hour research period. This is a local working repository; no remote publication or push is authorized.

Research started 2026-09-10 20:56:46 UTC (active-goal creation). Deadline: 2026-09-12 20:56:46 UTC. Target resource limits: at most 20 computational cores and 100 GB RAM in total.

Eight complete candidate resolutions are written for 21.106, 21.132,
21.121(a), 21.68, 16.87(a),(b), 10.35, 16.28(a), and 17.34, each with a
separate internal audit. All await independent review
and further novelty checks. An additional small counterexample to 13.19 is
retained as a rediscovery: a prior paper already implies a negative answer.
See `reports/STATUS.md`, `research/PLAN.md`, and `reports/LOG.md` for current
evidence and next actions.

The supplied Notebook is the 21st edition, updated through September 2026. SHA-256: `2fcce9b98a4df10267fe120229217bfe556c70510704e311540da0cef438f911`. Its searchable text was extracted with `pdftotext -layout`. Mathematical notation in extracted text must be checked against the PDF before relying on a statement.

Repository layout:

- `research/`: problem selection, mathematical work, proof drafts, and failed approaches.
- `scripts/`: reproducible exact computations and verification tools.
- `results/`: retained computation output and certificates.
- `reports/`: dated progress and reviewable reports.
- `references/`: bibliography and literature-status evidence.
- `state/`: research clock and job bookkeeping; live processes must be verified independently of these files.

GAP is supplied in `gap-4.16.1/` and excluded from version control. Research artifacts and the input Notebook are tracked. Claims are labeled conjectural, computational evidence, proved partial result, candidate solution, or reviewed solution; a finite negative search is never called a general proof.
