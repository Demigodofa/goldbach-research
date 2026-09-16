# Mobius positive-range lower-frame and axial-compression falsifier

## Question

After the post-q286 Mobius frontier reconciliation, can the six-coordinate
active/full lower-frame target be reduced to either of these simpler
certificates?

```text
full-positive-definite whitened Gershgorin
axial Schur-response compression
```

Or does the theorem target need to be rank-aware on the positive range of the
full Gram matrix?

## Receipt

```text
tools/build_mobius_positive_range_lower_frame_axial_falsifier.py
evidence/mobius-positive-range-lower-frame-axial-falsifier.json
```

## Result

The checked nonvacuous positive-range active/full comparisons all stay above
the one-half target:

```text
M=127  rank=6  lambda_min=0.8768802946823542
M=149  rank=6  lambda_min=0.9344345921816697
M=167  rank=5  lambda_min=0.8511480691308368
M=191  rank=6  lambda_min=0.9726898127803637
```

The small pre-support scales `M=83` and `M=101` have full denominator rank
zero for this lifted comparison, so they do not provide a nonvacuous
six-coordinate lower-frame test.

The stronger full-positive-definite whitening condition is too strong as a
frontier statement.  It fails at:

```text
M=83   full matrix must have a positive diagonal
M=101  full matrix must have a positive diagonal
M=167  full matrix must be positive definite
```

The `M=167` failure is especially useful: the full Gram has rank `5`, nullity
`1`, and no positive active direction in the full nullspace.  The positive
range still has lower-frame minimum `0.8511480691308368`.  This changes the
theorem shape from full-PD whitening to positive-range lower frame plus
nullspace control.

## Axial Compression

The axial moment-curve geometry remains real, but it is not a standalone
certificate.  The criterion

```text
nonaxial energy error < Schur margin
```

already fails on checked scales:

```text
M=149  nonaxial_error / schur_margin = 2.984294948930046
M=167  nonaxial_error / schur_margin = 15.791616087433386
M=191  nonaxial_error / schur_margin = 3.1008805418566903
```

This happens while the moment-curve projective fit remains small:

```text
M=149  distance = 0.000026137647432121346
M=167  distance = 0.000035175761283063655
M=191  distance = 0.00010322096105434436
```

So the visual/axial pattern is useful coordinate structure, not enough proof
engine by itself.

## Decision

The active theorem target becomes:

```text
rank-aware positive-range active/full lower-frame theorem
plus nullspace control
```

The axial Schur-response and moment-curve alignment stay in the toolbox as
coordinate heuristics.  They are moved out of the acceptance condition unless
a new estimate controls the nonaxial energy directly.

This is finite diagnostic evidence only.  No uniform active/full lower-frame
theorem, Mobius covariance theorem, signed prime-correlation estimate, q286
theorem, strict-central Goldbach theorem, or Goldbach proof is established.
