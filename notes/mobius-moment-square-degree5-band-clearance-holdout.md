# Mobius moment-square degree-5 band clearance holdout

## Question

The moving-prime band audit found the weakest checked source-start prime block
in each sigma band.  Does the denominator clearance-family mechanism survive
on those four weakest blocks, or is the positive moving-prime margin hiding a
near-threshold adverse denominator leak?

## Mechanism

Read the moving-prime band audit, take the `weakest_block` from each sigma
band, and recompute the exact reduced-denominator clearance-family ledger for
that block:

```text
tools/build_mobius_moment_square_degree5_band_clearance_holdout.py
evidence/mobius-moment-square-degree5-band-clearance-holdout.json
```

The tested candidate is:

```text
middle/far positive denominator margin > near-threshold adverse leakage
```

on each band-minimum block.

## Result

```text
bands checked:                                      4
all middle/far positive dominates near leakage:     true
all middle/far net dominates near leakage:          true
all negative denominators near threshold:           false
negative denominator family counts:
  near_1_to_2:                                      17
  middle_2_to_3:                                     1
  far_3_plus:                                        0
max near negative / middle-far positive:             0.0016400172796714467
```

Per band:

```text
sigma_1_00_1_25  M=229  p=283  ratio=0.0016400172796714467  all-negative-near=true
sigma_1_25_1_50  M=331  p=479  ratio=0.0009221371754277364  all-negative-near=true
sigma_1_50_1_75  M=229  p=379  ratio=0.0006756636813775213  all-negative-near=false
sigma_1_75_2_00  M=331  p=599  ratio=0.0009319007678001933  all-negative-near=true
```

The failed stronger statement is localized: the only non-near negative
denominator family appears in `sigma_1_50_1_75`, at `M=229`, `p=379`, in the
`middle_2_to_3` family.

## Decision

The clearance-family target survives all four sigma-band minimum blocks.  The
next theorem-shaped target can pair sigma-banded moving prime-block lower-frame
control with sigma-banded clearance-family denominator control.

The stronger shortcut "all adverse denominators are near threshold" is false
on this holdout and should not be used as a theorem target without a changed
definition.

This is finite holdout evidence only.  It proves no source-start theorem,
prime-block theorem, moving-prime theorem, sigma-band theorem,
clearance-family theorem, strict-central Goldbach theorem, or Goldbach proof.
