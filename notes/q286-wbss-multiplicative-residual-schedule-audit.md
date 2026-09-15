# q286-WBSS multiplicative residual schedule audit

## Question

The multiplicative-character burden audit compressed the coefficient side from
the additive Fourier basis, but still left a broad package.  If we keep the
largest multiplicative characters and put the rest into a residual bucket, can
coefficient energy alone make the residual harmless?

## Method

Keep the largest active nonprincipal multiplicative characters by coefficient
energy.  For the omitted residual on a modulus with `n` unit residues, use the
crude probability-discrepancy Cauchy bound:

```text
|<c_res, delta>| <= sqrt(n * (n-1) * energy(c_res))
```

This is deliberately pessimistic.  A real theorem may exploit arithmetic
cancellation, but coefficient truncation alone must at least survive this
stress test before it can be treated as a proof route.

## Result

Minimum local main from the coefficient-discrepancy budget:

```text
0.6039353780830684
```

Truncation schedule:

```text
kept chars   energy kept       crude residual bound
27           0.5055609184      527.674209047654
45           0.7512348644      375.2778786373645
60           0.9072346891      221.92337837137575
65           0.9504309411       90.463345121002
77           0.9907751703       46.26350760893429
100          0.9997225349       11.551525290045625
120          0.9999960134        1.3182746959839886
122          1.0                 0.0
```

So even the `77`-character `99%` coefficient-energy package leaves a crude
residual bound more than `76` times the minimum local main.  Even keeping
`120` of the `122` active nonzero characters leaves a crude residual bound
above the minimum local main.

## Decision

Coefficient-energy truncation alone cannot close the q286-WBSS pointwise
target.  The route needs either:

```text
1. an explicit residual character theorem strong enough to beat local_main(N), or
2. the full active nonzero multiplicative-character package.
```

Finite evidence is not the acceptance condition for this route.  The theorem
target is universal, pointwise, and unnormalized:

```text
AdverseDrag(N) < LocalMain(N)
```

for every sufficiently large eligible even `N`, with any finite computation
serving only as the initial-range bridge below the eventual analytic threshold
or as a falsifier/calibration device.

This receipt proves no residual character theorem, multiplicative-character
theorem, fixed-modulus binary-prime discrepancy theorem, pointwise adverse-drag
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof.
