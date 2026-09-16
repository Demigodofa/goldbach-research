# Mobius moment-square critical margin sensitivity audit

## Question

The robust Sturm route now has a weak row: `M=167`.  The source-curve
serialized polynomial has critical margin just above `427/1000`, while the
coefficient-provenance serialization slips just below it.  Which coefficient
delta actually causes that loss?

## Receipt

```text
tools/build_mobius_moment_square_critical_margin_sensitivity_audit.py
evidence/mobius-moment-square-critical-margin-sensitivity-audit.json
```

## Method

For each scale, compute the high-precision critical point of the source
serialized polynomial and decompose

```text
P_provenance(t_source) - P_source(t_source)
```

degree by degree as

```text
(c_provenance,k - c_source,k) * t_source^k.
```

Then separately record the small correction from moving the provenance
minimizer from `t_source` to its own critical point.

## Result

At the weak row `M=167`:

```text
source critical margin:      0.4270105091865797085
provenance critical margin:  0.4269818990580671773
total provenance-source loss:-0.0000286101285125313
direct coefficient loss:     -0.0000286101238055836
minimizer movement loss:     -0.0000000000047069476
```

The direct coefficient loss is entirely the degree-`5` serialized coefficient:

```text
degree:                     5
coefficient delta:          -0.02
t_source^5:                 0.0014305061902791815
margin contribution:        -0.0000286101238055836
```

Other coefficient deltas at `M=167` are zero in the serialized receipts.

## Decision

The weak-row source-to-provenance failure at the tight `427/1000` margin is
not a diffuse effect across all coefficients, and it is not materially caused
by motion of the critical point.  To the recorded precision, it is a single
degree-`5` coefficient effect.

This makes the next theorem-shaped task sharper: before treating the full
Sturm sequence as an opaque algebraic object, derive and control the exact
degree-`5` active-minus-half-full coefficient in the actual family, then check
whether the robust `21/50` margin can be certified by exact coefficient
formulas.  This is finite serialized coefficient-sensitivity evidence only.
No critical-margin sensitivity theorem, robust-margin universal theorem,
coefficient-family theorem, universal Sturm certificate, half-frame
curve-positivity theorem, uniform active/full lower-frame theorem, Mobius
covariance theorem, signed prime-correlation theorem, q286 theorem, or
Goldbach proof is established.
