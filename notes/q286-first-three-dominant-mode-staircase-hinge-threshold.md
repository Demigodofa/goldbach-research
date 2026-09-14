# q286 dominant-mode staircase hinge threshold

Status: finite hinge-threshold obligation.  Goldbach is not proved.

This note rewrites the selected q286 staircase hinge balance as a single
support-mass threshold inequality.

Receipt:
`evidence/q286-first-three-dominant-mode-staircase-hinge-threshold.json`

## Exact Threshold

For a selected row, let

```text
s   = classification-supporting mass fraction
L_s = classification-supporting landing mean
L_o = classification-opposing landing mean
```

Then the hinge margin satisfies

```text
s * L_s - (1 - s) * L_o >= 0
iff
s >= L_o / (L_s + L_o).
```

The right-hand side is the row's landing-dependent support-mass threshold.
This formulation is exact on the selected fixture; the classification side is
still inherited from the finite row classification.

## Measured Shape

At the full eleven-channel stage, every selected row satisfies the threshold.
The support-mass surplus over the threshold is small:

```text
minimum 0.00285922224
mean    0.01170040715
maximum 0.03308129834
```

The relative surplus is also small:

```text
minimum 0.00576470572
mean    0.02347681082
maximum 0.06544321112
```

The tightest row is target `1222142`, with support mass about
`0.4988467680`, threshold about `0.4959875458`, and surplus about
`0.0028592222`.  The maximum threshold reconstruction error is about
`3.19e-16`.

## Consequence

The active theorem obligation can now be stated as a small positive surplus:

```text
classification_supporting_mass
  - opposing_landing / (supporting_landing + opposing_landing)
  > 0.
```

This is not yet non-circular, because the support side is selected from the
finite pass/deficit classification.  The next proof step is to define the
intended support side arithmetically, or replace this threshold statement by a
signed aggregate theorem that implies the same positive surplus.
