# Mobius moment-square degree-5 source-margin M=383 clearance holdout

## Question

Does the clearance-family denominator target survive on the fresh `M=383`
full-sweep tight block?

## Mechanism

Read the completed `M=383` full prime sweep, take its tightest row
`p=599`, `(00,12)`, and recompute the exact reduced-denominator margin ledger.
Group denominators by clearance above `p*A`, where `A` is the source row count:

```text
near_1_to_2    p*A < Q < 2*p*A
middle_2_to_3  2*p*A <= Q < 3*p*A
far_3_plus     Q >= 3*p*A
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_margin_m383_clearance_holdout.py
evidence/mobius-moment-square-degree5-source-margin-m383-clearance-holdout.json
```

## Result

```text
status:                                  HOLDOUT_degree5_source_margin_m383_clearance_family
scale:                                   M=383
tight block:                             p=599, (00,12)
near negative absolute mass:             152079879558.52072
middle/far positive margin:              203565211531254.94
middle/far net margin:                   203565211531254.94
near negative / middle-far positive:     0.0007470818732461599
all negative denominators near threshold: true
middle/far net dominates near leakage:    true
```

Family counts:

```text
near_1_to_2:     38 rows, 35 positive, 3 negative
middle_2_to_3:   19 rows, 19 positive, 0 negative
far_3_plus:      13 rows, 13 positive, 0 negative
```

## Decision

The fresh `M=383` tight block supports the clearance-family target: all adverse
denominator mass is near-threshold here, and middle/far higher-clearance
positive and net mass dominate the near-threshold leakage.

This is one fresh block only.  It proves no clearance-family theorem,
denominator-margin theorem, prime-block theorem, source-start theorem,
strict-central Goldbach theorem, or Goldbach proof.
