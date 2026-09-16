# q286 residual support-order raw-scale bridge

## Question

The pointwise support-order target requires either an unnormalized estimate or
a separate positive-mass theorem.  Does the current finite horizon at least
show exactly how the normalized support-order inequality converts to raw
prime-pair scale?

## Receipt

```text
tools/build_q286_residual_support_order_raw_scale_bridge.py
evidence/q286-residual-support-order-raw-scale-bridge.json
```

## Identity

For the checked rows, the normalized action scale is

```text
scale(N) = principal_mean * strict_central_total_weight(N)
```

and

```text
raw_low_order_base(N) = normalized_low_order_base(N) * scale(N)
raw_high_order_tail(N)= normalized_high_order_tail(N) * scale(N)
raw_adverse_drag(N)  = normalized_adverse_drag(N) * scale(N)
```

When `scale(N)>0`, the normalized same-row condition

```text
normalized_low_order_base(N) > normalized_adverse_drag(N)
```

is sign-equivalent to the raw condition

```text
raw_low_order_base(N) > raw_adverse_drag(N).
```

## Finite Calibration

```text
horizon rows:                              224
positive scale rows:                       224
nonpositive scale targets:                   0
raw domination failures:                     0
sign-equivalence failures:                   0
principal mean, real:        44002.512499999146
principal mean, imag/real:   7.23271826100478e-15
minimum strict-central total weight:
                              9320.216763448925
minimum pair count target:                  24148
minimum ordered central prime-pair count:     106
tight raw margin target:                   44168
tight raw margin:             471324043.51697165
maximum relative reconstruction error:
                              2.1714989760691137e-16
```

## Decision

`CALIBRATION_raw_scale_bridge_verified_on_horizon`.

On the checked `224`-row horizon, the denominator scale is positive on every
row and the normalized same-row support-order domination is sign-equivalent to
raw domination.  This removes ambiguity about the normalization bridge on the
finite horizon.

It does not prove the needed theorem.  The remaining obligations are:

```text
1. prove total_weight(N)>0 for every sufficiently large eligible N in the
   named period classes, or avoid the denominator entirely;
2. prove raw_low_order_base(N)>raw_adverse_drag(N) pointwise after one period;
3. verify the finite initial interval separately.
```

This proves no positive-mass theorem, raw pointwise estimate, one-period
threshold theorem, low-order base theorem, high-order tail domination theorem,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
