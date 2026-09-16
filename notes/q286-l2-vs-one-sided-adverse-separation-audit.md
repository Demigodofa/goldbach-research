# q286 L2 versus one-sided adverse separation audit

## Question

Are the finite aggregate L2 cap failures the same obstruction as the raw one-sided adverse envelope, or does symmetric L2 reject rows that the one-sided adverse gate handles?

## Receipt

```text
tools/build_q286_l2_vs_one_sided_adverse_separation_audit.py
evidence/q286-l2-vs-one-sided-adverse-separation-audit.json
```

## Result

```text
joined rows:                              348
row-local L2 cap violations:              120
global-minimum L2 cap violations:         301
raw adverse gate failures:                0
row-local L2 violations with positive gate:120
max adverse ratio on L2 violations:       0.23148438379145228
min raw gate gap on L2 violations:        286929.1729900494
L2/adverse Pearson:                       0.16452492187036813
L2 violations with adverse ratio < .05:   77
L2 violations with adverse ratio < .10:   103
```

The worst adverse ratio among row-local L2 violations is at target
`1124642`: adverse ratio `0.23148438379145228`,
row-local L2 ratio `1.0557946886340719`, and raw
gate gap `330637.8470878761`.

## Interpretation

The finite L2 cap failures are not the same finite obstruction as the
one-sided adverse envelope.  Symmetric L2 charges all character moment
mass, including helpful directions.  The adverse envelope only charges
harmful projected mass.  On the checked rows, the latter is much less
stressed.

## Decision

The checked rows separate the aggregate L2 obstruction from the one-sided adverse envelope.  The row-local L2 cap fails on 120 rows, but every one of those rows still has positive raw adverse gate gap; 77 of the 120 have adverse ratio below 0.05, and the Pearson correlation between row-local L2 ratio and adverse ratio is weak.  This demotes symmetric aggregate L2 as the immediate bridge and promotes one-sided raw adverse projection control as the sharper theorem target.

This is finite separation evidence only.  It proves no aggregate L2
theorem, one-sided adverse projection theorem, raw adverse-envelope
theorem, strict-central Goldbach theorem, or Goldbach proof.
