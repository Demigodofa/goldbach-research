# q286 Centered `(3,1)` Threshold Subclass Audit

Status: finite threshold-subclass audit.  This proves no stress theorem,
signed correlation theorem, pointwise character-sum theorem, or Goldbach
theorem.

Receipt:

```text
tools/build_q286_centered_3_1_threshold_subclass_audit.py
evidence/q286-centered-3-1-threshold-subclass-audit.json
```

## Question

Could the selected-reference `(3,1)` result extend to other stress/deficit
references if we freeze the selected five's scalar threshold first?

## Frozen Threshold

The selected five have weighted centered `(3,1)` values:

```text
minimum: -0.04576028234769708
mean:    -0.029875565197628608
maximum: -0.0196487122614909
```

The fresh-window minimum is:

```text
-0.017835394356714915
```

So the selected-five maximum is below the fresh minimum by about
`0.001813317904775985`.

## Result

Applying that frozen selected threshold to the independent baseline
`full_nonpositive` class:

```text
broad full_nonpositive references:       89
below fresh minimum in (3,1):            33
at/below selected max threshold:         33
at/below selected min threshold:         24
scalar fresh-window failures in subset:  0
```

The lowest independent broad rows are far below `13822` in centered `(3,1)`:

```text
37568: -0.2027956998766996
17702: -0.15367007403813582
14852: -0.14492200660455642
13444: -0.12407627048311179
18626: -0.11811035816275595
```

## Interpretation

This strengthens the statement:

> Centered `(3,1)` is a useful stress/reference coordinate.

It does not prove:

> Centered `(3,1)` defines a non-post-hoc stress class.

The reason is mechanical: the passing subclass is selected by the same scalar
being tested.  That is a valid finite scalar-order certificate, but the missing
theorem still has to explain why an independently defined stress family should
fall below that scalar threshold.
