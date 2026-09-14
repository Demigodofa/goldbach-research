# q286 Dominant-Mode Adverse-Pair Near-Boundary Falsifier

Status: finite adverse-pair selector falsifier only.  This refutes the named
pair sign as a simple checked selector on the top-`20` near-boundary rows; it
is not an adverse-pair theorem, volatile-rim theorem, pointwise character-sum
estimate, or Goldbach proof.

## Mechanism

The live stress-row target has narrowed to the six-versus-two absorption
balance around the named pair `(1,7),(4,4)`.  This receipt tests the tempting
shortcut that the named pair's sign or magnitude alone selects the tight
near-boundary deficit.

It reuses the exact top-`20` signed q286 channel rows from the rank-`5`
template falsifier, sums the named pair `(1,7),(4,4)`, compares it with the
six-channel volatile complement, and audits whether pair sign isolates
`1222142`.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_adverse_pair_near_boundary_falsifier.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-adverse-pair-near-boundary-falsifier.json`
- Source:
  `evidence/q286-first-three-dominant-mode-rank5-template-near-boundary-falsifier.json`

## Results

The top-`20` closest near-boundary rows contain one dominant-floor deficit,
`1222142`, and nineteen clears.  Positive named-pair sum does not isolate the
deficit:

```text
positive (1,7),(4,4) pair rows:        7
positive-pair clear false positives:   6
negative-or-zero-pair clear rows:      13
```

The positive-pair targets are:

```text
1222142, 1242118, 1222048, 1220056, 1200208, 1222018, 1200362
```

The two tightest rows already refute the pair-sign shortcut:

```text
1222142   deficit   pair sum 0.0216228924
1242118   clear     pair sum 0.0287525311
```

Every checked near-boundary band through `.05` contains at least one clear row
with positive named-pair sum.

## Interpretation

The pair remains central to the stress-row absorption balance, but pair sign
alone is not the theorem.  The live target remains the coupled balance between
the named pair and the six-channel repair complement from actual binary-prime
residue weights, or a stronger signed aggregate arithmetic-placement theorem.
