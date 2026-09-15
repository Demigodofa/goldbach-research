# q286 centered (3,1) stress-class audit

Status: finite stress-class falsifier for a predeclared q286 class. This is
not a proof of a stress-classifier theorem, binary-prime correlation theorem,
signed projection theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-centered-3-1-stress-class-audit.json
```

The builder is:

```text
tools/build_q286_centered_3_1_stress_class_audit.py
```

It uses the earlier centered scalar audit:

```text
evidence/q286-centered-channel-scalar-order-audit.json
```

## Stress Class

The tested stress class is not chosen from `(3,1)`.  It is the
`full_nonpositive` population from the baseline filter-order receipt:

```text
q286_first_three_filter_order_audit_receipt(
    start=10000,
    cycle_count=8,
    targets_per_cycle=5005,
    tail_threshold=.3,
    complement_floor=.3,
)
```

This baseline fixture has `40040` targets and `89` `full_nonpositive` rows.
Its `nonrescued_first_three_tail` and `active_nonrescued` subclasses each
contain `86` rows.  The next contiguous eight-period holdout beginning at
`90080` has `0` `full_nonpositive` rows, so the classifier question is only
populated in the baseline window under this finite gate.

## Falsifier

The frozen fresh-window minimum from the centered scalar audit is the
threshold:

```text
(3,1) fresh minimum: -0.017835394356714915 at target 24000008
(5,5) fresh minimum: -0.023944926855061086 at target 24000146
```

If centered `(3,1)` were a classifier for the predeclared
`full_nonpositive` stress class, every `full_nonpositive` target should sit
below the `(3,1)` fresh minimum.

## Result

The broad classifier fails.

For `(3,1)`, only `33/89` `full_nonpositive` rows sit below the fresh minimum.
The other `56/89` are at or above it.  The maximum centered `(3,1)` row is
target `11902`, with weighted centered value `0.23016925898905402`.  The same
failure appears on the narrower subclasses: `54/86` rows fail for both
`nonrescued_first_three_tail` and `active_nonrescued`.

For `(5,5)`, only `40/89` `full_nonpositive` rows sit below the fresh minimum.
The other `49/89` are at or above it.  The maximum centered `(5,5)` row is
target `12032`, with value `0.21405310870173938`.

The selected-deficit separator result and the full-action stress-class test
are distinct facts, not the same population under different names.  A later
provenance audit records the precise span boundary: the baseline
`full_nonpositive` fixture covers `10000..90078`, so selected references
`164598` and `1222142` are outside that baseline window by construction.

## Interpretation

This falsifies the broad reading:

```text
centered (3,1) classifies all full_nonpositive q286 stress rows
```

The narrower result survives:

```text
centered (3,1) separates the five selected deficit references from the fresh
predeclared targets
```

The theorem target should not be promoted to a universal stress-classifier
lemma.  The next viable branch is either to define a different non-post-hoc
deficit class that actually contains the selected references, or to abandon
scalar classification and return to a signed/correlation estimate.
