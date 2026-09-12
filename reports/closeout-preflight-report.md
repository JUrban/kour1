# Closeout preflight: evidence and source archival

12 September 2026, 20:31 UTC. The research goal remains active until
20:56:46 UTC. This is a preflight audit, not the deadline completion.

The final-closeout auditor checked **4,231 hash bindings** across
**2,239 distinct files**, totaling **2,008,434,191 bytes**. Of these
bindings, 1,252 explicitly come from the accepted 19:00 handoff
checkpoint's current-file observations; 2,979 come from the 59
inspected manifests. This distinction does not create earlier
historical manifests for the seventeen early candidates.

It also checked all 46 candidate rows and their statement-index
agreement, 88 local Markdown links in the current report/review
documents, and the process list. No mathematical verifier was
replayed, no new PDF page was viewed, and no outside review or
priority certification is implied.

## Initial failure and correction

The initial process finished with actual exit 1 and empty stderr
in 5.167386 seconds (`aeea44`, session 64105 terminal). It found
**no missing files and no hash mismatches**, but three required
GAP catalogue source files were present without being tracked:

* `gap-4.16.1/pkg/smallgrp/gap/smlinfo.gi`
* `gap-4.16.1/pkg/smallgrp/small8/sml1536.b.gz`
* `gap-4.16.1/pkg/smallgrp/small8/smlgp8.g.gz`

These are the source inputs bound by the existing order-1536
exclusion packet. Their exact existing bytes were added to Git.
No catalogue source, expected digest, proof or mathematical output
was changed to obtain acceptance.

The second process used the same auditor and finished with actual
exit 0, empty stderr and its unique PASS marker in 5.211073 seconds
(`9fd91d`, session 50853 terminal). It had no missing files,
untracked required files or hash mismatches. Both invocations
observed no recognized mathematical jobs running outside their
own process ancestry. This is a process snapshot, not a continuous
resource monitor.

The initial and corrected outputs have prefixes
`results/closeout-preflight` and `results/closeout-preflight-archived`,
respectively. Each includes an integrity JSON, raw stdout, raw
stderr, and a separate actual-process receipt. The failed first
observation is retained.

## Deadline use

At closeout, update the draft final report and mutable status notes,
then run the same auditor with `--phase final` and a fresh output
path. The final phase additionally requires that the deadline has
arrived, that the report no longer has draft closeout wording, and
that no recognized mathematical jobs remain live. It does not mark
the goal complete or create a Git commit by itself.

The preflight audit is reproduced without overwriting its records by:

```sh
python3 scripts/audit_final_closeout.py --phase preflight --output results/closeout-preflight-recheck.json
```

The [preflight packet](../results/closeout-preflight-packet.json)
binds these records, the auditor, the archival source additions,
and the inspected manifest entry points. The final report remains
mutable until the deadline and is intentionally not a file binding
in this preflight packet. Its observed preflight bytes are recorded
as historical observations in the two integrity JSONs and are also
available from the Git checkpoint named in their receipts.
