# Mobius moment-square degree-5 Q46189 source-matrix margin audit

## Question

After the first-off-diagonal sign invariant failed, do variable-size
input-side source-matrix features correlate strongly enough with row
margin to justify a theorem target?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_source_matrix_margin_audit.py
evidence/mobius-moment-square-degree5-q46189-source-matrix-margin-audit.json
```

## Result

```text
replacement rows:                         34
best input feature for row margin:         missing_count
best input feature Pearson:                0.32654799306706145
best matrix feature for row margin:        tension_sum
best matrix feature Pearson:               -0.2169202637521853
strong input correlation threshold met:    no
strong matrix correlation threshold met:   no
```

The strongest row-margin signal among these simple input features is
weak.  More importantly, the strongest genuine source-matrix shape
feature is weaker still.  This does not disprove the existence of a
deeper source-matrix invariant, but it does block promotion of the
current obvious variable-size features into a theorem target.

## Decision

Demote the Q46189 source-matrix lane to diagnostic/falsifier status
until a changed invariant is predeclared.  The next theorem-shaped
move should return to the q286 raw adverse-envelope margin and test
whether its quantities can be defined without normalization or hidden
dependence on unknown prime-pair mass.

This is finite diagnostic evidence only.  It proves no source-matrix
margin theorem, source-block interaction sign theorem, strict-central
Goldbach theorem, or Goldbach proof.
