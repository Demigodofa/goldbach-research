# q286 residual support-order period-lift holdout

## Question

The support-order sign bridge survived the original seven-row fixture.  Does
the same fixed split survive changed prime-pair masses when the same seven
residues are lifted forward by full periods?

## Mechanism

Keep the exact split from the support-order bridge:

```text
low-order base  = aligned_only_full_action + support-size <= 2 packets
high-order tail = support-size >= 3 packets
```

Then evaluate the first `8` forward period-lifts of the original seven targets:

```text
target = original_target + k * 10010,  k = 1..8
```

This keeps the same residue operator and support-order dictionary while
changing the actual strict-central prime-pair masses.

## Receipt

```text
tools/build_q286_residual_support_order_period_lift_holdout.py
evidence/q286-residual-support-order-period-lift-holdout.json
```

## Result

```text
holdout rows:                                  56
actual full positive rows:                     56 / 56
low-order base positive rows:                  56 / 56
low-order/full sign mismatches:                 0

tight low-order base target:               124886
tight low-order base:          0.3739719483114472
tight full action:             0.39426181470078336

worst adverse/base target:                 164926
worst high-order adverse/base ratio:
                               0.13266261119465184
worst high-order abs/base ratio:
                               0.13266261119465184

holdout high-order adverse envelope:
                               0.06972227681175086
holdout envelope margin at tight base:
                               0.30424967149969634
```

The lifted rows are much less stressed than the original fixture.  The original
tight row `94856` had low-order base about `0.05371` and adverse/base ratio
about `0.76585`.  In the lifted holdout, the tight base is about `0.37397`,
and the worst adverse/base ratio is about `0.13266`.

On this lifted holdout only, even the disconnected high-order adverse envelope
stays below every low-order base.  This was false on the original fixture.

## Decision

`CANDIDATE_period_lift_support_order_bridge_survives_holdout`.

This supports an eventual-threshold hypothesis for the support-order split:
the early fixture contains the hard stress, while the first eight forward
period-lifts of the same residues show much larger low-order bases and much
smaller high-order tail ratios.

This is still finite evidence only.  It proves no eventual-threshold theorem,
low-order base theorem, high-order tail domination theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.
