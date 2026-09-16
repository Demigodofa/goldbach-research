# Mobius moment-square degree-5 Q46189 kernel co-occurrence relaxation audit

## Question

Do observed pairwise or three-way distance-bucket co-occurrence
constraints imply the nonadverse off-diagonal bound `> -1`?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_kernel_cooccurrence_relaxation_audit.py
evidence/mobius-moment-square-degree5-q46189-kernel-cooccurrence-relaxation-audit.json
```

## Result

```text
true weakest nonadverse q:           38038
true weakest nonadverse total:       -0.8472931845861708
target lower bound:                  -1.0
box relaxation minimum:              -1.8966400770509377
pair lower relaxation minimum:       -1.2838731540875807
pair lower+upper relaxation minimum: -1.2838731540875807
pair+triple lower minimum:           -1.0464818684588788
pair+triple lower+upper minimum:     -1.0464818684588788
```

## Decision

Low-order bucket co-occurrence is still insufficient.  Pairwise
constraints relax to about `-1.283873`, and pair-plus-triple
constraints still relax to about `-1.046482`, below the required
`-1` boundary.  The true finite rows survive, so the missing
constraint is not just low-order bucket co-occurrence.

The next route must use full packet geometry or a sharper arithmetic
invariant, such as high-prime support, small-prime replacement pair,
or exact source-conductor pair geometry.

This is finite diagnostic evidence only.  It proves no pairwise
co-occurrence bound theorem, triple co-occurrence bound theorem,
full packet geometry theorem, coordinate-00 residue-gap sign theorem,
strict-central Goldbach theorem, or Goldbach proof.
