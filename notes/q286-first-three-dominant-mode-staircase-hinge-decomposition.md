# q286 dominant-mode staircase hinge decomposition

Status: finite hinge-decomposition diagnostic.  Goldbach is not proved.

This note records the exact above-floor/below-floor orbit ledger for the
selected q286 dominant-mode residual staircase.

Receipt:
`evidence/q286-first-three-dominant-mode-staircase-hinge-decomposition.json`

## Mechanism Tested

For each selected target and staircase stage, decompose the measured slack as

```text
stage_sum - required_floor
  = positive_above_floor_hinge - negative_below_floor_hinge.
```

The positive hinge sums actual strict-central prime-pair mass on reflected
orbits above the row floor, weighted by their distance above that floor.  The
negative hinge does the same below the floor.  This asks what remains after the
weak synthetic breaker-orbit story is bolted to actual prime-pair mass.

## Measured Shape

The full eleven-channel stage reconstructs the recorded staircase slack with
maximum hinge identity error about `3.33e-16`.

The classification-supporting and classification-opposing mass fractions are
both close to half:

```text
supporting mass: min 0.4455761846, mean 0.5137663724, max 0.5747545981
opposing mass:   min 0.4252454019, mean 0.4862336276, max 0.5544238154
```

The hinge contributions are also close:

```text
supporting hinge: min 0.5354932623, mean 0.7547882043, max 0.8686962800
opposing hinge:   min 0.4987489163, mean 0.7209818570, max 0.8521673665
```

On the selected full-stage rows, `6` targets are mass-driven by this diagnostic
and `6` are landing-driven.  The sets are not identical:

```text
mass-driven:    13556, 13822, 40420, 55864, 164598, 1240888
landing-driven: 24424, 13822, 40420, 129706, 1222142, 1242118
```

The tightest hinge margin is target `1222142`, about `0.00883317956`.  The
largest opposing mass is target `24424`, about `0.5544238154`, but that row
still fails because the below-floor supporting landing is stronger than the
above-floor opposing landing.

## Consequence

The next theorem target should not be a one-dimensional mass cap or a
one-dimensional landing floor.  The selected fixture uses a mixed mechanism:
some classifications are helped mainly by which side has more mass, while
others are helped by better landing quality on the classification-supporting
side.

The sharpened unresolved statement is a row-dependent hinge-balance theorem
for actual q286 prime-pair reflection orbits, or a signed aggregate theorem
that implies the same balance without proving separate mass and landing
bounds.
