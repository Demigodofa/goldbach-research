# Mobius moment-square degree-5 Q46189 frozen selector unused-denominator holdout

## Question

After freezing the post-hoc `50A..60A` selector, does it survive
same-source reduced denominators that were not part of the original
replacement-family discovery set?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_frozen_selector_unused_denominator_holdout.py
evidence/mobius-moment-square-degree5-q46189-frozen-selector-unused-denominator-holdout.json
```

## Result

```text
frozen selector:                     50A_to_60A
distance range:                      [2151, 2580]
unused same-source denominators:     24
positive-fraction failures:          1
total-pressure failures:             0
both-test failures:                  1
minimum positive-fraction gap:       -0.07517830702507916
minimum total-pressure gap:          0.03424045325706524
weakest denominator:                 16302
weakest factorization:               {'2': 1, '3': 1, '11': 1, '13': 1, '19': 1}
weakest positive fraction:           0.2952966974458642
Q46189 positive fraction:            0.37047500447094334
weakest total / diag:                -0.04375121941657745
Q46189 total / diag:                 -0.08597078804878477
```

## Decision

The frozen selector fails as a too-broad same-source denominator rule.
The denominator `16302 = 2*3*11*13*19` has a lower positive-fraction
share than `Q=46189` in the frozen block.  Its total-pressure gap still
clears, so this is a targeted failure of the positive-share separator,
not a total-pressure failure.

This demotes the natural-boundary story unless a structural admissibility
filter is defined before looking at the test set.  A valid next step is
to trace the original replacement construction and state whether
`q=16302` is reachable or unreachable under that construction.  If it
is reachable, the `50A..60A` selector cannot be a theorem lane in its
current form.  If it is unreachable, the reason must be explicit and
predeclared before testing any further held-out conductors.

This proves no natural selector theorem, fresh-conductor theorem,
distance-slice theorem, replacement residue-gap theorem, strict-central
Goldbach theorem, or Goldbach proof.
