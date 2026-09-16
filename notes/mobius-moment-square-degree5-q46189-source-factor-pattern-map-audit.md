# Mobius moment-square degree-5 Q46189 source-factor pattern map audit

## Question

After the Q46189 replacement audits, which patterns survive a
step-back map, and which tempting dots should be eliminated?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_source_factor_pattern_map_audit.py
evidence/mobius-moment-square-degree5-q46189-source-factor-pattern-map-audit.json
```

## Result

```text
replacement rows:                         34
plain middle-loss threshold:              eliminated
small/missing product monotonicity:        eliminated
missing high prime alone:                  eliminated
q=38038 aggregate middle:                  -0.939992990438763
q=38038 aggregate non-middle:              0.09269980585259228
q=38038 first-block-pair middle:           -0.9680777579360889
q=38038 first-block-pair non-middle:       0.08681182947394983
q=41990 aggregate middle:                  -0.43222079205102754
q=41990 aggregate non-middle:              -0.10078449680431602
q=41990 first-block-pair middle:           -0.07507696020668778
q=41990 first-block-pair non-middle:       -0.17235321354798228
```

The surviving pattern is matrix-shaped.  `q=38038` has its extreme
middle loss in an off-diagonal interaction between its first two
source-factor blocks, and that interaction has positive non-middle
payment.  `q=41990` has a less extreme middle loss, but its analogous
first cross-block non-middle mass is negative.

## Decision

Do not add more scalar dots to the map as if they were theorem
objects.  The next evidence-bearing step is an all-row source-block
interaction sign audit: compute the ordered 3x3 source-block matrix
for all `34` replacement rows and test whether input-side block
topology predicts the sign of the first off-diagonal non-middle term.

This is finite diagnostic evidence only.  It proves no source-block
interaction sign theorem, source-factor isolation theorem, replacement
packet compensation theorem, strict-central Goldbach theorem, or
Goldbach proof.
