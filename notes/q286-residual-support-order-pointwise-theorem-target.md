# q286 residual support-order pointwise theorem target

## Question

Finite evidence is no longer the acceptance condition.  What exactly would
have to be proved to turn the one-period support-order pattern into a theorem?

## Receipt

```text
tools/build_q286_residual_support_order_pointwise_theorem_target.py
evidence/q286-residual-support-order-pointwise-theorem-target.json
```

## Target

For targets in the seven named period classes after one full period, define

```text
B_low(N)       = aligned_only_full_action(N)
                 + sum support-size <= 2 signed packets
T_high(N)      = sum support-size >= 3 signed packets
D_high_minus(N)= max(0, -T_high(N))
```

The theorem-shaped sufficient condition is pointwise and same-row:

```text
B_low(N) > 0
D_high_minus(N) < B_low(N)
```

for every sufficiently large eligible target, with the initial range handled
separately as a finite remainder.

## Finite Calibration

The checked horizon still has no same-row pointwise failures:

```text
horizon rows:                         224
same-row pointwise failures:            0
tight pointwise target:            255016
tight pointwise margin: 0.27673704750570044
tight low-order base:   0.2943409774960611
worst adverse/base target:         164926
worst adverse/base ratio: 0.13266261119465184
disconnected envelope margin:
                         0.22461870068431022
```

This calibration is useful because the same-row theorem target is weaker than
the disconnected envelope: the envelope combines the worst adverse tail from
any row against every row, while the theorem only needs the actual same-row
tail to stay below the actual same-row base.

## Normalization Boundary

The current support-order receipts are finite action/decomposition receipts.
They do not carry a raw unnormalized pair-count theorem or a raw positive-mass
theorem.  Therefore a proof must do one of two things:

```text
1. state and prove the inequality directly for unnormalized binary-prime sums;
2. or prove a separate positive-mass denominator theorem, then multiply the
   normalized action identity by that positive mass.
```

The older `L2` zero-mass status does not fill this gap.  The `L2` route remains
non-circular only as an external pointwise arithmetic premise, and it is not
confirmed.  It also does not prove existence when the normalizing mass is zero.

## Decision

`TARGET_pointwise_support_order_theorem_required`.

Finite evidence is now calibration/falsifier evidence for this lane, not the
acceptance condition.  The missing bridge is an unnormalized pointwise analytic
estimate, or an equivalent positive-mass theorem plus normalized same-row
support-order domination.  This proves no pointwise analytic estimate,
one-period threshold theorem, low-order base theorem, high-order tail
domination theorem, q286 threshold theorem, strict-central Goldbach theorem, or
Goldbach proof.
