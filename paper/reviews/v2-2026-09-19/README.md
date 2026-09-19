# Version 2 comparison

This directory records Codex's 19 September 2026 comparison of the eleven
candidate entries identified in Evgeny Khukhro's 18 September correspondence.
It is separate from Claude Opus's earlier independent review and the
17 September comparison of the parallel Fable experiment.

[comparison.json](comparison.json) gives the result, method, reading scope
and assessment for each entry. The readable comparison is Appendix N of
the [paper](../../kourovka-experiment.pdf), with individual attribution
notes following all eleven affected proofs. The comparison found matching
arguments, different constructions and stronger alternatives. It assigns
no discovery priority and does not classify the other 35 entries as new.

All eleven supplied Zenodo records name Achyuth Jayadevan. For 21.68 the
Notebook's WordPress repository also contains a separate paper by Aluna
Rizzoli, which was read and credited separately. The prior acknowledgment
of Lily Zhang and Evan Li for 21.106 is retained. The 16.9 comparison also
checked the older Dahmani–Guirardel decision theorem and the
Brandenbursky–Gal–Kędra–Marcinkowski recurrence and erratum directly.

[sources.json](sources.json) pins the eleven PDFs, their Lean source
archives, the separate Rizzoli PDF and two older source PDFs. Zenodo file
checksums were verified on download. The ten corresponding Jayadevan
WordPress PDFs are byte-identical to the Zenodo PDFs; the Rizzoli 21.68
PDF is a distinct work. Downloaded papers and code remain in the local
`paper/build/v2-sources/` cache, outside the publication bundles.
[metadata/](metadata/) preserves the public Zenodo and DataCite records.

[chronology.json](chronology.json) separates first local proof-file commits,
Zenodo publication-date fields, record creation, and DOI registration.
The local proof-file commits are earlier than the corresponding DOI
registrations. This is an artifact chronology, not proof of discovery order
or of independence. The metadata's research-repository URL returned HTTP
404 when inspected; its development history could not be reviewed.
[retrieval-comparison.json](retrieval-comparison.json) records the exact
URL-index search and its limits. No matching source URLs were found in
that index; this does not cover every form of access.

The mathematical reading found no error in these alternatives, subject to
their imported theorems and table data. New checks cover three algebraic
identities and the finite character input for the smaller 4.55 example:

```sh
python3 paper/reviews/v2-2026-09-19/check_identities.py
gap-4.16.1/gap -q -b -T paper/reviews/v2-2026-09-19/check_4_55.g
```

The Python check uses only the standard library. The GAP check reconstructs
PSL2(11), the two matrix-defined subgroups and the induced characters; its
decomposition-matrix comparison imports CTblLib. The descent arguments are
reviewed mathematically, not certified by that computation.
[checks.json](checks.json) binds the executions and retained outputs to
the programs. No Lean development was built here, and downloading its
source is not a formal verification of its theorem statements or proofs.

Khukhro's report of human specialist confirmation concerns alternative
solutions to 21.68, 16.28(a) and 15.89. It does not endorse the whole
experimental portfolio. The original editor email remains local; no raw
mail headers are included in these publication artifacts.

[baseline.json](baseline.json) binds the pre-v2 manuscript and preserved
PDF at local commit `5fcdfdf`. [changes.json](changes.json) records five
literal before/after excerpts for the change appendix. All 50 separate
mathematical exposition files are byte-identical to the pre-v2 version;
the representative-proof file changes only by including two attribution
notes. The historical deadline data and exchanged reviews are preserved.

```sh
python3 paper/scripts/audit_v2.py
python3 paper/scripts/audit_reader_revision.py
```

These audits check coverage, source bindings, version identity and
preservation. They do not establish theorem truth or priority.
