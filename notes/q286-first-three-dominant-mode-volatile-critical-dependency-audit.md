# q286 Dominant-Mode Volatile Critical-Dependency Audit

Status: finite volatile critical-dependency audit only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The critical-margin ledger says which individual channels are load-bearing.
This receipt asks whether the signed magnitude inequality itself compresses.

For each selected row, the audit enumerates all subsets of the sign-expected
repair channels and keeps the inclusion-minimal subsets whose total magnitude
beats the row's required repair magnitude.  It also enumerates the
inclusion-minimal adverse subsets whose total magnitude exceeds the row's
signed surplus.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_critical_dependency_audit.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-critical-dependency-audit.json`
- Source polarity-magnitude ledger:
  `evidence/q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json`
- Source critical-margin ledger:
  `evidence/q286-first-three-dominant-mode-volatile-critical-margin-ledger.json`

## Results

The tight stress row `1222142` does not compress at the repair-bundle level.
It has exactly one minimal sufficient repair bundle, and that bundle is the
full six-channel repair set:

```text
(1,1), (1,3), (1,5), (2,4), (3,3), (4,10)
```

The same row has exactly two minimal intolerable adverse bundles, both
singletons:

```text
(1,7)
(4,4)
```

Thus either adverse channel alone can erase the small signed surplus, while no
proper subset of the six repair channels is sufficient in the current signed
magnitude abstraction.

## Interpretation

The loop is tightening, but not by collapsing `1222142` to a smaller repair
dependency.  The finite hole is now a six-versus-two critical-channel balance:
all six repair channels are jointly necessary, and either of the two adverse
channels is individually too large to tolerate.

That closes the attractive lower-dimensional repair-compression route for the
current fixture.  The remaining theorem must control this full critical
bundle from actual binary-prime residue weights, or replace the local bundle
ledger with a stronger signed aggregate arithmetic-placement theorem.
