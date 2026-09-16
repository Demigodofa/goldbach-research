# Mobius moment-square degree-5 Q46189 source-block sign audit

## Question

Across all `34` Q46189 replacement rows, can input-side source-block
topology predict the sign of the first off-diagonal non-middle
interaction?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_source_block_sign_audit.py
evidence/mobius-moment-square-degree5-q46189-source-block-sign-audit.json
```

## Result

```text
replacement rows:                         34
source-block count distribution:          {3: 32, 5: 2}
non-3x3 rows:                             [17290, 22610]
first off-diagonal positive signs:        20
first off-diagonal negative signs:        14
curvature baseline matches:               13 / 32
curvature baseline mismatches:            19 / 32
best single-feature rule:                 predict + if third_small < 184.5
best single-feature matches:              23 / 32
best single-feature mismatches:           9 / 32
```

The audit falsifies the uniform `3x3` premise for the whole
replacement landscape: rows `17290` and `22610` have five source
blocks.  On the `32` three-block rows, the source-gap curvature rule
from the three-candidate synthesis audit remains mostly wrong.

## Decision

Do not promote a first-off-diagonal source-block sign invariant.  The
best one-feature input-side threshold is only a weak finite
classifier, and the original `3x3` object is not even well-formed for
all checked rows.  The source-block matrix remains a useful diagnostic
object, but any theorem-shaped next step must be a variable-size
matrix invariant or a predeclared restriction to a genuine three-block
subfamily.

This is finite diagnostic evidence only.  It proves no source-block
interaction sign theorem, source-factor isolation theorem, replacement
packet compensation theorem, strict-central Goldbach theorem, or
Goldbach proof.
