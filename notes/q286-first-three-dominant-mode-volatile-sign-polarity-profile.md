# q286 Dominant-Mode Volatile Sign-Polarity Profile

Status: finite volatile sign-polarity diagnostic only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The boundary-cut graph records which one-channel additions cross between
correct and incorrect selected-row classifications.  This receipt checks
whether those crossing directions are exactly explained by the signs of the
eight volatile channel contributions.

For a deficit row, a positive volatile contribution is adverse because it
raises the margin toward the wrong side of the floor.  A negative contribution
is repairing.  For a clear row, the interpretation reverses: a positive
contribution repairs, and a negative contribution is adverse.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_sign_polarity_profile.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-sign-polarity-profile.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source boundary-cut graph:
  `evidence/q286-first-three-dominant-mode-volatile-boundary-cut-graph.json`

## Results

Every boundary-crossing direction matches the sign-predicted direction of its
volatile channel contribution on the selected fixture.  There are no sign
direction violations.

The tight tail row `1222142` and tight clear row `1242118` share the same
positive volatile pair:

```text
(1,7)
(4,4)
```

For `1222142`, that pair is adverse: it is exactly the pair of
correct-to-wrong boundary channels.  The complementary six volatile channels
are sign-expected repairs.

For `1242118`, the same positive pair is repairing because the row is a clear
row.  Its negative volatile channels are adverse.

Clear row `1240888` is different again: all eight volatile channel
contributions are negative, but it is boundary-free because every one of the
`256` volatile subsets still classifies it correctly.

## Interpretation

The symmetry is real in the finite q286 fixture.  It is not merely a local
clause artifact: the tight tail `1222142` and tight clear `1242118` share the
same positive volatile pair, and the expected row classification determines
whether that pair acts as adverse pressure or repair.

This compresses the Boolean boundary-cut target to signed channel polarity
plus margin magnitude on this fixture.  A proof still needs a uniform theorem
for the actual binary-prime residue weights, or a replacement signed aggregate
arithmetic-placement theorem.
