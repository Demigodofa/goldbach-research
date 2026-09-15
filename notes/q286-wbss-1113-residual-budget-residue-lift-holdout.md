# q286-WBSS 11,13 Residual-Budget Residue-Lift Holdout

Status: finite targeted holdout only. Goldbach is not proved.

## Question

The prior source-population audit made a promising finite split:

```text
11,13 lead drag + signed residual from 5,7 / 5,13 / 7,11
```

On the original `230` rows, the `11,13` edge was negative on every row and a
one-sided residual theta `1/2` passed. This holdout asks whether that split
survives fresh target values for the exact residue classes where the residual
edges previously pushed upward.

## Mechanism

Select the `32` unique target residues whose prior residual edge sum was
positive. For each selected residue, test the next four period-lifts beyond
the old maximum target. The coefficient geometry is fixed modulo `10010`, but
the strict-central binary-prime measures are recomputed at the new target
values.

This is adversarially targeted by residue class. It is not an unbiased
asymptotic sample.

## Receipt

```text
tools/build_q286_wbss_1113_residual_budget_residue_lift_holdout.py
evidence/q286-wbss-1113-residual-budget-residue-lift-holdout.json
```

## Result

The holdout contains `128` targets, from `956364` through `995746`.

The `11,13` lead edge does not stay negative:

```text
lead edge negative rows:                56 / 128
lead edge nonnegative rows:             72 / 128
total edge negative after residual:     56 / 128
```

Failures occur across all four lift buckets:

```text
lift 0: lead negative 12 / 32, total negative  9 / 32
lift 1: lead negative 10 / 32, total negative 11 / 32
lift 2: lead negative 16 / 32, total negative 19 / 32
lift 3: lead negative 18 / 32, total negative 17 / 32
```

Even among rows where the `11,13` edge remains negative, the positive
pushback ratio can become large:

```text
observed maximum positive-pushback ratio: 16.998115502313933
theta 1/2: fails 91 rows
theta 1:   fails 84 rows
```

The most extreme ratio occurs at target `957744`, where the `11,13` drag is
only `0.00044726889496436023` and the positive residual pushback is
`0.007602728337196513`.

## Decision

This holdout falsifies the portable version of the `11,13`-led residual-budget
route for the current coefficient split. The original `.5` theta is a
source-population fit, not a theorem target.

The useful survivor is negative information: do not promote `11,13` lead edge
plus residual theta into a universal route without a changed mechanism. The
next plausible path is a more global signed-witness estimate or a different
aggregate inequality that does not require the `11,13` edge to stay negative
row by row.

No `11,13` edge theorem, residual theorem, character-sum bound, binary-prime
projection-control theorem, signed discrepancy theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof is established
here.
