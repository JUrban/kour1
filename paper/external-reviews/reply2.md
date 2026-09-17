# Reply to the follow-up report

17 September 2026

Thank you for the second round of checks and the corrections to the first report.
We have revised the paper as follows.

1. **14.72: the suggested repair works.** Let X be the original surface and
   restrict to the invariant affine open U defined by x^2 + 1 != 0. Put
   f = y - (1+i)x. In its coordinate ring,

   f(y + (1+i)x) = x(x-i)^2.

   Since x-i is a unit, x belongs to (f), hence so does y. The surface
   relation u = x^2 u - yv then gives u in (f). Thus (f) = (x,y,u), and
   the fixed scheme is the smooth reduced principal divisor with coordinate
   ring C[v]. The quotient is the original nodal surface localized at
   a+1, where a=x^2. Its singular point (a,v,d)=(1,0,0) survives.
   This gives the counterexample under the globally principal reading too.
   We credit your suggestion and identify this restriction as a post-review
   strengthening. The explanation of the original surface now distinguishes
   the reduced Cartier divisor D from the principal double divisor 2D.

2. **The missing ancillary input is included.** Both source bundles now
   contain `results/19.62-g2-monomial-certificates.jsonl` (2,194,486 bytes).
   Its SHA-256 is
   `29550181fd180ecf906395614398c8500f85d5fed950fa72efc8e0e424abbf68`.
   The README documents all four checks, including the 2,712-request
   monomial check. Our first reply overstated the completeness of the
   bundle: the three documented checks had their inputs, but this fourth
   script did not. The omission is corrected.

3. **The public repository is filtered.** The paper now gives the accessible
   research commit `bbfac1ac810117da37f01716d4594dc2b2e96980` separately from
   the original local commit `cff2c37b9bf6b737e8ad5f7ead12291a551b5201`.
   The owner used `--strip-blobs-bigger-than 90M`. All 4,146 retained blobs
   at the final research snapshot have the same object IDs; the omitted
   blob is the 1,271,256,410-byte 20.100 certificate. It is not supplied
   with this revision. The available logs document historical verification
   but do not enable a complete new replay. Our first reply's suggestion
   that publishing the repository would make this certificate available
   was therefore incorrect. No separate deposit is claimed.

4. **Scope and dependencies are visible in the inventory.** We retained
   the 46 deadline entries and their covered parts, adding a separate
   scope/dependency column. The annotations identify the conventions in
   18.92, 14.22 and 16.20 without attributing intentions to their proposers.
   They also distinguish shared imported constructions and the published
   19.63 criterion. A companion table highlights 21.132, 21.42 and 20.33
   under their prior-work classification. The 19.56 argument is now the
   fourth main example, with its imported theorems still credited.

5. **15.92 and 10.62/4.75.** The text now explains that the diagram's unique
   exceptional prime cycle determines the choice of 11 or 13, and points
   to the retained finite transcription and replay controls. We have made
   the use of Amelio's smaller initial scale and prescribed odd relation
   more explicit. The geometric quotient construction remains an imported
   dependency shared by 10.62 and 4.75.

6. **21.106.** We acknowledge the contemporaneous work credited to Lily
   Zhang and Evan Li, including the Lean formalisation. The dates quoted
   are commit timestamps, not verified upload times or discovery times;
   we assign no priority. We have not built that Lean development. The
   source bundle now includes a dated index of the structured web-tool
   observations in the supplied JSONL. It distinguishes requested page
   actions from returned search links and makes no inference of mathematical
   use. The exact repository URL has no literal occurrence in the raw
   input; this remains a narrow observation, not evidence excluding other
   exposure. The raw session is still separately retained.

7. **Smaller points and retained conclusions.** We identify GAP 4.16.1 and
   CTblLib 1.3.11 for the character-table indices; explain CA implies CN;
   specify the exponent-four restriction in the contrasting 15.76 example;
   add the foundational 1994 exponential-groups reference; and explain the
   one-cent rounding difference. The Rosser–Schoenfeld suggestion needs a
   correction: the lower bound used is Theorem 4, formula (3.14), on printed
   page 70. Formula (3.16) has a different denominator and threshold. We
   retained Theorem 4 and added (3.14). We retained characteristic five in
   16.28, without an unnecessary extension to all odd characteristics.
   The acknowledged source-index discrepancy in 15.65 remains explicit.

The revised paper contains an issue-by-issue change appendix followed by the
original report, our first reply, the follow-up and this reply. Their wording
is preserved, including superseded assertions. The lightly updated first
report is retained separately with an exact diff. References within the
historical correspondence still refer to the old paper's numbering.

We have pinned the reviewer artifacts in `JUrban/kour1cl` at commit
`0d76dc7fc947a89a6f02e37b81da2320450efab6`, distinguishing your reported
checks from executions performed during this revision. Neither the review
nor these changes alter the historical statement that there were no outside
reviews at the research deadline. The revision audit records the completed
build, algebra and portable-bundle checks separately.
