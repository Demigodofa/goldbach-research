# q286 Dominant-Mode Volatile Adverse-Absorption Ladder

Status: finite volatile adverse-absorption ladder only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The critical-dependency audit showed that `1222142` needs all six repair
channels when both adverse channels are present.  This receipt asks where that
full dependency turns on.

For each selected row, the audit enumerates all adverse-channel subsets,
computes the repair threshold after absorbing that adverse magnitude, then
enumerates the inclusion-minimal repair bundles that beat the threshold.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_adverse_absorption_ladder.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-adverse-absorption-ladder.json`
- Source polarity-magnitude ledger:
  `evidence/q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json`
- Source critical-dependency audit:
  `evidence/q286-first-three-dominant-mode-volatile-critical-dependency-audit.json`

## Results

For the tight stress row `1222142`, the minimum sufficient repair-bundle sizes
form a clean adverse-absorption ladder:

```text
no adverse channels:        4 repair channels suffice
adverse channel (1,7):      5 repair channels suffice
adverse channel (4,4):      5 repair channels suffice
adverse pair (1,7),(4,4):  6 repair channels are required
```

The full six-channel repair bundle is forced exactly at the full adverse-pair
step.  It is not forced by the base margin alone or by either singleton
adverse channel alone.

At the full adverse-pair step, the signed surplus is about `0.0088331796`.
The nearest five-channel repair near miss falls short by about `0.0021056957`.

## Interpretation

This keeps the loop tightening.  The stress row does not collapse to a smaller
repair bundle, but its all-six dependency turns on at a specific place: the
joint absorption of adverse channels `(1,7)` and `(4,4)`.

The next theorem target can therefore be narrower than "control everything":
prove the full adverse-pair absorption step from actual binary-prime residue
weights, or replace this local ladder with a stronger signed aggregate
arithmetic-placement theorem.
