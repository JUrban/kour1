# Version 3: correction and statement audit

The [paper](../../kourovka-experiment.pdf) withdraws the claimed resolution
of 10.35 following Evgeny Khukhro's 19 September correction. The Notebook
asks about GL_n(Qbar); the example already embeds over Q(i). The rational-
field observation survives, but does not resolve the printed question.

The current assessment is **46 historical candidates, one withdrawal and
45 remaining candidates**. The original ledger is preserved; current status
is recorded separately in [current-assessment.json](../../data/current-assessment.json).

[statement-audit.json](statement-audit.json) records Codex's visual review
of all 46 original candidate statements against the manuscript's scope.
It covers field and closure notation, quantifiers, hypotheses, subparts and
explicit convention qualifications. No additional transcription mismatch
requiring withdrawal was identified. This is a statement-fidelity review,
not a fresh proof, imported-source, intended-convention or novelty certification.

The [statement crops](statement-crops/) are direct Poppler renderings of the
supplied `docs/21tkt.pdf`, at 216 dpi. [statement-locations.json](statement-locations.json)
records one PDF page and a rectangle in PDF points for each entry, together
with its image hash. The Notebook's hash is pinned in [baseline.json](baseline.json).
Text extraction was used to locate the rectangles; the notation was read
from the images. All statements fit on their listed pages. Extra next-page
headers were inspected and omitted from the final crops.

For a recorded rectangle (x0,y0,x1,y1), rendering used `pdftoppm -r 216`,
with x/y equal to floor(3*x0), floor(3*y0), and W/H equal to
ceil(3*(x1-x0)), ceil(3*(y1-y0)); `-f` and `-l` select the recorded page,
and `-singlefile -png` selects the output. The full source bundle includes
the images; it does not need the entire Notebook to run the binding audit.

The [original statement audit](original-10.35-review.md) incorrectly claimed
that visual inspection confirmed the absence of closure bars. It and the
[original proof](original-10.35-proof.md) are preserved as historical evidence,
not current assertions. Their bindings are in [original-records.json](original-records.json).
Claude's historical review likewise accepted this entry; the four exchanged
documents remain verbatim in the paper, with the correction stated separately.

The complete v2 source snapshot and PDF are preserved. [changes.json](changes.json)
binds five literal before/after pairs for Appendix G, and
[10.35-source-change.diff](10.35-source-change.diff) shows the full mathematical
source correction. Forty-nine other separate mathematical files and all
representative proofs remain byte-identical to v2. The 10.35 matrix lemma
and construction are also unchanged. Its general centralizer argument
continues to support the relevant step in 20.90.

```sh
python3 paper/scripts/audit_v3.py
python3 paper/scripts/audit_v2.py
python3 paper/scripts/audit_reader_revision.py
```

The audits check counts, coverage, source/image bindings, exact change
records and preservation. They do not machine-certify the visual readings
or mathematical correctness. Historical v2 excerpts are checked against
the preserved v2 sources, rather than silently replaced by v3 text.
The current preservation receipts are stored here; the old dated receipts
remain in their earlier review directories.

Khukhro's communication is credited for the specific correction, not as
specialist endorsement of the other candidates. Both original editor emails
remain local and are excluded from the source bundles. No Lean project or
large historical computation was rerun for this statement correction.
