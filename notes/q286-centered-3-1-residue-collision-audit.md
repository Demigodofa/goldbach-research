# q286 centered (3,1) residue-collision audit

Status: finite same-residue selected-fixture audit only.  This is not a proof
of a stress-classifier theorem, signed correlation theorem, pointwise
character-sum theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-centered-3-1-residue-collision-audit.json
```

The builder is:

```text
tools/build_q286_centered_3_1_residue_collision_audit.py
```

It reads:

```text
evidence/q286-centered-channel-scalar-order-audit.json
evidence/q286-selected-deficit-provenance-audit.json
evidence/q286-centered-3-1-reference-lemma-audit.json
```

## Question

Could the selected-deficit `(3,1)` signal be only a local residue effect?

For rows with the same target residue modulo `143`, the stored local q286
channel vector is identical.  Therefore a selected deficit and selected clear
at the same residue have local `(3,1)` gap exactly zero after subtraction.
Any remaining centered `(3,1)` gap is empirical/correlation-side.

## Result

Four of the five selected deficit references have a selected clear-control
row at the same residue.  All four same-residue pairs split the right way:
the selected deficit is lower in centered `(3,1)` than the same-residue clear.

| residue mod 143 | deficit | clear | local gap | empirical gap clear-deficit | weighted centered gap |
|---:|---:|---:|---:|---:|---:|
| 5 | 164598 | 129706 | 0.0 | 0.002146484472 | 0.001852428867 |
| 94 | 13822 | 40420 | 0.0 | 0.072185764915 | 0.062296744487 |
| 94 | 55864 | 40420 | 0.0 | 0.092078361112 | 0.079464173328 |
| 114 | 24424 | 13556 | 0.0 | 0.183016649439 | 0.157944457060 |

Summary:

```text
same-residue collision pairs: 4
all pairs pass: true
minimum weighted gap: 0.0018524288669540291
mean weighted gap:    0.07538945093546084
maximum weighted gap: 0.15794445706006727
```

Reference `1222142` has residue `64` modulo `143` and has no selected
clear-control row at the same residue in this fixture, so this audit does not
test it by same-residue collision.

## Interpretation

This supports the non-local reading for the checked selected rows:

```text
the low centered (3,1) selected-deficit signal is not caused merely by the
stored local residue vector
```

The audit does not prove that `(3,1)` classifies a broad stress population.
The earlier broad `full_nonpositive` classifier falsifier remains active.
The next theorem-shaped path needs either a non-post-hoc class that contains
the selected deficit references, or a signed/correlation estimate explaining
why these same-residue empirical gaps have this sign.
