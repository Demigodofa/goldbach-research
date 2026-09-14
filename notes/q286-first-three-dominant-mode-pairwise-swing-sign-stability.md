# q286 Dominant-Mode Pairwise Swing Sign Stability

Status: finite derivative sign-stability diagnostic only.  This is not a
stable partition theorem, stable-core theorem, coupled pressure/offset curve
theorem, pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The pairwise channel-swing diagnostic showed that the named tail-to-clear
rescues are broad multi-channel balances.  This follow-up asks whether that
broad swing at least has a fixed helpful/harmful channel partition across the
two named clear comparisons:

```text
1222142 -> 1242118
1222142 -> 1240888
```

If every channel kept the same swing sign across both comparisons, the proof
target could narrow toward a fixed aggregate helpful-core theorem.  If signs
flip, a single fixed helpful/harmful channel partition is too narrow.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pairwise_swing_sign_stability.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pairwise-swing-sign-stability.json`
- Source evidence:
  `evidence/q286-first-three-dominant-mode-pairwise-channel-swing.json`

## Results

Across the `25` active real q286 channels:

```text
stable helpful channels: 10
stable harmful channels:  7
stable nonzero channels: 17
sign-flip channels:       8
zero channels:            0
```

The sign-flip labels are:

```text
(1,1), (1,3), (1,5), (1,7), (2,4), (3,3), (4,4), (4,10)
```

The stable helpful core contributes about `0.1946009263` to the
`1222142 -> 1242118` swing and about `0.1913315978` to the
`1222142 -> 1240888` swing.  The sign-flip set is net harmful in both pairs:
about `-0.0144620956` in the first pair and about `-0.0795878215` in the
second.

## Interpretation

This falsifies a single fixed helpful/harmful channel partition on the named
fixture.  The two rescues share a stable helpful core, but the volatile
eight-channel rim changes sign and materially changes the second comparison.

The live route is therefore narrower than arbitrary 25-channel control but
not as simple as a fixed partition.  A future candidate would need a stable
core plus volatile-rim theorem, a pressure-subregion split, or a
lower-support/complement rescue.  This diagnostic is finite and derivative;
it proves none of those uniform statements.
