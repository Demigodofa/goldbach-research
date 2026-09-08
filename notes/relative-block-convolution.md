# A short packed calculation for a distant block

Owner: Kevin's Goldbach investigation. Purpose: apply the collective Z test
without constructing a polynomial whose degree reaches the absolute target.
This is a finite computational refinement, not an unbounded positivity claim.

## Inputs and relative positions

Let the requested block be F,F+2,...,L, with m targets. Choose a nonempty
finite palette A of known odd primes with minimum alpha and maximum beta,
where beta<=F-3. Let B be the odd primes in [F-beta,L-alpha]. Every
representation of a requested target whose first summand belongs to A has
its second summand inside that segment.

Put d=(beta-alpha)/2 and choose a radix R=2^w with R/2>|A|. Encode

    P_A = sum_(a in A) R^((a-alpha)/2),
    P_B = sum_(b in B) R^((b-(F-beta))/2).

The coefficient arising from a+b=N has index

    k = (a-alpha)/2 + (b-(F-beta))/2
      = (N-F+beta-alpha)/2.

Thus target F+2t is coefficient d+t, for0<=t<m. Each coefficient is at most
|A|, because every a has at most one complement for a specified sum. Integer
multiplication has no radix carry, and the same simultaneous sentinel test
from `packed-block-certificate.md` applies to the extracted m coefficients.

The relevant degrees are bounded by

    degree(P_A)<=d,
    degree(P_B)<=d+m-1,
    degree(P_A*P_B)<=2d+m-1.

These bounds depend on palette width and block length, not on F. Absolute
target magnitude still matters when establishing which inputs are primes.

## What the implementation must establish

`segmented_packed.py` independently sieves the palette through its cap. For
the nearby segment it builds a complete prime table through the square root
of the segment's high endpoint and applies square-start segmented sieving.
It never accepts an incomplete caller-supplied divisor list as proof. Palette
and segment primality are separate inputs; the segment's square-root table
alone need not validate an arbitrarily large palette.

The default palette cap is1000, clamped to F-3 before selecting actual
primes. At F=6 this gives A={3}; the segment starts at3 and coefficient0
certifies6=3+3. This small palette need not certify every later target in a
large block. Empty or malformed palettes and invalid block parameters must
be rejected.

The resulting counts are restricted ordered counts: the first addend must
belong to A. They may be smaller than the full ordered counts in the earlier
square experiment. A positive restricted count is sufficient for Goldbach.
A zero is only a palette miss, and remains unresolved by this calculation.

Successful replay rebuilds both prime inputs, the relative product, and the
collective test before accepting a supplied receipt. Optional per-target
counts are diagnostic output; the default positivity decision uses the
sentinel mask directly.

## Limits retained from the earlier palette work

A fixed finite palette cannot serve forever. If S is such a palette,
N=4*product_(p in S) p makes N-p a proper composite multiple of every p in S.
For the earlier concrete case N=510510, all odd palette primes through17
fail, while29+510481 is a prime pair. A correct implementation reports this
as a palette miss, rather than silently promoting finite coverage to a
general theorem.

The new local encoding changes the finite computation and gives an
exact collective certificate when its Z test passes. It does not prove that
a chosen palette, fixed or growing, will always suffice.

## Review and validation state

The independent mathematical review confirmed the target index d+t,
coefficient bound, degree bounds, small-F case, and palette-miss limitation.
It required separate validation of the palette; the implementation's own
palette sieve meets that requirement.

The initial CLI appended verification into the strict receipt object, making
that saved object fail replay. Review corrected the output to a wrapper with
separate receipt and verification fields. A regression test covers this. The
default path was also changed to use only the sentinel decision and enumerate
only unresolved positions; all count expansion is explicitly diagnostic.

`evidence/relative-packed-blocks.json` retains three1,000-target receipts:

| First even | Last even | Certified | Minimum restricted count | Construction and Z |
|---:|---:|---:|---:|---:|
| 1,000,000 | 1,001,998 | 1,000 | 9 | 0.000451s |
| 1,000,000,000 | 1,000,001,998 | 1,000 | 4 | 0.002163s |
| 1,000,000,000,000 | 1,000,000,001,998 | 1,000 | 2 | 0.054595s |

All use the167 odd primes from3 through997 and a segment spanning2,993
integers. The relative product degree is at most1,993 in every row. The
one-trillion example uses complete base primes through1,000,000 to validate
its nearby segment. It does not sieve the entire line to one trillion.

Each receipt passed fresh replay. Separately, every palette and segment prime
was checked against direct trial primality, including testing the segment's
odd nonprimes, and every restricted convolution coefficient was compared to
an independent direct complement count. Minimum counts above come from this
diagnostic check. Single-run timings include input construction and Z but
exclude replay and independent validation; no comparative speed claim follows.

The complete53-test suite passes in normal and optimized Python.
