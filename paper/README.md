# Forty-eight hours with the Kourovka Notebook

This is the later manuscript about the experiment frozen at
cff2c37b9bf6b737e8ad5f7ead12291a551b5201. It contains the experimental
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

See ancillary/README.md for three short Python checks of the complete
carpet certificates. scripts/check_character_input.g checks the GAP
character-table input used for Problem 4.55. Large historical research
computations remain in the frozen research archive and were not all
rerun during manuscript preparation.

To reproduce the session and Git measurements, use the full frozen
research repository and the supplied session exports:

~~~sh
python3 paper/scripts/analyze_experiment.py --check
~~~

Without --check, this regenerates the measurement files. The analyzer
uses Python's standard library and Git. It does not run mathematical
verifiers or contact the network. Raw session exports remain separate;
their sizes and hashes are recorded. The included visible-message
projection excludes directives and omitted internal event bodies.

The same-agent review is documented in reviews/candidate-review-ledger.json,
reviews/issue-log.md, reviews/source-notes.md and reviews/completion-audit.md.
Internal review and targeted replay are distinct from outside acceptance,
formal verification and priority. All 46 entries preserve their historical
candidate status.

Author names and affiliations must be supplied before submission. The
configured repository URL does not establish anonymous availability of
the frozen snapshot. No arXiv submission, external upload or Git push
was performed. PLAN.md preserves the requested scope; STATUS.md records
the handoff state.
