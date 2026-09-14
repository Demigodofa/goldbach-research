# q286 Dominant-Mode Rank-5 Template Near-Boundary Falsifier

Status: finite rank-`5` template falsifier only.  This refutes one simple
checked selector on the named rows; it is not a selector theorem, rank-`5`
theorem, pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The Octave rank-`5` autopsy showed that the fifth SVD mode rescues exactly the
five selected rows that failed at rank `4`.  This receipt asks whether the
fixed rank-`5` volatile-channel template can be reused as a simple selector
for nearby tight q286 rows.

The test takes the `20` closest rows from the near-boundary selector audit,
recomputes their exact signed q286 channel profile, extracts the eight
volatile channels, orients each row by its actual finite dominant-floor
classification, and uses Octave to project each row onto the fixed rank-`5`
right singular vector.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_rank5_template_near_boundary_falsifier.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-rank5-template-near-boundary-falsifier.json`
- Source near-boundary audit:
  `evidence/q286-first-three-dominant-mode-near-boundary-selector-audit.json`
- Source rank-`5` autopsy:
  `evidence/q286-first-three-dominant-mode-volatile-octave-rank5-autopsy.json`

## Results

The top-`20` closest rows contain one dominant-floor deficit, `1222142`, and
nineteen clears.  The fixed rank-`5` template does not separate them:

```text
positive template increment rows:     10
nonpositive template increment rows:  10
positive-increment clear rows:         9
nonpositive-increment clear rows:     10
```

The two tightest rows already falsify the simple sign selector:

```text
1222142   deficit   abs surplus 0.0028592222   rank-5 increment  0.0226021079
1242118   clear     abs surplus 0.0047979813   rank-5 increment -0.0276644469
```

Every checked near-boundary band through `.05` has mixed rank-`5` increment
signs.  The sign that selects the deficit also selects nearby clear rows.

The Octave Pearson checks are likewise not a proof route:

```text
signed surplus vs increment:       -0.1104116522
absolute surplus vs abs increment: -0.6279456651
signed surplus vs cosine:           0.0761898051
absolute surplus vs abs cosine:    -0.2798482620
```

## Interpretation

This closes the fixed rank-`5` template as a simple near-boundary selector on
the checked fixture.  Rank `5` remains a useful diagnostic of the selected
matrix, but the reusable theorem target is still not "follow the fifth SVD
mode."

The live route remains signed adverse-pair absorption from actual binary-prime
residue weights, or a stronger signed aggregate arithmetic-placement theorem.
