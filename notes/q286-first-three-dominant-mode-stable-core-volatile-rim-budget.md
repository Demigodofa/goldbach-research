# q286 Dominant-Mode Stable-Core / Volatile-Rim Budget

Status: finite derivative budget diagnostic only.  This is not a stable-core
theorem, volatile-rim theorem, coupled pressure/offset curve theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The pairwise swing sign-stability diagnostic demoted a single fixed
helpful/harmful partition, but it left a narrower structure: a stable helpful
core, a stable harmful core, and an eight-channel volatile rim.  This
diagnostic asks whether the stable core alone clears the tail row and how much
negative volatile-rim swing can be tolerated.

The branch-independent floor margin is:

```text
dominant_sum + 0.3
```

not `positive_offset_slack_to_floor`, because offset slack changes meaning in
the pressure branch.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_stable_core_volatile_rim_budget.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-stable-core-volatile-rim-budget.json`
- Source evidence:
  `evidence/q286-first-three-dominant-mode-pairwise-channel-swing.json`
  and
  `evidence/q286-first-three-dominant-mode-pairwise-swing-sign-stability.json`

## Results

For `1222142 -> 1242118`:

```text
tail floor margin:          -0.008833179560527815
stable-core net swing:       0.0398241886398476
stable-core margin:          0.030991009079319787
volatile-rim net swing:     -0.014462095612572855
volatile drag budget:        0.030991009079319787
budget used:                 0.46665455698967123
final floor margin:          0.016528913466746932
reconstruction error:        below 9e-16
```

For `1222142 -> 1240888`:

```text
tail floor margin:          -0.008833179560527815
stable-core net swing:       0.11560757441857683
stable-core margin:          0.10677439485804902
volatile-rim net swing:     -0.0795878214771284
volatile drag budget:        0.10677439485804902
budget used:                 0.7453830254241782
final floor margin:          0.02718657338092062
reconstruction error:        below 3e-15
```

## Interpretation

On both named comparisons, the stable core alone would lift tail `1222142`
above the `-0.3` floor.  The volatile rim is net harmful in both comparisons,
but remains inside the finite named budget.

This does not prove a stable-core theorem or a volatile-rim bound.  It does
turn the next candidate into a sharper two-part obligation: prove positive
stable-core surplus and prove that volatile-rim drag stays below the displayed
kind of budget, or find a counterexample where one of those two parts fails.
