# Preliminary review of the parallel Fable experiment

The review and comparison are in `paper/appendices/parallel-fable.tex`
(Appendix M of the revised paper). Codex prepared them on 17 September 2026.
The source is the 29-page paper and selected reports and programs at
[JUrban/kour1cl commit 290fc829d2be01cab8a1784d006bfc0250d7f11c](https://github.com/JUrban/kour1cl/tree/290fc829d2be01cab8a1784d006bfc0250d7f11c).
`sources.json` records the URLs, sizes and SHA-256 digests of downloaded files.
It is a retrieval manifest, not a claim that every retrieved program was run.

The organizer supplied the common-machine/common-conditions comparison.
The Fable paper supplies its model, harness, reasoning settings, delegation,
deadlines and search totals. The review reads the mathematical arguments and
compares selected problem statements and prior status; it does not audit the
complete Fable transcript, all searches, or priority. The Fable research run
and the separate Claude Opus[1m] review of our paper are distinguished.

The principal findings are:

- 18.46: an independently written generator search confirms all 880 exclusions
  below order 128, the 14 successful groups of order 128, and the wreath-product
  witness. This still shares GAP and SmallGroups with the original checks.
- 13.19: a new standard-library Python reconstruction confirms the group of
  order 512, its normal subgroups and the D8 quotient. The all-prime construction
  with c+1 factors is discussed separately from this finite check and from the
  previously known negative answer.
- 2.78: the main finiteness construction survives preliminary reading and seven
  small family checks. The same formula covers every k >= 78, improving the
  reported sufficient threshold 86. The additional small-value classification
  was not independently verified. Its statement that f(G)=7 iff G=A5 needs
  the nonsolubility hypothesis already assumed in its proof: the soluble
  dihedral group of order 512 also has f=7, confirmed by our GAP check.
- 21.32: the central-extension proof appears sound on this reading, including
  the Baer-sum step preserving the derived subgroup. Priority remains unchecked.
- 16.60: the proof is sound, but the affirmative answer was stated in the May
  2026 Yerrapati–Dixit–Shukla preprint (already cited in our paper).
- The comparison records the complementary progress on 19.56, 20.21 and 20.100,
  and corrects two further local definitions/statements in the Fable exposition
  (20.37 and 21.111). Counts are not presented as a model ranking.

Run the checks from the repository root:

```sh
gap-4.16.1/gap -q -b --quitonbreak paper/reviews/parallel-fable-2026-09-17/checks.g
python3 paper/reviews/parallel-fable-2026-09-17/check_13_19.py
```

An installed GAP can replace the first path. The recorded execution uses GAP
4.16.1 and SmallGrp 1.7.0. `checks-output.txt` and `check-13-19.json` retain the
results; `checks-receipt.json` binds them to the programs. No source program
downloaded from the Fable repository is executed by these checks. The Python
program exhaustively verifies the cocycle identity on all 64^3 triples before
using the resulting multiplication law. The GAP script's subgroup-family
checks are finite examples, not a proof of the infinite family theorem.

The cutoff improvement follows without computation: the bases 7n+9 for
3 <= n <= 11 represent all residue classes modulo 9, and the largest integer
in any class below its base is 86-9=77. Thus adding 9r covers every integer
at least 78. The number 77 is absent from this family; that does not exclude
other groups with f(G)=77 or claim an optimal threshold over all groups.

The new review is appended after the verbatim historical correspondence.
The original reports, replies, deadline ledger and mathematical source files
are preserved. No large external certificate or session file is included.
