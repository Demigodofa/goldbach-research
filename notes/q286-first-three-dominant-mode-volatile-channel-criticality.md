# q286 Dominant-Mode Volatile Channel Criticality

Status: finite leave-one-out volatile-channel criticality diagnostic only.
This is not a volatile-rim theorem, stable-core theorem, selected-fixture
classifier theorem, pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The volatile-subset ablation showed that only the full eight-channel volatile
rim matches the selected ten-row q286 classification.  This derivative
receipt removes each volatile channel one at a time and records which selected
rows change classification.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_channel_criticality.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-channel-criticality.json`
- Source ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`

## Results

Every volatile channel is leave-one-out critical on the selected fixture:

```text
volatile channels:                 8
exact leave-one-out deletions:      0
total leave-one-out changed rows:   18
targets hit by any deletion error:  13556, 13822, 24424, 40420, 164598, 1222142
```

Two channels have mixed clear-support and deficit-blocking roles:

```text
(1,1), (1,5)
```

Deleting `(1,1)` creates false positives at `13822`, `24424`, and `1222142`,
but also creates a false negative at clear row `40420`.  Deleting `(1,5)`
creates false positives at `164598` and `1222142`, but also creates a false
negative at clear row `13556`.

The other six channels are pure deficit blockers under leave-one-out deletion
on this selected fixture:

```text
(1,3), (1,7), (2,4), (3,3), (4,4), (4,10)
```

The smallest witness deletions are:

```text
delete (1,7)  -> false positive at 13822
delete (4,10) -> false positive at 1222142
```

## Interpretation

This strengthens the finite reason not to discard the volatile rim.  The
volatile package is not just a uniform negative cap: two channels also support
selected clear rows, while six act as deficit blockers on this fixture.

The remaining proof obligation is row-specific and signed.  A future theorem
must explain why these volatile channels block stable-core false positives
without breaking true clears, or replace the entire stable/volatile split with
a stronger arithmetic-placement theorem.
