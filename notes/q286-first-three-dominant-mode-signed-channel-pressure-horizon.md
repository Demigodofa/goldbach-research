# q286 dominant-mode signed-channel pressure horizon

Status: finite deterministic pressure-horizon scout only.  This is not a
pressure-branch theorem, not a pointwise character-sum estimate, not a
signed-projection theorem, and not a Goldbach proof.

## Mechanism

The previous branch holdout found that all targets in the `1243000` window
cleared both exact branches of the dominant two-mode floor:

```text
negative_pressure <= 0.3
or
positive_offset >= negative_pressure - 0.3
```

This follow-up asks whether the direct pressure branch itself keeps clearing
the next sparse deterministic post-stress windows.  The falsifier is any
checked row with `negative_pressure > 0.3`, or any unresolved dominant-floor
deficit.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_signed_channel_pressure_horizon.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-signed-channel-pressure-horizon.json`
- Source receipt:
  `q286_first_three_dominant_mode_signed_channel_branch_holdout_receipt`

## Checked Windows

```text
(1244000, 51)
(1245000, 51)
(1246000, 51)
```

Counts:

```text
tested targets with prime pairs: 153
dominant floor passes:           153
dominant floor failures:           0
pressure branch only:              0
offset branch only:                0
pressure and offset branches:    153
unresolved deficits:               0
```

Every checked target clears the direct pressure branch.  The maximum
negative pressure row is target `1244072`, with negative pressure about
`0.2349931112`, still below the `0.3` threshold.  The tightest positive
offset slack row is target `1244094`, with slack about `0.0341459076`.

## Interpretation

This strengthens the finite post-`1243000` branch posture: the sampled rows
are not merely rescued by positive offset; their negative dominant-channel
pressure is already below the threshold.

It still proves no eventual theorem.  The missing input is an arithmetic bound
on negative dominant-channel pressure in the actual binary-prime q286 channel
distribution, or a finite classification/rescue of any future pressure
failures.
