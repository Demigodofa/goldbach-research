# q286 Dominant-Mode Volatile Subset Ablation

Status: finite volatile-subset ablation only.  This is not a volatile-rim
theorem, stable-core theorem, selected-fixture classifier theorem, pointwise
character-sum estimate, or Goldbach proof.

## Mechanism

The selected-classification receipt showed that the frozen `17`-channel
stable core preserves every selected clear, but over-rescues three selected
deficits:

```text
13822, 164598, 1222142
```

This diagnostic fixes the stable core and searches every subset of the `8`
volatile q286 channels.  For each subset it asks whether

```text
stable core + volatile subset
```

matches the selected q286 dominant-floor classification on all ten selected
rows.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_subset_ablation.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source partition:
  `evidence/q286-first-three-dominant-mode-pairwise-swing-sign-stability.json`
- Source selected-classification receipt:
  `evidence/q286-first-three-dominant-mode-stable-core-selected-classification.json`

## Results

All `256` volatile subsets were tested.  Exactly one subset gives exact
selected-fixture classification:

```text
exact subsets:                 1
minimum exact subset size:     8
proper exact subset exists:    false
clear-preserving subsets:      171
maximum reconstruction error:  below 8e-15
```

The only exact subset is the full volatile rim:

```text
(1,1), (1,3), (1,5), (1,7),
(2,4), (3,3), (4,4), (4,10)
```

The closest proper subsets still fail.  The best seven-channel subsets
preserve every selected clear but leave one selected deficit over-rescued:
one leaves `1222142` over-rescued, and another leaves `13822` over-rescued.

## Interpretation

On this selected fixture, the volatile-rim restoration job is not compressible
by arbitrary subset deletion.  This does not prove the full volatile rim is
universally necessary, and it does not prove any volatile-rim theorem.  It
does mean the current finite theorem target should treat the full volatile
package as live unless a new arithmetic structure replaces it.

The remaining proof obligation is still non-circular: explain why the stable
core preserves true clear rows and why the volatile/exclusion component blocks
stable-core false positives, or replace this partition with a stronger
pointwise arithmetic-placement theorem.
