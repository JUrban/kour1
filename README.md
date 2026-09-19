# Forty-eight hours with the Kourovka Notebook

**[Read the paper (PDF)](paper/kourovka-experiment.pdf)** ·
[Paper source and reproduction guide](paper/README.md) ·
[Notebook used in the experiment (PDF)](docs/21tkt.pdf)

This repository records a 48-hour mathematical research experiment conceived
and overseen by Michael Kinyon and Josef Urban. OpenAI's GPT-6 Astra, running
through Codex, used GAP, exact programs and mathematical literature to
investigate open problems in the
[Kourovka Notebook](https://arxiv.org/abs/1401.0300), a collection of problems
in group theory and neighboring areas edited by E. I. Khukhro and V. D. Mazurov.
The supplied input is the September 2026 revision of its 21st edition.

The research ran from **10 September 2026, 20:56:46 UTC**, to
**12 September 2026, 20:56:46 UTC**, with requested local limits of generally
20 CPU cores and 100 GB RAM.

The deadline ledger recorded **46 complete solution candidates**, covering
problem entries or specified subparts. **Version 3 withdraws the claim for
10.35, leaving 45 candidates**: the original problem concerns algebraic
numbers, while our argument concerns rational numbers. The Notebook's
editor, Evgeny Khukhro, identified the error after both model reviews had
accepted the entry. The paper also presents partial
results on nine questions, rediscoveries, deductions from prior work and
bounded computations. The 46-entry total records the deadline classification;
it is not a count of established new theorems.

Anthropic's **Claude Opus[1m]**, running through Claude Code, subsequently
reviewed all 46 entries, reported verifying a majority in detail, and independently
reconstructed many finite examples and calculations. The revised paper
incorporates corrections and a strengthened counterexample, and includes
the [review correspondence](paper/external-reviews/) verbatim in appendices.

The comparison added in **version 2 (19 September 2026)** covers eleven entries with contemporary
solutions identified by the Notebook's editor. It credits shared arguments,
different constructions and stronger alternatives, and identifies older
sources for the qualitative computability result in 16.9. The comparison
does not assign discovery priority or establish novelty of the other entries.

Start with **Section 2 of the paper** for the full results inventory and
**Section 3** for the independent review. **Appendix M** gives a preliminary
review and comparison of the
[parallel Claude Fable experiment](https://github.com/JUrban/kour1cl), run
by the same organizers on the same machine and local resource budget.
**Appendix N** presents the eleven-entry comparison; its
[review records](paper/reviews/v2-2026-09-19/) include source hashes,
artifact chronology and new mathematical checks.
**Appendix O** records the 10.35 withdrawal and the subsequent visual
statement audit. The [v3 review record](paper/reviews/v3-2026-09-19/)
includes the rendered Notebook statements for all 46 historical candidates
and individual scope notes. This audit does not certify the remaining proofs.

## Research records

The [final research report](reports/FINAL_REPORT.md),
[review guide](reports/REVIEW_GUIDE.md), and
[candidate ledger](research/complete-candidate-ledger.json) preserve the
deadline record. Dated progress reports retain their original counts and
review status; use the revised paper for the subsequent assessment.

- [paper/](paper/): current PDF, LaTeX sources, review records and reproduction instructions.
- [docs/](docs/): the supplied Notebook and searchable text.
- [research/](research/): proofs, partial results, source audits and unsuccessful approaches.
- [scripts/](scripts/): exact computations and verification programs.
- [results/](results/): retained computation outputs and certificates.
- [reports/](reports/): dated progress, final report and review guide.
- [references/](references/): literature and attribution records.
- [state/](state/): historical research-clock and job bookkeeping.

The public repository was filtered to remove blobs larger than 90M, so its
commit hashes differ from the original local archive. In particular, the
1.27 GB certificate for the final 20.100 case is omitted: retained logs
document its historical verification, but do not enable a complete new replay.
See the [artifact notes](paper/README.md) for the precise boundary and the
accessible research snapshot. The computations used GAP 4.16.1; the full
software installation is not bundled.
