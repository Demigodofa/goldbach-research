# q286 Dominant-Mode Volatile Octave Rank-5 Autopsy

Status: finite Octave rank-5 mode autopsy only.  This is not a low-rank
theorem, rank-5 theorem, volatile-rim theorem, selected-fixture classifier
theorem, pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The previous Octave SVD rank audit found that rank `4` captures more than
`93%` of the oriented volatile-channel matrix energy, but still leaves five
selected rows failing.  Rank `5` is the first all-pass truncation.

This receipt isolates the fifth SVD component:

```text
C_5 = sigma_5 u_5 v_5^T
```

It compares rank-`4` and rank-`5` reconstructed oriented margins, then
inspects the fifth right singular vector and the rank-`5` stress-row channel
contributions.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_octave_rank5_autopsy.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-octave-rank5-autopsy.json`
- Source rank audit:
  `evidence/q286-first-three-dominant-mode-volatile-octave-svd-rank-audit.json`
- Source polarity-magnitude ledger:
  `evidence/q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json`

## Results

Octave `11.3.0` was used for the SVD component audit.  The fifth mode rescues
exactly the five rows that failed at rank `4`:

```text
13556, 13822, 24424, 164598, 1222142
```

For stress row `1222142`:

```text
rank-4 oriented margin:       -0.0170305252
rank-5 row-sum increment:      0.0226021079
rank-5 oriented margin:        0.0055715827
full oriented margin:          0.0088331796
increment / rank-4 deficit:    1.3271527230
```

The fifth right singular vector is not a clean two-channel adverse-pair mode.
Its largest absolute channel loadings are:

```text
(2,4): 0.6021754535
(4,4): 0.5005636774
(1,7): 0.4774025852
(1,3): 0.2819158795
(1,1): 0.2544685688
```

At `1222142`, the largest rank-`5` component contributions are:

```text
(2,4):  0.0099516990  repair
(4,4):  0.0082724379  adverse
(1,7): -0.0078896720  adverse
(1,3):  0.0046590108  repair
```

The stress-row adverse pair `(1,7),(4,4)` has near-canceling signed rank-`5`
contribution, about `0.0003827659` net, while the repair-side contribution is
about `0.0222193420`.

## Interpretation

The q286 loop is still tightening: rank `5` names the first finite SVD
correction that closes the selected fixture.  But the fifth mode is a mixed
channel balance, not an obvious two-channel theorem.

So Octave is useful here as a diagnostic microscope.  It does not replace the
explicit six-versus-two adverse-absorption obligation for `1222142`.  The live
theorem target remains signed adverse-pair absorption from actual binary-prime
residue weights, or a stronger signed aggregate arithmetic-placement theorem.
