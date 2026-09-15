# q286 centered (3,1) residue-5 near-collision horizon

Status: finite falsifier of the residue-5 micro-horizon version.  This is not
a selected-stress theorem, signed correlation theorem, pointwise character-sum
theorem, or Goldbach proof.

## Source

The generated receipt is:

```text
evidence/q286-centered-3-1-residue5-near-collision-horizon.json
```

The builder is:

```text
tools/build_q286_centered_3_1_residue5_near_collision_horizon.py
```

## Mechanism

The previous available-population audit found the tightest checked selected
`(3,1)` gate at:

```text
164598 < 8000140
residue mod 143: 5
weighted centered (3,1) gap: 0.0003925287417802202
```

This audit predeclares the one-residue horizon:

```text
8000140 + 286*k,  -50 <= k <= 50
```

Every horizon target has the same residue modulo `143` as reference `164598`.
Therefore the local q286 `(3,1)` value cancels exactly, and any gap is
empirical/correlation-side.

## Result

The finite residue-5 horizon version fails.  Of `101` checked same-residue
horizon targets, `5` fall below reference `164598` in weighted centered
`(3,1)`.

```text
weighted gap summary:
  count 101
  min  -0.0073386462295386805
  mean  0.005106716546893218
  max   0.01699971169803815

empirical gap summary:
  count 101
  min  -0.008503587079606707
  mean  0.005917359617715862
  max   0.019698255540731166

local gap summary:
  count 101
  min  0.0
  mean 0.0
  max  0.0
```

Failing targets:

| target | offset from 8000140 in 286-steps | weighted gap above 164598 |
|---:|---:|---:|
| 7988986 | -39 | -0.007338646230 |
| 8008720 | 30 | -0.003734517079 |
| 7997852 | -8 | -0.003454249419 |
| 8010722 | 37 | -0.001712648752 |
| 8000998 | 3 | -0.000237256454 |

The previous near-collision target `8000140` still passes, but it is not the
local minimum in this residue-5 neighborhood.

## Decision

This clips the selected `(3,1)` stress-reference route.  The available
same-residue population pass remains true for its finite fixture, but it
cannot be promoted to a residue-5 neighborhood theorem.  Any future theorem
must either:

- define a narrower non-post-hoc selected target family that excludes these
  five residue-5 failures for an arithmetic reason; or
- abandon `(3,1)` as a scalar selected-stress theorem and use it only as one
  diagnostic coordinate inside a higher-dimensional signed-correlation model.

## Falsifier Boundary

This falsifies only the finite residue-5 horizon version:

```text
all targets 8000140 + 286*k, -50 <= k <= 50,
lie above reference 164598 in weighted centered (3,1)
```

It does not falsify the already checked fresh-window fixture, the
available-population fixture, or Goldbach.
