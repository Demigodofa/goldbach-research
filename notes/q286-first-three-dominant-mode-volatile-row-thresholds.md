# q286 Dominant-Mode Volatile Row Thresholds

Status: finite volatile-row threshold diagnostic only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

After the stable core is fixed, each selected row has the exact form:

```text
margin to floor = stable-core margin + volatile-subset sum
```

This receipt enumerates all `256` volatile subsets for each selected row and
records the threshold each subset must cross to match the selected q286
dominant-floor classification.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_row_thresholds.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-row-thresholds.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source channel criticality:
  `evidence/q286-first-three-dominant-mode-volatile-channel-criticality.json`

## Results

The full volatile rim matches every selected row classification.  The hardest
row by satisfying-subset count is `13822`:

```text
target:                         13822
dominant-floor classification:  deficit
stable-core margin:             0.302367068638312
volatile threshold:            -0.302367068638312
full volatile sum:             -0.339111414662605
satisfying volatile subsets:    5 of 256
minimum satisfying subset size: 6
```

The next hardest rows are:

```text
1222142: 32 satisfying subsets, minimum size 4
164598:  46 satisfying subsets, minimum size 3
24424:   143 satisfying subsets, minimum size 0
129706:  191 satisfying subsets, minimum size 0
```

Row `13822` has only two minimum-size satisfying subsets, both of size `6`.
Row `1222142` has ten minimum-size satisfying subsets of size `4`; one of
them clears the deficit by only about `0.0001305906`.

## Interpretation

This turns the volatile-rim problem into explicit rowwise inequalities.  The
finite selected fixture is not governed by one channel or one uniform cap:
some rows need aggregate volatile action from several channels, and the
hardest selected deficit `13822` is especially restrictive.

The remaining theorem must prove these signed row-threshold inequalities from
actual binary-prime residue arithmetic, or replace them with a non-circular
arithmetic-placement theorem.  The receipt is a finite threshold ledger only.
