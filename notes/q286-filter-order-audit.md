# q286 Filter-Order Audit

Status: finite diagnostic only.  This is not a proof of Goldbach.

## Purpose

This records Kevin's "which cloth comes first?" question as an executable
q286 receipt.  The same finite predicates commute as set intersections, but
their order still matters for theorem design: a coarse early filter can hide
which later predicate is actually doing the hard sorting.

The compact evidence file is:

```text
evidence/q286-filter-order-audit.json
```

It is built by:

```text
python tools/build_q286_filter_order_audit.py
```

The underlying executable receipt is:

```text
q286_first_three_filter_order_audit_receipt
```

## Eight-Period Result

On the unchanged eight-period fixture, `40040` targets were tested.

Predicate counts:

```text
complement_positive:           40040
complement_floor .3:           39976
full_positive:                 39951
first_two_active:               7768
first_three_tail .3:            4406
active_selector:                4405
full_nonpositive:                 89
nonrescued_first_three_tail:       86
active_nonrescued:                86
```

The one target in the first-three tail but not the active selector is:

```text
10648
```

The three full-nonpositive targets outside the first-three tail are:

```text
10354, 11614, 14888
```

The eleven first-three tail targets below the `.3` complement floor are:

```text
10294, 10564, 10814, 11902, 12424, 14138,
14852, 15026, 16388, 17042, 17522
```

## Interpretation

For this finite fixture:

- `first_three_tail` is almost the same as the active selector; applying
  `first_two_active` afterward removes exactly one target.
- `full_nonpositive` is the fine residual filter: only `89 / 40040` targets
  have nonpositive full action, and `86` of those are inside the first-three
  tail.
- The complement `.3` floor is extremely broad globally but does not decide
  the first-three tail: it removes only eleven first-three tail targets.

This suggests the theorem pressure should not primarily be "prove the
first-two active predicate is rare after first-three."  The sharper questions
are:

1. why the first-three tail almost contains all full-nonpositive rows;
2. why the `86` nonrescued first-three-tail rows disappear under lift or later
   cycles in the checked receipts;
3. what theorem would control the three full-nonpositive outliers outside the
   first-three tail.

## Curiosity Return

Status: `aha-candidate`.

Mechanism: the first-three predicate appears to be the main coarse separator
for early full-action failures, while the first-two active predicate is nearly
redundant after first-three on the checked fixture.

Prediction: applying unchanged filter-order audits to new q286 windows should
show either the same near-containment pattern or immediately produce named
outlier targets where the active selector and first-three tail differ.

Falsifier: a new unchanged window where `first_three_tail_not_first_two_active`
or `full_nonpositive_not_first_three_tail` becomes a large fraction of the
corresponding predicate set would falsify this compression.

Next useful test: run the unchanged audit on a later window and compare the
difference sets before adding any new thresholds.

## Boundary

This audit is finite evidence and theorem navigation.  It does not prove an
eventual first-three tail theorem, complement floor, strict closure, pointwise
signed prime-correlation estimate, outer assembly, or Goldbach.
