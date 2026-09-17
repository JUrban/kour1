# Finite carpet proofs

These byte-identical files come from research revision
cff2c37b9bf6b737e8ad5f7ead12291a551b5201. The manifest records
their sizes and hashes. They are included so the universal integer
derivations used for Problems 19.61 and 19.62 can be checked from
the portable paper source, without GAP, network access, or search.

From this directory, with standard Python 3 (do not use optimization):

~~~sh
python3 scripts/verify_19_62_rank_two.py
python3 scripts/verify_19_61_square_completion.py
python3 scripts/check_19_62_g2_integer_constants.py
python3 scripts/verify_19_62_monomial_certificates.py
~~~

The first two commands check target coverage, every derivation, and
deliberate corruptions; the first also checks Weyl coverage and the
short derivations printed in the paper. The third verifies all G2
commutator polynomial matrix identities over the integers against
the retained integral model. The fourth verifies the G2 monomial
certificate (2,712 requests and 62,835 nodes), including its negative
controls. That 2,194,486-byte file was missing from the first source
bundles and is included in this revision. They write small verification receipts
under results/. A2 and B2 use their standard integral Chevalley
constants; their original GAP model audits remain in the full archive.

A derivation node encodes a monomial, root, coefficient of the form
2^a 3^b, and either an initial variable or two earlier Chevalley-rule
applications. The two output coefficients must have the encoded gcd.
The final derived coefficient must divide the target coefficient.
Thus a checked derivation is valid in every commutative coefficient
ring, including characteristics two and three. This replay is distinct
from an independent formalization of Chevalley-group foundations.
