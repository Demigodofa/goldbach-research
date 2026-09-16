# q286 residual support-order one-period threshold audit

## Question

The original support-order fixture survived as a signed split, but failed the
disconnected high-order adverse-envelope test.  The 32-lift horizon survived
that envelope test.  Does this create a sharper finite theorem shape: finite
remainder at lift `0`, plus a one-period threshold for the same seven residue
classes?

## Mechanism

Compare two already validated receipts:

```text
evidence/q286-residual-support-order-sign-bridge-audit.json
evidence/q286-residual-support-order-period-lift-horizon.json
```

The split is unchanged:

```text
low-order base  = aligned_only_full_action + support-size <= 2 packets
high-order tail = support-size >= 3 packets
```

## Result

```text
fixture lift:                                      0
fixture tight low-order base:       0.05371090383605067
fixture high-order adverse envelope:
                                     0.23468203404186905
fixture envelope margin:            -0.18097113020581837
fixture envelope survives:                         false

horizon lift range:                              1..32
horizon rows:                                     224
horizon tight low-order base:       0.2943409774960611
horizon high-order adverse envelope:
                                     0.06972227681175086
horizon envelope margin:             0.22461870068431022
horizon envelope survives:                         true

base growth factor versus fixture tight:          5.480097270277175
adverse ratio drop factor:                        5.7729070026460025
```

## Decision

`CANDIDATE_one_period_threshold_removes_high_order_envelope_obstruction`.

The finite contrast is clean: lift `0` has the right signed support-order
structure but fails the disconnected high-order adverse envelope.  Lifts
`1..32` pass the same envelope test without changing the support split,
refitting an envelope, or changing constants.

This suggests a theorem shape:

```text
finite remainder:       handle the original lift-0 fixture directly
eventual threshold:     prove the support-order envelope/base inequality
                        after one full period for the same named residue class
```

This is still finite evidence only.  It proves no one-period threshold theorem,
eventual-threshold theorem, low-order base theorem, high-order tail domination
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof.  It also does not address all even `N`; it concerns the seven checked
residue classes.
