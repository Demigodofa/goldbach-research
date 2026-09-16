# q286 residual support-order raw-bound phase space

## Question

Can the current raw theorem target be laid out so stress points and possible
structure are easier to inspect?

## Receipt

```text
tools/build_q286_residual_support_order_raw_bound_phase_space.py
evidence/q286-residual-support-order-raw-bound-phase-space.json
evidence/q286-residual-support-order-raw-bound-phase-space.html
```

## Visual Coordinates

```text
x          = log(N)
y          = ordered strict-central prime-pair count
z          = raw pointwise margin
alternate z = adverse drag / raw low-order base
color      = target mod 286
brightness = raw pointwise margin as distance from failure
```

The HTML is a local linked view: click a point or table row to inspect the
exact target, residues, pair count, strict-central total weight, raw low-order
base, raw tail, adverse drag, margin, scale, and lift data.

## Finite Diagnostics

```text
checked rows:                         224
positive raw-margin rows:             224
raw domination failures:                0
negative high-order tail rows:        100
nonnegative high-order tail rows:     124
tightest raw-margin target:         44168
tightest raw margin:    471324043.51697165
largest adverse-ratio target:      164926
largest adverse / low: 0.13266261119465184
smallest pair-count target:         24148
minimum ordered pair count:           106
```

Finite shape correlations on the checked horizon:

```text
corr(log N, log raw margin):
  0.9456990848108981
corr(pair count, log raw margin):
  0.8915845948837736
corr(log strict-central total weight, log raw margin):
  0.980275224825557
```

## Decision

`CALIBRATION_raw_bound_phase_space_stress_locator`.

The view is useful for finding stress rows and for orienting the next analytic
attempt.  The tightest checked raw margin is target `44168`; the largest
adverse/low-order ratio is target `164926`.  The finite horizon suggests that
raw margin is tightly aligned with strict-central total weight, but that is
not a theorem and also warns against smuggling in positive mass.

Next theorem-shaped route: prove a pointwise raw witness lower bound directly,
or prove a structured adverse-ratio bound in raw scale whose hypotheses do not
assume the desired strict-central support.  This artifact proves no raw
lower-bound theorem, positive-mass theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
