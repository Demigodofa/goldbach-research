# q286 LP cone local singular audit

Status: finite local/admissibility and source-backed AP-bound audit.  This is
not a proof of Goldbach, a singular-series theorem, a rank-`1` theorem, or a
residual-drag theorem.

## Purpose

Kevin's good-cone question asks whether the frozen q286 LP vector is seeing
actual local prime-pair admissibility rather than only a fitted residual-cap
shadow.  The audit is:

```text
evidence/q286-lp-cone-local-singular-audit.json
```

The builder is:

```text
tools/build_q286_lp_cone_local_singular_audit.py
```

For each target residue `N mod 143`, it forms the locally admissible residue
measure

```text
{r in (Z/143Z)^* : N-r is also a unit mod 143}
```

then pushes that measure through the same `C10 x C12` real outside-channel
coordinates used by the rank-`1`, low-frequency, and LP receipts.  The local
delta is measured relative to the stress target `1222142 mod 143`.

## Result

The local admissible cone supports the frozen LP orientation:

```text
local LP negative residues: 0
local LP zero-action residues: 38,64,79,105
minimum local LP action: -5.27407587441604e-16 at N = 38 mod 143
maximum local LP action: 0.0960853972507348 at N = 142 mod 143
local low-frequency negative residues: 0
local rank-1 negative residues: 4
```

The tiny negative minimum is numerical zero at the receipt tolerance.  This is
a real structural signal: local admissibility pushed through the channel
dictionary has the correct nonnegative sign for the frozen LP vector on all
`143` target residues.

It does not explain the measured far-window deltas:

```text
far clear rows: 606
far distinct target residues mod 143: 108
empirical LP vs local LP Pearson:  0.00227142072234304
empirical LP vs local LP Spearman: 0.00862101112769288
zero-local-action but positive empirical LP rows: 12
```

The zero-local-action positive empirical targets are:

```text
6000032, 6000058, 8000030, 8000056, 10000028, 10000054,
12000026, 12000052, 16000022, 16000048, 20000018, 20000044
```

So the admissible cone is an orientation floor, not the quantitative theorem.
The remaining bridge is still a centered binary-prime residue discrepancy or
signed character-sum estimate.

## Bennett-Martin-O'Bryant-Rechnitzer q=286 constants

The actual table values for `q=286` from Bennett-Martin-O'Bryant-Rechnitzer
are:

```text
c_psi   = 0.0008379
c_theta = 0.0008411
c_pi    = 0.0008772
x_psi   = 85,882,271
x_theta = 85,881,413
x_pi    = 86,891,851
max-x   = 86,891,851
env-x   = 141,762,479
```

Source locators:

```text
https://arxiv.org/abs/1802.00085
https://www.nt.math.ubc.ca/BeMaObRe/
https://www.nt.math.ubc.ca/BeMaObRe/c-psi-theta-pi/c_all_rounded.txt
https://www.nt.math.ubc.ca/BeMaObRe/x-psi-theta-pi/x0-all-xm-xe.txt
```

BMOR Corollary 1.6 also gives a cruder but very simple `pi(x;q,a)` threshold
for all `q <= 1200`:

```text
x >= 50 q^2
50 * 286^2 = 4,089,800
```

This is useful, but it is an arithmetic-progression prime-count floor and
ceiling.  It is not a binary Goldbach-in-progressions theorem, and it is not a
bound for the 17-channel signed LP/rank-`1` functional by itself.

## Candidate 17-channel bridge verdict

Kevin proposed a bridge in which the 17-channel coefficient vector is fixed by
the product of the two unique nonprincipal real Dirichlet characters of
conductors `11` and `13`, or equivalently by an order-`2` conjugacy class in
the dual of `C10 x C12`.

As stated, this does not supply a new passing bridge:

- The product of the two quadratic characters is naturally a function on
  residue classes.  The 17 labels are character exponents.  Under the natural
  dual pairing with the order-`2` product character `(5,6)`, the label value is
  `exp(2*pi*i*(5a/10 + 6b/12)) = (-1)^(a+b)`.  All current outside and volatile
  labels have even `a+b`, so this collapses to the all-ones outside sum.
- The all-ones outside sum is already the exact outside delta baseline.  It
  has zero residual drag but only about `0.5129804485` cosine to the frozen
  rank-`1` vector and `0/10` high-drag overlap.  It is not a rank-`1`
  explanation.
- If the intended vector is the folded Legendre-product sign
  `(-1)^(floor(a/5)+floor(b/6))`, the existing dictionary audit falsifies it:
  cosine about `0.3552346438`, `11/17` sign mismatches, one positivity failure,
  one `0.75` cap failure, and `1/10` high-drag overlap.
- If the intended object is the literal indicator of the order-`2` character
  class `(5,6)`, then `(5,6)` is not one of the 17 outside labels, so its
  restriction to this outside basis is the zero vector unless a different
  explicit lift is defined.

The bridge can be revived only by specifying a nonzero lifted convolution map
from residue-class functions into these 17 real-character coordinates that is
not equivalent to the already-tested all-ones, edge/parity, or folded
Legendre-sign vectors.

## One-sidedness boundary

Brun-Titchmarsh-style control is the wrong shape for the missing lower bound:
it is an upper-bound sieve statement.  Maynard's Brun-Titchmarsh discussion is
useful context because it keeps the one-sided nature and exceptional-zero
boundary visible.  BMOR-style explicit AP bounds give real two-sided
prime-count input for fixed small `q`, but even that still has to be lifted
through a binary convolution and then through this exact 17-channel functional.

## Decision

The local singular/admissible cone closes one small hole: the frozen LP vector
has the correct local orientation for every target residue modulo `143`.

The proof path is not closed.  The flat empirical/local correlation and the
zero-local positive empirical rows show that the quantitative work is not
local admissibility; it is the centered binary-prime discrepancy inside the
admissible cone.

## Boundary

This audit gives a finite support/orientation result and a source-backed AP
constant lookup.  It does not prove a uniform LP cone theorem, a
Riesz-Thorin/interpolation theorem, a pointwise binary Goldbach-in-progressions
theorem, a signed projection theorem, or Goldbach.
