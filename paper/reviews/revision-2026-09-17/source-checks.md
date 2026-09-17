# Source checks during revision, 17 September 2026

- **14.72:** verified the new localization and ideal equality by an explicit
  algebraic argument and exact Groebner reduction over Q(i). Inverting
  x^2+1 makes x-i a unit; the equation f=y-(1+i)x generates the fixed ideal.
  Localization at the invariant a+1 retains the quotient node a=1.
  This is a new post-review argument. The symbolic script supplements the
  proof; it does not formalize invariant-ring completeness or geometry.
- **10.62/4.75:** rechecked arXiv:2509.11958v2, Proposition 6.1, the
  initialization of Theorem 6.7, and Remark 6.8. The maximal selection
  excludes primitive elements generating an elementary subgroup or conjugate
  in the ambient group. The primitive abc has length three; eligibility
  requires 3 lambda <= L_S delta_1. Remark 6.8 expressly permits a smaller
  scale at the cost of a larger critical exponent. The paper now contrasts
  this with the source's illustrative 2 lambda condition. The deep geometric
  estimates remain imported.
- **10.32:** visually inspected Rosser–Schoenfeld, printed page 70.
  Theorem 4, (3.14), is exactly x(1-1/(2 log x)) < theta(x) for x>=563.
  The review's proposed (3.16) instead has 1/log x and threshold 41.
  Retained Theorem 4, adding (3.14); the upper bound remains Theorem 9.
- **13.42:** added the 1994 foundational bibliographic record from
  https://www.mathnet.ru/eng/smj705. The proof continues to cite the
  definitions and universal property as restated in the retained second
  paper. No assertion of a complete new audit of the first paper is made.
- **15.76:** the retained Fernandes–Tsurkov source gives x^4=1 in (1.1),
  the metabelian identity in (1.2), and a further nilpotency identity in
  (1.3). The revision identifies exponent four; it does not enlarge that
  contrasting example to the full metabelian variety.
- **4.55:** the supplied installation reports GAP 4.16.1 and CTblLib
  1.3.11. The exact decomposition-row, Galois-orbit and projective-dimension
  manuscript check passed; this is a check of the library inputs.
- **15.92:** inspected the retained summary entry and the external
  second-round cycle log (150 rows, all passing; primes split 11 for
  h=7,8,11 and 13 for h=9,10,12). The manuscript points to the finite
  inputs and attributes the external replay, without claiming to have
  independently rerun all the reviewer's programs.
- **15.65:** no new resolution of the previously identified source-index
  discrepancy is claimed. Its existing qualification remains in place.
- **21.106:** the pinned contemporary README credits Lily Zhang and Evan
  Li. The commit metadata confirms the dates quoted in the revised paper.
  These are commit dates, not verified upload or discovery dates. No Lean
  build was performed. See 21.106-contemporary-artifacts.json.

Source-input hashes, public snapshot comparisons and reviewer artifact
metadata are preserved beside this note. The dates and judgments in the
verbatim correspondence have not been silently corrected.
