# q286 residual support-order positive low-order obligation

## Question

The raw adverse-ratio route needs

```text
B_low_raw(N) > 0.
```

Is that a harmless low-order side condition, or is it another support-strength
obligation?

## Receipt

```text
tools/build_q286_residual_support_order_positive_low_order_obligation.py
evidence/q286-residual-support-order-positive-low-order-obligation.json
```

## Identity

In the current raw-scale bridge,

```text
B_low_raw(N)
  = b_low_norm(N) * principal_mean * strict_central_total_weight(N).
```

The principal mean is positive in the checked fixed context.  Therefore a
factored proof of `B_low_raw(N)>0` needs:

```text
b_low_norm(N) > 0
strict_central_total_weight(N) > 0
```

on the eligible classes.

If strict-central support is empty, then
`strict_central_total_weight(N)=0`, and hence `B_low_raw(N)=0`.  So a direct
theorem proving `B_low_raw(N)>0` already forces nonempty strict-central
support.  A normalized theorem `b_low_norm(N)>0` alone does not create mass.

## Finite Calibration

```text
checked rows:                              224
positive raw low-order rows:               224
nonpositive raw low-order targets:           0
positive normalized low-order rows:        224
nonpositive normalized low-order targets:    0
smallest raw-low target:                 24148
smallest raw low:           494408133.6057817
smallest normalized-low target:         255016
smallest normalized low:   0.2943409774960611
smallest total-weight target:            24148
```

## Decision

`TARGET_positive_low_order_is_support_strength`.

Positive low-order cannot replace positive mass unless it is proved directly
in raw scale, in which case it already implies nonempty support for this
witness family.  A normalized low-order positivity theorem still needs a
positive-mass theorem.  The split route

```text
B_low_raw(N)>0
D_high_minus_raw(N)/B_low_raw(N) < 1
```

therefore has two theorem-strength inputs.  The cleaner target remains one
direct raw lower-bound theorem:

```text
R_raw(N)=B_low_raw(N)-D_high_minus_raw(N)>0.
```

This proves no positive low-order theorem, positive-mass theorem, raw
adverse-ratio theorem, raw lower-bound theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
