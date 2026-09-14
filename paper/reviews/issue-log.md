# Manuscript review and correction log

This log concerns the later paper-writing phase. It does not rewrite
the frozen experiment or represent same-agent review as outside review.
The final review remains pending while the manuscript is being written.

| ID | Finding | Action and evidence | Status |
|---|---|---|---|
| E001 | The HTML header advertises 34,102 events, but many event bodies are absent. | The structural parser and an independent tag count agree on 4,439 exported event elements. Report both counts with distinct meanings. | Resolved for measurements. |
| E002 | Summing cumulative or repeated Last counters would inflate usage. | Retain 3,616 token observations; use the final monotone cumulative counters. Record 96 identical successive cumulative snapshots. | Resolved for measurements. |
| E003 | The initial analyzer assumed every Last record was itemized as input plus output. Its first run failed that assertion (tool observation `2d10f2`, actual exit 1). | Examination found 80 positive Last totals with all component counters zero. Preserve these records explicitly, do not assign an undocumented meaning to them, and use the internally consistent cumulative counters. The corrected generation passed (`711107`, actual exit 0). | Resolved; interpretation remains explicitly limited. |
| E004 | The historical model and reasoning setting are absent from the provided export. | The user supplied `gpt-6-astra xhigh` on 14 September. Cite this as human-supplied metadata, distinct from export-derived facts. | Resolved by attributed metadata. |
| E005 | A configured GitHub remote does not prove public artifact availability. | Anonymous API requests for the repository and the two observed revisions returned HTTP 404. Record the address and local snapshot without claiming public access or equality with the remote HEAD. | Resolved by limiting the availability claim; publication metadata may be updated by the author. |
| E006 | The root README still names an older candidate count. | Use the final ledger and closeout report as the deadline outcome; retain the README as a historical document. No claim is based on its obsolete total. | Resolved by source precedence. |
| E007 | Commit count can include administrative work after the research deadline. | Derive the count from the frozen history: 198 commits in the 48-hour window, followed by the closeout commit 16 seconds after its end. | Resolved for measurements. |

The analyzer has two deliberately different checks on the supplied data:
HTMLParser extraction is compared with literal-tag counts and an independent
parse of the final cumulative usage section; message-class counts are also
compared with the text export. These checks establish properties of the
exports. They do not recover missing tool events, prove the renderer's
accounting against invoices, or validate any mathematical argument.
