# q286 Centered (3,1) Reference Sensitivity Audit

Status: finite centered-scalar reference-sensitivity audit.  This proves no
stress theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach theorem.

Receipt:

```text
tools/build_q286_centered_3_1_reference_sensitivity_audit.py
evidence/q286-centered-3-1-reference-sensitivity-audit.json
```

## Question

Is the centered `(3,1)` stress/reference signal specific to the large negative
selected witness `13822`, or does it persist across alternate selected and
broad q286 deficit/stress references?

## Target Groups

The audit keeps the target populations separate:

```text
same-window zero-local seed targets:    12
same-window nonseed targets:           594
fresh predeclared targets:             606
```

This is a target split, not a statement about neutral channels.

## Result

Against the `606` fresh predeclared targets:

```text
selected deficit five:                 0 failures
selected deficits excluding 13822:     0 failures
reference 13822 alone:                 0 failures
broad low-33 scalar-selected refs:     0 failures
broad strict low-24 scalar-selected:   0 failures
selected clear controls:            1518 failures
broad above-threshold controls:    32648 failures
```

So the fresh-window `(3,1)` pass is not a `13822`-only accident.  Removing
`13822` from the selected deficit references still leaves zero failures.

The same-window groups are sharper and must not be merged into the fresh-window
claim:

```text
selected deficit five -> 12 zero-local seed targets: 0 failures
selected deficit five -> 594 nonseed targets:        2 failures
broad low-33 -> 12 zero-local seed targets:          0 failures
broad low-33 -> 594 nonseed targets:                 2 failures
broad strict low-24 -> all same-window targets:      0 failures
```

Reference `13822` alone passes every tested target group, with minimum margins:

```text
same-window zero-local seeds:          0.019607157484913
same-window nonseeds:                  0.006377428116412568
fresh predeclared:                     0.010757459150664062
```

The strict broad low-24 group also passes all three target groups, but it is
selected by centered `(3,1)` itself and is therefore diagnostic, not a
non-post-hoc stress definition.

## Interpretation

The live `(3,1)` signal is not merely reference `13822` being unusually low.
It persists across the selected deficit references after removing `13822`, and
it also finds a scalar-selected broad low-reference family.

But the result is still not a stress theorem.  The broad low-33 and strict
low-24 groups are chosen by the same scalar being tested, while simple
independent filter/residue predicates were already falsified.  The next proof
obligation is unchanged: replace scalar-selected reference groups with an
independent arithmetic or correlation-defined family, or state the target as a
signed correlation estimate instead of a stress classifier.
