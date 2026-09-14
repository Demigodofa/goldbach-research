# q286 Dominant-Mode Volatile Polarity-Magnitude Ledger

Status: finite volatile polarity-magnitude ledger only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The sign-polarity profile explains boundary directions by channel signs.  This
receipt converts that into the exact magnitude inequality a theorem would need.

For a deficit row, the negative volatile magnitude must beat the base margin
plus positive volatile pressure:

```text
-negative_sum > base_margin + positive_sum
```

For a clear row, the positive volatile magnitude must beat the remaining
negative drag after the base margin is included:

```text
positive_sum > -base_margin - negative_sum
```

Rows with no positive-channel requirement can clear from base margin alone.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_polarity_magnitude_ledger.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source sign-polarity profile:
  `evidence/q286-first-three-dominant-mode-volatile-sign-polarity-profile.json`

## Results

The tightest selected row is the known tail row `1222142`.  Its signed
magnitude surplus is about:

```text
0.0088331796
```

Its repair-to-required ratio is about:

```text
1.112961
```

The next tightest row is clear row `13556`, with surplus about `0.0095640903`
and repair-to-required ratio about `1.179968`.

The tight tail `1222142` and tight clear `1242118` share the same positive
volatile pair:

```text
(1,7)
(4,4)
```

For `1222142`, that pair is adverse.  For `1242118`, it is repairing.
However, `1242118` is not the tightest magnitude row: its repair-to-required
ratio is about `2.352211`.

Clear row `1240888` has no positive volatile channel.  It remains clear
because its base margin already absorbs all negative volatile drag.

## Interpretation

The q286 hole is now a quantitative signed-margin problem on this fixture.
The symmetry did not vanish: it moved from boundary polarity to exact
repair-versus-adverse magnitude inequalities.

The remaining theorem is to prove these signed volatile magnitude inequalities
from actual binary-prime residue weights uniformly, or replace them with a
full signed aggregate arithmetic-placement theorem.
