# q286 residual support-order sign bridge audit

## Question

The signed-tail bridge made `support size <= 2` the cleaner structural target.
Does this support-order split have a non-circular finite shape?  In particular,
does the low-order base

```text
aligned_only_full_action + sum support-size <= 2 packet actions
```

already separate the frozen positive rows from the nonpositive stress rows
before the high-order tail is added?

## Mechanism

Split the `15` support packets into:

```text
low order:       support size <= 2
high-order tail: support size >= 3
```

Then test

```text
full_action = low_order_base + high_order_signed_tail
```

on the seven frozen support-packet rows.  A theorem route would need both:

```text
low_order_base(N) > 0
high_order_signed_tail(N) > -low_order_base(N)
```

or an equivalent pointwise signed lower bound.

## Receipt

```text
tools/build_q286_residual_support_order_sign_bridge_audit.py
evidence/q286-residual-support-order-sign-bridge-audit.json
```

## Result

```text
row count:                                      7
actual full positive rows:                     5
actual full nonpositive rows:                  2
low-order base positive rows:                  5
low-order/full sign mismatches:                0

tight positive target:                     94856
tight low-order base:          0.05371090383605067
tight high-order signed tail: -0.041134437542250886
tight full action:             0.012576466293799767
max high-order adverse/base ratio:
                               0.7658489171549095
max high-order abs/base ratio: 0.9694853511961387

closest nonpositive base target:           14996
closest nonpositive low-order base:
                              -0.16632720985767507

all-row high-order adverse envelope:
                               0.23468203404186905
all-row envelope margin at tight positive base:
                              -0.18097113020581837
```

## Decision

`CANDIDATE_support_order_sign_bridge_survives_fixture`.

The support-order split survives the frozen fixture as a candidate bridge.  The
low-order base sign agrees with the full action sign on all seven rows: the
five base-positive rows are exactly the five full-positive rows, and the two
nonpositive stress rows are base-negative.

The tight row is still `94856`.  There the high-order signed tail is adverse
and consumes about `76.58%` of the low-order base, leaving only about
`0.01258` full action.  This is a near but positive finite domination margin.

The wrong theorem remains rejected: an unqualified all-row high-order adverse
envelope fails because the worst high-order adverse tail over all rows is about
`0.23468`, much larger than the tight positive base.

The next proof object is therefore not a global adverse envelope.  It is a
pointwise low-order base positivity theorem plus a high-order signed-tail
domination theorem on the same mathematically named class.

No low-order base theorem, high-order tail domination theorem, signed packet
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof is established.
