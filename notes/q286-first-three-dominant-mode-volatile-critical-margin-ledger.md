# q286 Dominant-Mode Volatile Critical-Margin Ledger

Status: finite volatile critical-margin ledger only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The polarity-magnitude ledger gives each row's signed magnitude surplus.  This
receipt asks which individual channels exceed that surplus.

A repair channel whose magnitude exceeds the surplus is individually
load-bearing under removal.  An adverse channel whose magnitude exceeds the
surplus is individually intolerable under addition.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_critical_margin_ledger.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-critical-margin-ledger.json`
- Source polarity-magnitude ledger:
  `evidence/q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json`

## Results

Across the selected fixture:

```text
repair channels individually critical:      18 / 39
adverse channels individually intolerable:  19 / 41
```

The tightest row `1222142` is the all-critical stress row:

```text
repair channels individually critical:      6 / 6
adverse channels individually intolerable:  2 / 2
```

For clear row `13556`, one of two repair channels is individually critical,
and all six adverse channels are individually intolerable.

For tight clear row `1242118`, neither repair channel is individually
critical, but four of six adverse channels are individually intolerable.

For clear row `1240888`, there are no repair channels.  One of eight adverse
channels is individually larger than the surplus, but the actual full volatile
package remains clear.

## Interpretation

The loop is still tightening.  The known stress row `1222142` is not a broad
reserve case: every repair channel is load-bearing and both adverse channels
are too large to tolerate individually.

That means the live theorem target cannot be only aggregate sign balance unless
a stronger aggregate theorem replaces the channel ledger.  A channel-level
route must control named critical repair/adverse magnitudes from actual
binary-prime residue weights.
