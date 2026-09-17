# Forty-eight hours with the Kourovka Notebook

[Read the revised paper (PDF)](kourovka-experiment.pdf) ·
[Reviewed 15 September version (PDF)](versions/kourovka-experiment-2026-09-15.pdf).

This is the 17 September revision, on branch `paper/review-revision`.
The original unfiltered research snapshot is
`cff2c37b9bf6b737e8ad5f7ead12291a551b5201`; the accessible
[public filtered snapshot](https://github.com/JUrban/kour1/tree/bbfac1ac810117da37f01716d4594dc2b2e96980)
is `bbfac1ac810117da37f01716d4594dc2b2e96980`. The owner removed blobs over
90M with `--strip-blobs-bigger-than 90M`, rewriting commit identifiers.
`data/public-artifacts.json` records the comparison: all 4,146 retained
research blobs match; the sole omitted file at that snapshot is the
1.27 GB 20.100 certificate. That certificate is not in either paper bundle;
the public logs document its historical verification but do not permit a
complete new replay. No separate large-file deposit is claimed.

The manuscript contains the experimental
narrative, all 46 deadline candidate expositions, substantial partial
results, prior-result comparisons, and reproduction information.

The local handoff files are:

- dist/kourovka-experiment.pdf
- dist/kourovka-experiment-arxiv-source.tar.gz: main.tex, bibliography,
  compiled figure, and portable integer carpet proofs under anc/.
- dist/kourovka-experiment-full-source.zip: the complete manuscript
  project, measurements, review records, scripts, and ancillary proofs.
- dist/manifest.json: SHA-256 digests and sizes of those three files.

The source archives can be generated with:

~~~sh
python3 paper/scripts/build_paper.py --require-complete
python3 paper/scripts/package_paper.py
~~~

The build script uses Tectonic on PATH, PAPER_TECTONIC, or the local
software/paper-toolchain/tectonic binary. A standard LaTeX installation
can instead compile main.tex with XeLaTeX and BibTeX. The source archives
include main.bbl and the compiled trajectory figure; compiling the paper
does not require GAP, the full research repository, or raw session files.
The full archive's inventory generator uses the included frozen ledger.
The --require-complete option checks exposition coverage; it does not
certify mathematical correctness.

See ancillary/README.md for four short Python checks of the complete
carpet certificates. scripts/check_character_input.g checks the GAP
character-table input used for Problem 4.55. Large historical research
computations remain in the frozen research archive and were not all
rerun during manuscript preparation.

To reproduce the session and Git measurements, use the full frozen
research repository and the supplied HTML/text and full JSONL session inputs:

~~~sh
python3 paper/scripts/analyze_experiment.py --check
python3 paper/scripts/analyze_rollout.py --check
~~~

Without --check, these regenerate five legacy and six full-trace files.
The parsers use Python's standard library; the first also uses Git. They
do not run mathematical verifiers or contact the network. Raw inputs remain
separate and are identified by size and SHA-256. The full JSONL includes
research, closeout and initial manuscript preparation. Request IDs reconcile
the legacy cumulative ledger with separately recorded compaction requests;
data/ccusage-supplied.json preserves the organizers' exact row and the flat
rate assumptions. Included projections exclude internal reasoning, compaction
summaries, and system/developer instruction bodies.

Regenerate the three-panel chronology source with:

~~~sh
python3 paper/scripts/make_trajectory_figure.py
cd paper
tectonic --outdir figures figures/trajectory.tex
~~~

The revision adds a globally principal fixed divisor to the 14.72
counterexample by restricting to `x^2+1 != 0`, preserves 19.56 as a fourth
main example, and adds inventory scope notes, source clarifications and
acknowledgement of contemporaneous 21.106 work. The deadline ledger and
usage data retain their historical status.

The change appendix precedes four verbatim correspondence appendices.
Raw originals, the partial update of the first report, its exact diff, and
our final reply are in [external-reviews/](external-reviews/).
[reviews/revision-2026-09-17/](reviews/revision-2026-09-17/) holds exact
before/after excerpts, the baseline binding, and revision checks. The
reviewer programs and logs are separately pinned in
[JUrban/kour1cl](https://github.com/JUrban/kour1cl/tree/0d76dc7fc947a89a6f02e37b81da2320450efab6/review-other1).
Their reported checks are distinct from executions rerun here.

The dated retrieval index is in `data/retrieval-observations.jsonl`,
`data/retrieval-urls.csv` and `data/retrieval-metrics.json`. It records
structured web actions and returned links, not mathematical use or every
shell download. Regeneration needs the separately retained raw JSONL:

~~~sh
python3 paper/scripts/extract_retrievals.py --check
~~~

To regenerate the correspondence (Pandoc 3.1.3) and change appendix:

~~~sh
python3 paper/scripts/render_review_record.py
python3 paper/scripts/render_review_changes.py
~~~

The supplemental 14.72 algebra check uses SymPy:
`python3 paper/scripts/check_14_72_principal.py`. It is separate from the
four standard-library carpet checks. The proof itself requires no software.

The initial same-agent review is documented in reviews/candidate-review-ledger.json,
reviews/issue-log.md, reviews/source-notes.md and reviews/completion-audit.md.
Internal review and targeted replay are distinct from outside acceptance,
formal verification and priority. All 46 entries preserve their historical
candidate status.

The title page credits Codex gpt-6-astra (OpenAI), Michael Kinyon
(University of Denver), and Josef Urban (AI4REASON; University of Gothenburg),
in the order supplied by the organizers. Kinyon and Urban conceived and
oversaw the experiment. No arXiv submission, external upload or Git push
was performed. PLAN.md preserves the requested scope; STATUS.md records
the handoff state.
