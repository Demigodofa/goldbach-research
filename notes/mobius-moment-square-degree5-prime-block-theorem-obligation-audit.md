# Mobius moment-square degree-5 prime-block theorem-obligation audit

## Question

The six complete source-start sweeps support coherent prime-block morphology.
What universal pointwise theorem would replace finite acceptance?

## Mechanism

The finite receipts check a normalized condition:

```text
full < 0
active / full > 1/2
```

Because `full < 0`, the normalized inequality is equivalent to the
pointwise unnormalized inequality:

```text
full/2 - active > 0
```

So the theorem target should not be "more finite rows pass."  It should be a
source-start prime-block lower-frame theorem:

```text
For every sufficiently large source scale M
and every prime p in [M,2M],
every tracked component row and the degree-5 TOTAL row satisfy
full(M,p,label) < 0
and
full(M,p,label)/2 - active(M,p,label) > 0
at the canonical source start.
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_prime_block_theorem_obligation_audit.py
evidence/mobius-moment-square-degree5-prime-block-theorem-obligation-audit.json
```

## Finite Facts

The audit reads the six complete source-start sweeps:

```text
M=229, 251, 293, 331, 353, 379
```

Checked rows:

```text
dominance rows:                         1188
all full contributions negative:        true
all unnormalized half-frame margins >0: true
minimum normalized slack above 1/2:      0.40189096624031384
minimum unnormalized margin:             13356828127253.525
```

Prime-block separation:

```text
smallest top-to-second block slack gap:  0.003258445243465413
smallest gap/internal-spread factor:     6.297158705088222
maximum top-block internal spread:       0.0009780257632791
tightest prime counts:                  379 -> 2, 461 -> 1, 599 -> 3
```

The narrowest block separation occurs at `M=379`:

```text
top block:     p=599, min slack 0.4246854972346972
second block:  p=727, min slack 0.4279439424781626
gap:           0.003258445243465413
```

## Decision

The next mathematical target is not another raw finite acceptance threshold.
It is a pointwise unnormalized inequality:

```text
full/2 - active > 0
```

with `full < 0`, first by prime block and then over all primes in the
source-start interval.

The persistent `p=599` winner is only a diagnostic.  The checked block gap can
be narrow, so a fixed-winner theorem is the wrong target unless a new mechanism
appears.  A useful theorem should prove a lower envelope for all prime blocks,
not predict exactly which block is tightest.

This is a theorem-obligation audit only.  It proves no prime-block theorem, no
source-start theorem, no source-window theorem, no strict-central Goldbach
theorem, and no Goldbach proof.
