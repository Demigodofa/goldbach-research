# Mobius moment-square degree-5 Q46189 counterexample reachability audit

## Question

Is the `q=16302` frozen-selector counterexample reachable by the same
raw six source-conductor-pair mechanism as the selected `Q=46189`
replacement family?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_counterexample_reachability_audit.py
evidence/mobius-moment-square-degree5-q46189-counterexample-reachability-audit.json
```

## Result

```text
q=16302 status:                    REACHABLE
factorization:                     {'2': 1, '3': 1, '11': 1, '13': 1, '19': 1}
missing high prime:                [17]
small prime support:               [2, 3]
ordered source-conductor pairs:    6
raw frequency pairs:               25920
raw reduced residues:              4320
zero-left raw pairs:               0
raw scalar:                        -0.05374291102747207
max raw scalar deviation:          1.3877787807814457e-17
exact scalar minus raw scalar:      6.938893903907228e-18
common log numerator:              -l11*l13*l19 - l11*l13*l2 - l11*l13*l3 - l11*l19*l2 - l11*l19*l3 - l13*l19*l2 - l13*l19*l3
frozen positive-share gap:         -0.07517830702507916
frozen total-pressure gap:         0.04221956863220733
```

The ordered source-conductor pairs are:

```text
66 x 247 -> 4320
78 x 209 -> 4320
114 x 143 -> 4320
143 x 114 -> 4320
209 x 78 -> 4320
247 x 66 -> 4320
```

## Decision

`q=16302` is reachable by the same raw six source-conductor-pair
mechanism as the selected replacement rows.  It also satisfies the
same exact log-polynomial scalar identity pattern, now with missing
high prime `17` and small pair `(2,3)`.

Therefore the frozen-selector failure cannot be dismissed as an
irrelevant residue-cell artifact.  The `50A..60A` theorem lane needs
a stricter natural admissibility filter that excludes this packet
before testing, or it should be demoted as a fitted finite witness.

This proves no natural selector theorem, fresh-conductor theorem,
raw source-pair admissibility theorem, distance-slice theorem,
strict-central Goldbach theorem, or Goldbach proof.
