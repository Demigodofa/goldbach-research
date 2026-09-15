# q286 Additional Stress-Reference Generalization Audit

Status: finite falsifier.  This proves no broad stress theorem, selected-stress
theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach theorem.

Receipt:

```text
tools/build_q286_additional_stress_reference_generalization_audit.py
evidence/q286-additional-stress-reference-generalization-audit.json
```

## Question

Kevin asked whether `(3,1)` could be a stress-classifier lemma, and whether the
large negative reference `13822` was making the selected-reference result look
stronger than it really is.  The previous receipt showed `(3,1)` is
load-bearing for the five selected deficit references.  This audit tests the
next broader predeclared reference population: all additional references from
the channel-independent baseline `full_nonpositive` fixture.

The selected five references are excluded.  None of them overlap this baseline
`full_nonpositive` set, so the additional reference count remains `89`.

## Fixture

Fresh targets:

```text
48M, 52M, 56M, 60M, 64M, 68M
101 targets per window
606 total fresh-unseen targets
0 fresh-unseen dominant-floor deficits
```

References:

```text
additional full_nonpositive references: 89
comparison rows: 53,934
```

For every fresh target/reference pair, the script subtracts the full
target-reference local q286 vector and applies the frozen LP channel weights.
It tests scalar `(3,1)`, Kevin's watchlist
`(5,5),(3,1),(3,11),(3,7)`, the watchlist without `(3,1)`, and the frozen full
17-channel LP vector.

## Result

The broad generalization is finitely falsified:

```text
scalar (3,1):        32,661 nonpositive margins, min -0.246307015691
Kevin watchlist:     11,634 nonpositive margins, min -0.403051594472
watchlist no (3,1):   5,916 nonpositive margins, min -0.227177892839
frozen full 17 LP:   11,073 nonpositive margins, min -0.293436417771
```

Reference-level pass counts out of `89` additional references:

```text
scalar (3,1):        33 / 89
Kevin watchlist:     57 / 89
watchlist no (3,1):  71 / 89
frozen full 17 LP:   58 / 89
```

The watchlist still helps on many references, but it is not a theorem for this
broad stress predicate.  The surprising detail is that removing `(3,1)` helps
on the broad class even though `(3,1)` is load-bearing for the selected five.
That is evidence that the selected deficit fixture is not just a small sample
from the broad `full_nonpositive` population.

## Interpretation

Preserve the narrow result:

> `(3,1)` is a finite, load-bearing selected-reference coordinate for the five
> selected deficit references.

Reject the broad result:

> `(3,1)` and Kevin's four-channel watchlist do not generalize to arbitrary
> references from the baseline `full_nonpositive` q286 stress class.

The next theorem route should avoid one broad stress predicate.  It should
either define a sharper non-post-hoc selected-stress family or move from
classifier language to a signed empirical/correlation estimate that explains
why the selected five are separated while many baseline `full_nonpositive`
references are not.
