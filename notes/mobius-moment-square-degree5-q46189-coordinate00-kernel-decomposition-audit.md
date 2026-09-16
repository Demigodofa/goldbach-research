# Mobius moment-square degree-5 Q46189 coordinate-00 kernel decomposition audit

## Question

Can the coordinate-00 half-margin for `Q=46189` and the weakest
replacement row be decomposed into finite Dirichlet-kernel
autocorrelation terms that identify the sign-deciding residue-gap
structure?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_coordinate00_kernel_decomposition_audit.py
evidence/mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.json
```

## Result

```text
Q=46189 half-margin:          -112967899058.92188
Q=46189 diagonal half:        20990238237161.72
Q=46189 off-diagonal total:   -21103206136220.65
weakest replacement q:        38038
weakest replacement margin:   4380137469743.5
weakest replacement diagonal: 28683313563140.617
weakest replacement offdiag:  -24303176093397.117
```

## Decision

The one-coordinate obstruction has a concrete finite kernel shape:
diagonal half-energy competes with off-diagonal Dirichlet-kernel
residue-gap mass.  `Q=46189` is negative because the off-diagonal
total slightly overcomes the diagonal half; the weakest replacement
remains positive because the off-diagonal total does not erase the
diagonal half.

This is finite diagnostic evidence only.  It proves no coordinate-00
residue-gap sign theorem, symbolic coordinate-00 energy ratio theorem,
one-coordinate active/full ratio theorem, replacement-family payment
theorem, strict-central Goldbach theorem, or Goldbach proof.
