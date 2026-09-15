# q286 centered (3,1) stress-classifier boundary

Status: finite derived boundary receipt only.  This is not a proof of a
selected-stress theorem, broad stress-class theorem, signed correlation
theorem, pointwise character-sum theorem, or Goldbach.

## Source

The generated receipt is:

```text
evidence/q286-centered-3-1-stress-classifier-boundary.json
```

The builder is:

```text
tools/build_q286_centered_3_1_stress_classifier_boundary.py
```

It derives no new fitted vector.  It consolidates four checked receipts:

```text
evidence/q286-centered-3-1-reference-lemma-audit.json
evidence/q286-watchlist-fresh-unseen-window-audit.json
evidence/q286-centered-3-1-stress-class-audit.json
evidence/q286-selected-deficit-provenance-audit.json
```

## Decision

The supported finite claim is narrow:

```text
centered (3,1) is a useful selected-stress reference classifier coordinate
for the five pre-existing selected dominant-floor deficit references
```

The falsified finite claim is broad:

```text
centered (3,1) classifies every row in the independent baseline
full_nonpositive q286 stress predicate
```

This distinction matters because the selected references and the
`full_nonpositive` stress class come from different predicates.  The selected
references are stable/volatile dominant-floor failures in the selected
fixture.  The broad stress class is the independent filter-order
`full_action_to_principal_ratio <= 0` population.

## Evidence

For the selected-reference lane, scalar `(3,1)` passes:

```text
original fresh selected-reference comparisons: 3030/3030 positive
fresh unseen selected-reference comparisons:   3030/3030 positive
fresh unseen minimum scalar margin:            0.0035109555591320892
```

Kevin's four-channel watchlist
`(5,5),(3,1),(3,11),(3,7)` also passes all `3030` fresh unseen comparisons,
with minimum margin `0.0020345565333929026`.  The watchlist without `(3,1)`
fails `67` comparisons, so `(3,1)` carries real rescue load in the selected
reference family.

For the independent broad stress lane, centered `(3,1)` fails:

```text
full_nonpositive rows:       89
below fresh minimum:         33
at or above fresh minimum:   56
separator passes:            false
```

The active_nonrescued subclass also fails, with `54/86` rows at or above the
fresh minimum.

## Reference 13822

Reference `13822` is a strong witness for the narrow selected-reference
reading:

```text
target mod 143:                94
dominant margin to floor:      -0.03674434602428933
stable-core margin to floor:    0.3023670686383121
volatile rim to principal:     -0.3391114146626045
centered (3,1) rank:            2
centered (3,1) weighted value: -0.028592853507378977
```

On the later fresh unseen audit, scalar `(3,1)` passes all `606/606`
comparisons against `13822`, with minimum margin `0.012455096805020166`.
The four-channel watchlist passes the same `606/606` comparisons with a much
larger minimum margin `0.09719361604522675`.  The frozen full 17-channel LP
fails all `606/606` comparisons against `13822`, with minimum margin
`-0.14321442782269148`.

## Next obligation

Do not promote `(3,1)` to a broad q286 stress theorem.  The next theorem route
needs either:

- a new non-post-hoc stress predicate that captures the selected references
  and faces fresh holdout rows; or
- a signed empirical/correlation estimate for the selected family that no
  longer depends on the classifier wording.

