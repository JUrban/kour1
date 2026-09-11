# Late-evening source triage, 11 September 2026

These are source-scope findings and abandoned approaches, not additional
complete candidates. They prevent the same invalid reductions from being
reused. Work on 12.40 is documented separately.

## 16.90: infinite-rank free-group automorphisms

Tolstykh, *The Bergman property for automorphism groups of relatively
free groups*, arXiv:math/0406586v1, was read through the introduction,
Section 2 and Theorem 2.5, with Section 3 statements also read:
https://arxiv.org/pdf/math/0406586 . The cached copy is
`references/cache/tolstykh-bergman-2004.pdf`.

Theorem 2.5, under the BMN-variety hypothesis, expresses automorphisms
supported on a moietous free factor as bounded products of conjugates
of a basis-swapping involution. BMN generation then gives the whole
automorphism group and perfectness. The proposed shift argument is
therefore a rediscovery of a conditional mechanism, and its missing
generation hypothesis must not be suppressed. The author's survey,
https://arxiv.org/pdf/0807.4343 , explicitly asks whether the variety
of all groups is BMN. Results giving the Bergman property for countable
free groups by genericity do not automatically supply this hypothesis
at arbitrary rank. No general answer to 16.90 follows here.

Domat--Hoganson--Kwak, arXiv:2207.12518v2, was inspected for the
countable case only. Its coarse-boundedness conclusion does not fill
the arbitrary-rank generation step.

## 5.36: ascending chains in profinite groups

Lubotzky--Mann, *Powerful p-groups II*, Proposition 2.5, relates the
ascending chain condition on closed subgroups of a pro-p group to
finite generation of each closed subgroup:
https://www.math.uni-bielefeld.de/~baumeist/sommerschule/powerfulMann.pdf .
Finite rank requires a UNIFORM bound on generator numbers. It cannot
be inferred merely because each number is finite. Klopsch's 2008 notes
explicitly retain the corresponding analytic question as open on p.23:
https://www.math.uni-duesseldorf.de/~klopsch/mathematics/Manuskripte/analytic_groups.pdf .

A thesis search excerpt suggesting virtually pro-p structure has an
essential **just-infinite** hypothesis. The unrestricted assertion would
already fail for Z_p times Z_q. Attempts to obtain the 2021 Villanis
Ziani thesis PDF returned HTTP 403; no full-text proof was imported.
A 2023 research-profile claim was not verified against primary full
text and is not accepted as a resolution. No candidate is claimed.

## Other leads retained only as exclusions

- **12.8:** The varietal notion of discrimination in the question must
  not be confused with the stronger group-theoretic notion requiring
  discrimination of G times G. The Fine--Gaglione--Myasnikov--Spellman
  2006 survey uses the latter in its introductory definitions:
  https://ddd.uab.cat/pub/prepub/2006/hdl_2072_5309/Pr724.pdf .
  Introductory definitions and portions were read, not all final sections.
- **12.88:** A bounded translation-like action of Z on a Cayley graph
  need not be a graph-automorphism action for one finite generating
  set. It does not produce the demanded shared Cayley graph.
- **4.34:** A 2014 Bardakov--Gongopadhyay introduction attributes finite
  commutator width at derived length at most three to Rhemtulla, while
  retaining larger derived length as unknown at that time. It supplies
  no general answer.
- **12.92:** In characteristic two, the usual three-character argument
  from characteristic different from two cannot be imported. For odd
  group order, the observation about reduced traces does not establish
  the necessary lower characteristic-polynomial coefficients.

No external messages or submissions were made. These investigations
do not change the complete-candidate count.
