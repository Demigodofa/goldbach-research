# q286 Dominant-Mode Volatile Forced-Channel Attribution

Status: finite volatile forced-channel attribution only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The common-core obstruction shows that the hardest selected deficit rows share
only the full eight-channel volatile rim.  This receipt asks whether that full
rim is opaque, or whether its channels can be attributed to smaller hard-row
obligations.

It uses rowwise necessary channels from the satisfying-subset families, then
tests the union of individually forced hard-row channels against the remaining
hard deficit target.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_forced_channel_attribution.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-forced-channel-attribution.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source row thresholds:
  `evidence/q286-first-three-dominant-mode-volatile-row-thresholds.json`
- Source common-core obstruction:
  `evidence/q286-first-three-dominant-mode-volatile-common-core-obstruction.json`

## Results

The hard deficit rows are:

```text
13822, 1222142, 164598
```

Row `13822` individually forces five volatile channels across all of its
satisfying subsets:

```text
(1,1), (1,3), (1,7), (2,4), (3,3)
```

Row `164598` individually forces two different volatile channels:

```text
(1,5), (4,4)
```

The union of those row-forced channels is a seven-channel subset:

```text
(1,1), (1,3), (1,5), (1,7), (2,4), (3,3), (4,4)
```

That seven-channel subset correctly classifies every selected row except
`1222142`.  It still over-rescues `1222142`:

```text
1222142 seven-channel margin to floor:  0.0052135929
```

The remaining volatile channel is:

```text
(4,10)
```

Adding `(4,10)` changes `1222142` to the correct deficit side:

```text
1222142 full-rim margin to floor:      -0.0088331796
(4,10) contribution at 1222142:        -0.0140467724
```

The same hinge also pushes the other two hard rows farther into the correct
deficit side, but it is not individually necessary for their rowwise
satisfying-subset families:

```text
13822 full-rim margin to floor:        -0.0367443460
164598 full-rim margin to floor:       -0.0191517925
```

## Interpretation

The full volatile rim is not just an opaque eight-channel object on this
fixture.  It decomposes into:

```text
five-channel 13822 obligation
two-channel 164598 obligation
(4,10) combination hinge for 1222142
```

This gives a sharper non-circular target than the previous common-core
obstruction.  A proof route can now try to explain these three obligations
from actual binary-prime residue arithmetic, or replace the decomposition
with an aggregate arithmetic-placement theorem.

The receipt is finite attribution evidence only.  It does not prove the
volatile-rim theorem or Goldbach.
