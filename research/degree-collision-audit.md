# Audit of the character-degree collisions

The screen in `scripts/search_degree_collisions.g` compared all 2,750 ordinary
tables in the installed CTblLib and printed 106 collisions involving tables
marked almost simple. Every member of every printed collision is itself marked
almost simple. This already prevents these entries from supplying a group with
nontrivial solvable radical as a counterexample to 21.135. None is counted as a
solution to 21.59(a).

The suspicious primed table names were checked against the actual installed
library data and metadata:

- `InfoText(CharacterTable("O8+(3).2_1'"))` and the double-primed version both
  say that the difference from O8+(3).2_1 is only its fusion into O8+(3).(2^2)_{111}.
- The primed O8+(3).2_2 table differs only by its fusion into O8+(3).2^2.
- In `gap-4.16.1/pkg/ctbllib/data/ctounit1.tbl`, around line 6267,
  U4(3).2_2' is explicitly constructed by permuting U4(3).2_2.
- Around line 6361 of that file, U4(3).2_3' is constructed from U4(3).2_3 with
  identity permutations; it records another fusion map.

These primed cases encode the same abstract groups with alternative table
ordering or subgroup fusion. Other small familiar coincidences include standard
isomorphisms and multiple names for maximal subgroups. We have no established
pair of nonisomorphic almost simple groups in the output. Equality of character
tables alone is not used as a proof of group isomorphism.

This lead is deprioritized pending a construction outside this table inventory.
