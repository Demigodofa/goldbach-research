# q286 complement-rescue threshold candidate audit

Status: finite derived threshold-candidate audit.  This is not a threshold
theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach proof.

Receipt:

```text
tools/build_q286_complement_rescue_threshold_candidate_audit.py
evidence/q286-complement-rescue-threshold-candidate-audit.json
```

## Question

The complement-rescue schedule showed that post-discovery q286 tail rows are
rescued by the complement.  This derived receipt asks which threshold
statements are actually supported by that checked schedule and which attractive
shortcuts are tautological or already falsified.

## Result

The smallest supported suffix threshold in the current finite schedule is:

```text
block_index_after_discovery >= 1
```

For that post-discovery suffix:

```text
first_three_tail rows:                 1671
active_selector rows:                  1671
first_three_tail failures:                0
predicate full_nonpositive rows:          0
minimum rescue margin:       0.012576466293799509
minimum complement/required: 1.0214926472076773
```

The tightest post-discovery row remains target `94856`:

```text
first_three ratio:        -0.5851520369862627
complement ratio:          0.5977285032800622
rescue margin:             0.012576466293799509
complement/required:       1.0214926472076773
```

The all-block rescue claim is falsified by the discovery block:

```text
first_three_tail failures over all checked blocks: 86
discovery predicate full_nonpositive rows:         89
worst discovery rescue margin:     -0.8769412734408442
```

The tempting within-block shortcut `cycle >= 4` is also falsified.  Discovery
cycles `4..6` pass, but discovery cycle `7` has `2` full-nonpositive rows, so
late-cycle position alone is not the mechanism.

Finally, the condition

```text
complement_to_required_ratio > 1
```

is flagged as a tautology for first-three-tail rows: it exactly restates
positive rescue and is not an independent explanation.

## Interpretation

The current finite separator is a growth/phase boundary: after the discovery
block, the checked q286 tail rows persist but are all rescued by complement
surplus.  That is useful theorem-shaping evidence, but it is not a theorem
because the separator was derived from the same schedule.

The next honest falsifier is to freeze `block_index_after_discovery >= 1` before
testing additional q286 blocks beyond start `410400`.  Any future
first-three-tail or active-selector row in that frozen horizon with
`full_action_to_principal_ratio <= 0` falsifies the generalizing threshold
candidate.

The real proof obligation is still to replace the empirical suffix with a
non-circular arithmetic or signed-correlation condition that implies:

```text
complement_to_principal_ratio
  > -first_three_modes_to_principal_ratio
```

on the intended q286 class.
