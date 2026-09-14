# q286 Dominant-Mode Stable-Partition Label-Rule Audit

Status: finite label-rule audit only.  This is not a label-geometry theorem,
stable-core theorem, volatile-rim theorem, pointwise character-sum estimate, or
Goldbach proof.

## Mechanism

The stable-core named holdout kept the frozen partition alive on the named
fixture.  The next theorem handle would be much cleaner if the stable helpful,
stable harmful, or volatile-rim channel classes were explained by simple
representative-label geometry.

This audit tests coordinate equality, coordinate thresholds, parity, small
modular rules, and rectangles in the `(first, second)` representative-label
plane.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_stable_partition_label_rule_audit.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-stable-partition-label-rule-audit.json`
- Source evidence:
  `evidence/q286-first-three-dominant-mode-pairwise-swing-sign-stability.json`

## Results

The audit tested `1056` simple rules.  No tested rule exactly captures any of
the three partition classes:

```text
stable helpful exact matches: 0
stable harmful exact matches: 0
volatile exact matches:       0
```

Best single-rule approximations:

```text
stable helpful:
  rule:      3 <= first <= 4 and 1 <= second <= 11
  kind:      rectangle
  F1:        0.67
  precision: 0.64
  recall:    0.70
  false positives: 4
  false negatives: 3

stable harmful:
  rule:      first % 3 == 2
  kind:      first_mod
  F1:        0.67
  precision: 0.62
  recall:    0.71
  false positives: 3
  false negatives: 2

volatile:
  rule:      1 <= first <= 4 and 3 <= second <= 5
  kind:      rectangle
  F1:        0.71
  precision: 0.83
  recall:    0.62
  false positives: 1
  false negatives: 3
```

## Interpretation

The surviving stable-core / volatile-rim candidate is not explained by these
simple label-geometry rules.  That demotes a clean coordinate, parity,
threshold, or rectangle theorem for the current partition.

The next proof target must use arithmetic action of the channel sums, a richer
structured partition, pressure subregions, or lower-support/complement rescue.
This audit does not refute a more sophisticated label rule; it only closes the
tested simple-rule family.
