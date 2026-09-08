# Can rigorous density bounds finish the three-stage count?

Owner: Kevin's Goldbach investigation. Purpose: decide whether an elementary
CRT estimate can replace the finite first-stage and residual counts in
`cubic-three-stage-identity.md`. Retain the proof, failure evidence, and exact
condition that a stronger estimate would have to establish.

## Central interval and exact CRT main term

For even N>=6 put H=N-3 and z=floor(cuberoot(H)). Let L be the least odd
integer at least max(3,z^2), U=N-L, and I the odd integers in [L,U]. Write
T=|I|. Both arguments a and N-a are at least z^2. Thus a small-prime
square-start exclusion is exactly one or two congruence classes:

    rho_p = 1 if p divides N, and 2 otherwise,
    delta = product_(odd prime p<=z) (1-rho_p/p),
    E = product_(odd prime p<=z) (1+rho_p) - 1.

Parameterize a=L+2n with 0<=n<T. For a nonempty subset D of the small
primes, the forbidden intersection consists of product_(p in D) rho_p
residue classes modulo d=product_(p in D) p. The Chinese remainder theorem
is applicable because the primes are distinct, and the change from a to n
is invertible modulo d. Each class occurs T/d plus an error of absolute
value less than one. Inclusion-exclusion yields

    M_I = T*delta + epsilon_I,   |epsilon_I| <= E.

The empty-subset term is exact, explaining the minus one in E. This is a
deterministic identity and error bound; no independence of primality or of
the events has been assumed. A safe integer lower bound is

    M_lower = max(0, ceil(T*delta-E)).

## Residual exclusions with square thresholds retained

For an odd prime r>z with r^2<=U, let b_r count the odd multiples of r in
[max(L,r^2),U]. For a positive integer interval [l,u], the exact count is

    b_r = floor((floor(u/r)+1)/2)
          - floor((floor((l-1)/r)+1)/2).

Writing a=r*q makes the b_r admissible q values consecutive odd integers.
For every small prime p, r is invertible modulo p. The excluded q residues
are 0 and N*r^(-1), with the same rho_p as before. Consequently the
presieved first-arm count C_r satisfies

    C_r = b_r*delta + epsilon_r,   |epsilon_r| <= E,
    C_r <= min(b_r, floor(b_r*delta+E)).

Reflection a -> N-a preserves I and the presieve and gives the same count
for the second arm. We deliberately overcount any overlap of the arms:

    S1_I <= S1_upper
          = 2 sum_(z<r<=sqrt(U)) min(b_r, floor(b_r*delta+E)).

When r does not divide N the arms have distinct residues and are disjoint.
When r divides N an optional improvement merges overlapping arms. The code
keeps the simpler safe doubled bound, so this omission weakens the result
and cannot create a false positive. Empty arms contribute zero.

The earlier exact identity restricts to I unchanged:

    G_I = M_I-S1_I+S2_I,   S2_I>=0.

Therefore the fully explicit sufficient condition is

    max(0, ceil(T*delta-E)) > S1_upper.

If it holds, there is a prime pair in I. If it fails, it says nothing about
existence. These are individual-target bounds. A whole interval certificate
would additionally need their positive inequality established for every
target in that interval, for example by proved uniform bounds on its inputs.

## Measured gap between true error and safe worst-case error

`crt_error_bounds.py` computes the bound using only the small prime table,
rational arithmetic, and interval floor counts. Its optional mask comparison
is a separate finite diagnostic and never feeds the bound. The canonical
receipt is `evidence/central-crt-error-bounds.json`.

| N | T*delta | Exact M_I | Absolute CRT error allowance E | M_lower | S1_upper | Exact M_I-S1_I |
|---:|---:|---:|---:|---:|---:|---:|
| 30 | 4.667 | 4 | 1 | 4 | 0 | 4 |
| 100 | 11.333 | 12 | 2 | 10 | 14 | 8 |
| 1,000 | 80 | 80 | 17 | 63 | 182 | 36 |
| 10,000 | 474.725 | 476 | 1,457 | 0 | 2,354 | 198 |
| 100,000 | 3,401.136 | 3,402 | 1,062,881 | 0 | 28,526 | 1,182 |
| 1,000,000 | 25,030.946 | 25,166 | 188,286,357,653 | 0 | 316,470 | 7,286 |

