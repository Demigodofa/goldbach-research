# q286 dominant-mode above-floor threshold

Status: finite above-floor threshold formulation.  Goldbach is not proved.

This note removes the post-hoc "classification-supporting side" from the
hinge-threshold receipt.  The side is now defined arithmetically:

```text
above-floor side = reflected q286 orbits whose stage action is at least the
row's required floor.
```

Receipt:
`evidence/q286-first-three-dominant-mode-staircase-above-floor-threshold.json`

## Exact Formulation

For each selected row, let

```text
a   = above-floor mass fraction
L_a = above-floor landing mean
L_b = below-floor landing mean
```

Then the stage slack has the exact sign of

```text
a - L_b / (L_a + L_b).
```

This is no longer choosing the side from the finite pass/deficit label.  It
uses the above-floor orbit set defined by the row's stage action and required
floor.

## Measured Shape

At the full eleven-channel stage, the above-floor signed threshold surplus
classifies all selected rows:

```text
pass surplus range:    0.00343976885 .. 0.01868430462
deficit surplus range: -0.03308129834 .. -0.00285922224
```

The smallest absolute surplus is target `1222142`, about
`-0.00285922224`.  The tightest selected pass is target `13556`, about
`0.00343976885`.  The maximum threshold reconstruction error is about
`5.41e-16`.

The empty stage is not a useful classifier: it has ten selected sign errors.
This records a boundary on the formulation.  The above-floor threshold is a
full-stage obligation, not an all-prefix theorem.

## Consequence

The current sharp theorem target can now be stated without post-hoc side
selection:

```text
sign(above_mass - below_landing / (above_landing + below_landing))
```

must match the required q286 dominant staircase side at the full stage.  A
proof still needs actual prime-pair arithmetic: this receipt is an exact
finite reformulation, not a sign theorem.
