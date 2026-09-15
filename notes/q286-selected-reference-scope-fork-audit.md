# q286 Selected-Reference Scope Fork Audit

Status: finite scope-fork audit.  This compares existing checked receipts and
fits no new classifier.  It proves no selected-stress theorem, broad stress
theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach theorem.

Receipt:

```text
tools/build_q286_selected_reference_scope_fork_audit.py
evidence/q286-selected-reference-scope-fork-audit.json
```

## Question

The last two facts can look contradictory:

- scalar `(3,1)` is load-bearing for the five selected deficit references;
- scalar `(3,1)` and Kevin's watchlist fail badly on additional
  `full_nonpositive` references.

This audit records the fork explicitly instead of trying to repair it with a
new fitted feature.

## Result

The selected-five fixture:

```text
references:                    5
fresh-unseen comparisons:      3,030
scalar (3,1) failures:         0
Kevin watchlist failures:      0
watchlist without (3,1):       67 failures
```

The broad `full_nonpositive` fixture:

```text
additional references:         89
fresh-unseen comparisons:      53,934
scalar (3,1) failures:         32,661
Kevin watchlist failures:      11,634
watchlist no (3,1) pass refs:  71 / 89
```

The selected five are not a subset of the broad baseline `full_nonpositive`
fixture in the checked source predicates:

```text
selected overlap with broad full_nonpositive: 0
```

## Interpretation

Keep the selected result:

> `(3,1)` is a finite, load-bearing selected-reference coordinate for the five
> selected deficit references.

Reject the broad promotion:

> `(3,1)` and Kevin's four-channel watchlist do not define a stress-reference
> theorem for the broad baseline `full_nonpositive` population.

This is useful.  It prevents the project from chasing a closed broad route and
keeps the live work aimed at either:

- a sharper non-post-hoc selected-stress family derived from the selected-stable
  fixture itself; or
- a signed empirical/correlation estimate explaining why the selected five
  separate while many broad `full_nonpositive` references do not.
