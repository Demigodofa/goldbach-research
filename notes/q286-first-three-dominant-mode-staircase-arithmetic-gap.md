# q286 dominant-mode staircase arithmetic gap

Status: finite arithmetic-gap diagnostic.  Goldbach is not proved.

This note measures where the actual strict-central prime-pair rows sit inside
the weak reflected-geometry intervals from the staircase obstruction.

Receipt:
`evidence/q286-first-three-dominant-mode-staircase-arithmetic-gap.json`

## Mechanism Tested

The weak-geometry obstruction gives, for each cumulative staircase stage and
target, an interval:

```text
weak_geometry_min <= stage_sum <= weak_geometry_max
```

over synthetic nonnegative reflected weights with the same local support and
total mass.  This receipt records the actual prime-pair stage sum, its
position in that interval, and the one-sided margin to the rowwise floor.

For pass rows, the missing theorem is a lower bound:

```text
actual_stage_sum >= required_portfolio_for_floor.
```

For deficit rows, the missing theorem is an upper bound or exclusion:

```text
actual_stage_sum < required_portfolio_for_floor.
```

## Measured Shape

On the full eleven-channel stage, all actual selected rows lie inside the weak
geometry interval, but the interval is far too wide to prove anything by
itself.

Actual positions inside the weak interval:

```text
pass rows:    0.2166 .. 0.3528, mean 0.3097
deficit rows: 0.2887 .. 0.4044, mean 0.3167
```

Actual one-sided margins are tiny compared with the missing weak-geometry
margins:

```text
pass margins:    0.0095640903 .. 0.0584289263
deficit margins: 0.0088331796 .. 0.0992285758
```

The weak-geometry missing-margin summary over the same ten rows is:

```text
minimum 3.3131828970
mean    6.3372494788
maximum 9.9717580407
```

The tightest full-stage pass is `13556`, with margin about `0.0095640903`.
The tightest full-stage deficit is `1222142`, with margin about
`0.0088331796`.

Only three selected full-stage rows already have the correct sign under the
uniform action:

```text
40420, 1242118, 1240888
```

## Consequence

The proof target has narrowed again.  It is not enough to show that the
possible geometric interval is small; it is not small.  The needed theorem is
a pointwise arithmetic placement result:

- pass rows require a one-sided lower bound for the actual prime-pair weighted
  stage action;
- deficit rows require a one-sided upper bound, exclusion mechanism, or
  complement/lower-support rescue;
- the margins are small enough that a blunt norm or geometry estimate is
  unlikely to be adequate.

This is finite selected-fixture evidence only.  It is not a pointwise
prime-correlation theorem and not a proof of Goldbach.
