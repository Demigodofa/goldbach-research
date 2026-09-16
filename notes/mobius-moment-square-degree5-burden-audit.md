# Mobius moment-square degree-5 burden audit

## Question

The critical-margin sensitivity audit showed that the weak `M=167`
source-to-provenance margin loss is a single degree-`5` coefficient effect.
Which active/full Gram entries make that coefficient?

## Receipt

```text
tools/build_mobius_moment_square_degree5_burden_audit.py
evidence/mobius-moment-square-degree5-burden-audit.json
```

## Result

At `M=167`, the degree-`5` half-frame coefficient is

```text
active_degree5 - (1/2) full_degree5
```

and is contributed by exactly three degree-sum-`5` Gram pairs:

```text
(00,12): -17833463267559.586   about 14.14%
(01,02): -36071645892875.484   about 28.61%
(01,11): -72179970258478.02    about 57.25%
```

They have the same sign, so there is no hidden cancellation among the
degree-`5` half-frame contributors:

```text
degree-5 half-frame coefficient:     -126085079418913.1
sum of absolute contributions:        126085079418913.1
same-sign contributors:               true
```

The provenance/source degree-`5` coefficient delta remains the sensitivity
driver:

```text
source degree-5 coefficient:          -126085079418913.08
provenance degree-5 coefficient:      -126085079418913.1
provenance-source delta, decimal:     -0.02
margin contribution at t_source:      -0.0000286101238055836
```

The ordinary binary-float subtraction of those two huge displayed
coefficients is not reliable enough for a theorem-facing delta; the receipt
therefore carries the exact decimal-rational comparison separately as
`weak_scale_provenance_minus_source_degree5_delta_decimal`.

## Decision

The next exact-coefficient theorem does not have to begin as a black-box
degree-`8` polynomial problem.  For the weak row, the degree-`5` burden is the
sum of three concrete active/full Gram entries, dominated by `(01,11)`.

The theorem-shaped route is now sharper: derive exact formulas or bounds for
the `(00,12)`, `(01,02)`, and `(01,11)` degree-`5` active/full Gram
contributions, then re-evaluate whether the robust `21/50` lower margin can be
proved before carrying the full Sturm sequence.  This is finite degree-`5`
burden evidence only.  No degree-`5` coefficient theorem, robust-margin
universal theorem, coefficient-family theorem, universal Sturm certificate,
half-frame curve-positivity theorem, uniform active/full lower-frame theorem,
Mobius covariance theorem, signed prime-correlation theorem, q286 theorem, or
Goldbach proof is established.
