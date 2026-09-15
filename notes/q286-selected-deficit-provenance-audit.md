# q286 selected deficit provenance audit

Status: finite provenance audit. This is not a proof of a stress-class
theorem, selected-fixture classifier theorem, signed projection theorem,
binary-prime correlation theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-selected-deficit-provenance-audit.json
```

The builder is:

```text
tools/build_q286_selected_deficit_provenance_audit.py
```

It reads existing evidence only:

```text
evidence/q286-first-three-dominant-mode-stable-core-selected-classification.json
evidence/q286-first-three-dominant-mode-volatile-minimal-clause-structure.json
evidence/q286-centered-channel-scalar-order-audit.json
evidence/q286-centered-3-1-stress-class-audit.json
```

## Why This Audit Exists

The phrase "stress row" was carrying two different finite meanings:

```text
selected deficit references:
dominant-floor failures in the selected stable/volatile fixture

full_nonpositive stress class:
full-action nonpositive rows in the baseline filter-order fixture
```

The centered `(3,1)` scalar separates the five selected deficit references,
but the broad `full_nonpositive` classifier test fails.  This audit records
the provenance split instead of treating those populations as interchangeable.

## Result

The selected deficit references are:

```text
24424, 13822, 55864, 164598, 1222142
```

They are exactly the selected-fixture dominant-floor failures from the
stable/volatile classification lane.  Their margins and centered `(3,1)` ranks
are:

| target | in baseline filter span? | dominant margin | stable-core margin | volatile clauses | min size | centered `(3,1)` rank |
|---:|---|---:|---:|---:|---:|---:|
| 24424 | yes | -0.013458672694 | -0.000878478609 | 1 | 0 | 4 |
| 13822 | yes | -0.036744346024 | 0.302367068638 | 2 | 6 | 2 |
| 55864 | yes | -0.099228575792 | -0.169962981576 | 1 | 0 | 1 |
| 164598 | no | -0.019151792455 | 0.075686005197 | 2 | 3 | 7 |
| 1222142 | no | -0.008833179561 | 0.056573711698 | 10 | 4 | 3 |

The baseline filter-order span is:

```text
10000 .. 90078
```

Thus `164598` and `1222142` are outside the baseline `full_nonpositive`
fixture by construction.  The audit therefore does not say they passed or
failed that baseline predicate; it says the selected-deficit lane and the
baseline full-action stress-class lane are different finite populations.

## Interpretation

The valid narrow statement is:

```text
centered (3,1) separates the five selected stable/volatile dominant-floor
deficits from the fresh predeclared targets
```

The invalid promotion is:

```text
centered (3,1) classifies the whole full_nonpositive q286 stress class
```

Next theorem work should either define a new non-post-hoc deficit class that
actually contains the selected references, or leave scalar classification and
return to a signed/correlation estimate.
