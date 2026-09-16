# q286 residual support-order positive-mass obligation

## Question

The raw-scale bridge requires `total_weight(N)>0`.  Is that just a harmless
denominator side condition, or is it theorem-strength?

## Receipt

```text
tools/build_q286_residual_support_order_positive_mass_obligation.py
evidence/q286-residual-support-order-positive-mass-obligation.json
```

## Classification

For the support-order route,

```text
strict_central_total_weight(N)
  = sum log(p) log(N-p)
```

over strict-central prime pairs

```text
N/3 < p < 2N/3,  p prime,  N-p prime.
```

Every summand is positive.  Therefore

```text
strict_central_total_weight(N) > 0
```

if and only if at least one strict-central prime pair exists for `N`.

So the positive-mass theorem is not a cheap denominator lemma.  For the named
period classes, it is a strict-central Goldbach-in-window existence theorem.

## Finite Calibration

```text
horizon rows:                         224
positive pair-count rows:             224
positive total-weight rows:           224
zero pair-count targets:                0
zero/nonpositive weight targets:        0
minimum pair count target:          24148
minimum ordered central pair count:   106
minimum strict-central total weight:
                         9320.216763448925
```

## Decision

`TARGET_positive_mass_is_strict_central_existence_obligation`.

The checked horizon has positive mass everywhere, but the universal theorem
obligation is strict-central prime-pair existence.  Do not demote it to a
minor normalization condition.  A proof must either:

```text
1. prove positive strict-central mass and then prove raw/normalized
   support-order domination; or
2. prove a single raw lower-bound theorem that already implies positive
   strict-central mass.
```

This proves no positive-mass theorem, strict-central existence theorem, raw
pointwise estimate, one-period threshold theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
