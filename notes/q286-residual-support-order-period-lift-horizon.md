# q286 residual support-order period-lift horizon

## Question

The first support-order period-lift holdout survived eight forward lifts.  Does
the same fixed support-size `<= 2` split survive a wider consecutive horizon?

## Mechanism

Keep the split unchanged:

```text
low-order base  = aligned_only_full_action + support-size <= 2 packets
high-order tail = support-size >= 3 packets
```

Then evaluate the first `32` forward period-lifts of the original seven
targets:

```text
target = original_target + k * 10010,  k = 1..32
```

No support mask, envelope, or constant is refit.

## Receipt

```text
tools/build_q286_residual_support_order_period_lift_horizon.py
evidence/q286-residual-support-order-period-lift-horizon.json
```

## Result

```text
horizon rows:                                 224
actual full positive rows:                    224 / 224
low-order base positive rows:                 224 / 224
low-order/full sign mismatches:                 0

tight low-order base target:               255016
tight low-order base:          0.2943409774960611
tight full action:             0.27673704750570033

worst adverse/base target:                 164926
worst high-order adverse/base ratio:
                               0.13266261119465184
worst high-order abs/base ratio:
                               0.13266261119465184

horizon high-order adverse envelope:
                               0.06972227681175086
horizon envelope margin at tight base:
                               0.22461870068431022
```

The worst adverse/base row is unchanged from the eight-lift holdout.  The new
tight low-order base occurs at lift `16` of the original tight residue class
`94856`, but it still leaves a large positive margin against the disconnected
high-order adverse envelope.

## Decision

`CANDIDATE_period_lift_support_order_bridge_survives_32_lift_horizon`.

This strengthens the eventual-threshold hypothesis for the support-order
split.  Across this finite `224`-row horizon, the low-order base is always
positive, the full action is always positive, and even the disconnected
high-order adverse envelope stays below every low-order base.

This remains finite evidence only.  It proves no eventual-threshold theorem,
low-order base theorem, high-order tail domination theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.
