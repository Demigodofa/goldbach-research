# q286 dominant-mode staircase geometry obstruction

Status: finite proof-strategy obstruction.  Goldbach is not proved.

This note tests whether the residual staircase can be proved from weak
geometry alone after the prefix/tail order is frozen.

Receipt:
`evidence/q286-first-three-dominant-mode-staircase-geometry-obstruction.json`

## Mechanism Tested

For each selected target and each cumulative staircase stage, the receipt
minimizes and maximizes the stage action over synthetic weights satisfying:

- nonnegative local admissible q286 support;
- total mass one;
- ordered-pair reflection symmetry `w(r)=w(N-r)`.

The rowwise floor is still the actual staircase requirement:

```text
stage_sum >= required_portfolio_for_floor.
```

If a selected pass row can be made to fail under these constraints, or a
selected deficit row can be made to pass, then the classification is not forced
by this weak geometry.

## Measured Obstruction

On the full selected fixture, weak geometry forces none of the ten selected
full-stage classifications:

```text
full_stage_any_classification_forced_by_geometry = false
```

Every selected pass row is breakable by weak reflected geometry:

```text
13556, 40420, 129706, 1242118, 1240888
```

Every selected deficit row is also breakable in the opposite direction:

```text
24424, 13822, 55864, 164598, 1222142
```

This holds throughout the nonempty staircase stages.  From `prefix_1` through
the full `prefix_plus_tail_7` stage, all five selected pass classifications
and all five selected fail classifications remain breakable by weak geometry.

The four-channel prefix is also not forced as a clear-side theorem by these
constraints:

```text
prefix_stage_all_clear_passes_forced_by_geometry = false
```

## Consequence

The residual staircase cannot be promoted using only support, nonnegativity,
total mass, and pair-swap reflection.  The surviving theorem must use actual
binary-prime arithmetic, a stronger residue-weight structural constraint,
complement/lower-support rescue, or an external fixed-modulus pointwise
prime-pair theorem.

The synthetic witnesses are not prime-pair weights and are not Goldbach
counterexamples.  They only close the weak-geometry proof shortcut for the
frozen q286 staircase.
