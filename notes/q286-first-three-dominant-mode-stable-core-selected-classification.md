# q286 Dominant-Mode Stable-Core Selected Classification

Status: finite selected-fixture classification diagnostic only.  This is not
a stable-core theorem, volatile-rim theorem, coupled budget theorem, pointwise
character-sum estimate, or Goldbach proof.

## Mechanism

The stable-core holdout measured the frozen stable/volatile partition
relative to the late tail `1222142`.  This diagnostic applies the same
partition absolutely to the older selected deficit/clear fixture:

```text
24424, 13556, 13822, 40420, 55864,
164598, 129706, 1222142, 1242118, 1240888
```

The `17` stable channels are the `10` stable-positive plus `7`
stable-negative labels from the pairwise sign-stability receipt.  The
remaining `8` sign-flip labels form the volatile rim.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_stable_core_selected_classification.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-stable-core-selected-classification.json`
- Source partition:
  `evidence/q286-first-three-dominant-mode-pairwise-swing-sign-stability.json`

## Results

The stable core preserves every selected clear row:

```text
stable-core missed clears: 0
selected clear rows:       13556, 40420, 129706, 1242118, 1240888
```

Stable core alone is not a selected-fixture classifier.  It over-rescues
three selected q286 deficit rows:

```text
stable-core false positives: 13822, 164598, 1222142
stable-core false negatives: 0
```

Restoring the volatile rim restores exactly those stable-core false positives:

```text
volatile-restored false positives: 13822, 164598, 1222142
maximum reconstruction error:      below 8e-15
```

The volatile rim is signed and row-dependent.  It is harmful on four selected
clears, helpful on one selected clear, harmful on four selected deficits, and
helpful on one selected deficit.

## Interpretation

This result keeps a clear-side stable-core lower-bound target alive on the
selected fixture, but it demotes stable core as a standalone classifier.
The volatile rim cannot be discarded as noise: on these rows it carries the
classification/exclusion work needed to keep stable-core over-rescued deficits
below the q286 dominant floor.

A proof still needs a non-circular arithmetic theorem explaining stable-core
clear preservation and volatile/exclusion restoration, or a stronger
arithmetic-placement theorem that replaces this finite partition entirely.
