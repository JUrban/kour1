# Version 4: shared full and mathematical editions

Based on v3 commit 5ee9816; work on paper/v4. Preserve the v3 PDF and
source baseline, the historical reports, and all original review documents.

Produce two PDFs from one maintained set of mathematical sources:

1. The full research-and-review account, explicitly version 4.
2. A mathematical edition with a short introduction, current result index,
   original problem statements and authors, the proofs and attribution,
   substantive partial results, and required mathematical supplements.

Both editions must retain the same hypotheses, mathematical arguments,
qualifications and contemporary attribution. Omit experimental narrative,
review correspondence and bounded unsuccessful searches from the mathematical
edition. Briefly disclose AI provenance, review limits and the 10.35 withdrawal.
Extract the centralizer fact used by 20.90 so that omitting the withdrawn
application cannot break that proof. Preserve 10.35 in the full historical
account. Do not claim the 45 remaining candidates are verified new solutions.

Use the structure of reports/FINAL_REPORT.md for a current overview without
rewriting that frozen historical report. Check problem authors and restated
questions against the rendered Notebook, using the existing v3 evidence where
available. Keep problem metadata and proof inputs shared between editions.

Update build, source packaging and checks to cover both editions, including
references, mathematical dependencies, shared-source consistency, historical
preservation, source/PDF bindings and standalone archive builds. Inspect both
rendered PDFs and document actual checks and limitations. Update landing-page
links, commit the finished revision, and leave master and v3 unchanged.
All three raw editor emails remain local; no push or external submission.
