# Mobius moment-square degree-5 Q46189 far-tail sub-band balance audit

## Question

Does the far-tail positive-share separator localize to the far band,
the tail band, or only their combination?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_far_tail_subband_balance_audit.py
evidence/mobius-moment-square-degree5-q46189-far-tail-subband-balance-audit.json
```

## Result

```text
Q far positive share:                0.4408502583196725
min replacement far positive share:  0.46558306565994817
far positive-share gap:              0.024732807340275664
Q far total / diag:                  -0.47656170489466876
min replacement far total / diag:    -0.2285960671576456
far total gap:                       0.24796563773702315
Q tail positive share:               0.4837815168881257
min replacement tail positive share: 0.46898198848807515
Q tail total / diag:                 -0.10704120127193549
min replacement tail total / diag:   -0.11565247838727731
```

## Decision

The broad signed-balance separator localizes to the far band.  Tail is
a non-separator: `q=40755` is worse than `Q=46189` in tail positive
share and tail total.  The next theorem-shaped target is therefore a
far-band signed-balance lower bound.

This is finite selected-family diagnostic evidence only.  It proves no
far-band positive-share theorem, far-band pressure theorem, tail-band
pressure theorem, far-tail positive-share theorem, replacement
residue-gap bound theorem, coordinate-00 residue-gap sign theorem,
strict-central Goldbach theorem, or Goldbach proof.