At one million, the actual first-stage error is about135.054. The enormous
allowance is an artifact of bounding every inclusion-exclusion residue error
separately by its absolute value. The calculation shows what this elementary
bound loses. It is not evidence that the actual errors are large, or that
other estimates cannot succeed. Central counts differ from earlier full
candidate-window counts because small summands have been removed here.

Four focused tests check all small interval endpoints for raw odd-multiple
counts, compare central counts and every residual arm against direct
divisibility and trial primality for even6 through1000, retain the one-million
error explicitly, and validate inputs without assertion-dependent checks.
The complete39-test suite passes in normal and optimized Python.

There is also a uniform negative conclusion about this particular bound.
Let k=pi(z)-1 be the number of small odd primes for z>=2. Since rho_p>=1,
E>=2^k-1. The [prime number theorem, DLMF27.2.3]
(https://dlmf.nist.gov/27.2#E3) gives k asymptotic to z/log(z), while
z is asymptotic to N^(1/3). Hence

    log(2^k)/log(N) -> infinity,
    E/N -> infinity.

Because T*delta<=T<=N/2, this formula's M_lower is zero for every sufficiently
large N, regardless of which small primes divide N. This rules out the
unchanged elementary absolute-error bound as an eventual positive certificate.
It leaves the exact counting identity and more informative error estimates
untouched. No explicit numerical threshold is asserted by this asymptotic
argument.

## Does a standard lower-bound sieve automatically replace this error?

[Ford's 2023 sieve notes](https://ford126.web.illinois.edu/sieve2023.pdf),
Sections1.2-1.7 and its later lower-bound sieve development, supply the
standard framework: intersection counts have a multiplicative density main
term plus remainders. The paired linear forms have two forbidden classes
away from primes dividing N, so their natural sieve dimension is two.
An effective lower bound needs both an appropriate lower-sieve coefficient
and control of the required sums of remainder terms. Exact CRT formulas
alone do not furnish small aggregate remainder bounds at arbitrary levels.

[Kao, Almost-Prime Polynomials with Prime Arguments]
(https://arxiv.org/pdf/1606.03505), PDF pp.6-7, defines the DHR lower functions
with f_kappa(s)=0 for s<=beta_kappa; beta_2=4.2664... and beta_1=2. For this
specific dimension-two lower sieve, z=N^(1/3+o(1)) and even a hypothesized
usable distribution level D=N^(1+o(1)) give s=log(D)/log(z)=3+o(1), inside
the zero range. Positive main coefficient would require D>z^beta_2, roughly
N^1.4221, together with the corresponding remainder estimates. That level
has not been established here. This parameter calculation is our inference
from the cited sieve functions, not a theorem ruling out other methods.

Switching to prime a and sieving N-a gives dimension one, but the standard
Bombieri-Vinogradov-scale level near N^(1/2) with this same cubic z gives
s near1.5, also inside that linear lower function's zero range. This checks
one plausible substitution; it does not rule out weighted sieves, extra
correlation information, or new arguments.

The next substantive input must preserve useful signed error cancellation
or introduce additional proved arithmetic information. Replacing epsilon
by zero, invoking average density, or checking more favorable finite targets
would not close this gap.

## Independent mathematical review

The Sol review confirmed the central CRT identity, the exact progression
sharpening for b_r, the empty-small-prime case delta=1 and E=0, square
threshold equality, the reflection argument, and intentional overlap
overcounting. It also rejected an unproved universal halving of E: an
individual residue count can differ from its fractional main term by more
than one half. No primality-independence premise was added.
The subsequent code/note review found no material defect and confirmed that
exact diagnostics never feed the certificate and that the DHR discussion
does not make a universal impossibility claim.
