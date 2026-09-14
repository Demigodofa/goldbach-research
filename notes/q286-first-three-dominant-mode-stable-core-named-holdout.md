# q286 Dominant-Mode Stable-Core Named Holdout

Status: finite named-row holdout diagnostic only.  This is not a stable-core
theorem, volatile-rim theorem, coupled pressure/offset curve theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The stable-core / volatile-rim budget survived the two near-boundary clear
comparisons.  This holdout freezes the derived partition:

- stable helpful channels from the pairwise sign-stability receipt;
- stable harmful channels from the same receipt;
- volatile-rim sign-flip channels from the same receipt.

It then applies that partition to every clear row in the broader named
pressure fixture, always using tail `1222142` as the reference.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_stable_core_named_holdout.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-stable-core-named-holdout.json`
- Source partition:
  `evidence/q286-first-three-dominant-mode-pairwise-swing-sign-stability.json`
- Reference tail:
  `1222142`
- Holdout clear rows:
  `1242118`, `1240888`, `1243018`, `1243130`, `1244072`, `1244094`

## Results

All `6` named clear rows satisfy the frozen stable-core / volatile-rim budget:

```text
holdout rows:       6
failure rows:       0
max reconstruction error: below 3e-15
```

The tightest stable-core margin row remains `1242118`:

```text
stable-core margin: 0.0309910090793198
volatile-rim swing: -0.0144620956125729
budget used:        0.466654556989671
```

The largest volatile-drag budget use remains `1240888`:

```text
stable-core margin: 0.106774394858049
volatile-rim swing: -0.0795878214771284
budget used:        0.745383025424178
```

On the four post-stress clear rows `1243018`, `1243130`, `1244072`, and
`1244094`, the volatile rim is net positive rather than a drag.

## Interpretation

This holdout does not prove the stable-core theorem.  It does strengthen the
candidate target: on this named fixture, the frozen stable core clears the
tail for all named clear rows and the volatile rim never exceeds the
available budget.  A proof still needs arithmetic estimates forcing stable
core surplus and bounding volatile-rim drag outside this finite fixture, or a
new falsifying row where one of those two conditions fails.
