# q286 Independent Stress Feature Audit

Status: finite independent-feature audit.  This proves no stress theorem,
signed correlation theorem, pointwise character-sum theorem, or Goldbach
theorem.

Receipt:

```text
tools/build_q286_independent_stress_feature_audit.py
evidence/q286-independent-stress-feature-audit.json
```

## Question

Can the frozen low-`(3,1)` subclass be explained by pre-existing q286
filter/residue features that do not use centered `(3,1)` itself?

## Result

The broad baseline `full_nonpositive` population has:

```text
references:                         89
low centered (3,1) references:      33
strict low centered (3,1) refs:     24
```

No pre-existing natural filter predicate selected a nonempty zero-failure
family.  The best ordinary filter predicates still include many rows above the
frozen `(3,1)` threshold:

```text
first_two_active:                   88 refs, 33 low, 55 above
first_three_tail:                   86 refs, 32 low, 54 above
active_selector:                    86 refs, 32 low, 54 above
complement_floor:                   75 refs, 28 low, 47 above
prior seed residues 38/64:           4 refs,  2 low,  2 above
```

Even post-hoc one-feature numeric thresholds with support at least `5` did not
find a pure zero-failure subset.  The best F1 thresholds remain mixed; for
example:

```text
first_two <= -0.4716539663254832:   71 refs, 30 low, 41 above
first_three <= -0.5183748240171808: 69 refs, 29 low, 40 above
full <= -0.037814875664723656:      68 refs, 28 low, 40 above
```

Small residue pockets exist, but they are too small to serve as the theorem
family.  Residue `124 mod 143` has `4/4` low rows and residue `82 mod 143` has
`3/3`, while many residues have only one or two representatives.

## Interpretation

This demotes the simplest independent-filter explanation.

`(3,1)` remains a useful stress/reference coordinate, but the stress family is
not yet defined by the existing filter-order predicates, broad
`full_nonpositive`, active selector, complement floor, or prior seed residues.
The missing theorem still has to explain why an independently defined family
should land below the low-`(3,1)` scalar threshold, or replace classifier
language with a signed correlation estimate.
