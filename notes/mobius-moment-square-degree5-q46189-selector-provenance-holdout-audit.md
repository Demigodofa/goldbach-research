# Mobius moment-square degree-5 Q46189 selector provenance holdout audit

## Question

Was `50A..60A` a post-hoc selector, and does a
leave-one-replacement-denominator-out audit support or weaken it?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_selector_provenance_holdout_audit.py
evidence/mobius-moment-square-degree5-q46189-selector-provenance-holdout-audit.json
```

## Result

```text
post-hoc selector:                         yes
natural conductor selector proved:          no
selected coarse slice:                      50A_to_60A
selected slice positive-share gap:          0.041455517777469975
selected slice total gap:                   0.06613384233919847
coarse leave-one-out pass count:            10 / 10
coarse selected-block counts:               {'50A_to_60A': 10}
coarse min heldout positive-share gap:      0.041455517777469975
coarse min heldout total gap:               0.06613384233919847
nested microblock leave-one-out pass count: 10 / 10
nested microblock selected-block counts:    {'50A_to_58A': 7, '50A_to_60A': 1, '56A_to_57A': 1, '56A_to_58A': 1}
nested microblock min heldout share gap:    0.006780195258194677
nested microblock min heldout total gap:     0.008428105120766007
```

## Decision

Kevin's objection is correct: `50A..60A` is post-hoc because it was
chosen after examining slices.  The finite evidence does not become a
theorem, and the slice must not be treated as a predeclared acceptance
condition.

The selector is nevertheless more stable than a single fitted row.  In
leave-one-denominator-out selection over the coarse `10A` far-band
slices, the training set chooses `50A..60A` in all `10/10` folds, and
every held-out denominator clears both the selected positive-share and
total-pressure comparisons.  The nested microblock selector also
passes all held-out denominators, but its choice varies and remains
conditioned on the post-hoc `50A..60A` region.

The next theorem-shaped route therefore needs either a natural
predeclared selector from active-kernel, conductor, or residual
geometry, or a fresh-conductor holdout frozen before inspection.
This proves no natural selector theorem, distance-slice theorem,
replacement residue-gap theorem, strict-central Goldbach theorem, or
Goldbach proof.
