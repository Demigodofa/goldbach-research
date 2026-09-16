# q286 residual support-order single raw-bound target

## Question

Can the route avoid a separate positive-mass theorem by proving one universal,
pointwise, unnormalized analytical estimate?

## Receipt

```text
tools/build_q286_residual_support_order_single_raw_bound_target.py
evidence/q286-residual-support-order-single-raw-bound-target.json
```

## Target

Define the same-row raw quantities

```text
B_low_raw(N)
T_high_raw(N)
D_high_minus_raw(N) = max(0, -T_high_raw(N))
R_raw(N) = B_low_raw(N) - D_high_minus_raw(N)
```

The theorem target is:

```text
R_raw(N) > 0
```

for every sufficiently large eligible `N` in the named q286 support-order
period classes, with the finite initial interval verified separately.

This is pointwise and unnormalized.  It is not an L2 target and it is not
accepted by finite evidence.

## Why It Subsumes Positive Mass

If `T_high_raw(N)<0`, then `D_high_minus_raw(N)=-T_high_raw(N)`, so
`R_raw(N)>0` gives

```text
B_low_raw(N) + T_high_raw(N) > 0.
```

If `T_high_raw(N)>=0`, then `D_high_minus_raw(N)=0`, so `R_raw(N)>0` gives
`B_low_raw(N)>0`, and adding the nonnegative tail still gives a positive full
raw witness.

If the strict-central prime-pair support is empty, every raw prime-pair sum in
this witness is zero.  Then

```text
B_low_raw(N) = T_high_raw(N) = D_high_minus_raw(N) = R_raw(N) = 0,
```

contradicting a strict raw lower bound.  Therefore a proved strict raw bound
would force nonempty strict-central support, hence at least one prime pair
`N=p+(N-p)` with `N/3<p<2N/3`.

## Finite Calibration

```text
horizon rows:                         224
raw-margin positive rows:             224
raw domination failures:                0
positive pair-count rows:             224
positive total-weight rows:           224
zero pair-count targets:                0
zero/nonpositive weight targets:        0
tight raw-margin target:            44168
tight raw margin:       471324043.51697165
minimum pair count target:          24148
minimum ordered central pair count:   106
minimum strict-central total weight:
                         9320.216763448925
```

## Decision

`TARGET_single_raw_lower_bound_subsumes_positive_mass`.

A single strict raw lower-bound theorem would make the separate positive-mass
obligation sleep, because zero strict-central support makes strict raw
positivity impossible.  This is the cleaner route than normalizing first.

But it is still Goldbach-strength theorem work.  The raw lower-bound theorem is
not proved here, the finite horizon is not an acceptance condition, and this
establishes no q286 threshold theorem, strict-central Goldbach theorem, or
Goldbach proof.
